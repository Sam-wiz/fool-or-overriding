# Pull every number the report quotes from results/ (new sprint work) -> results/report_numbers.json
import json, os, numpy as np
ORDER = [t for t in ["qwen3-14b", "llama31-8b", "qwen3-8b", "qwen3-4b", "qwen25-7b", "qwen25-3b", "mistral-7b", "llama32-3b", "gemma2-9b", "gate-3b"] if __import__("os").path.exists(f"results/v2-{t}/v2summary.json")]
X = json.load(open("results/extra_stats.json")); TF = json.load(open("results/tfidf_baselines.json"))
out = {"models": {}, "tfidf": TF}
def wilson(k, n, z=1.96):
    p = k / n; d = 1 + z * z / n; c = p + z * z / (2 * n); h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return [(c - h) / d, (c + h) / d]
for t in ORDER:
    d = f"results/v2-{t}"; V = json.load(open(f"{d}/v2summary.json")); S = json.load(open(f"{d}/summary.json"))
    sc = json.load(open(f"{d}/layerscan.json")); NL = V["NL"]; b = V["behaviour"]
    m = dict(NL=NL, layer_synth=S["layer"], synth_val=S["probe_val"], synth_nse=S["probe_nse_L2"], synth_xfer=S["probe_xfer_L2"],
             behaviour=b, lv=V["layer_verdicts"], extra=X[f"v2-{t}"])
    m["commit_ci"] = {k: wilson(round(v["commit"] * v["n"]), v["n"]) for k, v in b.items() if k.startswith("unk_")}
    for probe in ("X_dm", "N_dm_crossfit"):
        deep = [o[probe] for L, o in sc["layers"].items() if o[probe]["valid"] and int(L) / NL >= 0.5]
        m[f"{probe}_deep"] = dict(n=len(deep),
            posctrl=float(np.median([v["posctrl_know_L0_L2"]["point"] for v in deep])) if deep else None,
            unk_shift=float(np.median([v["shift_unk_L0_L2"]["point"] for v in deep])) if deep else None,
            fab_shift=float(np.median([v["shift_unk_L0_L2fab"]["point"] for v in deep])) if deep else None,
            FI=float(np.median([v["FI_L2"]["point"] for v in deep])) if deep else None,
            FIfab=float(np.median([v["FI_L2fab"]["point"] for v in deep])) if deep else None,
            auc=float(np.median([v["auroc_L2_know_vs_unk"] for v in deep])) if deep else None)
        L = str(NL // 2); v = sc["layers"][L][probe]
        m[f"{probe}_mid"] = dict(layer=NL // 2, valid=v["valid"], FI=v["FI_L2"]["point"], FIci=v["FI_L2"]["ci"], posctrl=v["posctrl_know_L0_L2"]["point"],
                                 posctrl_ci=v["posctrl_know_L0_L2"]["ci"], auc=v["auroc_L2_know_vs_unk"])
    m["xsteer"] = V.get("xsteer"); m["push"] = V["push"]
    out["models"][t] = m
json.dump(out, open("results/report_numbers.json", "w"), indent=1, default=float)
for t, m in out["models"].items():
    print(t, "| X deep", {k: (round(v, 3) if isinstance(v, float) else v) for k, v in m["X_dm_deep"].items()})
    print("   N deep", {k: (round(v, 3) if isinstance(v, float) else v) for k, v in m["N_dm_crossfit_deep"].items()})
    print("   X mid", m["X_dm_mid"]); print("   commit CI L2", [round(x, 2) for x in m["commit_ci"]["unk_L2"]])
