# Matched-control steering summary (new sprint work): direction vs 3 random dirs at the same |alpha|, generation-based.
import json, sys, os, collections, numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from analyze import parse_semantic
rs = np.random.RandomState(0)
def cell(rows):
    n = len(rows); d = collections.Counter(parse_semantic(r["text"]) for r in rows)
    return dict(n=n, commit=d["ANSWER"] / n, decline=d["DECLINE"] / n, tool=d["CALL_TOOL"] / n, unparsed=d[None] / n,
                lo=float(np.mean([r["pact_lo"] for r in rows])))
out = {}
for d in sys.argv[1:]:
    tag = os.path.basename(d.rstrip("/")).replace("v3-", "").replace("v2-", "").replace("v5-", ""); S = json.load(open(os.path.join(d, "xsteer2.json")))
    if os.path.exists(f"results/v2-{tag}/xsteer.json"):
        base = [r for r in json.load(open(f"results/v2-{tag}/xsteer.json")) if r["alpha"] == 0 and r.get("text") is not None]
    else:  # no a=0 steering run: use the main unsteered generations
        base = [dict(iid=r["iid"], kind="xdir", alpha=0, pact_lo=r.get("pact_lo", 0.0), text=r["text"])
                for r in json.load(open(f"results/v2-{tag}/rows.json"))["rows"] if r["set"] == "nse" and r["level"] in ("L0", "L2", "L2fab") and r.get("text")]
    g = collections.defaultdict(list)
    for r in S + base:
        arm = ("unk_" if "/unk/" in r["iid"] else "know_") + r["iid"].split("/")[-1]
        g[(r["kind"], float(r["alpha"]), arm)].append(r)
    o = {f"{k}|{a:g}|{arm}": cell(v) for (k, a, arm), v in sorted(g.items())}
    out[tag] = o
    print(f"\n== {tag}")
    for arm in ("unk_L2", "unk_L2fab", "know_L2", "unk_L0"):
        line = []
        for k, a in (("xdir", 0), ("xdir", 8), ("random", 8), ("xdir", -8), ("random", -8)):
            c = o.get(f"{k}|{a:g}|{arm}")
            if c: line.append(f"{k}{a:+g}: c={c['commit']:.2f} d={c['decline']:.2f} t={c['tool']:.2f} u={c['unparsed']:.2f}")
        print(f"  {arm:9s} " + " | ".join(line))
json.dump(out, open(os.environ.get("STEER_OUT", "results/steer_v3_raw.json"), "w"), indent=1)
