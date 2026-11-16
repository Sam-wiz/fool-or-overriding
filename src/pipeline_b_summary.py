"""Collect every pipeline-B number the merged report quotes into results/pipeline_b_summary.json (CPU only).
Sources: pipeline_b/results/{jlens,jlens_all11} (Jacobian-lens readouts, 11 models), pipeline_b/results/{crypto,weather}
(new real-data domains: behaviour, asked classification, decision-orthogonalised probe gap, J-lens).
usage: python src/pipeline_b_summary.py"""
import json, os, re, numpy as np

B = "pipeline_b/results"
VOC = {"Meta_Llama": 128256, "Llama_3_3": 128256, "Qwen": 151936, "OLMo": 100352, "phi_4": 100352, "gemma": 256000, "mistral": 32768}
DOUBT = (" unpredictable", " uncertain", " unknown", " unclear")
NICE = {"Meta_Llama_3_1_8B_Instruct": "Llama-3.1-8B", "Qwen3_14B": "Qwen3-14B", "Qwen3_8B": "Qwen3-8B", "Qwen3_4B": "Qwen3-4B",
        "Qwen2_5_14B_Instruct": "Qwen2.5-14B", "Qwen2_5_7B_Instruct": "Qwen2.5-7B", "Qwen2_5_3B_Instruct": "Qwen2.5-3B",
        "OLMo_2_1124_7B_Instruct": "OLMo-2-7B", "phi_4": "Phi-4", "gemma_2_9b_it": "Gemma-2-9B", "mistral_7b_instruct_v0_3": "Mistral-7B-v0.3",
        "Llama_3_3_70B_Instruct_bnb_4bit": "Llama-3.3-70B (4-bit)"}


def voc(t):
    return next(v for k, v in VOC.items() if t.startswith(k))


def doubt_pct(d, t):
    """mean position of the four doubt words in the decoded panel (real+fabricated) and leak difference vectors at the
    pre-fixed 70% and 85% depth layers, as % of the way down the vocabulary (0 = promoted to the top, 100 = bottom)."""
    r = json.load(open(f"{d}/{t}.json")); n = voc(t); Ls = r["fd_layers"][2:]
    pan = [100 * r["ranked"][f"{c}@L{L}"]["concept_rank"][w] / n for L in Ls for c in ("panel(L2-L0)", "fabricated(L2fab-L0)") for w in DOUBT]
    lk = [100 * r["ranked"][f"{c}@L{L}"]["concept_rank"][w] / n for L in Ls for c in ("leak(leak-L2)",) for w in DOUBT]
    kn = [100 * r["ranked"][f"{c}@L{L}"]["concept_rank"][w] / n for L in Ls for c in ("knowable-unknowable(L2)",) for w in DOUBT]
    return dict(panel=float(np.mean(pan)), panel_max=float(np.max(pan)), leak=float(np.mean(lk)), leak_min=float(np.min(lk)),
                knowable=float(np.mean(kn)), layers=Ls, n_layers=r["n_layers"])


def jl_block(d):
    S = json.load(open(f"{d}/jlens_summary.json")); U = json.load(open(f"{d}/jlens_summary_unkonly.json"))
    out = {}
    for t in S:
        j, u = S[t]["js_dec"], U[t]["js_dec"]
        out[NICE.get(t, t)] = dict(fi_contrast=j["fi_med"], fi_contrast_ci=j["ci"], fi_contrast_fab=j["fi_fab"], leak_contrast=j["leak_fi"],
                                   fi_unc=u["fi_med"], leak_unc=u["leak_fi"], logit_fi_contrast=S[t]["ll_dec"]["fi_med"],
                                   doubt=doubt_pct(d, t))
    return out


out = {"jlens": {}, "domains": {}}
for d in (f"{B}/jlens", f"{B}/jlens_all11"):
    out["jlens"].update(jl_block(d))
for dom in ("crypto", "weather"):
    out["domains"][dom] = {}
    jl = jl_block(f"{B}/{dom}/jlens")
    rep = open(f"{B}/{dom}/REPORT.md").read()
    for t in ("Meta_Llama_3_1_8B_Instruct", "Qwen3_14B", "Qwen3_8B"):
        rows = json.load(open(f"{B}/{dom}/{t}.json"))["rows"]
        g = lambda l: float(np.mean([x["gen_decision"] == "ANSWER" for x in rows if x["arm"] == "unk" and x["level"] == l]))
        dec = lambda l: float(np.mean([x["p_decline"] for x in rows if x["arm"] == "unk" and x["level"] == l]))
        sec = rep.split(f"## ")[[i for i, s in enumerate(rep.split("## ")) if s.startswith(("unsloth/" if "Llama" in t else "Qwen/") + NICE[t].replace("Llama-3.1-8B", "Meta-Llama-3.1-8B-Instruct"))][0]]
        m = re.search(r"gap change zperp L1->L2 ([-\d.]+) \[([-\d.]+), ([-\d.]+)\] \(gap L1 ([-\d.]+)\)", sec)
        ch, lo, hi, gap = (float(x) for x in m.groups())
        out["domains"][dom][NICE[t]] = dict(commit_L0=g("L0"), commit_L2=g("L2"), commit_fab=g("L2fab"), commit_irr=g("L2irr"),
                                            pdecline_L0=dec("L0"), pdecline_L2=dec("L2"),
                                            ask_unk_L2=float(np.mean([x["ask_p3"] for x in rows if x["arm"] == "unk" and x["level"] == "L2"])),
                                            gap_change_rel=ch / gap, gap_change_ci_rel=[lo / gap, hi / gap], jlens=jl[NICE[t]])
# scale check: Llama-3.3-70B-Instruct (bitsandbytes 4-bit), stock items without the irrelevant arm
t70 = "Llama_3_3_70B_Instruct_bnb_4bit"
rows = json.load(open(f"{B}/scale_70b/{t70}.json"))["rows"]
g = lambda a, l, k: float(np.mean([x["gen_decision"] == k for x in rows if x["arm"] == a and x["level"] == l]))
out["scale70b"] = dict(commit_L0=g("unk", "L0", "ANSWER"), commit_L2=g("unk", "L2", "ANSWER"), commit_fab=g("unk", "L2fab", "ANSWER"),
                       decline_L2=g("unk", "L2", "DECLINE"), know_answer_L2=g("ans", "L2", "ANSWER"),
                       ask_unk_L2=float(np.mean([x["ask_p3"] for x in rows if x["arm"] == "unk" and x["level"] == "L2"])),
                       proj_unk_L0=float(np.mean([x["proj"] for x in rows if x["arm"] == "unk" and x["level"] == "L0"])),
                       proj_unk_L2=float(np.mean([x["proj"] for x in rows if x["arm"] == "unk" and x["level"] == "L2"])),
                       jlens=jl_block(f"{B}/scale_70b/jlens")["Llama-3.3-70B (4-bit)"])
os.makedirs("results", exist_ok=True)
json.dump(out, open("results/pipeline_b_summary.json", "w"), indent=1)
print("wrote results/pipeline_b_summary.json:", len(out["jlens"]), "J-lens models;",
      {k: list(v) for k, v in out["domains"].items()})
