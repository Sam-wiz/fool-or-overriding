"""Table 1 for the report from main_res/summary.json (+ verdict on the decision-free axis when available)."""
import json, sys
S = json.load(open(sys.argv[1] if len(sys.argv) > 1 else "main_res/summary.json"))
order = ["Qwen3-14B", "Meta-Llama-3.1-8B-Instruct", "Qwen3-8B", "OLMo-2-1124-7B-Instruct", "Qwen2.5-14B-Instruct",
         "phi-4", "mistral-7b-instruct-v0.3", "Qwen2.5-7B-Instruct", "gemma-2-9b-it"]
short = {"Meta-Llama-3.1-8B-Instruct": "Llama-3.1-8B", "OLMo-2-1124-7B-Instruct": "OLMo-2-7B", "Qwen2.5-14B-Instruct": "Qwen2.5-14B",
         "mistral-7b-instruct-v0.3": "Mistral-7B-v0.3", "Qwen2.5-7B-Instruct": "Qwen2.5-7B", "gemma-2-9b-it": "Gemma-2-9B", "phi-4": "Phi-4"}


def row(s, arm, lvl):
    return next(t for t in s["table"] if t["arm"] == arm and t["level"] == lvl)


def btype(s):
    a0, a2 = row(s, "unk", "L0"), row(s, "unk", "L2")
    if a2["fc_answer"] - a0["fc_answer"] >= 0.10:
        return "commits"
    if a2["gen_decline"] >= 0.9:
        return "resists"
    if a0["fc_decline"] - a2["fc_decline"] >= 0.10 and a2["fc_tool"] > a2["fc_answer"]:
        return "decline -> tool call"
    if a0["fc_tool"] >= 0.9 and a2["fc_tool"] >= 0.9:
        return "always tool call"
    return "other"


def verdict(s):
    ch = s["gapchange_zperp_L1L2"] if s["gapchange_zperp_L1L2"][0] == s["gapchange_zperp_L1L2"][0] else s["gapchange_z_L1L2"]
    g1 = s["gap_zperp"]["L1"][0] if s["gapchange_zperp_L1L2"][0] == s["gapchange_zperp_L1L2"][0] else s["gap_z"]["L1"][0]
    if ch[2] < 0 and ch[0] < -0.5 * abs(g1):
        return "FOOLED", ch, g1
    if ch[1] <= 0 <= ch[2] or ch[1] > 0:
        return "INTACT", ch, g1
    return "PARTIAL", ch, g1


lines = ["| Model | Behaviour under panel | P(ANSWER) none -> real (fabricated) | P(DECLINE) none -> real | Asked P(IRRED.), real panel | Inside: unk-ans gap change, thin -> real | Inside verdict |",
         "|---|---|---|---|---|---|---|"]
by = {s["model"].split("/")[-1]: s for s in S}
for m in order:
    if m not in by: continue
    s = by[m]
    a0, a2, af = row(s, "unk", "L0"), row(s, "unk", "L2"), row(s, "unk", "L2fab")
    v, ch, g1 = verdict(s)
    rel = ch[0] / abs(g1) if g1 else float("nan")
    note = "" if s["gapchange_zperp_L1L2"][0] == s["gapchange_zperp_L1L2"][0] else " (u)"
    lines.append(f"| {short.get(m, m)} | {btype(s)} | {a0['fc_answer']:.2f} -> {a2['fc_answer']:.2f} ({af['fc_answer']:.2f}) | "
                 f"{a0['fc_decline']:.2f} -> {a2['fc_decline']:.2f} | {a2['ask_p3']:.2f} | {rel*100:+.0f}% [{ch[1]/abs(g1)*100:+.0f}, {ch[2]/abs(g1)*100:+.0f}]{note} | {v if btype(s) not in ("always tool call",) else "n/a (no change)"} |")
print("\n".join(lines))
open("report/table1.md", "w").write("\n".join(lines) + "\n")
