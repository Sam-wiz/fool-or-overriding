# v2 analysis (new sprint work): layer scan, x-steering, pushback X-scores, behaviour table.
import json, os, sys, re, collections, numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from analyze import load, parse_semantic, prob
from sklearn.metrics import roc_auc_score

def layer_verdicts(scan, NL):
    out = {}
    for probe in ("X_dm", "N_dm_crossfit"):
        deep, early, allv = [], [], []
        for L, o in scan["layers"].items():
            v = o[probe]; L = int(L); fi = v["FI_L2"]["point"]
            if not v["valid"]: continue
            allv.append((L, fi)); (deep if L / NL >= 0.5 else early).append(fi)
        md = float(np.median(deep)) if deep else None
        out[probe] = dict(n_valid=len(allv), n_layers=NL, n_valid_deep=len(deep),
                          median_FI_deep=md, median_FI_early=float(np.median(early)) if early else None,
                          verdict_deep=(None if md is None else "Overriding" if md < .25 else "Fooled" if md > .5 else "Mixed"))
    return out

def xsteer(d):
    p = os.path.join(d, "xsteer.json")
    if not os.path.exists(p): return None
    S = json.load(open(p)); g = collections.defaultdict(list)
    for r in S:
        if r.get("text") is not None: r["decision"] = parse_semantic(r["text"])
        arm = "unk" if "/unk/" in r["iid"] else "know"; lv = r["iid"].split("/")[-1]
        g[(r["kind"], r["alpha"], f"{arm}_{lv}")].append(r)
    out = {}
    for (k, a, c), v in sorted(g.items()):
        e = dict(n=len(v), pact_lo=float(np.mean([r["pact_lo"] for r in v])))
        if v[0].get("text") is not None:
            dec = collections.Counter(r["decision"] for r in v)
            e.update(commit=dec["ANSWER"] / len(v), decline=dec["DECLINE"] / len(v), tool=dec["CALL_TOOL"] / len(v))
        out[f"{k}|{a}|{c}"] = e
    return out

def push(d, rows):
    p = os.path.join(d, "push.json")
    if not os.path.exists(p): return None
    P = json.load(open(p)); idr = {r["iid"]: r for r in rows}
    if "x_before" not in P[0]: return None
    g = collections.defaultdict(list)
    for q in P:
        q["decision"] = parse_semantic(q["text"]); r0 = idr[q["iid"]]
        g[("unk" if r0["label"] else "know") + "_" + r0["level"]].append((r0, q))
    out = {}
    for c, v in g.items():
        tr = collections.Counter(f"{a.get('decision')}->{b.get('decision')}" for a, b in v)
        out[c] = dict(n=len(v), commit_before=float(np.mean([a.get("decision") == "ANSWER" for a, b in v])),
                      commit_after=float(np.mean([b["decision"] == "ANSWER" for a, b in v])),
                      decline_before=float(np.mean([a.get("decision") == "DECLINE" for a, b in v])),
                      decline_after=float(np.mean([b["decision"] == "DECLINE" for a, b in v])),
                      x_before=float(np.mean([b["x_before"] for a, b in v])), x_after=float(np.mean([b["x_after"] for a, b in v])),
                      transitions=dict(tr))
    # does the knowable/unknowable separation survive pushback?
    def sep(key):
        k = [b[key] for a, b in g.get("know_L2", [])]; u = [b[key] for a, b in g.get("unk_L2", [])]
        return float(roc_auc_score([0] * len(k) + [1] * len(u), k + u)) if k and u else None
    out["sep_L2_before"] = sep("x_before"); out["sep_L2_after"] = sep("x_after")
    return out

def behaviour(rows):
    out = {}
    nse = [r for r in rows if r["set"] == "nse"]
    for arm in ("unk", "know"):
        for lv in ("L0", "L1", "L2", "L2irr", "L2fab"):
            g = [r for r in nse if (r["label"] == (arm == "unk")) and r["level"] == lv]
            if not g: continue
            dec = collections.Counter(r.get("decision") for r in g)
            out[f"{arm}_{lv}"] = dict(n=len(g), commit=dec["ANSWER"] / len(g), decline=dec["DECLINE"] / len(g),
                                      tool=dec["CALL_TOOL"] / len(g), unparsed=dec[None] / len(g),
                                      ask_unk=float(np.mean([r["ask_unk"] for r in g])),
                                      p50=float(np.mean([r.get("prob_yes") == 50 for r in g if r.get("decision") == "ANSWER"])) if dec["ANSWER"] else None)
    for dom in ("crypto", "sports", "weather"):
        for lv in ("L0", "L1", "L2"):
            g = [r for r in rows if r["set"] == "xfer" and r.get("domain") == dom and r["label"] == 1 and r["level"] == lv]
            if g: out[f"xfer_{dom}_unk_{lv}"] = dict(n=len(g), commit=float(np.mean([r["commit"] for r in g])))
        g = [r for r in rows if r["set"] == "xfer" and r.get("domain") == dom and r["label"] == 0]
        if g:
            acc = [(r["prob_yes"] > 50) == r["gold"] for r in g if r.get("decision") == "ANSWER" and r.get("prob_yes") is not None]
            out[f"xfer_{dom}_ans_L2"] = dict(n=len(g), commit=float(np.mean([r["commit"] for r in g])), acc=float(np.mean(acc)) if acc else None)
    for lv in ("thin", "rich", "scram", "scramfull"):
        g = [r for r in rows if r["set"] == "flag" and r["level"] == lv]
        if g: out[f"flag_{lv}"] = dict(n=len(g), commit=float(np.mean([r["commit"] for r in g])))
    return out

if __name__ == "__main__":
    ALL = {}
    for d in sys.argv[1:]:
        meta, rows = load(d); NL = meta["n_layers"]
        o = dict(tag=meta["tag"], model=meta["model"], NL=NL, behaviour=behaviour(rows))
        sp = os.path.join(d, "layerscan.json")
        if os.path.exists(sp):
            scan = json.load(open(sp)); o["layer_verdicts"] = layer_verdicts(scan, NL)
        o["xsteer"] = xsteer(d); o["push"] = push(d, rows)
        json.dump(o, open(os.path.join(d, "v2summary.json"), "w"), indent=1)
        ALL[o["tag"]] = o
        print(f"\n===== {o['tag']}  NL={NL}")
        b = o["behaviour"]
        print("  unk commit:", {k[4:]: round(v["commit"], 2) for k, v in b.items() if k.startswith("unk_")},
              "| decline:", {k[4:]: round(v["decline"], 2) for k, v in b.items() if k.startswith("unk_")})
        print("  know commit:", {k[5:]: round(v["commit"], 2) for k, v in b.items() if k.startswith("know_")}, "ask_unk L2:", round(b["unk_L2"]["ask_unk"], 3), round(b["know_L2"]["ask_unk"], 3))
        if "layer_verdicts" in o: print("  layer verdicts:", o["layer_verdicts"])
        if o["xsteer"]:
            for k, v in o["xsteer"].items():
                if any(t in k for t in ("unk_L2", "know_L2", "unk_L0")) and "L2fab" not in k: print("   xs", k, v)
        if o["push"]:
            for k, v in o["push"].items(): print("   push", k, v)
