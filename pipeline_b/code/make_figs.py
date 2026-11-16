"""Figures from analyze.py summary.json + raw per-model json. usage: python make_figs.py <dir>"""
import json, sys, os, glob
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

D = sys.argv[1]
FIG = os.path.join(D, "figs"); os.makedirs(FIG, exist_ok=True)
S = json.load(open(os.path.join(D, "summary.json")))
LV = ["L0", "L1", "L2", "L2fab", "L2irr"]
LVN = ["none", "thin", "real", "fabricated", "irrelevant"]
C_ACT, C_ASK, C_IN, C_TOOL = "#c2410c", "#1d4ed8", "#15803d", "#a16207"
short = lambda m: m.split("/")[-1].replace("-Instruct", "").replace("Meta-", "").replace("-it", "").replace("-1124", "")


def row(s, arm, lvl):
    for t in s["table"]:
        if t["arm"] == arm and t["level"] == lvl:
            return t


# ---- Fig 1: three channels per model on the unknowable arm (answerable arm dotted)
ORDER = ["Qwen3-14B", "Meta-Llama-3.1-8B-Instruct", "Qwen3-8B", "OLMo-2-1124-7B-Instruct", "Qwen2.5-14B-Instruct", "phi-4"]
S_all = S
S = [s for o in ORDER for s in S_all if s["model"].split("/")[-1] == o] or S_all
n = len(S); cols = min(3, n); rows_ = int(np.ceil(n / cols))
fig, axs = plt.subplots(rows_, cols, figsize=(4.3 * cols, 3.3 * rows_), squeeze=False)
for k, s in enumerate(S):
    ax = axs[k // cols][k % cols]
    lv = [l for l in LV if row(s, "unk", l)]
    x = np.arange(len(lv))
    ax.plot(x, [row(s, "unk", l)["fc_answer"] for l in lv], "-o", color=C_ACT, label="action: P(ANSWER)")
    ax.plot(x, [row(s, "unk", l)["gen_answer"] for l in lv], ":", color=C_ACT, lw=1, label="action: greedy ANSWER rate")
    ax.plot(x, [1 - row(s, "unk", l)["fc_decline"] for l in lv], "--", color=C_TOOL, lw=1, alpha=.8, label="action: 1 - P(DECLINE) (answer or tool)")
    ax.plot(x, [row(s, "unk", l)["ask_p3"] for l in lv], "-s", color=C_ASK, label="asked: P(IRREDUCIBLE)")
    use_perp = s.get("zperp") and s["zperp"].get("unk_L0") == s["zperp"].get("unk_L0")
    src = (lambda k: s["zperp"].get(k, np.nan)) if use_perp else (lambda k: s["z"].get(k, [np.nan])[0])
    zu = [src("unk_" + l) for l in lv]
    za = [src("ans_" + l) for l in lv]
    tag = "decision-orthogonalised axis" if use_perp else "knowability axis"
    ax.plot(x, zu, "-^", color=C_IN, label=f"inside: {tag} (unknowable)")
    ax.plot(x, za, "--^", color=C_IN, alpha=.45, ms=3, label=f"inside: {tag} (answerable twin)")
    ax.axhspan(-0.02, 0.02, color=C_IN, alpha=.15); ax.axhspan(0.98, 1.02, color=C_IN, alpha=.15)
    ax.set_xticks(x); ax.set_xticklabels([LVN[LV.index(l)] for l in lv], fontsize=8)
    lo = min(-0.1, np.nanmin(za + zu) - 0.05); hi = max(1.1, np.nanmax(za + zu) + 0.05)
    ax.set_ylim(lo, hi); ax.set_title(short(s["model"]) + ("" if use_perp else " (raw axis; fails leak control)" if "OLMo" in s["model"] else ""), fontsize=9)
    ax.grid(alpha=.3)
for k in range(n, rows_ * cols):
    axs[k // cols][k % cols].axis("off")
axs[0][0].legend(fontsize=6.5, loc="lower left")
fig.suptitle("Unknowable question by evidence shown (inside axis: 0 = synthetic answerable mean, 1 = synthetic unknowable mean)", fontsize=9)
fig.tight_layout(); fig.savefig(os.path.join(FIG, "fig1_channels.png"), dpi=170); plt.close(fig)

# ---- Fig 2: steering
have = [s for s in S if s.get("steer")][:4]
if have:
    fig, axs = plt.subplots(1, len(have), figsize=(3.3 * len(have), 3.0), squeeze=False)
    for k, s in enumerate(have):
        ax = axs[0][k]
        for arm, lvl, c, lab in (("unk", "L2", C_ACT, "unknowable, real panel"), ("ans", "L2", C_ASK, "answerable, real panel"), ("unk", "L0", "#555", "unknowable, no panel")):
            pts = sorted([(t["alpha"], t["d_decline"]) for t in s["steer"] if t["cond"] == "dir" and t["arm"] == arm and t["level"] == lvl])
            pts = [(0.0, 0.0)] + pts; pts.sort()
            ax.plot([p[0] for p in pts], [100 * p[1] for p in pts], "-o", color=c, ms=3, label=lab)
            for a in (-2.0, 2.0):
                rs = [100 * t["d_decline"] for t in s["steer"] if t["cond"].startswith("rand") and t["alpha"] == a and t["arm"] == arm and t["level"] == lvl]
                if rs:
                    ax.plot([a + (0.08 if arm == "ans" else 0)] * len(rs), rs, "x", color=c, alpha=.5, ms=4)
        ax.axhline(0, color="k", lw=.5); ax.set_title(short(s["model"]), fontsize=9)
        ax.set_xlabel("steering strength (x class separation)", fontsize=8)
        if k == 0: ax.set_ylabel("change in P(DECLINE), pp", fontsize=8); ax.legend(fontsize=6)
        ax.grid(alpha=.3)
    fig.suptitle("Adding the knowability direction vs 8 random directions (x)", fontsize=10)
    fig.tight_layout(); fig.savefig(os.path.join(FIG, "fig2_steer.png"), dpi=170); plt.close(fig)

# ---- Fig 3: lift vs gap change scatter
fig, ax = plt.subplots(figsize=(5, 3.8))
for s in S:
    lift = s["lift_fc"][0] * 100
    g = s["gapchange_projn_L0L2"]
    ax.errorbar(lift, g[0], yerr=[[g[0] - g[1]], [g[2] - g[0]]], fmt="o", color=C_IN)
    ax.annotate(short(s["model"]), (lift, g[0]), fontsize=7, xytext=(3, 3), textcoords="offset points")
ax.axhline(0, color="k", lw=.5)
ax.set_xlabel("commitment lift, none -> real panel (pp, P(ANSWER))")
ax.set_ylabel("change in inside unk-ans gap (rel. units)")
ax.set_title("FOOLED would sit low-right; OVERRIDING sits on the zero line", fontsize=9)
ax.grid(alpha=.3); fig.tight_layout(); fig.savefig(os.path.join(FIG, "fig3_lift_vs_gap.png"), dpi=170); plt.close(fig)
print("figs ->", FIG)
