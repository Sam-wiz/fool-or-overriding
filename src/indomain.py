# Post-hoc (added after seeing that the synthetic probe does not transfer to NSE for some models).
# Two probes that never see the NSE level manipulation in training:
#   X  "cross-domain": direction trained on crypto/sports/weather L2 (answerable vs unknowable, same rich panel),
#      applied to NSE.  No NSE data used for training.
#   N  "cross-fitted NSE": direction from NSE L2 know-vs-unk on half of the cases, applied to the other half
#      (20 random 50/50 splits).  Only L2 used for training; L0/L1/L2'/L2-fab and the positive control never seen.
# For both: diff-of-means direction (robust at n<100) and logistic regression; report scores in units of the
# training class gap, shifts with case bootstrap, the pre-registered fooling index, and a validity gate.
import json, sys, os, numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_auc_score
rs = np.random.RandomState(0)

def boot(vals_by_case, f, B=1000):
    cs = list(vals_by_case); out = []
    for _ in range(B):
        ii = rs.randint(0, len(cs), len(cs)); v = f([cs[i] for i in ii])
        if v is not None and np.isfinite(v): out.append(v)
    return (float(np.percentile(out, 2.5)), float(np.percentile(out, 97.5)))

def run(d):
    J = json.load(open(os.path.join(d, "rows.json"))); rows = J["rows"]; meta = J["meta"]
    A = np.load(os.path.join(d, "acts_sel.npy")).astype(np.float32)  # N, k, dim
    sel = meta["probe"]["sel_layers"]
    assert A.shape[0] == len(rows)
    return run_arrays(rows, lambda li: A[:, li], sel, meta["tag"])

def run_arrays(rows, getX, sel, tag, lr=True):
    res = {"tag": tag, "layers": {}}
    nse = [i for i, r in enumerate(rows) if r["set"] == "nse"]
    cases = sorted({rows[i]["case"] for i in nse})
    key = {(rows[i]["case"], "unk" if rows[i]["label"] else "know", rows[i]["level"]): i for i in nse}
    xtr = [i for i, r in enumerate(rows) if r["set"] == "xfer" and r["level"] == "L2"]
    for li, L in enumerate(sel):
        X = getX(li)
        out = {}
        # ---------- X: cross-domain ----------
        y = np.array([rows[i]["label"] for i in xtr])
        mu1, mu0 = X[xtr][y == 1].mean(0), X[xtr][y == 0].mean(0); u = mu1 - mu0
        s_dm = X @ u; gdm = (mu1 - mu0) @ u
        cands = [("X_dm", s_dm, gdm)]
        if lr:
            sc = StandardScaler().fit(X[xtr]); clf = LogisticRegression(C=0.01, max_iter=5000).fit(sc.transform(X[xtr]), y)
            s_lr = clf.decision_function(sc.transform(X)); glr = s_lr[xtr][y == 1].mean() - s_lr[xtr][y == 0].mean()
            cands.append(("X_lr", s_lr, glr))
        for nm, s, g in cands:
            out[nm] = summarize_scores(s / g, key, cases)
        # ---------- N: cross-fitted on NSE L2 only ----------
        acc = {c: {} for c in cases}
        for sp in range(20):
            r2 = np.random.RandomState(100 + sp); perm = r2.permutation(len(cases)); half = set(perm[: len(cases) // 2])
            trc = [c for j, c in enumerate(cases) if j in half]; tec = [c for j, c in enumerate(cases) if j not in half]
            iu = [key[(c, "unk", "L2")] for c in trc]; ik = [key[(c, "know", "L2")] for c in trc]
            u = X[iu].mean(0) - X[ik].mean(0); g = (X[iu].mean(0) - X[ik].mean(0)) @ u
            for c in tec:
                for (cc, arm, lv), i in key.items():
                    if cc == c: acc[c].setdefault((arm, lv), []).append(float(X[i] @ u / g))
        s_cf = np.full(len(rows), np.nan)
        for (c, arm, lv), i in key.items(): s_cf[i] = np.mean(acc[c][(arm, lv)])
        out["N_dm_crossfit"] = summarize_scores(s_cf, key, cases)
        res["layers"][str(L)] = out
    return res

def summarize_scores(s, key, cases):
    lv = {}
    extra = [l for l in ("L2leak", "L2post") if (cases[0], "unk", l) in key]  # post-review anchors
    for arm, levels in (("unk", ["L0", "L1", "L2", "L2irr", "L2fab"] + extra), ("know", ["L0", "L1", "L2"])):
        for l in levels: lv[f"{arm}_{l}"] = float(np.mean([s[key[(c, arm, l)]] for c in cases]))
    def m(cs, arm, l): return np.mean([s[key[(c, arm, l)]] for c in cs])
    def sh(arm, a, b): return lambda cs: m(cs, arm, a) - m(cs, arm, b)
    def fi(l): return lambda cs: (m(cs, "unk", "L0") - m(cs, "unk", l)) / (m(cs, "unk", "L0") - m(cs, "know", "L2"))
    out = dict(levels=lv)
    out["auroc_L2_know_vs_unk"] = float(roc_auc_score([0] * len(cases) + [1] * len(cases),
                                         [s[key[(c, "know", "L2")]] for c in cases] + [s[key[(c, "unk", "L2")]] for c in cases]))
    for nm, f in [("shift_unk_L0_L2", sh("unk", "L0", "L2")), ("shift_unk_L0_L2fab", sh("unk", "L0", "L2fab")),
                  ("shift_unk_L0_L2irr", sh("unk", "L0", "L2irr")), ("shift_unk_L0_L1", sh("unk", "L0", "L1")),
                  ("posctrl_know_L0_L2", sh("know", "L0", "L2")),
                  ("FI_L2", fi("L2")), ("FI_L2fab", fi("L2fab"))] + [(f"FI_{l}", fi(l)) for l in extra]:
        out[nm] = dict(point=float(f(cases)), ci=boot(cases, f))
    pc = out["posctrl_know_L0_L2"]; fiv = out["FI_L2"]
    valid = out["auroc_L2_know_vs_unk"] >= 0.8 and pc["ci"][0] > 0
    out["valid"] = bool(valid)
    out["verdict"] = ("invalid-probe" if not valid else "Overriding" if fiv["ci"][1] < 0.25 else "Fooled" if fiv["ci"][0] > 0.5 else "Mixed")
    return out

if __name__ == "__main__":
    allres = {}
    for d in sys.argv[1:]:
        r = run(d); allres[r["tag"]] = r
        print(f"\n=== {r['tag']}")
        for L, o in r["layers"].items():
            for nm, v in o.items():
                print(f"  L{L:>3s} {nm:14s} AUC={v['auroc_L2_know_vs_unk']:.3f} posctrl={v['posctrl_know_L0_L2']['point']:+.2f} {tuple(round(x,2) for x in v['posctrl_know_L0_L2']['ci'])} "
                      f"unkL0->L2={v['shift_unk_L0_L2']['point']:+.2f} fab={v['shift_unk_L0_L2fab']['point']:+.2f} irr={v['shift_unk_L0_L2irr']['point']:+.2f} "
                      f"FI={v['FI_L2']['point']:+.2f} {tuple(round(x,2) for x in v['FI_L2']['ci'])} -> {v['verdict']}")
        json.dump(r, open(os.path.join(d, "indomain.json"), "w"), indent=1)
