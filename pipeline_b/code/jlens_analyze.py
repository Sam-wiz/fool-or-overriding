"""Analyse fo_jlens.py output: J-lens vs logit-lens 'unknowable minus commit' readout at the decision token.

U(item, layer) = mean J-lens score over the 'unknowable' concept words minus mean over the 'commit' words, at DEC.
Fooling index on this readout, per layer: FI = (U_unkL0 - U_unkL2) / (U_unkL0 - U_ansL2)  (0 = panel leaves the
'unknowable' readout untouched; 1 = moves it to where the knowable twin with the same panel sits).
Positive control: leak (unknowable question + realised future close) should move U toward the knowable side.
Usage: python jlens_analyze.py <jl_dir> [main_res_dir]
"""
import json, os, sys, glob, re
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

D = sys.argv[1]; MAIN = sys.argv[2] if len(sys.argv) > 2 else "main_res"
rng = np.random.default_rng(0)
out_lines = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s); out_lines.append(s)

files = sorted(f for f in glob.glob(os.path.join(D, "*.json")) if not os.path.basename(f).startswith("jlens_summary"))
ORDER = ["Meta_Llama", "Qwen3_14B", "Qwen3_8B", "Qwen2_5_0_5B"]
files.sort(key=lambda f: next((i for i, o in enumerate(ORDER) if o in os.path.basename(f)), 9))
fig, axs = plt.subplots(2, max(len(files), 1), figsize=(3.7 * max(len(files), 1), 5.4), squeeze=False)
summary = {}
alpha = re.compile(r"^\s?[A-Za-z]{3,}$")
for ci, f in enumerate(files):
    r = json.load(open(f)); z = np.load(f.replace(".json", "_scores.npz"))
    tag = os.path.basename(f)[:-5]; nL = r["n_layers"]
    g = np.array(r["groups"]); ids = r["ids"]
    meta = [(i.split("|")[0], i.split("|")[1], i.split("|")[2]) for i in ids]
    cases = sorted(set(t[0] for t in meta))
    P(f"\n=== {r['model']}  (layers {nL}; corpus {r['ncorp']}x{r['seq']} {r['corpus']}; multi-token concepts: "
      f"{[w for w, mt in zip(r['concepts'], r['multitoken']) if mt]})")
    res = {}
    for lens in ("js_dec", "ll_dec"):
        S = z[lens]  # [N, nL+1, K]
        # standardise each concept's score per layer over all NSE items, so concepts with large norms do not dominate
        mu = S.mean(0, keepdims=True); sd = S.std(0, keepdims=True) + 1e-8
        Sz = (S - mu) / sd
        U = Sz[:, :, g == "unknowable"].mean(-1) - Sz[:, :, g == "commit"].mean(-1)  # [N, nL+1]
        if os.environ.get("UNK_ONLY") == "1":
            U = Sz[:, :, g == "unknowable"].mean(-1)
        def idx(arm, lvl):
            return {t[0]: i for i, t in enumerate(meta) if t[1] == arm and t[2] == lvl}
        cond = {k: idx(*v) for k, v in {"unkL0": ("unk", "L0"), "unkL1": ("unk", "L1"), "unkL2": ("unk", "L2"),
                                         "unkL2fab": ("unk", "L2fab"), "unkL2irr": ("unk", "L2irr"),
                                         "leak": ("unk", "L2leak"), "ansL2": ("ans", "L2")}.items()}
        means = {k: U[list(v.values())].mean(0) for k, v in cond.items()}
        common = [c for c in cases if all(c in cond[k] for k in ("unkL0", "unkL2", "ansL2", "leak"))]
        def fi_layer(cs, l, lvl="unkL2"):
            a = np.mean([U[cond["unkL0"][c], l] for c in cs]); b = np.mean([U[cond[lvl][c], l] for c in cs])
            k = np.mean([U[cond["ansL2"][c], l] for c in cs])
            return (a - b) / (a - k) if abs(a - k) > 1e-9 else np.nan
        deep = list(range(nL // 2, nL))  # final layer excluded: its J-lens vector is zero (HF last hidden state is post-norm)
        fis = np.array([fi_layer(common, l) for l in range(nL + 1)])
        fisf = np.array([fi_layer([c for c in common if c in cond["unkL2fab"]], l, "unkL2fab") for l in range(nL + 1)])
        # validity per layer: knowable twin separated (U_unkL2 > U_ansL2 for AUROC-ish) and leak moves toward knowable
        sep = np.array([np.mean([U[cond["unkL2"][c], l] > U[cond["ansL2"][c], l] for c in common]) for l in range(nL + 1)])
        leak = np.array([np.mean([U[cond["unkL2"][c], l] - U[cond["leak"][c], l] for c in common]) for l in range(nL + 1)])
        valid = [l for l in deep if sep[l] >= 0.8 and leak[l] > 0]
        if os.environ.get("NO_GATE", "1") == "1":  # headline: all deep layers (the gate can exclude fooled layers by construction)
            valid = deep
        med = float(np.nanmedian(fis[valid])) if valid else np.nan
        medf = float(np.nanmedian(fisf[valid])) if valid else np.nan
        boots = []
        for _ in range(1000):
            cs = list(rng.choice(common, len(common)))
            v = [fi_layer(cs, l) for l in valid]
            boots.append(np.nanmedian(v) if v else np.nan)
        lo, hi = (np.nanpercentile(boots, 2.5), np.nanpercentile(boots, 97.5)) if valid else (np.nan, np.nan)
        # leak control in units of the L0->ansL2 gap
        leakfi = float(np.nanmedian([fi_layer(common, l, "leak") for l in valid])) if valid else np.nan
        name = "J-lens" if lens == "js_dec" else "logit lens"
        P(f"  {name:10s}: valid deep layers {len(valid)}/{len(deep)}; median FI(real panel) {med:+.2f} [{lo:+.2f},{hi:+.2f}]; "
          f"FI(fabricated) {medf:+.2f}; leak control FI {leakfi:+.2f}")
        res[lens] = dict(valid=valid, fi=fis.tolist(), fi_med=med, ci=[lo, hi], fi_fab=medf, leak_fi=leakfi,
                         means={k: v.tolist() for k, v in means.items()})
        row = 0 if lens == "js_dec" else 1
        ax = axs[row, ci]; x = np.arange(nL + 1) / nL
        for k, c, lab in (("unkL0", "#6b7280", "unknowable, no data"), ("unkL2", "#c2410c", "unknowable + panel"),
                          ("unkL2fab", "#f59e0b", "unknowable + fabricated"), ("leak", "#2563eb", "leaked outcome (control)"),
                          ("ansL2", "#15803d", "knowable twin + panel")):
            ax.plot(x, means[k], color=c, lw=1.4, label=lab, ls="--" if k == "unkL2fab" else "-")
        ax.axhline(0, c="#999", lw=.6)
        ax.set_title(f"{r['model'].split('/')[-1]}: {name}", fontsize=8.5); ax.grid(alpha=.3)
        if ci == 0:
            ax.set_ylabel("'unknowable' minus 'commit' words\n(z-scored readout at DECISION token)", fontsize=7.5)
        if row == 1:
            ax.set_xlabel("relative depth", fontsize=8)
    # item-level: within L2, does the J-lens readout predict which items commit (B's greedy generation)?
    mf = os.path.join(MAIN, tag + ".json")
    if os.path.exists(mf):
        rows = {x["id"]: x for x in json.load(open(mf))["rows"]}
        S = z["js_dec"]; mu = S.mean(0, keepdims=True); sd = S.std(0, keepdims=True) + 1e-8; Sz = (S - mu) / sd
        U = Sz[:, :, g == "unknowable"].mean(-1) - Sz[:, :, g == "commit"].mean(-1)
        il = [i for i, t in enumerate(meta) if t[1] == "unk" and t[2] in ("L2", "L2fab") and ids[i] in rows]
        yc = np.array([rows[ids[i]]["gen_decision"] == "ANSWER" for i in il])
        if 0 < yc.sum() < len(yc):
            from sklearn.metrics import roc_auc_score
            aucs = [roc_auc_score(~yc, U[il, l]) for l in res["js_dec"]["valid"]] if res["js_dec"]["valid"] else []
            if aucs:
                P(f"  item level (L2+L2fab, n={len(il)}, {yc.sum()} commit): J-lens readout predicting NOT committing, "
                  f"median AUROC over valid layers {np.median(aucs):.2f} (range {min(aucs):.2f}-{max(aucs):.2f})")
        else:
            P(f"  item level: commitment is {yc.mean():.0%} on L2/L2fab, no within-condition variation to predict")
    # ranked readouts
    P("  Full-vocabulary J-lens readout of condition-difference vectors (alphabetic tokens only; top 12):")
    for k, v in r["ranked"].items():
        top = [t.strip() for t in v["jlens_top"] if alpha.match(t)][:12]
        bot = [t.strip() for t in v["jlens_bottom"] if alpha.match(t)][:8]
        ranks = {w.strip(): v["concept_rank"][w] for w in (" unpredictable", " uncertain", " random", " higher", " DECLINE", " ANSWER") if w in v["concept_rank"]}
        P(f"   {k:34s} + {top}\n   {'':34s} - {bot}\n   {'':34s} concept ranks {ranks}")
    summary[tag] = res
h, l = axs[0, 0].get_legend_handles_labels()
fig.legend(h, l, loc="lower center", ncol=3 if len(files) < 3 else 5, fontsize=7.5, frameon=False)
fig.tight_layout(rect=(0, 0.09 if len(files) < 3 else 0.06, 1, 1))
os.makedirs(os.path.join(D, "figs"), exist_ok=True)
SUF = "_unkonly" if os.environ.get("UNK_ONLY") == "1" else ""
fig.savefig(os.path.join(D, "figs", f"fig_jlens{SUF}.png"), dpi=170)
json.dump(summary, open(os.path.join(D, f"jlens_summary{SUF}.json"), "w"), default=float)
open(os.path.join(D, f"JLENS_ANALYSIS{SUF}.md"), "w").write("\n".join(out_lines) + "\n")
print("ok")
