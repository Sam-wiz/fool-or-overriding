"""Analyse fo_run.py outputs. usage: python analyze.py <dir> [out.md]
Case-clustered bootstrap (resample the 40 NSE cases) for every contrast."""
import json, sys, os, glob
import numpy as np
from sklearn.metrics import roc_auc_score

D = sys.argv[1]
OUTMD = sys.argv[2] if len(sys.argv) > 2 else os.path.join(D, "REPORT.md")
LV = ["L0", "L1", "L2", "L2irr", "L2fab"]
B = 2000
import re as _re
_src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "fo_run.py")).read()
_ns = {"re": _re}
exec(_src[_src.index("def parse(content):"):_src.index("def auroc")], _ns)
PARSE = _ns["parse"]
_ALL = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "fo_data.json")))
TRANSFER_ITEMS = [i for i in _ALL if i["set"] == "transfer"]
TRAIN_ITEMS = [i for i in json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "fo_data.json"))) if i["set"] == "train"]
rng = np.random.default_rng(0)


def auc(y, s):
    y = np.asarray(y); s = np.asarray(s, float)
    return float(roc_auc_score(y, s)) if len(set(y.tolist())) == 2 else float("nan")


def boot(cases, fn):
    """fn(list_of_case_ids) -> scalar; returns (point, lo, hi) 95% case-clustered."""
    pt = fn(cases)
    u = np.array(sorted(set(cases)))
    sym = {}
    if os.environ.get("CLUSTER", "case") == "symbol":
        for c in u:
            sym.setdefault(c.split("_")[1], []).append(c)
    vals = []
    for _ in range(B):
        if sym:
            ks = list(sym)
            samp = [c for k in rng.choice(ks, len(ks), replace=True) for c in sym[k]]
        else:
            samp = rng.choice(u, len(u), replace=True)
        try:
            v = fn(list(samp))
        except Exception:
            continue
        if v == v:
            vals.append(v)
    if not vals:
        return pt, float("nan"), float("nan")
    return pt, float(np.percentile(vals, 2.5)), float(np.percentile(vals, 97.5))


def fmt(t, pct=False):
    k = 100 if pct else 1
    d = 1 if pct else 3
    return f"{t[0]*k:.{d}f} [{t[1]*k:.{d}f}, {t[2]*k:.{d}f}]"


def analyse(path):
    r = json.load(open(path))
    rows = r["rows"]
    thr = r["thr_youden"]
    for x in rows:  # re-parse stored generations with the fixed parser (post-hoc fix for OLMo-style <ANSWER> tags)
        x["gen_decision"], x["gen_prob"] = PARSE(x["gen"])
    for x in rows:
        x["projn"] = x["proj"] / r["dnorm"]
    # signed position on the knowability axis: 0 = synthetic answerable mean, 1 = synthetic unknowable mean
    hz0 = path.replace(".json", "_hid.npz")
    if os.path.exists(hz0):
        Z0 = np.load(hz0); pos = r["best"]["pos"].lower()
        Xtr = Z0["train_" + pos].astype(np.float32); d0 = Z0["dvec"].astype(np.float32); u0 = d0 / np.linalg.norm(d0)
        ytr = np.array([it["y"] for it in TRAIN_ITEMS])
        m1, m0 = float((Xtr[ytr == 1] @ u0).mean()), float((Xtr[ytr == 0] @ u0).mean())
        for x in rows:
            x["z"] = (x["proj"] - m0) / (m1 - m0)
        # Addendum C: decision-orthogonalised direction (remove within-class decline direction from u)
        side = [q for q in r["side"]["train_transfer"] if q["set"] == "train"]
        dec = np.array([q["p_decline"] for q in side]) > 0.5
        cs = [Xtr[(ytr == k) & dec].mean(0) - Xtr[(ytr == k) & ~dec].mean(0) for k in (0, 1)
              if ((ytr == k) & dec).sum() > 3 and ((ytr == k) & ~dec).sum() > 3]
        Hn0 = Z0[pos].astype(np.float32)
        if cs:
            c0 = np.mean(cs, 0); c0 /= np.linalg.norm(c0)
            up = u0 - (u0 @ c0) * c0; up /= np.linalg.norm(up)
            pm1, pm0 = float((Xtr[ytr == 1] @ up).mean()), float((Xtr[ytr == 0] @ up).mean())
            zp = (Hn0 @ up - pm0) / (pm1 - pm0)
            for x, v in zip(rows, zp):
                x["zperp"] = float(v)
            Tt = Z0["transfer_" + pos].astype(np.float32)
            yt = np.array([it["y"] for it in TRANSFER_ITEMS])
            S_extra = dict(cos_u_decline=float(u0 @ c0), transfer_auroc_u=auc(yt, Tt @ u0), transfer_auroc_uperp=auc(yt, Tt @ up))
        else:
            for x in rows:
                x["zperp"] = float("nan")
            S_extra = dict(cos_u_decline=float("nan"), note="no within-class decline split")
    else:
        for x in rows:
            x["z"] = float("nan"); x["zperp"] = float("nan")
        S_extra = {}
    by = {}
    for x in rows:
        by.setdefault((x["arm"], x["level"]), []).append(x)
    cases = sorted({x["case"] for x in rows})
    idx = {}
    for x in rows:
        idx.setdefault(x["case"], {})[(x["arm"], x["level"])] = x

    def mean_over(cs, arm, lvl, key, f=lambda v: v):
        vals = [f(idx[c][(arm, lvl)][key]) for c in cs if (arm, lvl) in idx[c] and idx[c][(arm, lvl)][key] is not None]
        return float(np.mean(vals)) if vals else float("nan")

    def gen_rate(cs, arm, lvl, dec):
        vals = [idx[c][(arm, lvl)]["gen_decision"] == dec for c in cs if (arm, lvl) in idx[c]]
        return float(np.mean(vals)) if vals else float("nan")

    def sep(cs, lvl, key):
        ys, ss = [], []
        for c in cs:
            for arm in ("unk", "ans"):
                if (arm, lvl) in idx[c] and idx[c][(arm, lvl)][key] is not None:
                    ys.append(int(arm == "unk")); ss.append(idx[c][(arm, lvl)][key])
        return auc(ys, ss)

    S = dict(model=r["model"], best=r["best"], thr=thr, n_layers=r["n_layers"], decline_check=S_extra)
    tab = []
    for arm in ("unk", "ans"):
        for lvl in LV:
            if (arm, lvl) not in by:
                continue
            xs = by[(arm, lvl)]
            tab.append(dict(arm=arm, level=lvl, n=len(xs),
                            fc_answer=np.mean([x["p_answer"] for x in xs]), fc_tool=np.mean([x["p_tool"] for x in xs]),
                            fc_decline=np.mean([x["p_decline"] for x in xs]),
                            gen_answer=np.mean([x["gen_decision"] == "ANSWER" for x in xs]),
                            gen_tool=np.mean([x["gen_decision"] == "CALL_TOOL" for x in xs]),
                            gen_decline=np.mean([x["gen_decision"] == "DECLINE" for x in xs]),
                            gen_unparsed=np.mean([x["gen_decision"] is None for x in xs]),
                            probe=np.mean([x["probe"] for x in xs]), probe_above=np.mean([x["probe"] >= thr for x in xs]),
                            ask_p3=np.mean([x["ask_p3"] for x in xs]), ask_mass=np.mean([x["ask_mass"] for x in xs]),
                            fc_mass=np.mean([x["fc_mass"] for x in xs])))
    S["table"] = tab
    S["zperp"] = {f"{arm}_{lvl}": mean_over(cases, arm, lvl, "zperp") for arm in ("unk", "ans") for lvl in LV if (arm, lvl) in by}
    S["z"] = {f"{arm}_{lvl}": boot(cases, lambda cs, a=arm, l=lvl: mean_over(cs, a, l, "z")) for arm in ("unk", "ans") for lvl in LV if (arm, lvl) in by}
    # route of the commitment lift (forced choice): mass that moved into ANSWER came from DECLINE or from CALL_TOOL
    for lvl in ("L2", "L2fab"):
        S[f"route_{lvl}"] = dict(d_answer=mean_over(cases, "unk", lvl, "p_answer") - mean_over(cases, "unk", "L0", "p_answer"),
                                 d_decline=mean_over(cases, "unk", lvl, "p_decline") - mean_over(cases, "unk", "L0", "p_decline"),
                                 d_tool=mean_over(cases, "unk", lvl, "p_tool") - mean_over(cases, "unk", "L0", "p_tool"))
    # stated-probability skill on committed unknowable rows (sealed outcomes): Brier vs always-50
    for lvl in ("L1", "L2", "L2fab"):
        xs = [x for x in by.get(("unk", lvl), []) if x["gen_decision"] == "ANSWER" and x["gen_prob"] is not None]
        if xs:
            b = np.mean([(x["gen_prob"] / 100 - float(x["truthYes"])) ** 2 for x in xs])
            S[f"brier_{lvl}"] = dict(n=len(xs), brier=float(b), mean_abs_dev_from_50=float(np.mean([abs(x["gen_prob"] - 50) for x in xs])),
                                     acc=float(np.mean([(x["gen_prob"] > 50) == bool(x["truthYes"]) for x in xs if x["gen_prob"] != 50] or [float("nan")])))
    # separations per level
    S["sep"] = {lvl: dict(probe=sep(cases, lvl, "probe"), probe_shuf=sep(cases, lvl, "probe_shuf"),
                          proj=sep(cases, lvl, "proj"), ask_p3=sep(cases, lvl, "ask_p3"),
                          fc_decline=sep(cases, lvl, "p_decline"))
                for lvl in LV}
    S["sep_ci_probe"] = {lvl: boot(cases, lambda cs, l=lvl: sep(cs, l, "probe")) for lvl in ("L0", "L2", "L2fab")}
    # contrasts
    S["lift_fc"] = boot(cases, lambda cs: mean_over(cs, "unk", "L2", "p_answer") - mean_over(cs, "unk", "L0", "p_answer"))
    S["lift_fab_fc"] = boot(cases, lambda cs: mean_over(cs, "unk", "L2fab", "p_answer") - mean_over(cs, "unk", "L0", "p_answer"))
    S["fab_minus_real_fc"] = boot(cases, lambda cs: mean_over(cs, "unk", "L2fab", "p_answer") - mean_over(cs, "unk", "L2", "p_answer"))
    S["lift_gen"] = boot(cases, lambda cs: gen_rate(cs, "unk", "L2", "ANSWER") - gen_rate(cs, "unk", "L0", "ANSWER"))
    S["probe_shift_unk"] = boot(cases, lambda cs: mean_over(cs, "unk", "L2", "probe") - mean_over(cs, "unk", "L0", "probe"))
    S["probe_shift_ans"] = boot(cases, lambda cs: mean_over(cs, "ans", "L2", "probe") - mean_over(cs, "ans", "L0", "probe"))
    S["ask_shift_unk"] = boot(cases, lambda cs: mean_over(cs, "unk", "L2", "ask_p3") - mean_over(cs, "unk", "L0", "ask_p3"))
    # paired gap (difference-in-differences): per case, probe(unk,L) - probe(ans,L); FOOLED predicts the gap shrinks at L2
    def gap(cs, lvl, key="probe"):
        v = [idx[c][("unk", lvl)][key] - idx[c][("ans", lvl)][key] for c in cs if ("unk", lvl) in idx[c] and ("ans", lvl) in idx[c]]
        return float(np.mean(v)) if v else float("nan")
    for key in ("probe", "projn", "ask_p3", "z", "zperp"):
        S[f"gap_{key}"] = {lvl: boot(cases, lambda cs, l=lvl, k=key: gap(cs, l, k)) for lvl in LV}
        S[f"gapchange_{key}_L1L2"] = boot(cases, lambda cs, k=key: gap(cs, "L2", k) - gap(cs, "L1", k))
        S[f"gapchange_{key}_L0L2"] = boot(cases, lambda cs, k=key: gap(cs, "L2", k) - gap(cs, "L0", k))
        S[f"gapchange_{key}_L1L2fab"] = boot(cases, lambda cs, k=key: gap(cs, "L2fab", k) - gap(cs, "L1", k))
    S["lift_fc_L1L2"] = boot(cases, lambda cs: mean_over(cs, "unk", "L2", "p_answer") - mean_over(cs, "unk", "L1", "p_answer"))
    S["act_lift_fc"] = boot(cases, lambda cs: mean_over(cs, "unk", "L0", "p_decline") - mean_over(cs, "unk", "L2", "p_decline"))
    # random-direction separation baseline from the saved chosen-layer activations
    hz = path.replace(".json", "_hid.npz")
    if os.path.exists(hz):
        Z = np.load(hz)
        Hn = Z["end"] if r["best"]["pos"] == "END" else Z["dec"]
        Hn = Hn.astype(np.float32)
        ids = [x["id"] for x in rows]
        y_all = np.array([x["y"] for x in rows]); lv_all = np.array([x["level"] for x in rows])
        rs = np.random.default_rng(7)
        base = {}
        for lvl in ("L0", "L2"):
            m = lv_all == lvl
            aucs = []
            for _ in range(1000):
                v = rs.standard_normal(Hn.shape[1])
                a = auc(y_all[m], Hn[m] @ v); aucs.append(max(a, 1 - a))
            base[lvl] = dict(median=float(np.median(aucs)), p95=float(np.percentile(aucs, 95)))
        S["rand_sep"] = base
    # critical subset: unk & L2/L2fab & committed (gen ANSWER) vs ans at same level (Fomin/whitebox T2)
    crit = {}
    for lvl in ("L2", "L2fab"):
        com = [x for x in by.get(("unk", lvl), []) if x["gen_decision"] == "ANSWER"]
        an = by.get(("ans", lvl), [])
        crit[lvl] = dict(n=len(com), probe=auc([1] * len(com) + [0] * len(an), [x["probe"] for x in com] + [x["probe"] for x in an]) if com else float("nan"),
                         ask=auc([1] * len(com) + [0] * len(an), [x["ask_p3"] for x in com] + [x["ask_p3"] for x in an]) if com else float("nan"))
    S["crit"] = crit
    # act-intent: within unk rows with a panel (L1,L2,L2fab), does the inside signal predict the on-policy action?
    from scipy.stats import spearmanr
    S["act_intent"] = {}
    for lv_ in ("L2", "L2fab", "L1"):
      pool = [x for x in rows if x["arm"] == "unk" and x["level"] == lv_]
      ycom = [int(x["gen_decision"] == "ANSWER") for x in pool]
      S["act_intent"][lv_] = dict(n=len(pool), n_commit=int(sum(ycom)),
                           auc_probe_predicts_commit=auc(ycom, [-x["projn"] for x in pool]),
                           auc_ask_predicts_commit=auc(ycom, [-x["ask_p3"] for x in pool]),
                           auc_fc_predicts_commit=auc(ycom, [x["p_answer"] for x in pool]),
                           spearman_projn_vs_fcanswer=float(spearmanr([x["projn"] for x in pool], [x["p_answer"] for x in pool])[0]))
    # committed unk rows at L2 / L2fab (generation ANSWER): inside-knows fraction (group b vs c)
    grp = {}
    for lvl in ("L2", "L2fab", "L1"):
        com = [x for x in by.get(("unk", lvl), []) if x["gen_decision"] == "ANSWER"]
        grp[lvl] = dict(n_committed=len(com),
                        knows_inside=float(np.mean([x["probe"] >= thr for x in com])) if com else float("nan"),
                        says_irreducible_when_asked=float(np.mean([x["ask_p3"] > 0.5 for x in com])) if com else float("nan"))
    S["groups"] = grp
    # verdict per prereg rule
    lift = max(S["lift_fc"][0], S["lift_gen"][0])
    sepL2 = S["sep"]["L2"]["probe"]
    kn = grp["L2"]["knows_inside"]
    if lift < 0.10:
        v = "NO-LIFT"
    elif sepL2 >= 0.75 and (kn != kn or kn > 0.5):
        v = "OVERRIDING"
    elif sepL2 < 0.65 or (kn == kn and kn < 0.5):
        v = "FOOLED"
    else:
        v = "MIXED"
    S["verdict"] = v
    # Addendum-B rule on the paired projn gap, anchored at L1 (both arms have data; ans computable)
    vb = {}
    for tgt in ("L2", "L2fab"):
        ch = S[f"gapchange_projn_L1{tgt}"] if tgt == "L2fab" else S["gapchange_projn_L1L2"]
        g1 = S["gap_projn"]["L1"][0]
        lift_b = max(boot(cases, lambda cs, t=tgt: mean_over(cs, "unk", t, "p_answer") - mean_over(cs, "unk", "L0", "p_answer"))[0],
                     boot(cases, lambda cs, t=tgt: mean_over(cs, "unk", "L0", "p_decline") - mean_over(cs, "unk", t, "p_decline"))[0])
        if lift_b < 0.10:
            vv = "NO-LIFT"
        elif ch[2] < 0 and ch[0] < -0.5 * abs(g1):
            vv = "FOOLED"
        elif ch[1] <= 0 <= ch[2] or ch[1] > 0:
            vv = "OVERRIDING"
        else:
            vv = "MIXED"
        vb[tgt] = dict(verdict=vv, gap_L1=g1, change=ch, rel_change=ch[0] / abs(g1) if g1 else float("nan"), lift=lift_b)
    S["verdict_B"] = vb
    # transfer AUROC at chosen layer
    S["transfer_auroc"] = r["best"]["transfer_auroc"]
    # steering
    st = r.get("steer", [])
    if st:
        agg = {}
        for x in st:
            agg.setdefault((x["cond"], x["alpha"], x["arm"], x["level"]), []).append(x)
        base = {(a, l): np.mean([x["p_decline"] for x in v]) for (c, al, a, l), v in agg.items() if c == "none"}
        base_ans = {(a, l): np.mean([x["p_answer"] for x in v]) for (c, al, a, l), v in agg.items() if c == "none"}
        steer = []
        for (c, al, a, l), v in sorted(agg.items(), key=str):
            steer.append(dict(cond=c, alpha=al, arm=a, level=l, d_decline=np.mean([x["p_decline"] for x in v]) - base[(a, l)],
                              d_answer=np.mean([x["p_answer"] for x in v]) - base_ans[(a, l)]))
        S["steer"] = steer
    return S


def main():
    files = sorted(f for f in glob.glob(os.path.join(D, "*.json")) if not f.endswith("summary.json"))
    allS = [analyse(f) for f in files]
    L = []
    L.append(f"# Results: {D}\n")
    L.append("| model | layer (pos) | transfer AUROC | lift FC P(ANSWER) L0->L2 (pp) | lift gen ANSWER (pp) | fab-real FC (pp) | probe sep L0 | probe sep L2 | probe sep L2fab | shuf sep L2 | ask-P3 sep L2 | L2 committed n | knows-inside | says-irreducible | verdict |")
    L.append("|" + "---|" * 15)
    L_b = ["\n### Addendum-B verdicts (paired projn gap, L1 anchor)\n", "| model | target | lift (pp) | gap L1 | change | rel | verdict |", "|---|---|---|---|---|---|---|"]
    for S in allS:
        for t, d in S["verdict_B"].items():
            L_b.append(f"| {S['model'].split('/')[-1]} | {t} | {d['lift']*100:.1f} | {d['gap_L1']:.2f} | {fmt(d['change'])} | {d['rel_change']:+.2f} | **{d['verdict']}** |")
    for S in allS:
        g = S["groups"]["L2"]
        L.append(f"| {S['model'].split('/')[-1]} | {S['best']['layer']}/{S['n_layers']} ({S['best']['pos']}) | {S['transfer_auroc']:.3f} | "
                 f"{fmt(S['lift_fc'], True)} | {fmt(S['lift_gen'], True)} | {fmt(S['fab_minus_real_fc'], True)} | "
                 f"{S['sep']['L0']['probe']:.2f} | {fmt(S['sep_ci_probe']['L2'])} | {S['sep']['L2fab']['probe']:.2f} | {S['sep']['L2']['probe_shuf']:.2f} | "
                 f"{S['sep']['L2']['ask_p3']:.2f} | {g['n_committed']} | {g['knows_inside']:.2f} | {g['says_irreducible_when_asked']:.2f} | **{S['verdict']}** |")
    L += L_b
    for S in allS:
        L.append(f"\n## {S['model']}  (thr {S['thr']:.2f}; best {S['best']})\n")
        L.append("| arm | lvl | n | FC ans | FC tool | FC decl | gen ANS | gen TOOL | gen DECL | unparsed | probe | probe>thr | ask P3 | ask mass | fc mass |")
        L.append("|" + "---|" * 15)
        for t in S["table"]:
            L.append("| " + " | ".join([t["arm"], t["level"], str(t["n"])] + [f"{t[k]:.2f}" for k in
                     ("fc_answer", "fc_tool", "fc_decline", "gen_answer", "gen_tool", "gen_decline", "gen_unparsed", "probe", "probe_above", "ask_p3", "ask_mass", "fc_mass")]) + " |")
        L.append("\nSeparation AUROC (unk vs ans) by level: " + "; ".join(
            f"{l}: probe {S['sep'][l]['probe']:.2f}, shuf {S['sep'][l]['probe_shuf']:.2f}, ask {S['sep'][l]['ask_p3']:.2f}, fc_decl {S['sep'][l]['fc_decline']:.2f}" for l in LV))
        L.append(f"\nprobe shift unk L0->L2 {fmt(S['probe_shift_unk'])}; ans {fmt(S['probe_shift_ans'])}; ask P3 shift unk {fmt(S['ask_shift_unk'])}")
        L.append(f"groups: {S['groups']}")
        L.append(f"paired gap probe(unk-ans) by level: " + "; ".join(f"{l} {fmt(S['gap_probe'][l])}" for l in LV))
        L.append(f"gap change probe L1->L2 {fmt(S['gapchange_probe_L1L2'])}; L0->L2 {fmt(S['gapchange_probe_L0L2'])}; L1->L2fab {fmt(S['gapchange_probe_L1L2fab'])}")
        L.append(f"paired gap projn(unk-ans) by level: " + "; ".join(f"{l} {fmt(S['gap_projn'][l])}" for l in LV))
        L.append(f"gap change projn L1->L2 {fmt(S['gapchange_projn_L1L2'])}; L0->L2 {fmt(S['gapchange_projn_L0L2'])}; L1->L2fab {fmt(S['gapchange_projn_L1L2fab'])}")
        L.append(f"gap change ask-P3 L1->L2 {fmt(S['gapchange_ask_p3_L1L2'])}; FC P(ANSWER) lift L1->L2 {fmt(S['lift_fc_L1L2'], True)}pp; ACT (1-P(decl)) lift L0->L2 {fmt(S['act_lift_fc'], True)}pp")
        L.append("z (0=synthetic answerable mean, 1=synthetic unknowable mean): " + "; ".join(f"{k} {fmt(v)}" for k, v in S['z'].items()))
        L.append(f"Addendum C decline check: {S['decline_check']}")
        L.append(f"gap change z  L1->L2 {fmt(S['gapchange_z_L1L2'])} (gap L1 {S['gap_z']['L1'][0]:.2f}); L1->L2fab {fmt(S['gapchange_z_L1L2fab'])}")
        L.append(f"gap change zperp L1->L2 {fmt(S['gapchange_zperp_L1L2'])} (gap L1 {S['gap_zperp']['L1'][0]:.2f}); L1->L2fab {fmt(S['gapchange_zperp_L1L2fab'])}")
        L.append(f"route of lift from L0: L2 {S['route_L2']}; L2fab {S['route_L2fab']}")
        L.append("Brier on committed unk (always-50 = 0.25): " + "; ".join(f"{l} {S.get('brier_' + l)}" for l in ("L1", "L2", "L2fab")))
        L.append(f"critical subset (unk&committed vs ans): {S['crit']}")
        L.append(f"act-intent (unk, L1/L2/L2fab): {S['act_intent']}")
        if S.get('rand_sep'): L.append(f"random-direction |AUROC| baseline (unk vs ans): {S['rand_sep']}")
        if S.get("steer"):
            L.append("\nSteering (change vs no-steer):")
            dirs = [s for s in S["steer"] if s["cond"] == "dir"]
            for s in dirs:
                L.append(f"- dir a={s['alpha']:+.1f} {s['arm']} {s['level']}: dDecline {s['d_decline']*100:+.1f}pp dAnswer {s['d_answer']*100:+.1f}pp")
            for a in (-2.0, 2.0):
                for arm, lvl in (("unk", "L2"), ("ans", "L2"), ("unk", "L0")):
                    rs = [s["d_decline"] for s in S["steer"] if s["cond"].startswith("rand") and s["alpha"] == a and s["arm"] == arm and s["level"] == lvl]
                    if rs:
                        L.append(f"- random a={a:+.1f} {arm} {lvl}: dDecline range [{min(rs)*100:+.1f}, {max(rs)*100:+.1f}]pp")
    open(OUTMD, "w").write("\n".join(L))
    json.dump(allS, open(os.path.join(D, "summary.json"), "w"), default=float, indent=1)
    print("\n".join(L[:3 + len(allS)]))


if __name__ == "__main__":
    main()
