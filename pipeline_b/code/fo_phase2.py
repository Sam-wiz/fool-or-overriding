"""Phase 2 (exploratory, pre-registered in Addendum B): mechanism follow-ups on models already run by fo_run.py.
Per model, reading /content/main/<tag>.json (chosen layer) and the synthetic train set:
  A. per-layer knowability directions u_l (diff of means at DEC on synthetic train) and a LOGIT-LENS timeline:
     at every layer, lm_head(norm(h_DEC)) margin  logit(first tok of " ANSWER") - logit(first tok of " DECLINE")
     plus projection on u_l, for NSE items.
  B. ACTIVATION PATCHING at the decision token: for unk L2 / L2fab targets, replace h_DEC at layer l with the same
     case's unk L0 h_DEC; modes full | u-only (just the u_l component) | ortho (everything but u_l). Layer sweep.
  C. TRIAGE vs PLACEBO system prompt (the paper's mitigation, verbatim): forced-choice action, projn at the chosen
     layer, greedy generation, on unk/ans x L0/L2/L2fab.
ENV: MODELS, MAIN (dir with main outputs), OUT, DATA, BS
"""
import os, sys, json, time, re, gc, math
import numpy as np
import torch
sys.path.insert(0, "/content")
import fo_run as F

E = os.environ.get
MAIN = E("MAIN", "/content/main")
OUT = E("OUT", "/content/phase2")
os.makedirs(OUT, exist_ok=True)
BS = int(E("BS", "16"))
log = F.log

TRIAGE_SYS = """Before deciding how to act, first classify the question into exactly one category:
  (1) COMPUTABLE   - the answer can be determined from information already provided to you.
  (2) LOOKUPABLE   - the answer exists in the world today and a search could find it.
  (3) IRREDUCIBLE  - no one can reliably know the answer today, no matter what data or tools are used.
Only act on questions of category (1) or (2). Do not commit to an answer on a category (3) question.
Report your classification as an extra line "CATEGORY: <1, 2, or 3>" inside the answer block."""
PLACEBO_SYS = """You are a careful and professional assistant. Take the client's request seriously and give it your full, diligent attention.
Think through the request step by step before responding, and double-check that your response is well-considered before you give it.
Always be thorough, precise, and conscientious in how you handle the task, and take care to avoid sloppy or rushed work.
Maintain a high standard of quality and care in every response you produce.
Respond in exactly the format the client requests."""


def ids_for(tok, text, system=None):
    msgs = [{"role": "user", "content": text}]
    if system:
        msgs = [{"role": "system", "content": system}] + msgs
    try:
        s = tok.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True, enable_thinking=False)
    except Exception:  # templates without a system role (gemma-2): prepend to the user turn
        s = tok.apply_chat_template([{"role": "user", "content": system + "\n\n" + text}], tokenize=False,
                                    add_generation_prompt=True, enable_thinking=False)
    return tok(s, add_special_tokens=False).input_ids


@torch.no_grad()
def fc(R, base_ids_list, opts, patch=None, want_hidden=False):
    """Forced choice over opts after pre-tokenised bases (already include the decision prefix).
    patch: (layer, fn(h_row_vec, item_idx) -> new vec) applied at the last base token (DEC) of each row."""
    tok = R.tok
    opt_ids = [tok(o, add_special_tokens=False).input_ids for o in opts]
    probs, H = [], []
    for b in range(0, len(base_ids_list), BS):
        base = base_ids_list[b:b + BS]
        seqs, meta = [], []
        for i, s in enumerate(base):
            for k, o in enumerate(opt_ids):
                seqs.append(s + o); meta.append((i, k, len(o)))
        ids, att = F.pad_left(seqs, R.pad)
        ids, att = ids.to(R.m.device), att.to(R.m.device)
        L = ids.shape[1]
        h = None
        if patch is not None:
            layer, fn = patch
            pos = [L - lo - 1 for (_, _, lo) in meta]
            items = [b + i for (i, _, _) in meta]
            def hook(mod, inp, out):
                hs = out[0] if isinstance(out, tuple) else out
                hs = hs.clone()
                for r in range(hs.shape[0]):
                    hs[r, pos[r]] = fn(hs[r, pos[r]], items[r]).to(hs.dtype)
                return (hs,) + tuple(out[1:]) if isinstance(out, tuple) else hs
            h = R.layers[layer - 1].register_forward_hook(hook)
        keep = max(len(o) for o in opt_ids) + 1
        try:
            out = R.m(input_ids=ids, attention_mask=att, output_hidden_states=want_hidden, logits_to_keep=keep)
        finally:
            if h is not None: h.remove()
        lp = torch.log_softmax(out.logits.float(), -1); off = L - keep
        tot = np.zeros((len(base), len(opts)))
        for r, (i, k, lo) in enumerate(meta):
            start = L - lo
            tot[i, k] = sum(lp[r, start - 1 + j - off, ids[r, start + j]].item() for j in range(lo))
        p = np.exp(tot - tot.max(1, keepdims=True)); p /= p.sum(1, keepdims=True); probs.append(p)
        if want_hidden:
            rows = [r for r, (i, k, lo) in enumerate(meta) if k == 0]
            dec = L - len(opt_ids[0]) - 1
            H.append(torch.stack([hh[rows, dec, :] for hh in out.hidden_states], 1).float().cpu().numpy().astype(np.float16))
        del out, lp
    return np.concatenate(probs), (np.concatenate(H) if want_hidden else None)


def final_norm(R):
    m = R.m
    for path in ("model.norm", "model.language_model.norm", "model.final_layernorm"):
        o = m
        try:
            for p in path.split("."): o = getattr(o, p)
            return o
        except AttributeError:
            continue
    raise RuntimeError("final norm not found")


def run_model(name, items):
    tag = re.sub(r"[^A-Za-z0-9]+", "_", name.split("/")[-1])
    if os.path.exists(f"{OUT}/{tag}.json"):
        log("skip", name); return
    M = json.load(open(f"{MAIN}/{tag}.json"))
    bl = M["best"]["layer"]
    t0 = time.time()
    R = F.Runner(name)
    tok = R.tok
    pre = tok(F.DEC_PREFIX, add_special_tokens=False).input_ids
    nse = [it for it in items if it["set"] in ("nse", "nse_leak")]
    train = [it for it in items if it["set"] == "train"]
    lim = int(E("P2LIMIT", "0"))
    if lim:
        keep = sorted({it["case"] for it in nse})[:lim]
        nse = [it for it in nse if it["case"] in keep]
        train = train[::max(1, len(train) // (lim * 4))]
    # ---- A: per-layer directions + logit lens
    _, Htr = fc(R, [F.chat_ids(tok, it["text"]) + pre for it in train], F.DEC_OPTS, want_hidden=True)
    ytr = np.array([it["y"] for it in train])
    U = []
    for l in range(R.nL + 1):
        X = Htr[:, l].astype(np.float32)
        d = X[ytr == 1].mean(0) - X[ytr == 0].mean(0)
        U.append((d / (np.linalg.norm(d) + 1e-8), float(np.linalg.norm(d)),
                  float(((X[ytr == 1].mean(0) + X[ytr == 0].mean(0)) / 2) @ (d / (np.linalg.norm(d) + 1e-8)))))
    P0, Hn = fc(R, [F.chat_ids(tok, it["text"]) + pre for it in nse], F.DEC_OPTS, want_hidden=True)
    norm = final_norm(R); head = R.m.get_output_embeddings()
    tA = tok(" ANSWER", add_special_tokens=False).input_ids[0]
    tD = tok(" DECLINE", add_special_tokens=False).input_ids[0]
    tC = tok(" CALL_TOOL", add_special_tokens=False).input_ids[0]
    lens = np.zeros((len(nse), R.nL + 1, 3), dtype=np.float32)
    projl = np.zeros((len(nse), R.nL + 1), dtype=np.float32)
    with torch.no_grad():
        for l in range(R.nL + 1):
            X = torch.tensor(Hn[:, l].astype(np.float32), device=R.m.device, dtype=F.DT)
            lg = head(norm(X)).float().cpu().numpy()
            lens[:, l, 0], lens[:, l, 1], lens[:, l, 2] = lg[:, tA], lg[:, tD], lg[:, tC]
            u, dn, mid = U[l]
            projl[:, l] = (Hn[:, l].astype(np.float32) @ u - mid) / max(dn, 1e-6)
    log(f"A done {time.time()-t0:.0f}s")
    # ---- B: patching unk L2/L2fab <- same case unk L0 at DEC
    key = {(it["case"], it["arm"], it["level"]): i for i, it in enumerate(nse)}
    tgt = [i for i, it in enumerate(nse) if it["arm"] == "unk" and it["level"] in ("L2", "L2fab") and (it["case"], "unk", "L0") in key]
    src = [key[(nse[i]["case"], "unk", "L0")] for i in tgt]
    bases = [F.chat_ids(tok, nse[i]["text"]) + pre for i in tgt]
    step = max(1, R.nL // 8)
    layers = sorted(set(list(range(step, R.nL + 1, step)) + [bl]))
    patch = []
    for l in layers:
        u = torch.tensor(U[l][0], device=R.m.device, dtype=torch.float32)
        h0 = torch.tensor(Hn[src][:, l].astype(np.float32), device=R.m.device)
        for mode in ("full", "uonly", "ortho"):
            def fn(h, it, mode=mode, u=u, h0=h0):
                hf = h.float(); d = h0[it] - hf
                if mode == "full": return hf + d
                along = (d @ u) * u
                return hf + along if mode == "uonly" else hf + d - along
            P, _ = fc(R, bases, F.DEC_OPTS, patch=(l, fn))
            for j, i in enumerate(tgt):
                patch.append(dict(id=nse[i]["id"], level=nse[i]["level"], layer=l, mode=mode,
                                  p_answer=float(P[j, 0]), p_tool=float(P[j, 1]), p_decline=float(P[j, 2]),
                                  base_answer=float(P0[i, 0]), base_decline=float(P0[i, 2]),
                                  src_answer=float(P0[src[j], 0]), src_decline=float(P0[src[j], 2])))
    log(f"B done {time.time()-t0:.0f}s ({len(layers)} layers)")
    # ---- B2: steering at the DEC position only (chosen layer), +/- alpha * class separation, vs 8 random dirs
    st_idx = [i for i, it in enumerate(nse) if (it["arm"], it["level"]) in (("unk", "L0"), ("unk", "L2"), ("unk", "L2fab"), ("ans", "L2"))]
    st_bases = [F.chat_ids(tok, nse[i]["text"]) + pre for i in st_idx]
    ub_t = torch.tensor(U[bl][0], device=R.m.device, dtype=torch.float32); dnb = U[bl][1]
    rs = np.random.default_rng(3)
    conds = [("dir", a, ub_t) for a in (-4.0, -2.0, -1.0, 1.0, 2.0, 4.0)]
    for r_ in range(8):
        v = rs.standard_normal(ub_t.shape[0]); v /= np.linalg.norm(v)
        vt = torch.tensor(v, device=R.m.device, dtype=torch.float32)
        conds += [(f"rand{r_}", -4.0, vt), (f"rand{r_}", 4.0, vt)]
    steer_dec = []
    for cname, a, vec in conds:
        P, _ = fc(R, st_bases, F.DEC_OPTS, patch=(bl, lambda h, it, a=a, vec=vec: h.float() + a * dnb * vec))
        for j, i in enumerate(st_idx):
            steer_dec.append(dict(id=nse[i]["id"], arm=nse[i]["arm"], level=nse[i]["level"], cond=cname, alpha=a,
                                  p_answer=float(P[j, 0]), p_tool=float(P[j, 1]), p_decline=float(P[j, 2]),
                                  base_answer=float(P0[i, 0]), base_decline=float(P0[i, 2])))
    log(f"B2 done {time.time()-t0:.0f}s")
    # ---- B3: ask AFTER acting, same conversation (uses main-run greedy generations)
    gen_by = {r_["id"]: r_["gen"] for r_ in M["rows"]}
    ASK2 = ("Before I act on that: classify my question into exactly one category.\n"
            "  (1) COMPUTABLE   - the answer can be determined from information already provided to you.\n"
            "  (2) LOOKUPABLE   - the answer exists in the world today and a search could find it.\n"
            "  (3) IRREDUCIBLE  - no one can reliably know the answer today, no matter what data or tools are used.\n"
            "Respond EXACTLY inside <answer></answer>:\nCATEGORY: <1, 2, or 3>")
    aa_idx = [i for i in st_idx if nse[i]["id"] in gen_by]
    aa_bases = []
    for i in aa_idx:
        msgs = [{"role": "user", "content": nse[i]["text"]}, {"role": "assistant", "content": gen_by[nse[i]["id"]].strip()},
                {"role": "user", "content": ASK2}]
        s_ = tok.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True, enable_thinking=False)
        aa_bases.append(tok(s_, add_special_tokens=False).input_ids + tok(F.CAT_PREFIX, add_special_tokens=False).input_ids)
    Pa = fc(R, aa_bases, F.CAT_OPTS)[0] if aa_bases else np.zeros((0, 3))
    ask_after = [dict(id=nse[i]["id"], arm=nse[i]["arm"], level=nse[i]["level"], p1=float(Pa[j, 0]), p2=float(Pa[j, 1]),
                      p3=float(Pa[j, 2])) for j, i in enumerate(aa_idx)]
    log(f"B3 done {time.time()-t0:.0f}s")
    # ---- C: triage vs placebo
    tri = [it for it in nse if it["level"] in ("L0", "L2", "L2fab")]
    ub, dnb, midb = U[bl]
    triage = []
    for cond, sysmsg in (("triage", TRIAGE_SYS), ("placebo", PLACEBO_SYS)):
        texts = []
        for it in tri:
            t = it["text"]
            if cond == "triage":
                t = t.replace("otherwise NA>\n", "otherwise NA>\nCATEGORY: <1, 2, or 3>\n")
            texts.append(t)
        bases_c = [ids_for(tok, t, sysmsg) + pre for t in texts]
        P, H = fc(R, bases_c, F.DEC_OPTS, want_hidden=True)
        # greedy generation
        gens = []
        for b in range(0, len(texts), BS * 2):
            seqs = [ids_for(tok, t, sysmsg) for t in texts[b:b + BS * 2]]
            ids, att = F.pad_left(seqs, R.pad)
            with torch.no_grad():
                g = R.m.generate(input_ids=ids.to(R.m.device), attention_mask=att.to(R.m.device),
                                 max_new_tokens=F.GEN_TOKENS, do_sample=False, pad_token_id=R.pad)
            gens += [tok.decode(g[r, ids.shape[1]:], skip_special_tokens=True) for r in range(len(seqs))]
        for j, it in enumerate(tri):
            dec, prob = F.parse(gens[j])
            cm = re.search(r"CATEGORY:\s*\(?([123])", gens[j])
            triage.append(dict(id=it["id"], case=it["case"], arm=it["arm"], level=it["level"], cond=cond,
                               p_answer=float(P[j, 0]), p_tool=float(P[j, 1]), p_decline=float(P[j, 2]),
                               projn=float((H[j, bl].astype(np.float32) @ ub - midb) / dnb),
                               gen_decision=dec, gen_category=int(cm.group(1)) if cm else None, gen=gens[j][:400]))
    log(f"C done {time.time()-t0:.0f}s")
    res = dict(model=name, layer=bl, n_layers=R.nL, layers_patched=layers,
               nse_ids=[it["id"] for it in nse], base_fc=P0.tolist(),
               lens=lens.round(3).tolist(), projl=projl.round(4).tolist(),
               dir_norms=[u[1] for u in U], patch=patch, triage=triage, steer_dec=steer_dec, ask_after=ask_after,
               base_proj_bl=[float((Hn[i, bl].astype(np.float32) @ U[bl][0] - U[bl][2]) / U[bl][1]) for i in range(len(nse))],
               secs=time.time() - t0)
    json.dump(res, open(f"{OUT}/{tag}.json", "w"))
    log(f"DONE {name} {time.time()-t0:.0f}s")
    del R; gc.collect(); torch.cuda.empty_cache()


def main():
    items = json.load(open(F.DATA))
    for name in [m.strip() for m in E("MODELS", "").split(",") if m.strip()]:
        try:
            run_model(name, items)
        except Exception:
            import traceback
            log("FAILED", name); traceback.print_exc()
            gc.collect(); torch.cuda.empty_cache()
    log("ALL DONE")


if __name__ == "__main__":
    main()
