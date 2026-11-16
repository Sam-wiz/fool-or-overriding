# Not Fooled, Decoupled

Code and data for the Apart Research AI x Epistemics sprint (Nov 2026, Track 1) report
"Not Fooled, Decoupled: an authoritative data panel changes what open-weight LLMs do on unknowable questions, not
what they represent".

## What is pre-existing vs built during the sprint

| Item | Status |
|---|---|
| 40 post-cutoff NSE cases, evidence panels, sealed outcomes (`knowability_postcutoff.json`) | Pre-existing, from arXiv:2608.27167 |
| Natural agentic prompt text and decision parser | Pre-existing (paper), ported verbatim to Python here |
| Triage and placebo system prompts | Pre-existing (paper), used verbatim |
| Synthetic knowability items (`v3_cases.json`) and crypto/sports/weather transfer set (`v3_transfer_deconf.json`) | Pre-existing, from the author's earlier gate-training work |
| `build_data.py` (answerable twin arm, fabricated and irrelevant panels in this format, leaked-outcome control) | Sprint |
| `fo_run.py` (three-channel runner: forced-choice action, asked classification, residual-stream probe, steering) | Sprint |
| `fo_phase2.py` (activation patching, decision-token steering, ask-after-acting, triage vs placebo, logit lens) | Sprint |
| `analyze.py`, `make_figs.py`, `text_baseline.py` | Sprint |
| `fo_jlens.py`, `jlens_analyze.py` (Jacobian-lens readout of the decision state, after Gurnee et al. 2026) | Sprint (last day, post-hoc) |
| `PREREGISTRATION.md` (+ addenda A and B, hashes in `PREREGISTRATION.sha256`) | Sprint, written before main results |

## Reproduce

```bash
python build_data.py                       # -> fo_data.json (1,676 prompts); OUTNAME=fo_data2.json adds the leak control
MODELS=unsloth/Meta-Llama-3.1-8B-Instruct DATA=fo_data.json OUT=out python fo_run.py      # one A100, ~13 min per 8B model
MODELS=... DATA=fo_data2.json MAIN=out OUT=out_p2 python fo_phase2.py
python analyze.py out ; python make_figs.py out ; python text_baseline.py
MODELS=... DATA=fo_data2.json OUT=jl python fo_jlens.py ; python jlens_analyze.py jl out   # J-lens, ~3 min per model
```
Models used are all public, ungated Hugging Face checkpoints (unsloth mirrors for Llama, Gemma and Mistral).
Every per-item output (forced-choice probabilities, probe scores, generations) is in the per-model JSON files.

## Layout

- `code/` runners and analysis (see table above). `SRC_ROOT` points `build_data.py` at the folder holding the source sets.
- `data/fo_data.json` all prompts for the main run (1,676); `fo_data2.json` adds the leaked-outcome control (40);
  `fo_data_t2.json` / `fo_data_t3.json` are the paraphrased-template robustness sets; `text_baseline.json` the TF-IDF control.
- `results/main/` per-model outputs (`<model>.json`: every item's forced-choice action, asked classification, probe scores,
  generation, and steering) and chosen-layer activations (`<model>_hid.npz`); `ANALYSIS.md` is the full analysis printout.
- `results/phase2/` patching, decision-token steering, ask-after-acting, triage vs placebo, logit lens.
- `results/phase3/` component-wise patching (decline vs decision-free knowability vs random).
- `results/template2/` paraphrased-template replication (Llama, Qwen3-8B, Qwen3-14B).
- `results/template3/` paraphrased wording with the original option order (Qwen3-8B, Qwen3-14B): isolates wording vs order.
- `results/jlens/` J-lens vectors' item scores (`*_scores.npz`), full-vocabulary readouts of condition differences (`*.json`),
  `JLENS_ANALYSIS.md` (uncertainty-minus-commitment score) and `JLENS_ANALYSIS_unkonly.md` (uncertainty words only).
- `report/` pipeline B's standalone report; `report_merged/` the joint report with pipeline A (Jain & Aggarwal).
- `PREREGISTRATION.md` with addenda A (smoke), B (before main results) and C (post-hoc), hashes in `PREREGISTRATION.sha256`;
  `PREREGISTRATION_frozen_0147.md` is the untouched original.
