"""Phase 3 (post-hoc, Addendum C): which component of the panel's effect at the decision token carries the action?
For unk L2/L2fab targets, patch the same-case unk L0 value of ONE component into the panel run at DEC, at layer l:
  h' = h + ((h0 - h) . v) v   for v in {c_l (within-class decline direction), uperp_l (u_l with c_l removed), u_l, 8 random}
Directions are recomputed per layer from synthetic train activations at DEC (decline split from forced choice on train).
ENV: MODELS, LAYERS_<tag> optional, DATA, OUT, BS"""
import os, sys, json, time, re, gc
import numpy as np
import torch
sys.path.insert(0, "/content")
import fo_run as F
import fo_phase2 as P2

E = os.environ.get
OUT = E("OUT", "/content/phase3"); os.makedirs(OUT, exist_ok=True)
log = F.log


def run_model(name, items):
    tag = re.sub(r"[^A-Za-z0-9]+", "_", name.split("/")[-1])
    if os.path.exists(f"{OUT}/{tag}.json"):
        return
    t0 = time.time()
    R = F.Runner(name); tok = R.tok
    pre = tok(F.DEC_PREFIX, add_special_tokens=False).input_ids
    train = [it for it in items if it["set"] == "train"]
    nse = [it for it in items if it["set"] == "nse"]
    Ptr, Htr = P2.fc(R, [F.chat_ids(tok, it["text"]) + pre for it in train], F.DEC_OPTS, want_hidden=True)
    ytr = np.array([it["y"] for it in train]); dec = Ptr[:, 2] > 0.5
    P0, Hn = P2.fc(R, [F.chat_ids(tok, it["text"]) + pre for it in nse], F.DEC_OPTS, want_hidden=True)
    key = {(it["case"], it["arm"], it["level"]): i for i, it in enumerate(nse)}
    tgt = [i for i, it in enumerate(nse) if it["arm"] == "unk" and it["level"] in ("L2", "L2fab")]
    src = [key[(nse[i]["case"], "unk", "L0")] for i in tgt]
    bases = [F.chat_ids(tok, nse[i]["text"]) + pre for i in tgt]
    nL = R.nL
    default = sorted(set(int(round(nL * f)) for f in (0.45, 0.55, 0.65, 0.75, 0.85, 0.95)))
    layers = [int(x) for x in E("LAYERS_" + tag, ",".join(map(str, default))).split(",")]
    rs = np.random.default_rng(11)
    res = []
    info = {}
    for l in layers:
        X = Htr[:, l].astype(np.float32)
        u = X[ytr == 1].mean(0) - X[ytr == 0].mean(0); u /= np.linalg.norm(u)
        cs = [X[(ytr == k) & dec].mean(0) - X[(ytr == k) & ~dec].mean(0) for k in (0, 1)
              if ((ytr == k) & dec).sum() > 3 and ((ytr == k) & ~dec).sum() > 3]
        dirs = {"u": u}
        if cs:
            c = np.mean(cs, 0); c /= np.linalg.norm(c)
            up = u - (u @ c) * c; up /= np.linalg.norm(up)
            dirs["c"] = c; dirs["uperp"] = up
            info[l] = dict(cos_u_c=float(u @ c))
        for k in range(8):
            v = rs.standard_normal(u.shape[0]); dirs[f"rand{k}"] = v / np.linalg.norm(v)
        h0 = torch.tensor(Hn[src][:, l].astype(np.float32), device=R.m.device)
        for dn, v in dirs.items():
            vt = torch.tensor(v, device=R.m.device, dtype=torch.float32)
            def fn(h, it, vt=vt, h0=h0):
                hf = h.float(); return hf + ((h0[it] - hf) @ vt) * vt
            Pp, _ = P2.fc(R, bases, F.DEC_OPTS, patch=(l, fn))
            # how much of the L0-L2 difference lies along v (fraction of squared norm)
            dH = (Hn[src][:, l] - Hn[tgt][:, l]).astype(np.float32)
            frac = float(np.mean((dH @ v) ** 2 / (np.sum(dH ** 2, 1) + 1e-8)))
            res.append(dict(layer=l, dir=dn, p_answer=float(Pp[:, 0].mean()), p_decline=float(Pp[:, 2].mean()),
                            p_tool=float(Pp[:, 1].mean()), frac_sq=frac))
        log(f"{name} layer {l} done {time.time()-t0:.0f}s")
    out = dict(model=name, layers=layers, info=info, base_answer=float(P0[tgt, 0].mean()), base_decline=float(P0[tgt, 2].mean()),
               src_answer=float(P0[src, 0].mean()), src_decline=float(P0[src, 2].mean()), res=res,
               train_decline_rate=dict(unk=float(dec[ytr == 1].mean()), ans=float(dec[ytr == 0].mean())))
    json.dump(out, open(f"{OUT}/{tag}.json", "w"))
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
    log("ALL DONE")


if __name__ == "__main__":
    main()
