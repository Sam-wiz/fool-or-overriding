# Fooled or Overriding?

Code and results for an Apart Research **AI x Epistemics Research Sprint** project (13–16 Nov 2026). Authors: Samrudh Jain and Pranav Aggarwal.

**Result in one line.** Panels make agents commit, but the internal unknowability signal and the model's own self-report barely move even when the answer is placed in the panel, so the probe cannot separate *fooled* from *overriding*. Patching shows the panel acts through the question tokens mid-network, largely outside that signal.

**Question.** An authoritative-looking indicator panel makes LLM agents commit to answers on questions nobody can know yet. When that happens, is the model *fooled*, meaning its internal representation that the question is unknowable disappears? Or is it *overriding*, meaning it still represents the question as unknowable and commits anyway?

## What is new and what was pre-existing

| Pre-existing (before the sprint) | New during the sprint (13–16 Nov 2026) |
|---|---|
| The evaluation cases, the agentic prompt and the decision parser from Aggarwal (2026), arXiv:2608.27167. The public release is at https://github.com/Pranav-1100/confidence-calibration-evaluation (MIT). The files are copied unchanged into `data/`. | `src/fof.py` collects activations, generates answers, trains probes, and runs the steering, pushback and layer-scan experiments. |
| The SFT-gate training recipe, `src/PREEXISTING_upstream_sft2.py`, copied verbatim from that repository. | `src/train_gate.py` wraps that recipe and retrains it in bf16 on an A100. |
| | Post-review: `src/deep.py` (graded leakage, matched pairs, read-out gain, activation patching, base vs instruct), `src/analyze_v4.py`, `src/review_fixes.py`, `src/make_figs_v4.py`, `src/modal_deep.py`, `src/modal_new.py`; the leaked-answer anchor (`--anchor`), neutral pushback (`push2`) and valid-layer steering (`--steer_layer`) in `fof.py`. |
| | `src/analyze.py`, `src/analyze_v2.py`, `src/indomain.py`, `src/baselines.py`, `src/make_figs*.py`, `src/modal_*.py` and `src/build_report.py`. |
| | The fabricated NSE panels (`fabricate()` in `fof.py`), the know/L0 positive control, the "just ask the model" and belief prompts, and the one-turn pushback. |
| | Everything under `results/` and `report/`. |

## Reproduce

```bash
# GPU (one A100 per model; 80GB for Qwen3-14B; about 10-15 min each)
python src/fof.py --model unsloth/Meta-Llama-3.1-8B-Instruct --tag v2-llama31-8b --phases act,gen,probe,nx,xsteer,push
# gate pole: python src/train_gate.py /tmp/gate data && python src/fof.py --model Qwen/Qwen2.5-3B-Instruct --adapter /tmp/gate ...
# CPU analysis
python src/analyze.py results/v2-*      # behaviour, synthetic-probe channels, monitor
python src/analyze_v2.py results/v2-*   # layer scan verdicts, steering, pushback
python src/baselines.py                 # TF-IDF text baselines
python src/extra_stats.py results/v2-*   # monitor, item-level, stated-probability stats
python src/steer_v3.py results/v3-* results/v2-qwen3-14b   # matched random-direction steering controls
python src/tables.py                    # every number quoted in the report -> results/report_numbers.json
python src/make_figs_v2.py results/v2-*
# post-review (GPU): leaked-answer anchor + neutral pushback, then deep.py
python src/fof.py --model <m> --tag v4-<t> --anchor --phases act,gennew,nx,push2 --prev results/v2-<t>/rows.json
python src/deep.py --model <m> --tag <t> --tests act,grad,patch
python src/fof.py --model <m> --tag v5-<t> --phases act,xsteer2 --steer_layer 21   # only where n_layers//2 fails the gate
# post-review (CPU)
python src/review_fixes.py && python src/analyze_v4.py && STEER_OUT=results/steer_v5_raw.json python src/steer_v3.py results/v5-*
python src/make_figs_v4.py
python src/build_report.py              # report/out/report.docx (official template); PDF via LibreOffice
```

## Results layout

- `results/v2-<model>/`: the main runs (10 models). Files: `rows.json` (every item: generation, decision, probe scores, ask-the-model score), `layerscan.json` (cross-domain and cross-fitted probes at every layer), `xsteer.json`/`xsteer2.json` (steering), `push.json` (pushback).
- `results/v3-<model>/xsteer2.json`: steering at α = ±8 with three same-norm random-direction controls.
- `results/v4-<model>/`: re-run with the leaked-answer anchor items (`layerscan.json`, `rows.json`) and original vs neutral pushback read at every layer (`push2.json`).
- `results/v5-<model>/`: steering at the first valid layer (Qwen3-14B, gate).
- `results/deep-<model>/summary.json`: graded leakage, matched pairs, read-out gain (T2) and activation patching (T3); `*-raw` = base vs instruct with raw prompts.
- `results/v4_summary.json`: everything the revised report quotes from these runs.
- `results/<model>/` without a prefix: the first pass. It used the pre-registered synthetic probe and steering along the synthetic direction, and is superseded by v2 but kept for transparency.

The decision is parsed with the release's semantic parser. Two fixes were added and applied to every cell: placeholder brackets are stripped, because models write `DECISION: <ANSWER>`, and a bare decision label opening the response is accepted when the `DECISION:` prefix is missing.

## Data notes

- NSE cases are the 40 post-cutoff Indian equities from the upstream release. Unknowable questions ask about the close 10 trading days ahead; knowable questions ask about the past 10 days, using only the data shown.
- Panel levels are L0 (none), L1 (thin), L2 (the full indicator panel), L2′ (an irrelevant stock's panel, dates rewritten) and L2-fab (every indicator invented; this arm is new).
- `results/*/rows.json` holds every generation, parsed decision, probe score and logit read-out, so all numbers can be recomputed on a CPU.
