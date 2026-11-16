# Knowable-question accuracy under steering (new sprint work) -> results/steer_accuracy.json
import json, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from analyze import parse_semantic, prob
out = {}
for tag in ["qwen3-14b", "llama31-8b", "qwen3-8b", "qwen3-4b", "qwen25-7b", "qwen25-3b", "mistral-7b", "llama32-3b", "gate-3b"]:
    rows = {r["iid"]: r for r in json.load(open(f"results/v2-{tag}/rows.json"))["rows"]}
    srcs = [("v2", "xsteer.json", "xdir", 0), ("v3", "xsteer2.json", "xdir", 8), ("v3", "xsteer2.json", "random", 8)]
    o = {}
    for v, f, kind, a in srcs:
        path = f"results/{v}-{tag}/{f}" if os.path.exists(f"results/{v}-{tag}/{f}") else f"results/v2-{tag}/{f}"
        if not os.path.exists(path): continue
        S = [r for r in json.load(open(path)) if r["kind"] == kind and r["alpha"] == a and "/know/L2" in r["iid"] and r.get("text")]
        if kind == "xdir" and a == 0 and not S:  # no a=0 steering run: unsteered main generations
            S = [dict(iid=r["iid"], text=r["text"]) for r in rows.values() if r["set"] == "nse" and r["label"] == 0 and r["level"] == "L2" and r.get("text")]
        ok = [(prob(r["text"]) > 50) == rows[r["iid"]]["gold"] for r in S if parse_semantic(r["text"]) == "ANSWER" and prob(r["text"]) is not None]
        o[f"{kind}{a:+d}"] = dict(acc=sum(ok) / max(1, len(ok)), n_answered=len(ok), n=len(S))
    out[tag] = o; print(tag, {k: round(v["acc"], 2) for k, v in o.items()})
json.dump(out, open("results/steer_accuracy.json", "w"), indent=1)
