# Item-level + monitor stats with the cross-domain direction at layer NL//2 (new sprint work).
import json, sys, os, numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from analyze import load
from sklearn.metrics import roc_auc_score
def auc(y, s):
    return float(roc_auc_score(y, s)) if len(set(y)) == 2 else None
out = {}
for d in sys.argv[1:]:
    meta, rows = load(d); NL = meta["n_layers"]; sel = meta["probe"]["sel_layers"]
    A = np.load(os.path.join(d, "acts_sel.npy")).astype(np.float32); li = sel.index(NL // 2); X = A[:, li]
    xi = [i for i, r in enumerate(rows) if r["set"] == "xfer" and r["level"] == "L2"]
    y = np.array([rows[i]["label"] for i in xi]); u = X[xi][y == 1].mean(0) - X[xi][y == 0].mean(0)
    s = X @ u / (u @ u)
    for i, r in enumerate(rows): r["x"] = float(s[i])
    o = {}
    # (1) within-condition: are committed unknowable items represented as less unknowable?
    for lv in ("L2", "L2fab", "L2irr"):
        g = [r for r in rows if r["set"] == "nse" and r["label"] == 1 and r["level"] == lv and r.get("decision")]
        o[f"within_{lv}_commit_auc"] = auc([r["commit"] for r in g], [-r["x"] for r in g]); o[f"within_{lv}_n_commit"] = int(sum(r["commit"] for r in g))
    g = [r for r in rows if r["set"] == "flag" and r.get("decision")]
    o["within_flag_commit_auc"] = auc([r["commit"] for r in g], [-r["x"] for r in g]); o["flag_n_commit"] = int(sum(r["commit"] for r in g))
    # (2) monitor on NSE+flagship items the agent ANSWERED (xfer excluded: used to train the direction)
    ans = [r for r in rows if r["set"] in ("nse", "flag") and r.get("decision") == "ANSWER"]
    yb = [r["label"] for r in ans]
    conf = lambda r: -abs(r["prob_yes"] - 50) if r.get("prob_yes") is not None else 0.0
    o["monitor"] = dict(n=len(ans), n_bad=int(sum(yb)), xprobe=auc(yb, [r["x"] for r in ans]), ask=auc(yb, [r["ask_unk"] for r in ans]),
                        stated_conf=auc(yb, [conf(r) for r in ans]), synth_probe=auc(yb, [r["s"] for r in ans]))
    # (3) stated probability when committing on unknowable items
    cm = [r for r in rows if r["set"] == "nse" and r["label"] == 1 and r.get("decision") == "ANSWER"]
    p = [r["prob_yes"] for r in cm if r.get("prob_yes") is not None]
    o["commit_prob"] = dict(n=len(cm), frac_50=float(np.mean([x == 50 for x in p])) if p else None,
                            mean_abs_dev=float(np.mean([abs(x - 50) for x in p])) if p else None,
                            frac_confident=float(np.mean([abs(x - 50) >= 15 for x in p])) if p else None)
    kn = [r for r in rows if r["set"] == "nse" and r["label"] == 0 and r["level"] == "L2" and r.get("decision") == "ANSWER" and r.get("prob_yes") is not None]
    o["know_L2_acc"] = float(np.mean([(r["prob_yes"] > 50) == r["gold"] for r in kn])) if kn else None
    out[meta["tag"]] = o
    print(meta["tag"], json.dumps(o))
json.dump(out, open("results/extra_stats.json", "w"), indent=1)
