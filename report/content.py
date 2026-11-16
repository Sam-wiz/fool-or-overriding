# Report content (new sprint work, revised after review). Every number is read from results/*.json.
import json, os, numpy as np
R = json.load(open("results/report_numbers.json"))["models"]
RF = json.load(open("results/review_fixes.json"))
V4 = json.load(open("results/v4_summary.json")); V4m, DP = V4["v4"], V4["deep"]
SV3 = json.load(open("results/steer_v3_raw.json"))
SV5 = json.load(open("results/steer_v5_raw.json")) if os.path.exists("results/steer_v5_raw.json") else {}
PB = json.load(open("results/pipeline_b_summary.json"))   # pipeline B (pipeline_b/): Jacobian lens, new domains
JL, DOM = PB["jlens"], PB["domains"]
S70 = PB["scale70b"]; JL["Llama-3.3-70B (4-bit)"] = S70["jlens"]
ALL = ["qwen3-14b", "llama31-8b", "qwen3-8b", "qwen3-4b", "qwen25-7b", "qwen25-3b", "mistral-7b", "llama32-3b", "gemma2-9b", "gate-3b"]
ORDER = [t for t in ALL if t in R and t in V4m and t in RF]
NICE = {"qwen3-14b": "Qwen3-14B", "llama31-8b": "Llama-3.1-8B", "qwen3-8b": "Qwen3-8B", "qwen3-4b": "Qwen3-4B", "qwen25-3b": "Qwen2.5-3B",
        "gemma2-9b": "Gemma-2-9B", "gate-3b": "SFT gate (Qwen2.5-3B)", "qwen25-7b": "Qwen2.5-7B", "mistral-7b": "Mistral-7B-v0.3", "llama32-3b": "Llama-3.2-3B"}
NM = len(ORDER); NMW = {6: "six", 7: "seven", 8: "eight", 9: "nine", 10: "ten"}.get(NM, str(NM))
pc = lambda x: "–" if x is None else f"{100 * x:.0f}%"
f2 = lambda x: "–" if x is None or (isinstance(x, float) and not np.isfinite(x)) else f"{x:.2f}"
def rng(v, fmt=None, sep="–"):
    v = [x for x in v if x is not None and np.isfinite(x)]
    if not v: return "–"
    if fmt is pc or fmt is None and False: pass
    if fmt is pc:
        a, b = f"{100 * min(v):.0f}", f"{100 * max(v):.0f}"
        return f"{a}%" if a == b else f"{a}–{b}%"
    fmt = fmt or f2
    a, b = fmt(min(v)).replace("-", "−"), fmt(max(v)).replace("-", "−")
    if a == b: return a
    return f"{a} to {b}" if min(v) < 0 else f"{a}{sep}{b}"
NG = [t for t in ORDER if t != "gate-3b"]
USE = [t for t in ORDER if V4m[t]["behaviour"]["L2post"]["commit"] >= 0.5]      # models that act on the leaked answer
PANEL = [t for t in ORDER if R[t]["behaviour"]["unk_L2"]["commit"] >= 0.25]     # models the panel pushes to commit
RESIST = [t for t in ORDER if t not in USE]
WN = lambda n: {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine", 10: "ten"}.get(n, str(n))
b4 = lambda t, lv: V4m[t]["behaviour"][lv]
X4 = lambda t: V4m[t]["X_dm"]; N4 = lambda t: V4m[t]["N_dm_crossfit"]

# ---------- computed numbers used in the text ----------
N = {}
N["post_commit"] = rng([b4(t, "L2post")["commit"] for t in USE], pc)
N["post_acc"] = rng([b4(t, "L2post")["acc_of_committed"] for t in USE if t != "gate-3b"], pc)
N["post_ask"] = rng([b4(t, "L2post")["ask_unk"] for t in USE if t != "llama31-8b"])
N["resist_post"] = rng([b4(t, "L2post")["commit"] for t in RESIST], pc)
N["resist_names"] = ", ".join(NICE[t] for t in RESIST)
N["n_use"], N["n_panel"] = WN(len(USE)), WN(len(PANEL))
N["post_ask_llama"] = f2(b4("llama31-8b", "L2post")["ask_unk"]) if "llama31-8b" in ORDER else "–"
N["fipost_X"] = rng([X4(t)["FI_L2post"] for t in USE if X4(t)["n"]])
N["fipost_N"] = rng([N4(t)["FI_L2post"] for t in USE if N4(t)["n"]])
N["fi_X"] = rng([R[t]["X_dm_deep"]["FI"] for t in ORDER if R[t]["X_dm_deep"]["n"]])
N["fi_N"] = rng([R[t]["N_dm_crossfit_deep"]["FI"] for t in ORDER if R[t]["N_dm_crossfit_deep"]["n"]])
N["ratio_X"] = rng([X4(t)["calib_ratio"] for t in USE if X4(t)["calib_ratio"] is not None and X4(t)["n"] >= 5])
N["ratio_N"] = rng([N4(t)["calib_ratio"] for t in USE if N4(t)["calib_ratio"] is not None and N4(t)["n"] >= 5])
N["ratio_all"] = rng([P(t)["calib_ratio"] for t in USE for P in (X4, N4) if P(t)["calib_ratio"] is not None and P(t)["n"] >= 5], pc)
N["fi_max"] = f2(max(R[t][p]["FI"] for t in ORDER for p in ("X_dm_deep", "N_dm_crossfit_deep") if R[t][p]["n"]))
gt = sum(X4(t)["post_gt_panel"] + N4(t)["post_gt_panel"] for t in USE); tot = sum(X4(t)["n"] + N4(t)["n"] for t in USE)
N["post_gt"] = f"{gt} of {tot}"
cr = {c: sum(RF[t][f"ci_rule_{p}"][c] for t in ORDER for p in ("X_dm", "N_dm_crossfit")) for c in ("Overriding", "Mixed", "Fooled")}
N["ci_O"], N["ci_M"], N["ci_F"], N["ci_tot"] = cr["Overriding"], cr["Mixed"], cr["Fooled"], sum(cr.values())
N["ask_unk"] = rng([R[t]["behaviour"]["unk_L2"]["ask_unk"] for t in ORDER])
N["commit_max"] = pc(max(R[t]["behaviour"]["unk_L2"]["commit"] for t in ORDER))
N["n_full"] = sum(1 for t in ORDER if R[t]["behaviour"]["unk_L2"]["commit"] >= 0.95)
gl = [DP[t]["summary"]["FI_leak"] for t in ORDER if t in DP and DP[t]["summary"]["n_valid_deep"]]
N["graded_spread"] = f2(max(max(g.values()) - min(g.values()) for g in gl)) if gl else "–"
def first_depth(t, mode, thr):
    if t not in DP or "T3" not in DP[t]: return None
    NL = R[t]["NL"]; L = sorted((int(k), v) for k, v in DP[t]["T3"]["layers"].items())
    for l, v in L:
        if v[mode] >= thr: return l / NL
    return None
PT = [t for t in ORDER if t in DP and "T3" in DP[t]]
N["patch_suffix"] = rng([first_depth(t, "suffix", 0.9) for t in PT])
N["patch_last"] = rng([first_depth(t, "last", 0.5) for t in PT])
N["patch_x_mid"] = f2(max(max(v["xdir_last"] for l, v in DP[t]["T3"]["layers"].items() if int(l) / R[t]["NL"] <= 0.55) for t in PT)) if PT else "–"
N["patch_x_late"] = rng([max(v["xdir_last"] for v in DP[t]["T3"]["layers"].values()) for t in PT])
fd = {t: {(f["layer"] / R[t]["NL"] > 0.6, f["level"]): f["delta"] for f in DP[t]["T2_fd"]} for t in PT if "T2_fd" in DP[t]}
N["fd_late_L0"] = rng([v[(True, "L0")] for v in fd.values()], lambda x: f"{x:.1f}")
N["fd_late_L2"] = rng([v[(True, "L2")] for v in fd.values()], lambda x: f"{x:.1f}")
N["fd_mid"] = rng([v[(False, "L2")] for v in fd.values()], lambda x: f"{x:.1f}")
N["n_patch"] = len(PT)

def push_ab(t, nm, lv="know/L2"):
    p = V4m.get(t, {}).get("push2", {}).get(nm)
    return p["behaviour"][lv]["abandon"] if p else "–"

# ---------- tables ----------
def behaviour_table():
    rows = []
    for t in ORDER:
        b = R[t]["behaviour"]; p = b4(t, "L2post")
        rows.append([NICE[t], pc(b["unk_L0"]["commit"]), pc(b["unk_L2"]["commit"]), pc(b["unk_L2irr"]["commit"]), pc(b["unk_L2fab"]["commit"]),
                     f'{pc(p["commit"])} / {pc(p["acc_of_committed"])}', f'{pc(b["unk_L0"]["decline"])} → {pc(b["unk_L2"]["decline"])}',
                     f'{pc(b["know_L2"]["commit"])} / {pc(RF[t]["know_L2_acc"])}',
                     f'{f2(b["unk_L2"]["ask_unk"])} / {f2(b["know_L2"]["ask_unk"])} / {f2(p["ask_unk"])}'])
    return rows

def probe_table():
    rows = []
    for t in ORDER:
        m = R[t]; X = m["X_dm_deep"]; Nn = m["N_dm_crossfit_deep"]; x4, n4 = X4(t), N4(t)
        rows.append([NICE[t], f'{X["n"]}/{Nn["n"]}', f'{f2(X["posctrl"])} / {f2(Nn["posctrl"])}',
                     f'{f2(X["FI"])} / {f2(Nn["FI"])}', f'{f2(X["FIfab"])} / {f2(Nn["FIfab"])}',
                     f'{f2(x4["FI_L2post"])} / {f2(n4["FI_L2post"])}', f'{f2(x4["calib_ratio"])} / {f2(n4["calib_ratio"])}',
                     f'X {RF[t]["ci_rule_X_dm"]["Overriding"]}/{RF[t]["ci_rule_X_dm"]["Mixed"]}/{RF[t]["ci_rule_X_dm"]["Fooled"]}; N {RF[t]["ci_rule_N_dm_crossfit"]["Overriding"]}/{RF[t]["ci_rule_N_dm_crossfit"]["Mixed"]}/{RF[t]["ci_rule_N_dm_crossfit"]["Fooled"]}'])
    return rows

def steer_src(t):
    """steering at a layer where the X direction passes the validity gate: the a-priori n_layers//2 if valid, else the v5 rerun."""
    if RF[t]["steer_layer_valid"] or t not in SV5: return SV3.get(t), RF[t]["steer_layer"], RF[t]["steer_layer_valid"]
    meta = json.load(open(f"results/v5-{t}/xsteer2_meta.json")); return SV5[t], meta["layer"], True
def sc(S, k, a, arm): return (S.get(f"{k}|{a}|{arm}") or {}).get("commit")
def steer_table():
    rows = []
    for t in ORDER:
        S, L, ok = steer_src(t)
        if S is None or t not in PANEL: continue
        rows.append([NICE[t], f'{L}{"" if ok else "*"}',
                     f"{pc(sc(S,'xdir',0,'unk_L2'))} → {pc(sc(S,'xdir',8,'unk_L2'))} ({pc(sc(S,'random',8,'unk_L2'))})",
                     f"{pc(sc(S,'xdir',0,'unk_L2fab'))} → {pc(sc(S,'xdir',8,'unk_L2fab'))} ({pc(sc(S,'random',8,'unk_L2fab'))})",
                     f"{pc(sc(S,'xdir',8,'know_L2'))} ({pc(sc(S,'random',8,'know_L2'))})",
                     f"{pc(sc(S,'xdir',0,'unk_L0'))} → {pc(sc(S,'xdir',-8,'unk_L0'))} ({pc(sc(S,'random',-8,'unk_L0'))})"])
    return rows
def steer_extra():
    out = []
    for t in ORDER:
        if t in ("llama31-8b", "qwen25-3b", "qwen3-8b") or t not in PANEL: continue
        S, L, ok = steer_src(t)
        if not S: continue
        out.append(f"{NICE[t]} {pc(sc(S,'xdir',0,'unk_L2'))} → {pc(sc(S,'xdir',8,'unk_L2'))} (random {pc(sc(S,'random',8,'unk_L2'))})")
    return ("Elsewhere: " + "; ".join(out) + ".") if out else ""

def leak_table():
    rows = []
    for t in ORDER:
        if t not in DP or not DP[t]["summary"]["n_valid_deep"]: continue
        g = DP[t]["summary"]["FI_leak"]; b = DP[t]["behaviour"]
        rows.append([NICE[t], f2(DP[t]["summary"]["FI_L2"])] + [f2(g[k]) for k in ("r25", "r08", "r03", "r01", "exact")] +
                    [f'{f2(b["leak_r25"]["p_answer"])} → {f2(b["leak_exact"]["p_answer"])}'])
    return rows

JL_VALID = [m for m in JL if JL[m]["doubt"]["leak"] >= 70]                        # leak control works for the J-lens readout
JL_BIG = ["Llama-3.3-70B (4-bit)", "Qwen3-14B", "Qwen2.5-14B", "Phi-4", "Llama-3.1-8B", "Qwen3-8B"]   # 8B and above, leak control works
JL_COMMIT = ["Llama-3.1-8B", "Qwen3-14B", "Qwen3-8B", "Qwen2.5-3B"]                   # committers whose doubt words stay near the top
_BF = {"Llama-3.1-8B": "Meta_Llama_3_1_8B_Instruct", "Qwen3-14B": "Qwen3_14B", "Qwen3-8B": "Qwen3_8B", "OLMo-2-7B": "OLMo_2_1124_7B_Instruct",
       "Qwen2.5-14B": "Qwen2_5_14B_Instruct", "Qwen2.5-7B": "Qwen2_5_7B_Instruct", "Gemma-2-9B": "gemma_2_9b_it", "Mistral-7B-v0.3": "mistral_7b_instruct_v0_3", "Phi-4": "phi_4"}
def b_commit(m):
    """commitment with the real panel: B's greedy generation (forced-choice P(ANSWER) for OLMo, which ignores the format)."""
    if m == "Llama-3.3-70B (4-bit)": return pc(S70["commit_L2"])
    if m == "Qwen3-4B": return pc(R["qwen3-4b"]["behaviour"]["unk_L2"]["commit"]) + " (A)"
    if m == "Qwen2.5-3B": return pc(R["qwen25-3b"]["behaviour"]["unk_L2"]["commit"]) + " (A)"
    rows = json.load(open(f"pipeline_b/results/main/{_BF[m]}.json"))["rows"]; xs = [x for x in rows if x["arm"] == "unk" and x["level"] == "L2"]
    if m == "OLMo-2-7B": return f'{np.mean([x["p_answer"] for x in xs]):.2f}†'
    return pc(np.mean([x["gen_decision"] == "ANSWER" for x in xs]))
def jl_rng(ms, key):
    return rng([JL[m]["doubt"][key] for m in ms], lambda x: f"{x:.0f}")
N["jl_big_panel"] = jl_rng(JL_BIG, "panel"); N["jl_valid_leak"] = jl_rng(JL_VALID, "leak"); N["jl_commit_panel"] = jl_rng(JL_COMMIT, "panel")
N["jl_unc_leak"] = rng([JL[m]["leak_unc"] for m in JL_COMMIT])
N["fileak_X"] = rng([X4(t)["FI_L2leak"] for t in USE if X4(t)["n"]])
N["jl_fi_big"] = rng([JL[m]["fi_contrast"] for m in ("Llama-3.1-8B", "Qwen3-14B", "Qwen3-8B")])
N["jl_leak_big"] = rng([JL[m]["leak_contrast"] for m in ("Llama-3.1-8B", "Qwen3-14B", "Qwen3-8B")])
N["dom_gap"] = rng([100 * v["gap_change_rel"] for d in DOM.values() for v in d.values()], lambda x: f"+{x:.0f}%")
N["dom_panel"] = rng([v["jlens"]["doubt"]["panel"] for d in DOM.values() for v in d.values()], lambda x: f"{x:.0f}")
N["dom_leak"] = rng([v["jlens"]["doubt"]["leak"] for d in DOM.values() for v in d.values()], lambda x: f"{x:.0f}")
def jl_reading(m):
    d = JL[m]["doubt"]
    if d["leak"] < 70: return "leak control fails: no reading"
    if d["panel"] >= 85: return "demoted like the leak (tentative: weak control)"
    if d["panel"] >= 50: return "partly demoted"
    return "not demoted: doubt kept"
def jl_table():
    order = ["Llama-3.3-70B (4-bit)", "Qwen3-14B", "Qwen2.5-14B", "Phi-4", "Llama-3.1-8B", "Qwen3-8B", "Qwen2.5-7B", "OLMo-2-7B", "Qwen3-4B", "Qwen2.5-3B", "Gemma-2-9B", "Mistral-7B-v0.3"]
    return [[m, b_commit(m), f'{JL[m]["doubt"]["panel"]:.0f} / {JL[m]["doubt"]["leak"]:.0f}', f'{f2(JL[m]["fi_contrast"])} / {f2(JL[m]["leak_contrast"])}',
             f'{f2(JL[m]["fi_unc"])} / {f2(JL[m]["leak_unc"])}', jl_reading(m)] for m in order]
def dom_table():
    rows = []
    for d, mods in DOM.items():
        for m, v in mods.items():
            rows.append([d, m, f'{pc(v["commit_L0"])} → {pc(v["commit_L2"])} ({pc(v["commit_fab"])})', f2(v["ask_unk_L2"]),
                         f'+{100 * v["gap_change_rel"]:.0f}%', f'{v["jlens"]["doubt"]["panel"]:.0f} / {v["jlens"]["doubt"]["leak"]:.0f}'])
    return rows

GITHUB_URL = "https://github.com/Sam-wiz/fool-or-overriding"
TITLE = "Fooled or Overriding? Probes Barely Respond to a Leaked Answer, but a Jacobian-Lens Readout Suggests LLM Agents Override"
AUTHORS = [("Samrudh Jain", "Independent researcher"), ("Pranav Aggarwal", "Independent researcher")]

ABSTRACT = (
    "An LLM agent shown an official-looking indicator panel commits on questions nobody can answer, and a fabricated panel works as well as real data "
    "(Aggarwal, 2026). Is the agent fooled, losing its internal sense that the question is unknowable, or overriding, keeping it and acting anyway? "
    f"Across 13 open-weight models (3–70B) on 40 matched stock questions, panels raise commitment from 0% to as much as {N['commit_max']}. Uncalibrated, linear "
    f"probes suggest overriding, but a leaked-answer calibration shows they cannot decide: with the realised price in the panel, models answer correctly while "
    f"the probes move only {N['fipost_X']} of the way and the models still call the question unknowable. A Jacobian-lens rank readout of the decision state does "
    f"respond: the leaked answer pushes 'uncertain', 'unpredictable', 'unknown' and 'unclear' {N['jl_valid_leak']}% of the way down the vocabulary. In four of the six "
    f"models the panel moves to commit, the panel leaves them near the top ({N['jl_commit_panel']}%), also on crypto and weather data, which suggests overriding; "
    "Qwen3-4B is partly demoted and OLMo-2-7B looks fooled, tentatively. Patching places the panel's effect in the question tokens, outside the knowability "
    "direction, and a one-paragraph triage prompt removes the commitments. Internal readouts should be calibrated against an answer-revealing context before "
    "they are read as beliefs."
)

BODY = [
    ("h2", "1. Introduction"),
    ("p", "AI agents increasingly sit behind dashboards, market feeds and research tools, and are asked to act. Some questions they get cannot be answered by anyone, "
          "such as whether a stock will close higher in ten trading days; the right action is to decline and say so. Aggarwal (2026) showed that across 12 frontier models, "
          "a professional-looking indicator panel raises commitment on such questions from 6.5% to 54.0%, and a fully fabricated panel works as well as real data. The same "
          "models classify the questions as irreducible when asked."),
    ("p", "That leaves open the question that matters for fixing it. Is the model **fooled**, so that the packaging corrupts what it represents about the question and the fix is "
          "better evidence handling? Or is it **overriding**: it still represents 'this is unknowable' and commits anyway, so the fix is an action-level gate, perhaps monitored "
          "from the inside? This is the sprint's Track 1 question of how large the gap is between what a model implies by acting and what it represents. **Our answer:** linear probes and "
          "self-report cannot tell, because they barely respond even to a leaked answer; calibrated against that answer, a Jacobian-lens readout suggests that the models the "
          "panel moves keep their doubt and override it."),
    ("p", "We measure three channels on every item: **inside** (linear probes for unknowability at every layer, and a Jacobian-lens readout of what the decision state disposes "
          "the model to say), **words** (the model's answer when asked whether the question is knowable) and **action** (ANSWER / CALL_TOOL / DECLINE under the original agentic prompt). "
          "Probes, patching and steering use ten models (pipeline A); the Jacobian lens, the new domains and a 70B model come from an independently built second pipeline (B, in pipeline_b/). Our contributions:"),
    ("num", [
        f"**Behaviour in {WN(NM - 1)} open models and a decline-tuned gate.** In {N['n_panel']} models panels raise commitment on unknowable questions, by up to {N['commit_max'].rstrip('%')} points ({N['n_full']} reach ≥95%); fabricated panels "
        f"work as well as real ones and an irrelevant panel mostly does not. Gemma-2-9B swaps correct declines for useless tool calls, and three further models ({N['resist_names']}) resist panels entirely.",
        f"**A calibration that changes the conclusion.** Uncalibrated, the probes say *overriding*: the median deep-layer fooling index is {N['fi_N']} (cross-fitted) and {N['fi_X']} (cross-domain). "
        f"We add the missing 'fooled' reference, the same question with the answer in the panel. The {N['n_use']} models that act on it answer it, mostly correctly, but the probes move only to {N['fipost_X']} "
        "and the self-report barely moves, also when 'Today' is left unchanged. Both mostly encode the question's form, so fooled and overriding are not separable with them.",
        f"**A readout that responds to the calibration.** A Jacobian lens (Gurnee et al., 2026) at the decision token responds to the leaked answer: it pushes the doubt words "
        f"('uncertain', 'unpredictable', 'unknown', 'unclear') {N['jl_valid_leak']}% of the way down the vocabulary wherever the control works. In four of the six "
        f"committers (Llama-3.1-8B, Qwen3-8B, Qwen3-14B, Qwen2.5-3B) the panel leaves them near the top ({N['jl_commit_panel']}%), also on crypto and weather, consistent with overriding; "
        "Qwen3-4B is partly demoted and OLMo-2-7B looks fooled, tentatively. Models the panel does not move keep them too.",
        "**Where the panel acts.** Activation patching shows that the panel's effect is carried at the question and instruction tokens in the middle of the network, largely outside "
        "the probe direction, which the decision does read in late layers.",
        "**Interventions with controls.** Steering along the direction at a layer that passes the validity gate reduces commitment beyond random directions in two models only. "
        "A neutral 'Are you sure?' control shows that the finding that pushback makes models abandon correct answers was mostly driven by knowability wording.",
    ]),

    ("h2", "2. Related Work"),
    ("p", "**Behavioural honesty and calibration.** MASK (Ren et al., 2025) shows models knowingly contradict their beliefs under pressure; SycEval (Fanous et al., 2025) and FlipFlop "
          "(Laban et al., 2023) measure answer flipping under rebuttal. Kalai et al. (2025) argue that grading rewards confident guessing, and AbstentionBench (Kirichenko et al., 2025) "
          "finds abstention unsolved; agents also fail to abstain (Liu et al., 2026) and are misled by adversarial tool outputs (Zhan et al., 2026). Our setting is agentic: the model has a DECLINE action and a tool, and the question is unknowable for everyone."),
    ("p", "**Knowing what you don't know, from the inside.** Hidden states encode answerability and hallucination risk (Kadavath et al., 2022; Slobodkin et al., 2023; Orgad et al., 2024; "
          "Ferrando et al., 2024). Lavi, Milo & Geva (2025) find an unanswerability direction that classifies and steers abstention. Du & Hu (2026) show that models linearly represent "
          "structurally impossible prompts, that this direction is nearly orthogonal to refusal (Arditi et al., 2024), and call answering anyway a routing failure. Probe-based lie and "
          "deception detectors (Azaria & Mitchell, 2023; Marks & Tegmark, 2023; Goldowsky-Dill et al., 2025) motivate internal monitors, with known caveats (Levinstein & Herrmann, 2023). "
          "Our calibration adds a concrete caveat: an unknowability direction can separate question types perfectly yet barely respond when context makes the question answerable."),
    ("p", "**Authority overriding internal knowledge.** Halawi et al. (2023) show correct answers formed early being overwritten later; Wang et al. (2025) locate sycophancy in late layers; "
          "Joswin et al. (2026) find that persona authority *erases* the correct answer's representation late in Llama-3.1-8B, Qwen3-8B and Gemma-2-9B. **What is new here:** authority "
          "carried by evidence packaging (including fabricated and irrelevant panels) rather than by the question or a persona; three channels on the same items; a positive control and a "
          "leaked-answer anchor for the probe scale; and patching that locates where the panel acts. The behavioural phenomenon, cases, prompt and SFT recipe come from the second author's "
          "prior paper (Aggarwal, 2026); all internal measurements are new sprint work."),

    ("h2", "3. Methods"),
    ("p", "**Items.** 40 post-cutoff Indian-equity cases (NSE, Feb 2026) from Aggarwal (2026). Each gives an *unknowable* question (will the close 10 trading days ahead be higher?) "
          "and a matched *knowable* one (based only on the data shown, is the current close higher than 10 trading days ago?). Unknowable questions appear at **L0** (no data), "
          "**L1** (two prices), **L2** (full indicator panel), **L2′** (another stock's panel, dates rewritten) and **L2-fab** (new: every indicator invented). Knowable questions "
          "appear at L1 and L2. **Positive control (know/L0):** the knowable question with no data, which context alone makes unanswerable. **Leaked-answer anchor (new):** the same "
          "unknowable question and L2 panel plus a line giving the realised close on the target date, with 'Today' moved to that date (**answer shown**). "
          "**Graded leakage:** the target-date close given as a range of half-width 0–25% of price. Crypto/sports/weather sets (216 unknowable, 72 answerable items) train the cross-domain probe."),
    ("p", "**Models and prompt.** Qwen3-14B, Qwen3-8B, Qwen3-4B (thinking off), Qwen2.5-7B, Qwen2.5-3B, Llama-3.1-8B, Llama-3.2-3B, Mistral-7B-v0.3 and Gemma-2-9B (all instruct), "
          "and a known-to-decline pole: Qwen2.5-3B with a LoRA decline gate retrained with the release's SFT recipe. Every model gets the original agentic prompt verbatim (a "
          "web_search tool that cannot see the future; ANSWER / CALL_TOOL / DECLINE), greedy decoding, ≤200 new tokens. Decisions use the release's parser with two fixes (echoed "
          "placeholder brackets are stripped; a bare leading label is accepted). Commitment = ANSWER."),
    ("p", "**Channels and probes.** *Action*: the parsed decision and the next-token log-odds of ANSWER vs CALL_TOOL/DECLINE after '<answer>\\nDECISION:'. *Words*: a separate prompt "
          "with the same data asking whether the question is knowable now (we read P(NO)). *Inside*: the residual stream at the last prompt token. Two probes: **X** (cross-domain), the "
          "difference of class means between unknowable and answerable crypto/sports/weather L2 items; it sees no stock items. **N** (cross-fitted), the difference of means between knowable "
          "and unknowable L2 stock questions on half the cases, scored on the other half (20 splits); L0/L1/L2′/L2-fab, the anchor and the positive control are never seen. A pre-registered "
          "synthetic-data probe failed validity (Appendix C)."),
    ("p", "**Fooling index.** FI = (s̄_unk,L0 − s̄_unk,c) / (s̄_unk,L0 − s̄_know,L2) for condition c: 0 = the context leaves the unknowable question's representation untouched, 1 = it moves "
          "it to where a knowable question with the panel sits. A layer is **valid** if the probe separates knowable from unknowable L2 questions (AUROC ≥ 0.8) and the positive control moves "
          "it toward unknowable (bootstrap 95% CI > 0). Per model we report the median FI over valid layers in the second half of the network, and the pre-registered per-layer rule "
          "(Overriding if the FI CI's upper bound < 0.25, Fooled if the lower bound > 0.5). The **calibrated ratio** is FI(panel) / FI(answer shown), the median over valid deep layers. CIs are case bootstraps (1,000 resamples)."),
    ("p", "**Jacobian lens, second pipeline and new domains.** Pipeline B (pipeline_b/) runs the same prompt and parser on Llama-3.1-8B, Qwen3-14B, Qwen3-8B, Gemma-2-9B, Qwen2.5-7B, "
          "Mistral-7B-v0.3, Qwen2.5-14B, OLMo-2-7B and Phi-4 (14B), with forced-choice and greedy actions, the triage classification asked in words, a probe trained on synthetic items, "
          "and a **leaked outcome** (the unknowable question word for word, with the realised close appended; 'Today' unchanged). The **Jacobian lens** (Gurnee et al., 2026) maps a "
          "residual vector through the average Jacobian of the rest of the network (64 wikitext sequences of 128 tokens; 32 for the 70B model; full-vocabulary readouts by finite differences on 16, or 8) onto the vocabulary. We decode the condition-mean change of the decision-token "
          "state (panel − no data; leak − panel; knowable − unknowable) over the full vocabulary at 70% and 85% depth (fixed in advance) and report where four doubt words land, as % of "
          "the way down the vocabulary. **New domains** (B): crypto (10 coins × 4 dates, Binance public daily candles, close 10 days ahead) and weather (10 cities × 4 dates, Open-Meteo "
          "archive, maximum temperature 14 days ahead), each with every arm above, 2026 data. The J-lens and the new domains were added on the last day (post-hoc)."),
    ("p", "**Mechanism tests.** *Patching*: we run the panel (L2) prompt and replace, at one layer, the hidden states of the shared suffix (the question and instructions "
          "after the data block, identical tokens in the L0 and L2 prompts) with those from the no-panel run: the whole suffix, the last token only, or only the X component at the last "
          "token. We report the fraction of the L0–L2 gap in abstain log-odds restored. *Read-out gain*: the change in abstain log-odds when one class gap along X is added at the last "
          "token at mid and three-quarter depth. *Steering*: add α·Δ (Δ = X class-mean difference, α = ±8) at every position at layer n_layers//2, or at the first valid layer above it "
          "where n_layers//2 fails the gate; controls are three same-norm random directions. *Pushback*: append the model's answer and either the original 'Are you sure? Think again carefully "
          "about whether this can really be known…' or a **neutral** 'Are you sure? Please give your final decision…'. Compute: one A100 per model (Colab and Modal)."),

    ("h2", "4. Results"),
    ("h3", "4.1 Panels unlock commitment; the words do not move"),
    ("p", f"The panel effect reproduces in {N['n_panel']} of {NM - 1} open models; {N['n_full']} go to ≥95% commitment. Fabricated panels are about as effective; the irrelevant panel "
          "mostly is not (Llama-3.1-8B: 8% vs 100%). Gemma-2-9B never commits, but its correct DECLINE collapses from 90% to 0% in favour of a search tool that cannot see the future. "
          f"Three further models ({N['resist_names']}) never commit with any panel and mostly ignore even a leaked answer (commitment {N['resist_post']}); Llama-3.2-3B even commits "
          "more with no data (75%) than with any panel (0%). "
          f"Asked directly, models call the unknowable questions unknowable at every level (mean P = {N['ask_unk']} at L2). With the answer shown, the other {N['n_use']} models commit on {N['post_commit']} and "
          f"their directional calls are right {N['post_acc']} of the time (the gate excepted), so they use the leaked price. Yet asked whether the question is knowable, all but "
          f"Llama-3.1-8B still mostly say no (P = {N['post_ask']}; Llama {N['post_ask_llama']}). The words channel is thus largely blind to evidence, not a stable belief that the panel fails to shift."),
    ("table", ["Model", "L0", "L2", "L2′ irrel.", "L2-fab", "answer shown: commit / correct", "decline L0→L2", "know L2: answered / correct", "asked P(unk): unk L2 / know L2 / answer shown"],
     behaviour_table(),
     "Table 1. Commitment (ANSWER) on the 40 unknowable stock questions by evidence level (n = 40 per cell; Wilson 95% CI half-width ≤ ±15 points). 'Answer shown': the panel also reports the realised "
     "close and 'Today' is that date; correct = share of directional calls (PROBABILITY_YES ≠ 50) that match the realised move. Always-NO scores 72.5% on knowable L2 questions. Last column: mean P(unknowable) when asked directly.",
     [1.15, 0.38, 0.38, 0.5, 0.45, 0.8, 0.7, 0.75, 1.05]),
    ("fig", "report/figs/fig1_channels_v4.png", 5.3,
     "Figure 1. Three channels for the 40 unknowable stock questions across evidence levels, with the leaked-answer anchor (yellow). Red: commitment (solid) and decline (dashed). Blue: P(unknowable) "
     "when asked. Green: X-probe position averaged over valid deep layers, scaled so that 1 = unknowable with no data and 0 = knowable with the panel. Purple star: positive control. With the answer "
     "shown, the action flips to ANSWER and the answers are mostly right, but the probe moves only modestly and the words barely move."),

    ("h3", "4.2 The uncalibrated reading: 'overriding'"),
    ("p", f"Both probes separate knowable from unknowable L2 questions (median AUROC ≈ 1.00 over valid layers) and the positive control moves them strongly. Adding the panel moves the unknowable "
          f"question only a little: median deep-layer FI {N['fi_N']} with N and {N['fi_X']} with X (Table 2). Under the pre-registered per-layer rule, {N['ci_O']} of {N['ci_tot']} valid deep layers "
          f"are Overriding, {N['ci_M']} Mixed and {N['ci_F']} Fooled. Fabricated panels behave like real ones inside as well (FI on L2-fab ≈ FI on L2). Read alone, this says "
          "the model keeps its doubt and acts against it. But on X, models with weaker positive controls show lower FI, so the probe's sensitivity needs checking."),
    ("table", ["Model", "valid deep layers X/N", "positive control X/N", "FI panel X/N", "FI fabricated X/N", "FI answer shown X/N", "panel ÷ answer X/N", "layers O/M/F (CI rule)"],
     probe_table(),
     "Table 2. Probes, medians over valid layers in the second half of the network (X = cross-domain, N = cross-fitted stock). FI: 0 = untouched, 1 = moved to the knowable-with-panel position. "
     "'Answer shown' comes from a re-run that adds the anchor items (it reproduces the panel FI closely). 'Panel ÷ answer' is the median per-layer ratio over layers where FI(answer shown) > 0.1. "
     "Last column: Overriding / Mixed / Fooled under the pre-registered per-layer CI rule for the panel.",
     [1.15, 0.6, 0.75, 0.7, 0.7, 0.75, 0.7, 1.05]),

    ("h3", "4.3 The calibration: the probes barely respond to evidence"),
    ("p", f"If a low FI meant 'still represents the question as unknowable', a context that actually makes the question answerable should push FI toward 1. It does not. In the {N['n_use']} models that act on "
          f"the leaked answer, median deep-layer FI is only {N['fipost_X']} (X) and {N['fipost_N']} (N). The answer does move the probe more than the panel does ({N['post_gt']} valid deep layers, "
          f"non-overlapping 95% CIs), but not by much. Measured against this empirical 'fooled' end, the panel moves the probe {N['ratio_X']} (X) and {N['ratio_N']} (N) of the way the real answer does (models with at least five valid layers): "
          "by that yardstick several models look substantially fooled, while Llama-3.1-8B's cross-fitted probe does not respond to the answer at all. Graded leakage confirms the insensitivity: "
          f"from a ±25% range (uninformative) to the exact price, X-probe FI changes by at most {N['graded_spread']} in any model, while behaviour sometimes tracks the information (Appendix C, Table 4). "
          "Matched pairs that differ only in the target date (past vs future) are separated perfectly by the probe, but also by TF-IDF (AUROC ≈ 1.00, because the dates differ), "
          "so they do not remove the lexical confound. The insensitivity does not come from moving 'Today': with the realised close appended and 'Today' unchanged, as in pipeline B, "
          f"X-probe FI is {N['fileak_X']}. Similar format-over-content failures of linear probes are reported by Sahoo et al. (2026), Boxo et al. (2025) and Jayabahu (2026)."),
    ("p", "**What the calibration implies.** The linear 'unknowability' signal, like the model's self-report, mainly encodes the *form* of the question (a future-dated forecast), not whether the "
          "context makes it answerable. A small FI under the panel is therefore not evidence that the model keeps its doubt, and a ratio near 1 is not strong evidence that it is fooled: the "
          "scale's dynamic range is too small. Fooled vs overriding is not identifiable with this signal, and the 'overriding' reading of Section 4.2 does not survive on these probes (their response to evidence is compressed, not absent). Section 4.4 asks whether a different readout does better."),

    ("h3", "4.4 A readout that responds to the calibration: the Jacobian lens"),
    ("p", f"A probe direction is one number per item; the J-lens asks what the whole decision state disposes the model to say. Decoded, the knowable-minus-unknowable change reads as "
          "uncertainty against ease ('uncertain, unsure, unpredictable, unknown' vs 'straightforward, simple, immediately, already, solved'), and leaking the outcome removes "
          "uncertainty ('Unknown, unclear, TBD, unsure' at the bottom; 'correct, confirmed, already' at the top). The panel instead adds a forecasting or analysis frame "
          "('predictions, estimated' in Llama; 'calculated, analysis' in Qwen3-14B). Figure 2 shows the calibration directly. In every model whose leak control works, the leaked "
          f"answer pushes the four doubt words {N['jl_valid_leak']}% of the way down the vocabulary. In four of the six models the panel moves to commit (Llama-3.1-8B, "
          f"Qwen3-14B, Qwen3-8B, Qwen2.5-3B), the panel, real or fabricated, leaves them at {N['jl_commit_panel']}%: the action changes while the readout keeps the doubt, which is what "
          "overriding predicts. Models the panel does not move (Llama-3.3-70B, Qwen2.5-14B, Phi-4) keep them as well. The panel demotes them partly in Qwen3-4B (78%, which commits on "
          "100%) and Qwen2.5-7B (65%, which does not commit), and as far "
          "as the leak in OLMo-2-7B (91% vs 89%); OLMo rarely calls the question unknowable (P = 0.20), but its leak control is the weakest of the passing models and every contrast "
          "pushes its doubt words down, so we read OLMo as fooled only tentatively. For Gemma-2-9B and Mistral-7B the leak itself fails, so the J-lens gives no reading. Three "
          "caveats. The rank readout was chosen post-hoc. On an item score built from the doubt words alone, the leak barely moves the committers "
          f"({N['jl_unc_leak']}), as weak as the probes; only the rank readout and a doubt-minus-forecast score ({N['jl_fi_big']} for the panel vs {N['jl_leak_big']} for the leak, "
          "Appendix Table 5) separate them. And the panel promotes the doubt words well above neutral (10–24% vs 50%), which may reflect a forecasting-topic association rather than kept belief."),
    ("fig", "report/figs/fig5_jlens.png", 5.5,
     "Figure 2. Jacobian-lens calibration (pipeline B). Where the change of the decision-token state puts the doubt words ('uncertain', 'unpredictable', 'unknown', 'unclear'), as % of the way "
     "down the vocabulary, at 70% and 85% depth (fixed in advance). Blue: leaked answer (the calibration: it should demote them). Orange: panel, real and fabricated pooled. Grey: the leak "
     "control fails. Right: the same for the two new domains."),

    ("h3", "4.5 Two more real-data domains, and a 70B model"),
    ("p", f"Rebuilt with every arm on crypto and weather (Appendix Table 6), in the three models tested the J-lens pattern recurs and behaviour replicates on crypto, weakly on weather: Llama-3.1-8B commits on 100% (crypto) and 40% "
          f"(weather) with real panels and as much with fabricated ones; asked, models still call the question unknowable; B's decision-orthogonalised probe gap grows ({N['dom_gap']}); and the "
          f"panel leaves the doubt words at {N['dom_panel']}% while the leak pushes them to {N['dom_leak']}%. Behaviour is domain-dependent: Qwen3-14B commits on 78% of crypto items "
          "but on no weather item, where the panel instead raises its decline probability. **At 70B** (Llama-3.3-70B-Instruct, 4-bit; B), the panel no longer works: "
          f"the model commits on {pc(S70['commit_L2'])} of unknowable items with the real and {pc(S70['commit_fab'])} with the fabricated panel (Llama-3.1-8B: 100%), declines "
          f"{pc(S70['decline_L2'])}, still answers every knowable question, and B's probe position (1 = synthetic unknowable mean) does not move ({S70['proj_unk_L0']:.2f} → {S70['proj_unk_L2']:.2f}). The J-lens is consistent, with a weaker leak control: "
          f"the panel leaves the doubt words {S70['jlens']['doubt']['panel']:.0f}% of the way down while the leak pushes them to {S70['jlens']['doubt']['leak']:.0f}%, and the knowable "
          "direction reads 'straightforward, easy'. We do not attribute this to scale: Llama-3.3 also has newer post-training, Llama-3.2-3B resists too, and frontier models still commit (Aggarwal, 2026)."),

    ("h3", "4.6 Where the panel acts"),
    ("p", f"Patching (Figure 3; {N['n_patch']} models) locates the panel's effect. Replacing the panel run's activations over the question-and-instruction tokens with no-panel activations restores "
          f"≥90% of abstention from {N['patch_suffix']} relative depth onward: by mid-network, the panel's influence has been written into the question tokens. Patching the last token alone "
          f"restores half of it only from {N['patch_last']} depth. Patching only the X component at the last token restores at most {N['patch_x_mid']} up to mid-depth and {N['patch_x_late']} in the "
          "final layers. The decision does read the X direction late: adding one class gap along X at three-quarter depth raises abstain log-odds by "
          f"{N['fd_late_L0']} nats without a panel and {N['fd_late_L2']} with it (mid-depth: {N['fd_mid']}). So the panel does not cut the direction's read-out; it acts mostly through other "
          "features, moved from the data tokens into the question tokens in the middle layers, which the late decision then integrates. Pipeline B's component patching at the decision "
          "token agrees: copying the no-panel state restores the no-panel action (Llama-3.1-8B from layer 16, Qwen3-14B from layer 25), the within-class decline component alone "
          "restores declining (Qwen3-8B 0.60 → 0.00–0.02 P(ANSWER)), and the decision-orthogonalised knowability component alone does nothing in any of the three committers tested."),
    ("fig", "report/figs/fig2_patch.png", 4.7,
     "Figure 3. Activation patching from the no-panel (L0) run into the panel (L2) run of each unknowable question, at the decision token. y = fraction of the L0–L2 gap in abstain log-odds "
     "restored (1 = full abstention restored). Black: all shared question/instruction tokens; red: last token only; green dashed: only the X-direction component at the last token. n = 40 per point."),

    ("h3", "4.7 Steering along the direction, and a prompt-level gate"),
    ("p", "Adding the direction at a valid layer (α = +8, in multiples of the class-mean gap; in the two re-run models this is STEER_REL of the mean residual-stream norm) moves only some models off ANSWER "
          "beyond same-norm random directions (Appendix Table 3). Llama-3.1-8B falls from 100% to 18% commitment, mostly to DECLINE; Qwen2.5-3B falls from 48% to 0%, but to CALL_TOOL, which is no better than "
          "committing since the tool cannot see the future. Knowable questions remain answered, but at lower accuracy (Llama 100% → 75%, close to the 72.5% always-NO baseline; Qwen3-8B 78% → 28%). "
          "PER_MODEL_EXTRA Given Section 4.6 this is expected: the direction is read late, and the panel's effect runs largely elsewhere. A prompt-level gate works better (pipeline B): "
          "the original paper's one-paragraph triage system prompt brings P(DECLINE) on unknowable items with the real or fabricated panel to 0.99–1.00 in Llama-3.1-8B, Qwen3-8B and "
          "Qwen3-14B with answerable items untouched, while a matched-length placebo raises commitment (Llama 0.82 → 0.91). It does not help OLMo-2-7B, which the J-lens tentatively reads as fooled."),
    ("h3", "4.8 Pushback, with a neutral control"),
    ("p", "With the original, knowability-laden wording, one 'Are you sure?' made several models abandon their committed knowable answers (Llama-3.1-8B LLAMA_ORIG, Qwen3-8B QW8_ORIG, Qwen2.5-3B "
          "QW3_ORIG, gate GATE_ORIG). With a **neutral** 'Are you sure?', Llama-3.1-8B abandons LLAMA_NEU and Qwen3-8B QW8_NEU: the effect came from the wording, not the challenge. "
          "Llama-3.2-3B (LL32_ORIG vs LL32_NEU) and Mistral-7B (MIS_ORIG vs MIS_NEU) show the same pattern. The small Qwen2.5-3B models still fold (QW3_NEU, gate GATE_NEU), Qwen2.5-7B folds more under the neutral wording (Q7_ORIG vs Q7_NEU), and Gemma-2-9B starts *committing* on unknowable panel items (0% → GEMMA_NEU). Inside, "
          "the X-probe gap between unknowable and knowable L2 questions shrinks after either wording (median ratio PUSH_RANGE over layers that stay valid at the new position), even where behaviour "
          "does not change. Given Section 4.3, we read this as both prompts now sharing an appended turn, not as a belief update."),

    ("h2", "5. Discussion and Limitations"),
    ("p", "**Implications.** Panels change what agents do far more than the standard measures of what they represent. Those measures, linear probes and the model's own "
          "self-report, respond only weakly to evidence: they track the form of the question and barely respond when context truly answers it. A Jacobian-lens readout of the decision "
          "state responds to the same calibration, and by it the models the panel moves appear to override: the panel adds a reason to act without removing the words of doubt, while a real answer removes "
          "them. OLMo-2-7B may be fooled, tentatively, and two smaller models partly. Four consequences follow. (1) A model's statement or probe reading that 'this is unknowable' is "
          "not evidence of withheld belief unless the readout is calibrated against an answer-revealing context; we recommend that check for any honesty or doubt monitor, as verbal confidence "
          "also fails to drive decisions (Wang et al., 2026). (2) Evals "
          "should score actions against calibrated internal states on matched answerable twins, with fabricated and irrelevant panels as standard arms. (3) The panel's effect is "
          "written into the question tokens mid-network, outside the knowability direction, so fixes belong at the action: a one-paragraph triage prompt removed the commitments in the "
          "overriding models, though not in OLMo-2-7B, which the J-lens tentatively reads as fooled. (4) The SFT gate fixes behaviour bluntly: it calls knowable questions unknowable too, and must be checked on knowable accuracy."),
    ("p", "**Limitations and future work** (details in Appendix A). Thirteen 3–70B models; one main domain plus two replications; several probe choices, the leaked-answer anchor and the "
          "J-lens are post-hoc. Next: head-level path patching from data to question tokens, J-lens and SAE features at frontier scale, and consistency training that ties the action "
          "to a calibrated judgement, checked on knowable accuracy."),
    ("h2", "6. Conclusion"),
    ("p", "Authoritative panels make open-weight agents commit on unknowable questions. Linear probes and the model's own words cannot settle whether they are fooled: both "
          "barely move even when the answer is in front of the model. Calibrated against that answer, a Jacobian-lens readout suggests an answer: the models the panel moves keep their "
          "doubt and act anyway, and one small model may be truly fooled. Before reading a probe or a self-report as an agent's belief, calibrate it against a context that actually answers the question."),

    ("h2", "Code and Data"),
    ("bullets", [
        "Code repository: GITHUB_URL. Pipeline A is in src/ and results/; pipeline B (nine-model runner, leaked-outcome control, component patching, triage, Jacobian lens, crypto and weather domains) is in pipeline_b/, with its own README. Every cached generation and probe score is included, and scripts regenerate each table and figure on a CPU.",
        "Data: the evaluation cases, agentic prompt and SFT recipe are pre-existing work from Aggarwal (2026), https://github.com/Pranav-1100/confidence-calibration-evaluation (MIT), "
        "marked as such in the README. New items (fabricated panels, the positive control, leaked-answer anchors, graded leakage, matched pairs, the ask prompt, pushback variants) are generated by src/fof.py and src/deep.py.",
    ]),
    ("h2", "Author Contributions"),
    ("p", "P.A. authored the original behavioural study, cases, prompt and SFT recipe (pre-existing). S.J. designed and ran pipeline A (probes, controls, leaked-answer calibration, patching, steering, "
          "pushback) and wrote the report. P.A. designed and ran pipeline B (nine-model runner, leaked-outcome control, decision-token component patching, triage prompt, Jacobian lens, crypto and "
          "weather domains) and merged it into the report. Both authors reviewed the manuscript."),
    ("h2", "References"),
    ("refs", None),
    ("pagebreak",),
    ("h2", "Appendix A. Limitations and Dual-Use / Ethical Considerations"),
    ("p", f"**What this does and does not establish.** For thirteen open models of 3–70B parameters, we establish that panels change actions; that linear unknowability probes and the model's "
          "self-report barely respond even when context answers the question; that a Jacobian-lens rank readout does respond, and by it the three models the panel moves keep their doubt "
          "(on three domains) while OLMo-2-7B tentatively does not; and that the panel's effect on the decision is carried at the question tokens mid-network. We do not establish behaviour at frontier "
          "scale, that the J-lens doubt words are the mechanism the model uses, or a deployable fix beyond the triage prompt."),
    ("bullets", [
        "**Scale.** Thirteen open models of 3–70B parameters (one at 70B, in 4-bit) and a gate, greedy decoding, 40 cases per domain (stocks; crypto and weather in three models); n = 40 per cell. Frontier models were tested only behaviourally, in the original paper.",
        "**Jacobian lens.** Post-hoc and from pipeline B only; 64 corpus sequences (32 at 70B; rank readout by finite differences on 16, or 8; the original method uses more), and no null distribution or CI for the rank readout and a finite-difference readout; one four-word doubt set fixed in advance. "
        "The J-lens leak test does not separate evidence from the mere presence of an outcome string (graded leakage was run for the probes only). B's leak keeps 'Today' unchanged, unlike A's anchor; A's probes respond as weakly to both. The leak control fails for Gemma-2-9B and Mistral-7B, so they get no J-lens reading.",
        "**Post-hoc choices.** The pre-registered synthetic probe failed validity; the X and N probes, validity gate, deep-half aggregation, leaked-answer anchor, patching, neutral pushback and "
        "valid-layer steering were added afterwards (Appendix B). Adjacent layers are correlated, so per-layer counts overstate the evidence.",
        "**The anchor is imperfect.** 'Answer shown' keeps the future-tense wording of the question; a probe that reads tense would stay put by design. That is part of the finding (the "
        "representation tracks form), but a calibration that changes knowability while keeping form fixed would need rephrased items, which reintroduce lexical differences.",
        "**One linear direction per probe.** The weak response to evidence is shown for difference-of-means directions; other features (sparse-autoencoder features, nonlinear probes) might track answerability.",
        "**Steering and patching are coarse.** Steering at one strength and one layer per model; patching at the decision token only, without head-level attribution.",
    ]),
    ("p", "**Dual use.** Knowing that packaging moves actions could help someone design panels that push agents into confident calls, for example in automated trading or advice. The original "
          "behavioural paper already demonstrated this publicly; we add only that fabricated and real panels act alike inside. Steering directions that raise commitment need white-box access, "
          "which already allows fine-tuning. We think the defensive value (calibrated monitors, evals that compare actions with internal states, action-level gates) outweighs this."),
    ("p", "**Data and privacy.** No personal data. Stock prices are public market data; fabricated panels are labelled as such in the code. No human subjects. Models ran on rented GPUs; no outputs were deployed."),
    ("h2", "Appendix B. Pre-registration and deviations"),
    ("p", "Written before any model was run (PREREGISTRATION_AND_LOG.md, Step 1): FI decision rule (Overriding if the FI CI's upper bound < 0.25, Fooled if the lower bound > 0.5) at a layer selected on "
          "synthetic validation data; credences Overriding 55% / Fooled 25% / Mixed 20%; the probe beats stated confidence as a monitor (70%); the probe beats TF-IDF on de-confounded transfer (75%). "
          "Deviations: (1) the layer search was restricted to 25–75% depth after the smoke test picked layer 1; (2) the know/L0 positive control was added after the TF-IDF result, before any full run; "
          "(3) after the synthetic probe failed transfer, the X and N probes and the validity gate were added (post-hoc), and the deep-half median rule was fixed before the all-layer scan; (4) the "
          "steering layer (n_layers//2) and α grid were fixed before the steering runs; (5) matched random-direction controls were added after the first steering results. **Added after an external "
          "review, after all of the above:** (6) the leaked-answer anchor and graded leakage; (7) the neutral pushback; (8) patching and read-out gain; (9) steering at the first valid layer where "
          "n_layers//2 failed the gate; (10) three more models (Qwen2.5-7B, Mistral-7B-v0.3, Llama-3.2-3B), run with the unchanged pipeline; (11) merging pipeline B, pre-registered separately (pipeline_b/PREREGISTRATION.md, hashed; addenda A and B before its main results, C post-hoc), whose Jacobian lens and crypto/weather domains were added on the last day, after all other results. Outcomes: the pre-registered Overriding prediction is "
          "supported by the uncalibrated rule but not by the calibration, which shows the rule cannot distinguish the hypotheses; probe beats stated confidence (supported in most models); probe "
          "beats TF-IDF on transfer (mixed: it beats full-prompt TF-IDF at 0.55 but not question-only TF-IDF at 0.91–0.99)."),
    ("h2", "Appendix C. Additional results"),
    ("table", ["Model", "layer", "commit unk+panel: base → +dir (random)", "commit unk+fabricated: base → +dir (random)", "knowable answered: +dir (random)", "unk, no data: base → −dir (random)"],
     steer_table(),
     "Table 3. Steering with matched controls (n = 40 per cell; random = mean of three same-norm random directions; α = ±8). Base = the unsteered run in the same batch setup (batch-dependent bf16 "
     "numerics shift some greedy decisions by a few items). Layer: n_layers//2 if the X direction is valid there, else the first valid layer above it. Models that never commit with the panel are omitted.",
     [1.15, 0.4, 1.25, 1.25, 0.95, 1.15]),

    ("table", ["Model", "FI panel", "±25% range", "±8%", "±3%", "±1%", "exact", "P(ANSWER): ±25% → exact"],
     leak_table(),
     "Table 4. Graded leakage (X probe, median over valid deep layers; deep.py). The panel reports the target-date close as a range of half-width w × price ('Today' = target date). The probe barely "
     "changes with the information content, while P(ANSWER) sometimes does.",
     [1.25, 0.6, 0.65, 0.5, 0.5, 0.5, 0.5, 1.2]),
    ("table", ["Model", "commits with panel", "doubt words, % down: panel / leak", "FI doubt−forecast: panel / leak", "FI doubt only: panel / leak", "reading"],
     jl_table(),
     "Table 5. Jacobian lens, twelve models (decision token; the 70B model at 70% and 85% depth as well). Doubt words = mean position of 'unpredictable', 'uncertain', 'unknown', 'unclear' in the decoded change, % of the "
     "way down the vocabulary (0 = promoted, 100 = demoted), 70% and 85% depth. FI: fooling index of an item score built from 12 doubt and 12 forecast words (median over deep layers); the "
     "doubt-minus-forecast score partly tracks the decision; the doubt-only score barely responds to the leak; the rank readout (chosen post-hoc) is primary. "
     "Commits with panel: greedy commitment on unknowable items with the real panel (B; (A) = pipeline A; † OLMo: forced-choice P(ANSWER), it ignores the output format).",
     [1.2, 0.75, 1.0, 1.05, 1.0, 1.5]),
    ("table", ["Domain", "Model", "commit: no data → panel (fabricated)", "asked P(unk)", "probe gap, thin → panel", "doubt words: panel / leak"],
     dom_table(),
     "Table 6. New real-data domains (pipeline B; 40 cases each; 2026 data). Probe gap: change in B's decision-orthogonalised unknowable-minus-answerable gap (positive = not fooled).",
     [0.7, 1.1, 1.5, 0.75, 1.0, 1.0]),
    ("fig", "report/figs/fig2_depth.png", 5.6,
     "Figure 4. Fooling index (panel) at every layer for the X (green) and N (purple) probes; filled points pass the validity gate. Green band < 0.25, red band > 0.5; clipped to [−0.5, 1.6]. "
     "Early layers often sit in the 'fooled' zone; Section 4.3 shows the scale itself is compressed."),
    ("fig", "report/figs/fig4_push.png", 6.0,
     "Figure 5. Commitment before and after the original (knowability-laden) 'Are you sure?' for unknowable and knowable L2 questions (n = 40 each)."),
    ("p", "**Monitors.** Among items an agent chose to ANSWER (original seven models), flagging the unknowable ones works with the X probe (AUROC 1.00 for most models) and almost as well by simply asking the model (0.96–1.00); stated "
          "confidence does worse (0.48–0.94). On these lexically distinct questions TF-IDF on the question alone also scores 1.00, so these monitors detect question type. The leaked-answer "
          "result shows they would flag an answerable question as unknowable just as confidently. Our pre-registered prediction that the probe would beat asking is not supported."),
    ("p", "**Synthetic probe.** The pre-registered probe (layer chosen on synthetic validation data) reached validation AUROC 0.99–1.00 but stock-L2 AUROC as low as 0.22–0.64 in several models, "
          "so its fooling indices are uninterpretable. Text baselines: TF-IDF on the question alone separates knowable from unknowable with AUROC 1.00 on stock L2 and 0.91–0.99 on transfer. "
          "**Base vs instruct** (raw prompts, deep.py): base Qwen2.5-3B and Llama-3.1-8B do not follow the decision format and no layer passes the validity gate, so the comparison is inconclusive. "
          "The full steering sweep is in results/v2-*/xsteer.json."),
]

REFS = [
    "Aggarwal, P. (2026). Calibrated Enough to Know, Not Calibrated to Act: Fabricated Evidence Makes LLM Agents Commit to the Unknowable. arXiv:2608.27167.",
    "Arditi, A. et al. (2024). Refusal in Language Models Is Mediated by a Single Direction. arXiv:2406.11717.",
    "Azaria, A. & Mitchell, T. (2023). The Internal State of an LLM Knows When It's Lying. arXiv:2304.13734.",
    "Du, Y. & Hu, X. (2026). Recognition-Refusal Misalignment in LLMs: Why Models Answer Structurally Unanswerable Questions. arXiv:2608.29109.",
    "Fanous, A. et al. (2025). SycEval: Evaluating LLM Sycophancy. arXiv:2502.08177.",
    "Ferrando, J., Obeso, O., Rajamanoharan, S. & Nanda, N. (2024). Do I Know This Entity? Knowledge Awareness and Hallucinations in Language Models. arXiv:2411.14257.",
    "Goldowsky-Dill, N., Chughtai, B., Heimersheim, S. & Hobbhahn, M. (2025). Detecting Strategic Deception Using Linear Probes. arXiv:2502.03407.",
    "Boxo, G., Neelappa, A. & Raval, S. (2025). Linear Probes Rely on Textual Evidence: Results from Leakage Mitigation Studies in Language Models. arXiv:2509.21344.",
    "Gurnee, W., Sofroniew, N. et al. (2026). Verbalizable Representations Form a Global Workspace in Language Models. arXiv:2607.15495.",
    "Halawi, D., Denain, J.-S. & Steinhardt, J. (2023). Overthinking the Truth: Understanding how Language Models Process False Demonstrations. arXiv:2307.09476.",
    "Jayabahu, D. (2026). The Truth Was Never Gone: Perfect Aliasing in Compliant-Context Truth Probes. arXiv:2609.10739.",
    "Joswin, E., Medicherla, S., Mammen, P. M. et al. (2026). A Mechanistic View of Authority Hierarchy in LLM Sycophancy. arXiv:2607.00415.",
    "Kadavath, S. et al. (2022). Language Models (Mostly) Know What They Know. arXiv:2207.05221.",
    "Kalai, A. T. et al. (2025). Why Language Models Hallucinate. arXiv:2509.04664.",
    "Kirichenko, P. et al. (2025). AbstentionBench: Reasoning LLMs Fail on Unanswerable Questions. arXiv:2506.09038.",
    "Laban, P. et al. (2023). Are You Sure? Challenging LLMs Leads to Performance Drops in The FlipFlop Experiment. arXiv:2311.08596.",
    "Lavi, M. J., Milo, T. & Geva, M. (2025). Detecting (Un)answerability in Large Language Models with Linear Directions. arXiv:2509.22449.",
    "Liu, X. et al. (2026). AgentAbstain: Do LLM Agents Know When Not to Act? arXiv:2607.10059.",
    "Levinstein, B. A. & Herrmann, D. A. (2023). Still No Lie Detector for Language Models: Probing Empirical and Conceptual Roadblocks. arXiv:2307.00175.",
    "Marks, S. & Tegmark, M. (2023). The Geometry of Truth: Emergent Linear Structure in LLM Representations of True/False Datasets. arXiv:2310.06824.",
    "Orgad, H. et al. (2024). LLMs Know More Than They Show: On the Intrinsic Representation of LLM Hallucinations. arXiv:2410.02707.",
    "Ren, R. et al. (2025). The MASK Benchmark: Disentangling Honesty From Accuracy in AI Systems. arXiv:2503.03750.",
    "Rimsky, N. et al. (2023). Steering Llama 2 via Contrastive Activation Addition. arXiv:2312.06681.",
    "Sahoo, S. et al. (2026). Linear Probes Detect Task Format, Not Reasoning Mode in Language Model Hidden States. arXiv:2606.02907.",
    "Slobodkin, A. et al. (2023). The Curious Case of Hallucinatory (Un)answerability: Finding Truths in the Hidden States of Over-Confident Large Language Models. arXiv:2310.11877.",
    "Wang, K. et al. (2025). When Truth Is Overridden: Uncovering the Internal Origins of Sycophancy in Large Language Models. arXiv:2508.02087.",
    "Wang, J., Zhou, Y., Devic, S. & Fu, D. (2026). Are LLM Decisions Faithful to Verbal Confidence? arXiv:2601.07767.",
    "Zhan, Z. et al. (2026). How Adversarial Environments Mislead Agentic AI? arXiv:2604.18874.",
    "Zou, A. et al. (2023). Representation Engineering: A Top-Down Approach to AI Transparency. arXiv:2310.01405.",
]

# ---------- placeholders filled from results ----------
def _sub(s):
    rep = {"LLAMA_ORIG": push_ab("llama31-8b", "orig"), "QW8_ORIG": push_ab("qwen3-8b", "orig"), "QW3_ORIG": push_ab("qwen25-3b", "orig"), "GATE_ORIG": push_ab("gate-3b", "orig"),
           "LLAMA_NEU": push_ab("llama31-8b", "neutral"), "LL32_ORIG": push_ab("llama32-3b", "orig"), "LL32_NEU": push_ab("llama32-3b", "neutral"),
           "MIS_ORIG": push_ab("mistral-7b", "orig"), "MIS_NEU": push_ab("mistral-7b", "neutral"), "Q7_ORIG": push_ab("qwen25-7b", "orig"), "Q7_NEU": push_ab("qwen25-7b", "neutral"), "QW8_NEU": push_ab("qwen3-8b", "neutral"), "QW3_NEU": push_ab("qwen25-3b", "neutral"), "GATE_NEU": push_ab("gate-3b", "neutral")}
    g = V4m.get("gemma2-9b", {}).get("push2", {}).get("neutral")
    rep["GEMMA_NEU"] = pc(g["behaviour"]["unk/L2"]["commit_after"]) if g else "–"
    rr = [V4m[t]["push2"][nm]["gap_ratio_deep"] for t in ORDER if t != "gate-3b" and "push2" in V4m[t] for nm in ("orig", "neutral") if V4m[t]["push2"][nm]["gap_ratio_deep"] is not None]
    rep["PUSH_RANGE"] = rng(rr)
    metas = [f"results/{d}/xsteer2_meta.json" for d in os.listdir("results") if os.path.exists(f"results/{d}/xsteer2_meta.json")]
    rel = [m["gap_norm"] * 8 / m["resid_norm"] for m in (json.load(open(f)) for f in metas)]
    rep["STEER_REL"] = rng(rel, pc) if rel else "a fraction"
    for k, v in rep.items(): s = s.replace(k, v)
    return s
BODY = [tuple(_sub(x) if isinstance(x, str) else x for x in blk) for blk in BODY]
EXTRA_TEXT = steer_extra()
