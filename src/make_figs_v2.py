# v2 figures (new sprint work). usage: python make_figs_v2.py results/v2-*
import json, sys, os, numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"font.size": 8, "axes.spines.top": False, "axes.spines.right": False, "figure.dpi": 220,
                     "savefig.bbox": "tight", "font.family": "DejaVu Sans", "axes.titlesize": 8})
ORDER = [t for t in ["qwen3-14b", "llama31-8b", "qwen3-8b", "qwen3-4b", "qwen25-7b", "qwen25-3b", "mistral-7b", "llama32-3b", "gemma2-9b", "gate-3b"] if __import__("os").path.exists(f"results/v2-{t}/v2summary.json")]
NICE = {"qwen3-14b": "Qwen3-14B", "llama31-8b": "Llama-3.1-8B-Instruct", "qwen3-8b": "Qwen3-8B", "qwen3-4b": "Qwen3-4B", "qwen25-3b": "Qwen2.5-3B-Instruct",
        "gemma2-9b": "Gemma-2-9B-it", "gate-3b": "Qwen2.5-3B + SFT gate",
        "qwen25-7b": "Qwen2.5-7B-Instruct", "mistral-7b": "Mistral-7B-Instruct-v0.3", "llama32-3b": "Llama-3.2-3B-Instruct"}
C = dict(act="#c2410c", dec="#9a3412", ask="#2563eb", inside="#15803d", know="#7c3aed", grey="#9ca3af", tool="#f59e0b")
OUT = "report/figs"; os.makedirs(OUT, exist_ok=True)
dirs = {}
for d in sys.argv[1:]:
    t = os.path.basename(d.rstrip("/")).replace("v2-", "")
    dirs[t] = d
tags = [t for t in ORDER if t in dirs]
V = {t: json.load(open(os.path.join(dirs[t], "v2summary.json"))) for t in tags}
SC = {t: json.load(open(os.path.join(dirs[t], "layerscan.json"))) for t in tags if os.path.exists(os.path.join(dirs[t], "layerscan.json"))}
LV = ["L0", "L1", "L2", "L2irr", "L2fab"]; LVN = ["none", "thin", "panel", "irrel.", "fabric."]

def inside_pos(t, probe="X_dm"):
    """mean over valid deep layers of probe position: 1 = unknowable@L0, 0 = knowable@L2."""
    NL = V[t]["NL"]; acc = {k: [] for k in ["unk_" + l for l in LV] + ["know_L0", "know_L1", "know_L2"]}
    for L, o in SC[t]["layers"].items():
        v = o[probe]
        if not v["valid"] or int(L) / NL < 0.5: continue
        lv = v["levels"]; a, k = lv["unk_L0"], lv["know_L2"]
        for key in acc: acc[key].append((lv[key] - k) / (a - k))
    return {k: (float(np.mean(v)) if v else np.nan) for k, v in acc.items()}

# ---------- Figure 1: three channels ----------
n = len(tags); cols = 3 if n <= 6 else 4; rows_ = int(np.ceil(n / cols))
fig, axs = plt.subplots(rows_, cols, figsize=(7.2, 2.25 * rows_), squeeze=False, sharey=True)
fig.subplots_adjust(hspace=0.45, wspace=0.12)
for ax, t in zip(axs.flat, tags):
    b = V[t]["behaviour"]; x = np.arange(len(LV)); pos = inside_pos(t) if t in SC else None
    ax.plot(x, [b["unk_" + l]["commit"] for l in LV], "-o", c=C["act"], ms=3.5, lw=1.7, label="Action: commits (ANSWER)")
    ax.plot(x, [b["unk_" + l]["decline"] for l in LV], "--o", c=C["dec"], ms=2.5, lw=1.0, mfc="white", label="Action: declines")
    ax.plot(x, [b["unk_" + l]["ask_unk"] for l in LV], "-s", c=C["ask"], ms=3, lw=1.2, label="Words: asked directly, P(unknowable)")
    if pos:
        ax.plot(x, [pos["unk_" + l] for l in LV], "-D", c=C["inside"], ms=3, lw=1.7, label="Inside: probe position (1 = unknowable, 0 = knowable ref.)")
        ax.scatter([0], [pos["know_L0"]], marker="*", s=70, c=C["know"], zorder=6, label="Positive control: knowable Q, data removed")
    ax.set_xticks(x); ax.set_xticklabels(LVN, fontsize=6.3, rotation=40, ha="right"); ax.set_ylim(-0.12, 1.15); ax.axhline(0, c="#e5e7eb", lw=0.6, zorder=0)
    ax.set_title(NICE[t])
for ax in axs.flat[n:]: ax.axis("off")
h, l = axs.flat[0].get_legend_handles_labels()
fig.legend(h, l, loc="lower center", ncol=2, fontsize=6.8, frameon=False, bbox_to_anchor=(0.5, -0.1))
fig.savefig(f"{OUT}/fig1_channels.png"); plt.close(fig)

# ---------- Figure 2: fooling index by depth ----------
_n2 = len([t for t in tags if t in SC]); _c2 = 3 if _n2 <= 6 else 4; _r2 = int(np.ceil(_n2 / _c2))
fig, axs = plt.subplots(_r2, _c2, figsize=(7.0, 1.8 * _r2), squeeze=False, sharey=True, sharex=True)
fig.subplots_adjust(hspace=0.35, wspace=0.1)
for ax, t in zip(axs.flat, [t for t in tags if t in SC]):
    NL = V[t]["NL"]
    ax.axhspan(-0.5, 0.25, color="#dcfce7", zorder=0); ax.axhspan(0.5, 1.6, color="#fee2e2", zorder=0)
    for probe, c, lab in (("X_dm", C["inside"], "cross-domain probe"), ("N_dm_crossfit", C["know"], "cross-fitted NSE probe")):
        Ls = sorted(int(L) for L in SC[t]["layers"]); fi = []; lo = []; hi = []; ok = []
        for L in Ls:
            v = SC[t]["layers"][str(L)][probe]; fi.append(v["FI_L2"]["point"]); lo.append(v["FI_L2"]["ci"][0]); hi.append(v["FI_L2"]["ci"][1]); ok.append(v["valid"])
        d = np.array(Ls) / NL; fi = np.clip(fi, -0.5, 1.6); ok = np.array(ok)
        ax.plot(d, fi, c=c, lw=0.6, alpha=0.4)
        ax.scatter(d[ok], fi[ok], s=7, c=c, label=lab, zorder=3); ax.scatter(d[~ok], fi[~ok], s=7, facecolors="none", edgecolors=c, lw=0.5, alpha=0.6, zorder=3)
    ax.set_ylim(-0.5, 1.6); ax.set_xlim(0, 1.02); ax.axvline(0.5, c="#6b7280", lw=0.5, ls=":")
    ax.set_title(NICE[t], fontsize=7.5); ax.set_xticks([0, 0.5, 1.0]); ax.set_xticklabels(["0", "0.5", "1"])
for ax in axs.flat[_n2:]: ax.axis("off")
for ax in axs[-1]: ax.set_xlabel("relative depth", fontsize=7)
for ax in axs[:, 0]: ax.set_ylabel("fooling index", fontsize=7.5)
axs.flat[0].text(0.55, 1.42, "fooled (>0.5)", fontsize=5.5, color="#991b1b")
h, l = axs.flat[0].get_legend_handles_labels()
fig.legend(h + [plt.Line2D([], [], marker="o", ls="", mfc="none", mec="#6b7280")], l + ["hollow = fails validity gate"], loc="lower center", ncol=3, fontsize=6.8, frameon=False, bbox_to_anchor=(0.5, -0.1))
fig.savefig(f"{OUT}/fig2_depth.png"); plt.close(fig)

# ---------- Figure 3: steering along the cross-domain unknowability direction ----------
st = [t for t in tags if V[t].get("xsteer")]
if st:
    fig, axs = plt.subplots(2, len(st), figsize=(7.2, 3.4), squeeze=False, sharex=True)
    fig.subplots_adjust(wspace=0.45, hspace=0.15)
    for j, t in enumerate(st):
        xs = V[t]["xsteer"]
        for cond, c, lab in (("unk_L2", C["act"], "unknowable + panel"), ("unk_L2fab", "#fb923c", "unknowable + fabricated"),
                             ("unk_L0", C["grey"], "unknowable, no data"), ("know_L2", C["know"], "knowable + panel")):
            al = sorted({float(k.split("|")[1]) for k in xs if k.startswith("xdir|") and k.endswith("|" + cond)})
            axs[0, j].plot(al, [xs[f"xdir|{a:g}|{cond}"]["pact_lo"] for a in al], "-o", c=c, ms=2.2, lw=1.2, label=lab)
            ra = sorted({float(k.split("|")[1]) for k in xs if k.startswith("random|") and k.endswith("|" + cond)})
            axs[0, j].scatter(ra, [xs[f"random|{a:g}|{cond}"]["pact_lo"] for a in ra], marker="x", c=c, s=12, lw=0.8)
            ga = [a for a in al if "commit" in xs[f"xdir|{a:g}|{cond}"]]
            if cond in ("unk_L2", "know_L2", "unk_L2fab"):
                off = {"know_L2": 0.02, "unk_L2": 0.0, "unk_L2fab": -0.02}[cond]
                axs[1, j].plot(ga, [xs[f"xdir|{a:g}|{cond}"]["commit"] + off for a in ga], "-o" if cond != "know_L2" else "--o", c=c, ms=2.2, lw=1.2)
                if f"random|16|{cond}" in xs and "commit" in xs[f"random|16|{cond}"]:
                    axs[1, j].scatter([16], [xs[f"random|16|{cond}"]["commit"]], marker="x", c=c, s=14)
        axs[0, j].axhline(0, c="#e5e7eb", lw=0.6); axs[0, j].set_title(NICE[t].replace("-Instruct", "").replace(" + SFT gate", "+gate"), fontsize=7)
        axs[1, j].set_ylim(-0.06, 1.06); axs[1, j].set_xticks([-8, 0, 8, 16]); axs[1, j].tick_params(labelsize=6.5); axs[0, j].tick_params(labelsize=6.5)
    fig.text(0.5, 0.0, "steering strength α (multiples of the cross-domain class-mean gap), added at layer n_layers/2;  × = random direction, same norm", ha="center", fontsize=6.8)
    axs[0, 0].set_ylabel("log-odds ANSWER\nvs TOOL/DECLINE"); axs[1, 0].set_ylabel("commit rate\n(greedy generation)")
    h, l = axs[0, 0].get_legend_handles_labels()
    fig.legend(h, l, loc="lower center", ncol=4, fontsize=6.6, frameon=False, bbox_to_anchor=(0.5, -0.09))
    fig.savefig(f"{OUT}/fig3_steer.png"); plt.close(fig)

# ---------- Figure 4: one round of pushback ----------
pu = [t for t in tags if V[t].get("push")]
if pu:
    fig, ax = plt.subplots(figsize=(7.0, 1.9))
    w = 0.2; x = np.arange(len(pu))
    for j, (cond, c, lab) in enumerate((("unk_L2", C["act"], "unknowable+panel: committed before"), ("unk_L2", "#fdba74", "…after 'Are you sure?'"),
                                        ("know_L2", C["know"], "knowable+panel: committed before"), ("know_L2", "#c4b5fd", "…after"))):
        key = "commit_before" if j % 2 == 0 else "commit_after"
        ax.bar(x + (j - 1.5) * w, [V[t]["push"].get(cond, {}).get(key, np.nan) for t in pu], w, color=c, label=lab)
    ax.set_xticks(x); ax.set_xticklabels([NICE[t].replace("-Instruct", "").replace("-it", "").replace(" + ", "\n+ ") for t in pu], fontsize=6.8); ax.set_ylabel("commit rate"); ax.set_ylim(0, 1.05)
    ax.legend(fontsize=6.3, ncol=4, frameon=False, loc="upper center", bbox_to_anchor=(0.5, 1.22))
    fig.savefig(f"{OUT}/fig4_push.png"); plt.close(fig)
print("v2 figs ->", OUT, tags)
