"""Figure: Jacobian-lens calibration. For each model, where the panel (real/fabricated) and the leaked answer put the
doubt words ('unpredictable', 'uncertain', 'unknown', 'unclear') in the decoded change of the decision state, as % of the
way down the vocabulary. A readout that is not evidence-blind must push them down for the leaked answer.
usage: python src/make_fig_jlens.py   (reads results/pipeline_b_summary.json)"""
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

S = json.load(open("results/pipeline_b_summary.json"))
J = S["jlens"]
order = ["Qwen3-14B", "Qwen2.5-14B", "Phi-4", "Llama-3.1-8B", "Qwen3-8B", "Qwen2.5-7B", "OLMo-2-7B", "Qwen3-4B", "Qwen2.5-3B",
         "Gemma-2-9B", "Mistral-7B-v0.3"]
size = {"Qwen3-14B": "14B", "Qwen2.5-14B": "14B", "Phi-4": "14B", "Llama-3.1-8B": "8B", "Qwen3-8B": "8B", "Qwen2.5-7B": "7B",
        "OLMo-2-7B": "7B", "Qwen3-4B": "4B", "Qwen2.5-3B": "3B", "Gemma-2-9B": "9B", "Mistral-7B-v0.3": "7B"}
fig, axs = plt.subplots(1, 2, figsize=(10, 3.9), gridspec_kw=dict(width_ratios=[1.45, 1]))
ax = axs[0]
for i, m in enumerate(order):
    d = J[m]["doubt"]; y = len(order) - 1 - i
    bad = d["leak"] < 70
    ax.plot([d["panel"], d["leak"]], [y, y], color="#d1d5db", lw=2, zorder=1)
    ax.scatter(d["leak"], y, color="#9ca3af" if bad else "#2563eb", s=36, zorder=3, label="leaked answer" if i == 0 else None)
    ax.scatter(d["panel"], y, color="#9ca3af" if bad else "#c2410c", s=36, zorder=3, marker="D", label="panel (real + fabricated)" if i == 0 else None)
ax.set_yticks(range(len(order)))
ax.set_yticklabels([f"{m} ({size[m]})" + ("  [leak fails]" if J[m]["doubt"]["leak"] < 70 else "") for m in order][::-1], fontsize=7.5)
ax.axvline(50, color="#999", lw=.8, ls=":")
ax.set_xlim(-2, 102); ax.set_xlabel("doubt words, % of the way down the vocabulary\n(0 = promoted, 100 = demoted to the bottom)", fontsize=8)
ax.set_title("Stocks: what the change to the decision state says", fontsize=9); ax.legend(fontsize=7.5, loc="upper center", bbox_to_anchor=(0.5, -0.24), ncol=2, frameon=False)
ax.grid(axis="x", alpha=.3)
ax = axs[1]
lab = []
for i, (dom, mods) in enumerate(S["domains"].items()):
    for j, (m, v) in enumerate(mods.items()):
        y = 5 - (3 * i + j); d = v["jlens"]["doubt"]
        ax.plot([d["panel"], d["leak"]], [y, y], color="#d1d5db", lw=2, zorder=1)
        ax.scatter(d["leak"], y, color="#2563eb", s=36, zorder=3); ax.scatter(d["panel"], y, color="#c2410c", s=36, marker="D", zorder=3)
        lab.append((y, f"{dom}: {m}"))
ax.set_yticks([y for y, _ in lab]); ax.set_yticklabels([l for _, l in lab], fontsize=7.5)
ax.axvline(50, color="#999", lw=.8, ls=":"); ax.set_xlim(-2, 102); ax.grid(axis="x", alpha=.3)
ax.set_xlabel("doubt words, % down the vocabulary", fontsize=8); ax.set_title("New domains (crypto, weather)", fontsize=9)
fig.tight_layout(); fig.savefig("report/figs/fig5_jlens.png", dpi=170); print("saved report/figs/fig5_jlens.png")
