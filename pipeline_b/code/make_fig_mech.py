"""Figure 3: the knowability component carries none of the panel's effect. Left: Llama phase-2 patches; right: Qwen3 phase-3
component patches. y = P(ANSWER) on unknowable items with the panel shown, after patching the no-panel value in."""
import json, os, sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = sys.argv[1] if len(sys.argv) > 1 else "report/figs"
os.makedirs(OUT, exist_ok=True)
panels = []
p2 = "p2_res/Meta_Llama_3_1_8B_Instruct.json"
p3q = "p3_gpu/Qwen3_8B.json"
p3q14 = "p3_gpu/Qwen3_14B.json"
fig, axs = plt.subplots(1, 3 if os.path.exists(p3q14) else 2, figsize=(11 if os.path.exists(p3q14) else 8, 3.3))

# Llama phase 2
r = json.load(open(p2)); pt = r["patch"]; Ls = r["layers_patched"]
b = np.mean([x["base_answer"] for x in pt if x["mode"] == "full" and x["layer"] == Ls[0]])
s = np.mean([x["src_answer"] for x in pt if x["mode"] == "full" and x["layer"] == Ls[0]])
ax = axs[0]
for m, c, lab in (("full", "#111", "whole no-panel vector"), ("ortho", "#c2410c", "all but knowability direction"), ("uonly", "#15803d", "knowability direction only")):
    ax.plot(Ls, [np.mean([x["p_answer"] for x in pt if x["layer"] == l and x["mode"] == m]) for l in Ls], "-o", ms=3, color=c, label=lab)
ax.axhline(b, ls="--", c="#999", lw=1); ax.axhline(s, ls=":", c="#999", lw=1)
ax.set_title("Llama-3.1-8B (tool call -> answer)", fontsize=9)


def p3panel(ax, path, title):
    r = json.load(open(path)); Ls = r["layers"]
    for d, c, lab in (("c", "#c2410c", "decline direction only"), ("uperp", "#15803d", "decision-orthogonalised knowability only")):
        ax.plot(Ls, [next(x["p_answer"] for x in r["res"] if x["layer"] == l and x["dir"] == d) for l in Ls], "-o", ms=3, color=c, label=lab)
    lo = [min(x["p_answer"] for x in r["res"] if x["layer"] == l and x["dir"].startswith("rand")) for l in Ls]
    hi = [max(x["p_answer"] for x in r["res"] if x["layer"] == l and x["dir"].startswith("rand")) for l in Ls]
    ax.fill_between(Ls, [v - 0.01 for v in lo], [v + 0.01 for v in hi], color="#6b7280", alpha=.45, label="8 random directions")
    ax.axhline(r["base_answer"], ls="--", c="#999", lw=1); ax.axhline(r["src_answer"], ls=":", c="#999", lw=1)
    ax.set_title(title, fontsize=9)


p3panel(axs[1], p3q, "Qwen3-8B (decline -> answer)")
if os.path.exists(p3q14):
    p3panel(axs[2], p3q14, "Qwen3-14B")
for ax in axs:
    ax.set_ylim(-0.03, 1.0); ax.grid(alpha=.3); ax.set_xlabel("layer patched (decision token)", fontsize=8)
    ax.legend(fontsize=6.5, loc="center left")
axs[0].set_ylabel("P(ANSWER), unknowable, panel shown", fontsize=8)
fig.suptitle("Patching the no-panel state into the panel run. Dashed: panel, unpatched. Dotted: no panel.", fontsize=9)
fig.tight_layout(); fig.savefig(os.path.join(OUT, "fig3_mechanism.png"), dpi=170)
print("ok")
