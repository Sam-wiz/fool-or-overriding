"""Analyse fo_phase2.py outputs. usage: python analyze_p2.py <p2_dir> [main_dir]
z here = position on the knowability axis at the main run's chosen layer: 0 = synthetic answerable mean,
1 = synthetic unknowable mean (phase-2 stores (h.u - midpoint)/|d|, so z = that + 0.5)."""
import json, sys, os, glob
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

D = sys.argv[1]
os.makedirs(os.path.join(D, "figs"), exist_ok=True)
rng = np.random.default_rng(0)


def ci(v, B=2000):
    v = np.asarray([x for x in v if x == x], float)
    if len(v) == 0: return (float("nan"),) * 3
    bs = [rng.choice(v, len(v)).mean() for _ in range(B)]
    return float(v.mean()), float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))


def f(t, k=1, d=2):
    return f"{t[0]*k:.{d}f} [{t[1]*k:.{d}f}, {t[2]*k:.{d}f}]"


out, summ = [], []
for p in sorted(glob.glob(os.path.join(D, "*.json"))):
    if p.endswith("summary_p2.json"): continue
    r = json.load(open(p)); name = r["model"].split("/")[-1]
    ids = r["nse_ids"]; grp = lambda i: tuple(i.split("|")[1:3])  # (arm, level)
    base = np.array(r["base_fc"]); z = np.array(r["base_proj_bl"]) + 0.5
    G = {}
    for k, i in enumerate(ids):
        G.setdefault(grp(i), []).append(k)
    S = dict(model=r["model"], layer=r["layer"])
    out.append(f"\n## {r['model']} (layer {r['layer']}/{r['n_layers']})\n")
    # leak control
    rows = []
    for g in [("unk", "L0"), ("unk", "L2"), ("unk", "L2fab"), ("unk", "L2leak"), ("ans", "L2")]:
        if g in G:
            ix = G[g]
            rows.append((g, ci(z[ix]), ci(base[ix, 0]), ci(base[ix, 2])))
    S["leak"] = {f"{a}_{l}": dict(z=zz, p_answer=pa, p_decline=pd) for (a, l), zz, pa, pd in rows}
    out.append("**Leaked-outcome positive control** (z; P(ANSWER); P(DECLINE)):")
    for (a, l), zz, pa, pd in rows:
        out.append(f"- {a} {l}: z {f(zz)}; P(ANS) {f(pa)}; P(DEC) {f(pd)}")
    # patching
    out.append("\n**Patching unk L2/L2fab <- same case unk L0 at the decision token** (mean P(ANSWER), P(DECLINE)):")
    pt = r["patch"]
    b_ans = np.mean([x["base_answer"] for x in pt if x["mode"] == "full" and x["layer"] == pt[0]["layer"]])
    s_ans = np.mean([x["src_answer"] for x in pt if x["mode"] == "full" and x["layer"] == pt[0]["layer"]])
    b_dec = np.mean([x["base_decline"] for x in pt if x["mode"] == "full" and x["layer"] == pt[0]["layer"]])
    s_dec = np.mean([x["src_decline"] for x in pt if x["mode"] == "full" and x["layer"] == pt[0]["layer"]])
    out.append(f"- unpatched target P(ANS) {b_ans:.2f} P(DEC) {b_dec:.2f}; L0 source P(ANS) {s_ans:.2f} P(DEC) {s_dec:.2f}")
    PT = {}
    for x in pt:
        PT.setdefault((x["layer"], x["mode"]), []).append(x)
    S["patch"] = {}
    for l in r["layers_patched"]:
        cells = []
        for m in ("full", "uonly", "ortho"):
            xs = PT.get((l, m), [])
            pa, pdc = np.mean([x["p_answer"] for x in xs]), np.mean([x["p_decline"] for x in xs])
            S["patch"][f"{l}_{m}"] = dict(p_answer=pa, p_decline=pdc)
            cells.append(f"{m}: ANS {pa:.2f} DEC {pdc:.2f}")
        out.append(f"- layer {l}: " + " | ".join(cells))
    # DEC-only steering
    st = r.get("steer_dec", [])
    if st:
        out.append("\n**Steering at the decision token only (chosen layer)**, change in P(DECLINE) / P(ANSWER) vs unsteered:")
        SD = {}
        for x in st:
            SD.setdefault((x["cond"], x["alpha"], x["arm"], x["level"]), []).append(x)
        S["steer_dec"] = {}
        for (c, a, arm, lvl), xs in sorted(SD.items(), key=str):
            dd = np.mean([x["p_decline"] - x["base_decline"] for x in xs]); da = np.mean([x["p_answer"] - x["base_answer"] for x in xs])
            S["steer_dec"][f"{c}|{a}|{arm}|{lvl}"] = dict(d_decline=dd, d_answer=da)
            if c == "dir":
                out.append(f"- dir a={a:+.0f} {arm} {lvl}: dDEC {dd*100:+.1f}pp dANS {da*100:+.1f}pp")
        for a in (-4.0, 4.0):
            for arm, lvl in (("unk", "L2"), ("ans", "L2"), ("unk", "L0")):
                v = [S["steer_dec"][k]["d_decline"] for k in S["steer_dec"] if k.startswith("rand") and k.split("|")[1] == str(a) and k.endswith(f"|{arm}|{lvl}")]
                if v: out.append(f"- random (8) a={a:+.0f} {arm} {lvl}: dDEC [{min(v)*100:+.1f}, {max(v)*100:+.1f}]pp")
    # ask after acting
    aa = r.get("ask_after", [])
    if aa:
        out.append("\n**Asked after acting, same conversation** (mean P(1 COMPUTABLE), P(3 IRREDUCIBLE)):")
        AA = {}
        for x in aa: AA.setdefault((x["arm"], x["level"]), []).append(x)
        S["ask_after"] = {}
        for k, xs in sorted(AA.items()):
            S["ask_after"][f"{k[0]}_{k[1]}"] = dict(p1=float(np.mean([x["p1"] for x in xs])), p3=float(np.mean([x["p3"] for x in xs])))
            out.append(f"- {k[0]} {k[1]}: P1 {np.mean([x['p1'] for x in xs]):.2f}  P3 {np.mean([x['p3'] for x in xs]):.2f}")
    # triage vs placebo
    tr = r.get("triage", [])
    if tr:
        out.append("\n**Triage vs placebo system prompt** (FC P(ANSWER), P(DECLINE), greedy ANSWER rate, z):")
        TR = {}
        for x in tr: TR.setdefault((x["cond"], x["arm"], x["level"]), []).append(x)
        S["triage"] = {}
        for k, xs in sorted(TR.items()):
            zz = np.mean([x["projn"] for x in xs]) + 0.5
            d = dict(p_answer=float(np.mean([x["p_answer"] for x in xs])), p_decline=float(np.mean([x["p_decline"] for x in xs])),
                     gen_answer=float(np.mean([x["gen_decision"] == "ANSWER" for x in xs])), z=float(zz),
                     cat3=float(np.mean([x["gen_category"] == 3 for x in xs])))
            S["triage"]["|".join(k)] = d
            out.append(f"- {k[0]:7s} {k[1]} {k[2]:5s}: P(ANS) {d['p_answer']:.2f} P(DEC) {d['p_decline']:.2f} gen-ANS {d['gen_answer']:.2f} z {zz:.2f} cat3 {d['cat3']:.2f}")
    # logit lens timeline figure
    lens = np.array(r["lens"]); projl = np.array(r["projl"]) + 0.5
    fig, ax = plt.subplots(1, 2, figsize=(9, 3.2))
    for g, c, lab in ((("unk", "L0"), "#555", "unk, no panel"), (("unk", "L2"), "#c2410c", "unk, real panel"),
                      (("unk", "L2fab"), "#a16207", "unk, fabricated"), (("ans", "L2"), "#1d4ed8", "ans, real panel"),
                      (("unk", "L2leak"), "#15803d", "unk, outcome leaked")):
        if g not in G: continue
        ix = G[g]
        ax[0].plot(projl[ix].mean(0), color=c, label=lab)
        ax[1].plot((lens[ix, :, 0] - np.maximum(lens[ix, :, 1], lens[ix, :, 2])).mean(0), color=c, label=lab)
    ax[0].set_title("inside: knowability axis by layer (0 ans, 1 unk)", fontsize=9); ax[0].axhline(0, c="k", lw=.4); ax[0].axhline(1, c="k", lw=.4)
    ax[1].set_title("logit lens: logit(ANSWER) - max(DECLINE, CALL_TOOL)", fontsize=9); ax[1].axhline(0, c="k", lw=.4)
    ax[0].axvline(r["layer"], ls=":", c="k"); ax[1].axvline(r["layer"], ls=":", c="k")
    for a in ax: a.set_xlabel("layer", fontsize=8); a.grid(alpha=.3)
    ax[1].legend(fontsize=6.5); fig.suptitle(name, fontsize=10); fig.tight_layout()
    fig.savefig(os.path.join(D, "figs", f"lens_{name}.png"), dpi=160); plt.close(fig)
    # patching figure
    fig, ax = plt.subplots(figsize=(4.4, 3.2))
    Ls = r["layers_patched"]
    for m, c, lab in (("full", "#111", "full L0 vector"), ("uonly", "#15803d", "knowability component only"), ("ortho", "#c2410c", "everything except knowability")):
        ax.plot(Ls, [S["patch"][f"{l}_{m}"]["p_answer"] for l in Ls], "-o", ms=3, color=c, label=lab)
    ax.axhline(b_ans, ls="--", c="#999", lw=1); ax.axhline(s_ans, ls=":", c="#999", lw=1)
    ax.text(Ls[0], b_ans + 0.02, "with panel", fontsize=7, color="#666"); ax.text(Ls[0], s_ans + 0.02, "no panel", fontsize=7, color="#666")
    ax.set_xlabel("layer patched (decision token)", fontsize=8); ax.set_ylabel("P(ANSWER) on unknowable, panel shown", fontsize=8)
    ax.set_ylim(-0.02, 1.02); ax.legend(fontsize=6.5, loc="center left"); ax.grid(alpha=.3); ax.set_title(name + ": patch no-panel state into panel run", fontsize=8)
    fig.tight_layout(); fig.savefig(os.path.join(D, "figs", f"patch_{name}.png"), dpi=160); plt.close(fig)
    summ.append(S)
open(os.path.join(D, "REPORT_P2.md"), "w").write("\n".join(out))
json.dump(summ, open(os.path.join(D, "summary_p2.json"), "w"), indent=1, default=float)
print("\n".join(out))
