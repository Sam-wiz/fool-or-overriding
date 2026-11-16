"""Fooled or Overriding? -- one-model-at-a-time white-box run (Colab VM or local CPU smoke).

Per model:
  1. forward pass on every item with the assistant prefix "<answer>\\nDECISION:" appended; cache the
     residual stream at two positions (END = last prompt token, DEC = last prefix token) for all layers
  2. ACTION: forced-choice log-probs of " ANSWER"/" CALL_TOOL"/" DECLINE" (teacher-forced, summed)
  3. WORDS-WHEN-ASKED: forced-choice " 1"/" 2"/" 3" on the triage-classification prompt
  4. GENERATION: greedy decode of the agentic prompt (decision + stated probability + reasoning)
  5. INSIDE: per-layer logistic probe (unknowable vs answerable) fit on synthetic `train`,
     layer/position chosen by AUROC on `transfer` only; scored on NSE (held out from all selection)
  6. CAUSAL: add +/- a * (diff-of-means knowability direction) at the chosen layer, all positions;
     re-score ACTION on NSE L2/L0 items; 8 norm-matched random directions as control
ENV: MODELS (comma list of HF ids) | LIMIT (items per subset, smoke) | OUT (dir) | DATA (json path)
     | STEER (1/0) | GEN_TOKENS
"""
import os, sys, json, time, re, gc, math, random, traceback
import numpy as np
import torch

E = os.environ.get
DATA = E("DATA", "/content/fo_data.json")
OUT = E("OUT", "/content/fo_out")
LIMIT = int(E("LIMIT", "0"))
GEN_TOKENS = int(E("GEN_TOKENS", "160"))
STEER = E("STEER", "1") == "1"
BS = int(E("BS", "16"))
os.makedirs(OUT, exist_ok=True)
DEV = "cuda" if torch.cuda.is_available() else "cpu"
DT = torch.bfloat16 if DEV == "cuda" else torch.float32

DEC_PREFIX = "<answer>\nDECISION:"
CAT_PREFIX = "<answer>\nCATEGORY:"
DEC_OPTS = [" ANSWER", " CALL_TOOL", " DECLINE"]
CAT_OPTS = [" 1", " 2", " 3"]


def log(*a):
    print(time.strftime("%H:%M:%S"), *a, flush=True)


def load_items():
    items = json.load(open(DATA))
    if LIMIT:
        out, seen = [], {}
        for it in items:
            k = (it["set"], it.get("arm"), it.get("level"), it["y"])
            if seen.get(k, 0) < LIMIT:
                out.append(it); seen[k] = seen.get(k, 0) + 1
        items = out
    return items


def chat_ids(tok, text):
    s = tok.apply_chat_template([{"role": "user", "content": text}], tokenize=False,
                                add_generation_prompt=True, enable_thinking=False)
    return tok(s, add_special_tokens=False).input_ids


def pad_left(seqs, pad_id):
    L = max(len(s) for s in seqs)
    ids = torch.full((len(seqs), L), pad_id, dtype=torch.long)
    att = torch.zeros((len(seqs), L), dtype=torch.long)
    for i, s in enumerate(seqs):
        ids[i, L - len(s):] = torch.tensor(s); att[i, L - len(s):] = 1
    return ids, att


class Runner:
    def __init__(self, name):
        from transformers import AutoTokenizer, AutoModelForCausalLM
        self.name = name
        self.tok = AutoTokenizer.from_pretrained(name)
        if self.tok.pad_token_id is None:
            self.tok.pad_token = self.tok.eos_token
        kw = dict(dtype=DT, device_map=DEV) if DEV == "cuda" else dict(dtype=DT)
        if "gemma" in name.lower():
            kw["attn_implementation"] = "eager"
        self.m = AutoModelForCausalLM.from_pretrained(name, **kw).eval()
        self.layers = self._layers()
        self.nL = len(self.layers)
        self.pad = self.tok.pad_token_id
        self.hook = None

    def _layers(self):
        m = self.m
        for path in ("model.layers", "model.language_model.layers", "model.model.layers", "transformer.h"):
            o = m
            try:
                for p in path.split("."):
                    o = getattr(o, p)
                return o
            except AttributeError:
                continue
        raise RuntimeError("layers not found")

    # ---------- steering hook
    def set_steer(self, layer, vec):
        self.clear_steer()
        if vec is None:
            return
        v = torch.tensor(vec, dtype=DT, device=self.m.device)
        def fn(mod, inp, out):
            if isinstance(out, tuple):
                return (out[0] + v,) + tuple(out[1:])
            return out + v
        # hidden_states[layer] is the output of block layer-1
        self.hook = self.layers[layer - 1].register_forward_hook(fn)

    def clear_steer(self):
        if self.hook is not None:
            self.hook.remove(); self.hook = None

    # ---------- forced choice + hidden capture
    @torch.no_grad()
    def score(self, texts, prefix, opts, want_hidden=False):
        """Returns (probs[N,len(opts)], massfrac[N], hid_end, hid_dec) ; hid as float16 [N, nL+1, d]."""
        tok = self.tok
        pre_ids = tok(prefix, add_special_tokens=False).input_ids
        opt_ids = [tok(o, add_special_tokens=False).input_ids for o in opts]
        probs, mass, H_end, H_dec = [], [], [], []
        for b in range(0, len(texts), BS):
            base = [chat_ids(tok, t) + pre_ids for t in texts[b:b + BS]]
            # one sequence per (item, option): base + option tokens; hidden taken from the option-0 copy
            seqs, meta = [], []
            for i, s in enumerate(base):
                for k, o in enumerate(opt_ids):
                    seqs.append(s + o); meta.append((i, k, len(s), len(o)))
            ids, att = pad_left(seqs, self.pad)
            ids, att = ids.to(self.m.device), att.to(self.m.device)
            keep = max(len(o) for o in opt_ids) + 1
            out = self.m(input_ids=ids, attention_mask=att, output_hidden_states=want_hidden, logits_to_keep=keep)
            lp = torch.log_softmax(out.logits.float(), -1)  # [B, keep, V]
            L = ids.shape[1]
            off = L - keep  # full-seq position p -> lp index p - off
            tot = np.zeros((len(base), len(opts)))
            first_mass = np.zeros(len(base))
            for r, (i, k, ls, lo) in enumerate(meta):
                start = L - lo  # first option token position in padded seq
                s = 0.0
                for j in range(lo):
                    s += lp[r, start - 1 + j - off, ids[r, start + j]].item()
                tot[i, k] = s
                first_mass[i] += math.exp(s)  # total prob of the full option strings
            p = np.exp(tot - tot.max(1, keepdims=True)); p /= p.sum(1, keepdims=True)
            probs.append(p); mass.append(first_mass)
            if want_hidden:
                hs = out.hidden_states  # tuple nL+1 of [B, L, d]
                rows = [r for r, (i, k, ls, lo) in enumerate(meta) if k == 0]
                lo0 = len(opt_ids[0]); npre = len(pre_ids)
                dec_pos = L - lo0 - 1
                end_pos = dec_pos - npre
                st = torch.stack([h[rows] for h in hs], 1)  # [B, nL+1, L, d]
                H_dec.append(st[:, :, dec_pos, :].float().cpu().numpy().astype(np.float16))
                H_end.append(st[:, :, end_pos, :].float().cpu().numpy().astype(np.float16))
                del st
            del out, lp
        probs = np.concatenate(probs); mass = np.concatenate(mass)
        if want_hidden:
            return probs, mass, np.concatenate(H_end), np.concatenate(H_dec)
        return probs, mass, None, None

    @torch.no_grad()
    def generate(self, texts):
        tok = self.tok; outs = []
        gbs = max(1, BS * 2)
        for b in range(0, len(texts), gbs):
            seqs = [chat_ids(tok, t) for t in texts[b:b + gbs]]
            ids, att = pad_left(seqs, self.pad)
            g = self.m.generate(input_ids=ids.to(self.m.device), attention_mask=att.to(self.m.device),
                                max_new_tokens=GEN_TOKENS, do_sample=False, pad_token_id=self.pad)
            for r in range(len(seqs)):
                outs.append(tok.decode(g[r, ids.shape[1]:], skip_special_tokens=True))
        return outs


def parse(content):
    parts = re.split(r"</?answer>", content, flags=re.I)
    ans = parts[1] if len(parts) > 1 else content
    dm = re.search(r"DECISION:\s*\**\s*(ANSWER|CALL[_\s-]?TOOL|DECLINE)", ans, re.I)
    dec = dm.group(1).upper().replace(" ", "_").replace("-", "_") if dm else None
    if dec is None:
        lm = re.search(r"DECISION:\s*\(?([ABC])\)?", ans, re.I)
        if lm: dec = ["ANSWER", "CALL_TOOL", "DECLINE"][ord(lm.group(1).upper()) - 65]
    if dec is None:
        allm = re.findall(r"(ANSWER|CALL[_\s-]?TOOL|DECLINE)", ans, re.I)
        if allm: dec = allm[-1].upper().replace(" ", "_").replace("-", "_")
    if dec and dec.startswith("CALL"): dec = "CALL_TOOL"
    pm = re.search(r"PROBABILITY_YES:\s*(\d+(?:\.\d+)?)", ans, re.I)
    prob = max(0.0, min(100.0, float(pm.group(1)))) if pm else None
    return dec, prob


def auroc(y, s):
    from sklearn.metrics import roc_auc_score
    y = np.asarray(y)
    return float(roc_auc_score(y, s)) if len(set(y.tolist())) == 2 else None


def run_model(name, items):
    tag = re.sub(r"[^A-Za-z0-9]+", "_", name.split("/")[-1])
    if os.path.exists(f"{OUT}/{tag}.json"):
        log("skip (done)", name); return
    t0 = time.time()
    log("load", name)
    R = Runner(name)
    log(f"loaded {name}: {R.nL} layers, dtype {DT}, {time.time()-t0:.0f}s")
    act = [it for it in items if it["set"] in ("train", "transfer", "nse")]
    ask = [it for it in items if it["set"] == "nse_ask"]
    nse = [it for it in items if it["set"] == "nse"]

    # 1-2 action forced choice + hidden
    t1 = time.time()
    P_act, M_act, H_end, H_dec = R.score([it["text"] for it in act], DEC_PREFIX, DEC_OPTS, want_hidden=True)
    log(f"action FC + hidden: {len(act)} items {time.time()-t1:.0f}s; mean first-token mass {M_act.mean():.3f}")
    # 3 ask
    P_ask, M_ask, _, _ = R.score([it["text"] for it in ask], CAT_PREFIX, CAT_OPTS)
    log(f"ask FC: {len(ask)} items; mean mass {M_ask.mean():.3f}")
    # 4 generation on NSE only
    t1 = time.time()
    gens = R.generate([it["text"] for it in nse])
    log(f"gen: {len(nse)} items {time.time()-t1:.0f}s")

    # 5 probes
    from sklearn.linear_model import LogisticRegression
    from sklearn.preprocessing import StandardScaler
    from sklearn.pipeline import make_pipeline
    idx = {s: np.array([i for i, it in enumerate(act) if it["set"] == s]) for s in ("train", "transfer", "nse")}
    y = np.array([it["y"] for it in act])
    layer_table = []
    best = None
    for pos, H in (("END", H_end), ("DEC", H_dec)):
        for l in range(1, R.nL + 1):
            Xtr, Xte = H[idx["train"], l].astype(np.float32), H[idx["transfer"], l].astype(np.float32)
            clf = make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000, C=0.05)).fit(Xtr, y[idx["train"]])
            a_lr = auroc(y[idx["transfer"]], clf.predict_proba(Xte)[:, 1])
            mu1 = Xtr[y[idx["train"]] == 1].mean(0); mu0 = Xtr[y[idx["train"]] == 0].mean(0)
            d = mu1 - mu0
            a_dm = auroc(y[idx["transfer"]], Xte @ d)
            row = dict(pos=pos, layer=l, transfer_auroc_lr=a_lr, transfer_auroc_dm=a_dm)
            layer_table.append(row)
            if best is None or (a_lr or 0) > best[0]:
                best = (a_lr or 0, pos, l)
    _, bpos, bl = best
    H = H_end if bpos == "END" else H_dec
    Xtr = H[idx["train"], bl].astype(np.float32)
    clf = make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000, C=0.05)).fit(Xtr, y[idx["train"]])
    mu1 = Xtr[y[idx["train"]] == 1].mean(0); mu0 = Xtr[y[idx["train"]] == 0].mean(0)
    dvec = mu1 - mu0
    p_all = clf.predict_proba(H[:, bl].astype(np.float32))[:, 1]
    proj_all = H[:, bl].astype(np.float32) @ (dvec / np.linalg.norm(dvec))
    # shuffled-label control probe
    rng = np.random.default_rng(0)
    clf_sh = make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000, C=0.05)).fit(Xtr, rng.permutation(y[idx["train"]]))
    p_sh = clf_sh.predict_proba(H[:, bl].astype(np.float32))[:, 1]
    # threshold: Youden-optimal on transfer
    from sklearn.metrics import roc_curve
    fpr, tpr, thr = roc_curve(y[idx["transfer"]], p_all[idx["transfer"]])
    thr_y = float(thr[np.argmax(tpr - fpr)])
    log(f"probe: best {bpos} L{bl}/{R.nL} transfer AUROC {best[0]:.3f}; NSE AUROC {auroc(y[idx['nse']], p_all[idx['nse']])}")
    # save chosen-layer hidden for NSE (both positions) for offline analysis
    np.savez_compressed(f"{OUT}/{tag}_hid.npz", end=H_end[idx["nse"], bl], dec=H_dec[idx["nse"], bl],
                        train_end=H_end[idx["train"], bl], train_dec=H_dec[idx["train"], bl],
                        transfer_end=H_end[idx["transfer"], bl], transfer_dec=H_dec[idx["transfer"], bl],
                        dvec=dvec, layer=bl)

    rows = []
    ask_by = {it["id"][:-4]: (P_ask[i], M_ask[i]) for i, it in enumerate(ask)}
    for k, i in enumerate(idx["nse"]):
        it = act[i]
        dec, prob = parse(gens[k])
        pa, ma = ask_by.get(it["id"], (None, None))
        rows.append(dict(id=it["id"], case=it["case"], arm=it["arm"], level=it["level"], y=it["y"], truthYes=it["truthYes"],
                         p_answer=float(P_act[i, 0]), p_tool=float(P_act[i, 1]), p_decline=float(P_act[i, 2]), fc_mass=float(M_act[i]),
                         probe=float(p_all[i]), probe_shuf=float(p_sh[i]), proj=float(proj_all[i]),
                         ask_p1=float(pa[0]) if pa is not None else None, ask_p2=float(pa[1]) if pa is not None else None,
                         ask_p3=float(pa[2]) if pa is not None else None, ask_mass=float(ma) if ma is not None else None,
                         gen_decision=dec, gen_prob=prob, gen=gens[k][:600]))
    side = dict(train_transfer=[dict(id=act[i]["id"], set=act[i]["set"], y=int(y[i]), family=act[i].get("family"),
                                     p_answer=float(P_act[i, 0]), p_decline=float(P_act[i, 2]), probe=float(p_all[i]))
                                for i in np.concatenate([idx["train"], idx["transfer"]])])

    # 6 steering (forced-choice action only)
    steer = []
    if STEER:
        st_items = [it for it in nse if it["level"] in ("L0", "L2", "L2fab")]
        texts = [it["text"] for it in st_items]
        u = dvec / np.linalg.norm(dvec)
        dnorm = float(np.linalg.norm(dvec))
        # typical residual norm at this layer for scale reference
        rnorm = float(np.linalg.norm(H[idx["nse"], bl].astype(np.float32), axis=1).mean())
        conds = [("none", 0.0, None)]
        for a in (-2.0, -1.0, -0.5, 0.5, 1.0, 2.0):
            conds.append(("dir", a, u * a * dnorm))
        rs = np.random.default_rng(1)
        for r in range(8):
            v = rs.standard_normal(u.shape); v /= np.linalg.norm(v)
            for a in (-2.0, 2.0):
                conds.append((f"rand{r}", a, v * a * dnorm))
        for cname, a, vec in conds:
            R.set_steer(bl, vec)
            P, _, _, _ = R.score(texts, DEC_PREFIX, DEC_OPTS)
            R.clear_steer()
            for it, p in zip(st_items, P):
                steer.append(dict(id=it["id"], arm=it["arm"], level=it["level"], cond=cname, alpha=a,
                                  p_answer=float(p[0]), p_tool=float(p[1]), p_decline=float(p[2])))
        log(f"steer: {len(conds)} conds x {len(st_items)} items; |d|={dnorm:.2f} resid norm {rnorm:.1f}")
    res = dict(model=name, n_layers=R.nL, best=dict(pos=bpos, layer=bl, transfer_auroc=best[0]), thr_youden=thr_y,
               layer_table=layer_table, rows=rows, side=side, steer=steer,
               dnorm=float(np.linalg.norm(dvec)), secs=time.time() - t0,
               opt_first_tokens={o: R.tok(o, add_special_tokens=False).input_ids for o in DEC_OPTS + CAT_OPTS})
    json.dump(res, open(f"{OUT}/{tag}.json", "w"))
    log(f"DONE {name} in {time.time()-t0:.0f}s")
    del R; gc.collect()
    if E("CLEAN", "0") == "1":
        import shutil, glob
        for d in glob.glob(os.path.expanduser("~/.cache/huggingface/hub/models--" + name.replace("/", "--"))):
            shutil.rmtree(d, ignore_errors=True)
    if DEV == "cuda": torch.cuda.empty_cache()


def main():
    items = load_items()
    log(f"{len(items)} items; device {DEV}")
    for name in [m.strip() for m in E("MODELS", "Qwen/Qwen2.5-0.5B-Instruct").split(",") if m.strip()]:
        try:
            run_model(name, items)
        except Exception:
            log("FAILED", name); traceback.print_exc()
            gc.collect()
            if DEV == "cuda": torch.cuda.empty_cache()
    log("ALL DONE")


if __name__ == "__main__":
    main()
