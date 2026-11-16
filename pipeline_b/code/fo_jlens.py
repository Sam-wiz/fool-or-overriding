"""J-lens (Jacobian lens; Gurnee et al. 2026, arXiv:2607.15495) readout of the decision state.

Question: at the decision token, is the model still 'poised to say' that the question is unpredictable/unknown while it
commits under the panel? A logit lens reads h_L as if it were the final layer; the J-lens first maps h_L through the
average Jacobian of the rest of the network (averaged over source/target positions and a generic corpus).

Per model:
  1. J-lens vectors v_X^L for a fixed concept vocabulary X at every layer L, as averaged vector-Jacobian products:
     v_X^L = mean over corpus sequences and source positions t of d/dh_L[t] sum_{t'} u_X . h_fin[t'] / rms_fin[t'],
     u_X = gamma_final * W_U[X] (final RMSNorm scale times unembedding; rms detached). One forward, one backward per X.
  2. All-layer residual at END (last prompt token) and DEC (last token of "<answer>\\nDECISION:") for the NSE items
     (unk L0/L1/L2/L2irr/L2fab, leak, ans L1/L2) -> J-lens scores h.v_X and plain logit-lens scores.
  3. Ranked readout over the full vocabulary of condition-mean DIFFERENCE vectors (panel effect L2-L0, fabricated
     L2fab-L0, leak effect leak-L2, knowability ansL2-unkL2) at a few layers: J_bar @ delta estimated by a central finite
     difference (add +/- eps*delta at layer L at every corpus position), then (gamma*W_U) . (J_bar delta / rms).
ENV: MODELS, DATA (fo_data2.json), OUT, NCORP (corpus seqs, default 64), SEQ (128), BS (4)
"""
import os, json, time, math
import numpy as np
import torch
import fo_run as F

E = os.environ.get
OUT = E("OUT", "/content/jl_out"); os.makedirs(OUT, exist_ok=True)
NCORP = int(E("NCORP", "64")); SEQ = int(E("SEQ", "128")); BS = int(E("BS", "4"))
NFD = int(E("NFD", "16"))
log = F.log

CONCEPTS = {
    "unknowable": [" unpredictable", " uncertain", " unknown", " impossible", " random", " cannot", " unclear",
                   " speculative", " guess", " unsure", " unknowable", " uncertainty"],
    "commit": [" higher", " bullish", " likely", " confident", " rise", " increase", " upward", " momentum",
               " probability", " trend", " positive", " expect"],
    "action": [" ANSWER", " DECLINE", " CALL", " search", " decline", " answer"],
    "control": [" the", " table", " river", " music", " blue", " dog"],
}


def corpus(tok):
    texts = []
    try:
        from datasets import load_dataset
        ds = load_dataset("Salesforce/wikitext", "wikitext-103-raw-v1", split="train", streaming=True)
        buf = ""
        for r in ds:
            t = r["text"].strip()
            if len(t) < 400 or t.startswith("="):
                continue
            texts.append(t)
            if len(texts) >= NCORP * 2:
                break
        src = "wikitext-103"
    except Exception as e:  # offline fallback
        log("wikitext unavailable:", repr(e)[:200])
        d = json.load(open(F.DATA))
        texts = [x["text"] for x in d if x["set"] in ("train", "transfer")][: NCORP * 2]
        src = "synthetic+transfer prompts"
    seqs = []
    for t in texts:
        ids = tok(t, add_special_tokens=False).input_ids
        if len(ids) >= SEQ:
            seqs.append(ids[:SEQ])
        if len(seqs) >= NCORP:
            break
    log(f"corpus: {len(seqs)} x {SEQ} tokens from {src}")
    return torch.tensor(seqs), src


def main():
    models = [m for m in E("MODELS", "").split(",") if m]
    d = json.load(open(F.DATA))
    nse = [x for x in d if x["set"] in ("nse", "nse_leak")]
    for name in models:
        t0 = time.time()
        tag = name.split("/")[-1].replace("-", "_").replace(".", "_")
        R = F.Runner(name); m, tok = R.m, R.tok
        for p in m.parameters():
            p.requires_grad_(False)
        nL = R.nL
        normw = None
        for path in ("model.norm", "model.language_model.norm", "model.model.norm"):
            o = m
            try:
                for p in path.split("."):
                    o = getattr(o, p)
                normw = o.weight.float()
                if "gemma" in name.lower():  # Gemma RMSNorm scales by (1 + weight)
                    normw = normw + 1.0
                break
            except AttributeError:
                continue
        WU = m.get_output_embeddings().weight  # [V, d]
        # concept vocabulary (first token of each word)
        cw, cid, cgroup, multi = [], [], [], []
        for g, ws in CONCEPTS.items():
            for w in ws:
                ids = tok(w, add_special_tokens=False).input_ids
                cw.append(w); cid.append(ids[0]); cgroup.append(g); multi.append(len(ids) > 1)
        U = (WU[cid].float() * normw[None, :]).to(m.device)  # [K, d]
        K = len(cid)

        # capture pre-norm final residual via hook on the last block
        cap = {}
        def lasthook(mod, inp, out):
            cap["fin"] = out[0] if isinstance(out, tuple) else out
        hlast = R.layers[-1].register_forward_hook(lasthook)

        # ---- 1. J-lens vectors by averaged VJP
        C, csrc = corpus(tok)
        emb = m.get_input_embeddings()
        V = torch.zeros(K, nL + 1, U.shape[1], dtype=torch.float32, device=m.device)
        nb = 0
        for i in range(0, len(C), BS):
            ids = C[i:i + BS].to(m.device)
            x = emb(ids).detach().requires_grad_(True)
            out = m(inputs_embeds=x, output_hidden_states=True, use_cache=False)
            hs = out.hidden_states  # nL+1, each [b,T,d]; hs[0] = embeddings
            fin = cap["fin"].float()
            rms = fin.pow(2).mean(-1, keepdim=True).add(1e-6).sqrt().detach()
            finn = fin / rms
            for k in range(K):
                obj = (finn @ U[k]).sum()
                gr = torch.autograd.grad(obj, list(hs), retain_graph=(k < K - 1), allow_unused=True)
                for l, g in enumerate(gr):
                    if g is not None:
                        V[k, l] += g.float().mean(dim=(0, 1))
            nb += 1
            del out, hs, fin, finn, gr
            torch.cuda.empty_cache()
        V /= nb
        log(f"J-lens vectors done ({K} concepts x {nL+1} layers) {time.time()-t0:.0f}s")

        # ---- 2. all-layer residual at END and DEC for NSE items, J-lens + logit-lens scores
        pre_ids = tok(F.DEC_PREFIX, add_special_tokens=False).input_ids
        seqs = [F.chat_ids(tok, x["text"]) + pre_ids for x in nse]
        endpos = [len(s) - len(pre_ids) - 1 for s in seqs]
        Hdec = np.zeros((len(nse), nL + 1, U.shape[1]), dtype=np.float16)
        Hend = np.zeros_like(Hdec)
        with torch.no_grad():
            for i in range(0, len(seqs), 8):
                ids, att = F.pad_left(seqs[i:i + 8], R.pad)
                out = m(input_ids=ids.to(m.device), attention_mask=att.to(m.device), output_hidden_states=True,
                        use_cache=False)
                T = ids.shape[1]
                for j in range(ids.shape[0]):
                    L = len(seqs[i + j]); e = T - L + endpos[i + j]
                    for l, h in enumerate(out.hidden_states):
                        Hdec[i + j, l] = h[j, -1].float().cpu().numpy()
                        Hend[i + j, l] = h[j, e].float().cpu().numpy()
                del out
        Vn = V.cpu().numpy()
        js_dec = np.einsum("nld,kld->nlk", Hdec.astype(np.float32), Vn)
        js_end = np.einsum("nld,kld->nlk", Hend.astype(np.float32), Vn)
        Un = U.cpu().numpy()
        def ll(H):
            Hf = H.astype(np.float32)
            Hf = Hf / np.sqrt((Hf ** 2).mean(-1, keepdims=True) + 1e-6)
            return np.einsum("nld,kd->nlk", Hf, Un)
        ll_dec, ll_end = ll(Hdec), ll(Hend)
        log(f"item scores done {time.time()-t0:.0f}s")

        # ---- 3. ranked readout of condition-mean difference vectors by finite-difference JVP
        meta = [(x["id"].split("|")[0], x["id"].split("|")[1], x["id"].split("|")[2]) for x in nse]
        def cmean(arm, lvl):
            idx = [i for i, t in enumerate(meta) if t[1] == arm and t[2] == lvl]
            return Hdec[idx].astype(np.float32).mean(0)
        conds = {"unkL0": cmean("unk", "L0"), "unkL2": cmean("unk", "L2"), "unkL2fab": cmean("unk", "L2fab"),
                 "unkLeak": cmean("unk", "L2leak"), "ansL2": cmean("ans", "L2"), "unkL2irr": cmean("unk", "L2irr")}
        diffs = {"panel(L2-L0)": conds["unkL2"] - conds["unkL0"],
                 "fabricated(L2fab-L0)": conds["unkL2fab"] - conds["unkL0"],
                 "leak(leak-L2)": conds["unkLeak"] - conds["unkL2"],
                 "knowable-unknowable(L2)": conds["ansL2"] - conds["unkL2"],
                 "relevant-irrelevant(L2-L2irr)": conds["unkL2"] - conds["unkL2irr"]}
        Ls = sorted(set(int(round(f * nL)) for f in (0.4, 0.55, 0.7, 0.85)))
        Cfd = C[:NFD].to(m.device)
        WUn = (WU.float() * normw[None, :])  # [V,d] on device
        state = {}
        def addhook(mod, inp, out):
            if "vec" not in state:
                return out
            if isinstance(out, tuple):
                return (out[0] + state["vec"],) + tuple(out[1:])
            return out + state["vec"]
        ranked = {}
        with torch.no_grad():
            base_rms = []
            for b in range(0, NFD, BS):
                m(input_ids=Cfd[b:b + BS], use_cache=False)
                base_rms.append(cap["fin"].float().pow(2).mean(-1, keepdim=True).add(1e-6).sqrt())
            for L in Ls:
                hk = R.layers[L - 1].register_forward_hook(addhook)
                typ = float(np.sqrt((conds["unkL0"][L] ** 2).sum()))
                for dn, dv in diffs.items():
                    dl = torch.tensor(dv[L], dtype=torch.float32, device=m.device)
                    eps = 0.25 * typ / (dl.norm().item() + 1e-6)
                    acc = torch.zeros(dl.shape[0], device=m.device)
                    for b in range(0, NFD, BS):
                        outs = []
                        for sgn in (1, -1):
                            state["vec"] = (sgn * eps * dl).to(F.DT)
                            m(input_ids=Cfd[b:b + BS], use_cache=False)
                            outs.append(cap["fin"].float())
                        jd = (outs[0] - outs[1]) / (2 * eps) / base_rms[b // BS]
                        acc += jd.mean(dim=(0, 1))
                    state.pop("vec", None)
                    acc /= math.ceil(NFD / BS)
                    lg = WUn @ acc
                    top = torch.topk(lg, 25).indices.tolist(); bot = torch.topk(-lg, 25).indices.tolist()
                    # logit lens of the same vector (no Jacobian) for comparison
                    lgl = WUn @ dl
                    topl = torch.topk(lgl, 25).indices.tolist()
                    ranked[f"{dn}@L{L}"] = dict(
                        jlens_top=[tok.decode([t]) for t in top], jlens_bottom=[tok.decode([t]) for t in bot],
                        logitlens_top=[tok.decode([t]) for t in topl],
                        concept_jlens={w: float(lg[c]) for w, c in zip(cw, cid)},
                        concept_rank={w: int((lg > lg[c]).sum()) for w, c in zip(cw, cid)})
                hk.remove()
        hlast.remove()
        res = dict(model=name, n_layers=nL, corpus=csrc, ncorp=int(len(C)), seq=SEQ, concepts=cw, groups=cgroup,
                   multitoken=multi, ids=[x["id"] for x in nse], ranked=ranked, fd_layers=Ls, secs=time.time() - t0)
        json.dump(res, open(os.path.join(OUT, f"{tag}.json"), "w"))
        np.savez_compressed(os.path.join(OUT, f"{tag}_scores.npz"), js_dec=js_dec.astype(np.float32),
                            js_end=js_end.astype(np.float32), ll_dec=ll_dec.astype(np.float32),
                            ll_end=ll_end.astype(np.float32), vnorm=np.linalg.norm(Vn, axis=-1))
        log(f"{name} done {time.time()-t0:.0f}s")
        del R, m, V, Hdec, Hend
        torch.cuda.empty_cache()


if __name__ == "__main__":
    main()
