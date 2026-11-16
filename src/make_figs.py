# Figures for the report (new sprint work). usage: python make_figs.py results/tagA results/tagB ...
import json, sys, os, numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
sys.path.insert(0, os.path.dirname(__file__))
from analyze import load

plt.rcParams.update({"font.size": 8.5, "axes.spines.top": False, "axes.spines.right": False,
                     "figure.dpi": 200, "savefig.bbox": "tight", "font.family": "DejaVu Sans"})
C_ACT, C_ASK, C_PROBE, C_KNOW, C_GREY = "#c2410c", "#2563eb", "#15803d", "#7c3aed", "#9ca3af"
NICE = {"qwen3-4b": "Qwen3-4B", "qwen3-8b": "Qwen3-8B", "llama31-8b": "Llama-3.1-8B-Inst", "gemma2-9b": "Gemma-2-9B-it",
        "qwen25-3b": "Qwen2.5-3B-Inst (base)", "gate-3b": "Qwen2.5-3B + SFT gate"}
LV = ["L0", "L1", "L2", "L2irr", "L2fab"]
LVN = ["L0\nnone", "L1\nthin", "L2\npanel", "L2'\nirrelevant", "L2-fab\nfabricated"]
OUT = "report/figs"; os.makedirs(OUT, exist_ok=True)
dirs = sys.argv[1:]
S = {d: json.load(open(os.path.join(d, "summary.json"))) for d in dirs}

def probe_pos(summary):
    lv = summary["levels"]; a = lv["L0"]["probe"]; k = lv["know_L2"]["probe"]
    return lambda s: (s - k) / (a - k)

# ---------------- Figure 1: three channels across evidence levels ----------------
n = len(dirs); cols = min(3, n); rows_ = int(np.ceil(n / cols))
fig, axs = plt.subplots(rows_, cols, figsize=(2.55 * cols, 2.25 * rows_), squeeze=False, sharey=True)
for ax, d in zip(axs.flat, dirs):
    s = S[d]; lv = s["levels"]; pos = probe_pos(s); x = np.arange(len(LV))
    ax.plot(x, [lv[l]["commit"] for l in LV], "-o", c=C_ACT, ms=3.5, lw=1.6, label="Action: commits (ANSWER)")
    ax.plot(x, [lv[l]["ask_unk"] for l in LV], "-s", c=C_ASK, ms=3, lw=1.2, label="Words: asked, says unknowable")
    ax.plot(x, [pos(lv[l]["probe"]) for l in LV], "-D", c=C_PROBE, ms=3, lw=1.6, label="Inside: probe position (1=unk L0, 0=know L2)")
    # positive control: same knowable question, data removed (L0) vs shown (L2)
    ax.scatter([0], [pos(lv["know_L0"]["probe"])], marker="*", s=55, c=C_KNOW, zorder=5, label="Positive control: knowable Q, no data")
    ax.scatter([2], [pos(lv["know_L2"]["probe"])], marker="*", s=30, c=C_GREY, zorder=5, label="Knowable Q with panel (=0)")
    ax.set_xticks(x); ax.set_xticklabels(LVN, fontsize=6.5); ax.set_ylim(-0.25, 1.3); ax.axhline(0, c="#e5e7eb", lw=0.6, zorder=0)
    ax.set_title(f"{NICE.get(s['tag'], s['tag'])}  (layer {s['layer']}/{s['n_layers']})", fontsize=8)
for ax in axs.flat[n:]: ax.axis("off")
h, l = axs.flat[0].get_legend_handles_labels()
fig.legend(h, l, loc="lower center", ncol=3, fontsize=6.8, frameon=False, bbox_to_anchor=(0.5, -0.06 if rows_ > 1 else -0.14))
fig.suptitle("Figure 1. Unknowable NSE questions (n=40/level): commitment vs. what the model says and represents", fontsize=8.5, y=1.01)
fig.savefig(f"{OUT}/fig1_channels.png"); plt.close(fig)

# ---------------- Figure 2: normalised probe shifts with case-bootstrap CIs ----------------
keys = [("unk_L0_minus_L2", "Unknowable: L0 → L2 panel"), ("unk_L0_minus_L2fab", "Unknowable: L0 → fabricated panel"),
        ("unk_L0_minus_L2irr", "Unknowable: L0 → irrelevant panel"),
        ("know_L0_minus_L2 (positive control)", "Positive control: knowable Q,\nno data → panel")]
fig, ax = plt.subplots(figsize=(6.6, 0.42 * len(dirs) * len(keys) / 2 + 1.2))
yy = 0; yt, yl = [], []
cols4 = [C_ACT, "#ea580c", C_GREY, C_KNOW]
for d in dirs:
    s = S[d]
    for j, (k, lab) in enumerate(keys):
        v = s["shift"][k]
        if v.get("point") is None: continue
        ax.errorbar(v["point"], yy, xerr=[[v["point"] - v["ci"][0]], [v["ci"][1] - v["point"]]], fmt="o", c=cols4[j], ms=3.5, capsize=2, lw=1)
        yy -= 1
    yt.append(yy + len(keys) / 2 + 0.5); yl.append(NICE.get(s["tag"], s["tag"])); yy -= 0.8
ax.axvline(0, c="k", lw=0.6); ax.set_yticks(yt); ax.set_yticklabels(yl, fontsize=7.5)
for j, (k, lab) in enumerate(keys): ax.plot([], [], "o", c=cols4[j], label=lab.replace("\n", " "))
ax.legend(fontsize=6.8, frameon=False, loc="lower right")
ax.set_xlabel("Probe shift toward 'knowable', in units of the training-set class gap (95% case-bootstrap CI)")
ax.set_title("Figure 2. Panels barely move the internal unknowability signal; removing data from a knowable question does", fontsize=8.5)
fig.savefig(f"{OUT}/fig2_shifts.png"); plt.close(fig)

# ---------------- Figure 3: steering dose-response ----------------
have = [d for d in dirs if "steer" in S[d]]
if have:
    fig, axs = plt.subplots(1, len(have), figsize=(2.4 * len(have), 2.3), squeeze=False)
    for ax, d in zip(axs.flat, have):
        st = S[d]["steer"]
        for lvl, c, lab in (("L2", C_ACT, "unknowable + panel"), ("L2fab", "#ea580c", "unknowable + fabricated"),
                            ("L0", "#fdba74", "unknowable, no data"), ("L2_know", C_KNOW, "knowable + panel")):
            al = sorted({float(k.split("|")[1]) for k in st if k.startswith("probe|") and k.endswith("|" + lvl)})
            if not al: continue
            ax.plot(al, [st[f"probe|{a:g}|{lvl}"]["pact_lo"] if f"probe|{a:g}|{lvl}" in st else np.nan for a in al], "-o", c=c, ms=2.5, lw=1.3, label=lab)
            ra = sorted({float(k.split("|")[1]) for k in st if k.startswith("random|") and k.endswith("|" + lvl)})
            ax.plot(ra, [st[f"random|{a:g}|{lvl}"]["pact_lo"] for a in ra], ":x", c=c, ms=3, lw=0.9, alpha=0.7)
        ax.axhline(0, c="#e5e7eb", lw=0.6); ax.set_xlabel("steering α (× class gap)  — dotted: random dirs")
        ax.set_title(NICE.get(S[d]["tag"], S[d]["tag"]), fontsize=8)
    axs.flat[0].set_ylabel("log-odds ANSWER vs (TOOL|DECLINE)")
    h, l = axs.flat[0].get_legend_handles_labels()
    fig.legend(h, l, loc="lower center", ncol=4, fontsize=6.8, frameon=False, bbox_to_anchor=(0.5, -0.12))
    fig.suptitle("Figure 3. Adding the unknowability direction at the probe layer: decision propensity", fontsize=8.5, y=1.02)
    fig.savefig(f"{OUT}/fig3_steer.png"); plt.close(fig)

# ---------------- Figure 4: monitor AUROC ----------------
fig, ax = plt.subplots(figsize=(6.4, 2.1))
meth = [("probe", "Probe (inside)", C_PROBE), ("ask_model", "Ask the model", C_ASK), ("stated_conf", "Stated confidence", C_ACT),
        ("belief_conf", "Separate belief prompt", "#f59e0b"), ("lens", "Logit-lens doubt words", C_GREY)]
w = 0.16; x = np.arange(len(dirs))
for j, (k, lab, c) in enumerate(meth):
    ax.bar(x + (j - 2) * w, [S[d]["monitor"].get(k, np.nan) for d in dirs], w, color=c, label=lab)
ax.axhline(0.5, c="k", lw=0.6, ls="--"); ax.set_ylim(0, 1.05); ax.set_xticks(x)
ax.set_xticklabels([f"{NICE.get(S[d]['tag'], S[d]['tag'])}\n(n={S[d]['monitor']['n']}, bad={S[d]['monitor']['n_bad']})" for d in dirs], fontsize=6.5)
ax.set_ylabel("AUROC"); ax.legend(fontsize=6.5, ncol=5, frameon=False, loc="upper center", bbox_to_anchor=(0.5, 1.2))
ax.set_title("Figure 4. Monitor: among items the agent ANSWERS, flag the unknowable ones", fontsize=8.5, y=1.18)
fig.savefig(f"{OUT}/fig4_monitor.png"); plt.close(fig)

# ---------------- Figure 5 (appendix): probe AUROC by layer ----------------
fig, axs = plt.subplots(1, len(dirs), figsize=(2.1 * len(dirs), 1.9), squeeze=False, sharey=True)
for ax, d in zip(axs.flat, dirs):
    meta, rows = load(d); pl = meta["probe"]["per_layer"]; L = [p["layer"] for p in pl]
    ax.plot(L, [p["val"] for p in pl], c=C_GREY, lw=1.2, label="synthetic val")
    ax.plot(L, [p["nse_L2"] for p in pl], c=C_ACT, lw=1.2, label="NSE L2 (matched)")
    ax.plot(L, [p["xfer_L2"] for p in pl], c=C_ASK, lw=1.2, label="transfer L2")
    ax.axvline(meta["probe"]["layer"], c=C_PROBE, ls="--", lw=0.8); ax.set_title(NICE.get(meta["tag"], meta["tag"]), fontsize=7.5)
    ax.set_xlabel("layer"); ax.set_ylim(0.3, 1.02)
axs.flat[0].set_ylabel("AUROC"); axs.flat[0].legend(fontsize=6, frameon=False)
fig.savefig(f"{OUT}/fig5_layers.png"); plt.close(fig)
print("figs ->", OUT)
