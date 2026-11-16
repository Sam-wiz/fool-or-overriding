# Post-review figures (new): Fig 1 with the leaked-answer ("answer shown") level, Fig 2 activation patching.
# usage: python src/make_figs_v4.py
import json, os, numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"font.size": 7.5, "axes.spines.top": False, "axes.spines.right": False, "figure.dpi": 220,
                     "savefig.bbox": "tight", "font.family": "DejaVu Sans", "axes.titlesize": 7.5})
ALL = ["qwen3-14b", "llama31-8b", "qwen3-8b", "qwen3-4b", "qwen25-7b", "qwen25-3b", "mistral-7b", "llama32-3b", "gemma2-9b", "gate-3b"]
NICE = {"qwen3-14b": "Qwen3-14B", "llama31-8b": "Llama-3.1-8B", "qwen3-8b": "Qwen3-8B", "qwen3-4b": "Qwen3-4B", "qwen25-3b": "Qwen2.5-3B",
        "gemma2-9b": "Gemma-2-9B", "gate-3b": "Qwen2.5-3B + SFT gate", "qwen25-7b": "Qwen2.5-7B", "mistral-7b": "Mistral-7B-v0.3", "llama32-3b": "Llama-3.2-3B"}
C = dict(act="#c2410c", dec="#9a3412", ask="#2563eb", inside="#15803d", know="#7c3aed")
OUT = "report/figs"; os.makedirs(OUT, exist_ok=True)
tags = [t for t in ALL if os.path.exists(f"results/v4-{t}/layerscan.json") and os.path.exists(f"results/v2-{t}/v2summary.json")]
LV = ["L0", "L1", "L2", "L2irr", "L2fab", "L2post"]; LVN = ["none", "thin", "panel", "irrel.", "fabric.", "ANSWER\nSHOWN"]

def inside_pos(t, probe="X_dm"):
    sc = json.load(open(f"results/v4-{t}/layerscan.json")); NL = json.load(open(f"results/v4-{t}/rows.json"))["meta"]["n_layers"]
    acc = {}
    for L, o in sc["layers"].items():
        v = o[probe]
        if not v["valid"] or int(L) / NL < 0.5: continue
        lv = v["levels"]; a, k = lv["unk_L0"], lv["know_L2"]
        for key, x in lv.items(): acc.setdefault(key, []).append((x - k) / (a - k))
    return {k: float(np.mean(v)) for k, v in acc.items()}

def beh(t):
    b = json.load(open(f"results/v2-{t}/v2summary.json"))["behaviour"]
    rows = [r for r in json.load(open(f"results/v4-{t}/rows.json"))["rows"] if r["set"] == "nse" and r["level"] == "L2post"]
    b = dict(b); b["unk_L2post"] = dict(commit=np.mean([r.get("decision") == "ANSWER" for r in rows]), decline=np.mean([r.get("decision") == "DECLINE" for r in rows]),
                                    ask_unk=np.mean([r["ask_unk"] for r in rows]))
    return b

n = len(tags); cols = 5 if n > 8 else 4; rows_ = int(np.ceil(n / cols))
fig, axs = plt.subplots(rows_, cols, figsize=(7.4, 2.05 * rows_), squeeze=False, sharey=True)
fig.subplots_adjust(hspace=0.62, wspace=0.1)
for ax, t in zip(axs.flat, tags):
    b = beh(t); x = np.arange(len(LV)); pos = inside_pos(t)
    ax.axvspan(4.5, 5.5, color="#fef3c7", zorder=0)
    ax.plot(x, [b["unk_" + l]["commit"] for l in LV], "-o", c=C["act"], ms=3, lw=1.5, label="Action: commits (ANSWER)")
    ax.plot(x, [b["unk_" + l]["decline"] for l in LV], "--o", c=C["dec"], ms=2.2, lw=0.9, mfc="white", label="Action: declines")
    ax.plot(x, [b["unk_" + l]["ask_unk"] for l in LV], "-s", c=C["ask"], ms=2.6, lw=1.1, label="Words: asked directly, P(unknowable)")
    if pos:
        ax.plot(x, [pos.get("unk_" + l, np.nan) for l in LV], "-D", c=C["inside"], ms=2.6, lw=1.5, label="Inside: X-probe position (1 = unknowable, 0 = knowable ref.)")
        ax.scatter([0], [pos["know_L0"]], marker="*", s=55, c=C["know"], zorder=6, label="Positive control: knowable Q, data removed")
    ax.set_xticks(x); ax.set_xticklabels(LVN, fontsize=5.6, rotation=50, ha="right"); ax.set_ylim(-0.12, 1.15); ax.axhline(0, c="#e5e7eb", lw=0.6, zorder=0)
    ax.set_title(NICE[t])
for ax in axs.flat[n:]: ax.axis("off")
h, l = axs.flat[0].get_legend_handles_labels()
fig.legend(h, l, loc="lower center", ncol=3, fontsize=6.4, frameon=False, bbox_to_anchor=(0.5, -0.07))
fig.savefig(f"{OUT}/fig1_channels_v4.png"); plt.close(fig)

# ---------- Fig 2: activation patching (no-panel -> panel), fraction of abstention restored ----------
pt = [t for t in tags if os.path.exists(f"results/deep-{t}/summary.json") and "T3" in json.load(open(f"results/deep-{t}/summary.json"))]
n2 = len(pt); c2 = 5 if n2 > 8 else 4; r2 = int(np.ceil(n2 / c2))
fig, axs = plt.subplots(r2, c2, figsize=(7.4, 1.6 * r2), squeeze=False, sharey=True, sharex=True)
fig.subplots_adjust(hspace=0.45, wspace=0.1)
for ax, t in zip(axs.flat, pt):
    s = json.load(open(f"results/deep-{t}/summary.json")); NL = s["meta"]["n_layers"]; P = s["T3"]["layers"]
    Ls = sorted(int(L) for L in P); d = np.array(Ls) / NL
    for m, c, lab, ls in (("suffix", "#111827", "whole question + instruction span", "-"), ("last", C["act"], "last token only", "-"),
                          ("xdir_last", C["inside"], "X direction only, last token", "--")):
        ax.plot(d, np.clip([P[str(L)][m]["restored"] for L in Ls], -0.2, 1.2), ls, c=c, lw=1.3, marker="o", ms=1.8, label=lab)
    ax.axhline(0, c="#e5e7eb", lw=0.6); ax.axhline(1, c="#e5e7eb", lw=0.6); ax.set_title(NICE[t]); ax.set_ylim(-0.2, 1.2)
for ax in axs.flat[n2:]: ax.axis("off")
for ax in axs[-1]: ax.set_xlabel("relative depth of patched layer", fontsize=6.5)
for ax in axs[:, 0]: ax.set_ylabel("abstention restored", fontsize=6.5)
h, l = axs.flat[0].get_legend_handles_labels()
fig.legend(h, l, loc="lower center", ncol=3, fontsize=6.4, frameon=False, bbox_to_anchor=(0.5, -0.09 if r2 > 1 else -0.16))
fig.savefig(f"{OUT}/fig2_patch.png"); plt.close(fig)
print("figs", tags, pt)
