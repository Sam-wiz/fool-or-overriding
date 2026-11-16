# Post-review analysis (new): leaked-answer anchors under the paper's X/N layer scan, neutral vs original
# pushback, and deep.py (graded leakage, matched pairs, read-out gain, patching, base vs instruct).
# usage: python src/analyze_v4.py   -> results/v4_summary.json
import json, os, glob, numpy as np
from sklearn.metrics import roc_auc_score
OUT = {}
def med(x): x = [v for v in x if v is not None and np.isfinite(v)]; return float(np.median(x)) if x else None

for d in sorted(glob.glob("results/v4-*")):
    t = d.split("v4-")[1]; o = {}
    if not os.path.exists(f"{d}/layerscan.json"): continue
    sc = json.load(open(f"{d}/layerscan.json")); rows = json.load(open(f"{d}/rows.json"))["rows"]; NL = json.load(open(f"{d}/rows.json"))["meta"]["n_layers"]
    for pr in ("X_dm", "N_dm_crossfit"):
        V = [(int(L), v[pr]) for L, v in sc["layers"].items() if v[pr]["valid"] and int(L) / NL >= 0.5]
        o[pr] = dict(n=len(V), **{k: med([v[k]["point"] for _, v in V]) for k in ("FI_L2", "FI_L2fab", "FI_L2leak", "FI_L2post", "posctrl_know_L0_L2")},
                     post_gt_panel=sum(1 for _, v in V if v["FI_L2post"]["ci"][0] > v["FI_L2"]["ci"][1]),
                     calib_ratio=med([v["FI_L2"]["point"] / v["FI_L2post"]["point"] for _, v in V if v["FI_L2post"]["point"] > 0.1]),
                     verdict_post={c: sum(1 for _, v in V if c == ("Overriding" if v["FI_L2post"]["ci"][1] < 0.25 else "Fooled" if v["FI_L2post"]["ci"][0] > 0.5 else "Mixed")) for c in ("Overriding", "Mixed", "Fooled")},
                     # all-layer profile for plotting
                     profile={L: dict(valid=v[pr]["valid"], FI_L2=v[pr]["FI_L2"]["point"], FI_L2post=v[pr]["FI_L2post"]["point"], FI_L2leak=v[pr]["FI_L2leak"]["point"]) for L, v in ((int(L), v) for L, v in sc["layers"].items())})
    beh = {}
    for lv in ("L2leak", "L2post"):
        rr = [r for r in rows if r["set"] == "nse" and r["level"] == lv]
        com = [r for r in rr if r.get("decision") == "ANSWER"]
        acc = [((r.get("prob_yes") or 50) > 50) == r["gold"] for r in com if r.get("prob_yes") is not None and r.get("prob_yes") != 50]
        beh[lv] = dict(n=len(rr), commit=float(np.mean([r.get("decision") == "ANSWER" for r in rr])), decline=float(np.mean([r.get("decision") == "DECLINE" for r in rr])),
                       tool=float(np.mean([r.get("decision") == "CALL_TOOL" for r in rr])), acc_of_committed=float(np.mean(acc)) if acc else None, n_dir=len(acc),
                       ask_unk=float(np.mean([r["ask_unk"] for r in rr])), pact_answer=float(np.mean([r["pact"]["ANSWER"] for r in rr])))
    o["behaviour"] = beh
    if os.path.exists(f"{d}/push2.json"):
        P = json.load(open(f"{d}/push2.json")); res = {}
        ids = list(P["before"]); lev = lambda i: "/".join(i.split("/")[2:])
        for nm in ("orig", "neutral"):
            if nm not in P: continue
            gap = {}; aucs = {}
            for L in range(1, NL + 1):
                for when, src in (("before", lambda i: P["before"][i][L - 1]), ("after", lambda i: P[nm][i]["x"][L - 1])):
                    u = [src(i) for i in ids if lev(i) == "unk/L2"]; k = [src(i) for i in ids if lev(i) == "know/L2"]
                    gap.setdefault(when, {})[L] = float(np.mean(u) - np.mean(k))
                    aucs.setdefault(when, {})[L] = float(roc_auc_score([0] * len(k) + [1] * len(u), k + u))
            deep = [L for L in range(NL // 2, NL + 1)]
            # validity at the new position: AUROC >= 0.8 after pushback
            vd = [L for L in deep if aucs["after"][L] >= 0.8 and aucs["before"][L] >= 0.8]
            beh2 = {}
            for lv in ("unk/L2", "unk/L2fab", "know/L2", "know/L0", "unk/L0"):
                ii = [i for i in ids if lev(i) == lv]
                was = [i for i in ii if P[nm][i]["prev_decision"] == "ANSWER"]
                beh2[lv] = dict(commit_before=float(np.mean([P[nm][i]["prev_decision"] == "ANSWER" for i in ii])),
                                commit_after=float(np.mean([P[nm][i]["decision"] == "ANSWER" for i in ii])),
                                abandon=f"{sum(P[nm][i]['decision'] != 'ANSWER' for i in was)}/{len(was)}")
            res[nm] = dict(gap_mid_before=gap["before"][NL // 2], gap_mid_after=gap["after"][NL // 2], auc_mid_after=aucs["after"][NL // 2],
                           n_valid_deep_after=len(vd), gap_ratio_deep=med([gap["after"][L] / gap["before"][L] for L in vd]), behaviour=beh2)
        o["push2"] = res
    OUT[t] = o

D = {}
for d in sorted(glob.glob("results/deep-*")):
    if not os.path.isdir(d) or not os.path.exists(f"{d}/summary.json"): continue
    s = json.load(open(f"{d}/summary.json")); t = d.split("deep-")[1]; o = dict(summary=s["summary"], tfidf=s.get("tfidf"), behaviour=s.get("behaviour"))
    if "T2" in s:
        NL = s["meta"]["n_layers"]; T2 = s["T2"]["by_cond"]; o["T2_fd"] = s["T2"]["fd"]
        o["T2_mid"] = {c: v.get(str(NL // 2)) or v.get(str(NL // 2 + 1)) for c, v in T2.items()}
    if "T3" in s:
        P = s["T3"]; o["T3"] = dict(k=P["k"], src=P["src"], tgt=P["tgt"], layers={L: {m: round(v["restored"], 3) for m, v in x.items()} for L, x in P["layers"].items()})
    D[t] = o
json.dump(dict(v4=OUT, deep=D), open("results/v4_summary.json", "w"), indent=1)
for t, o in OUT.items():
    print(t, {p: {k: (round(v, 2) if isinstance(v, float) else v) for k, v in o[p].items() if k != "profile"} for p in ("X_dm", "N_dm_crossfit")})
    print("   beh", {k: {kk: (round(vv, 2) if isinstance(vv, float) else vv) for kk, vv in v.items()} for k, v in o["behaviour"].items()})
    if "push2" in o: print("   pushbeh", {nm: {lv: x["abandon"] + f' c{x["commit_before"]:.2f}->{x["commit_after"]:.2f}' for lv, x in r["behaviour"].items()} for nm, r in o["push2"].items()})
    if "push2" in o: print("   push", {nm: {k: (round(v, 2) if isinstance(v, float) else v) for k, v in r.items() if k != "behaviour"} for nm, r in o["push2"].items()})
for t, o in D.items():
    print("deep", t, json.dumps(o["summary"])[:600], o.get("tfidf"))
