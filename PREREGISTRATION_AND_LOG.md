# Apart AI x Epistemics sprint — "Fooled or Overriding?" working notes (16 Nov 2026; section order = chronological order; clock times were not recorded reliably and are omitted)
Deadline: Nov 16 17:29 IST (Nov 15 23:59 AoE). Template: report/template.docx (Google Doc copy link in sprint page).
Upstream (pre-existing, public, MIT): upstream/confidence-calibration-evaluation = Aggarwal 2026 arXiv:2608.27167. Data, agentic prompt, parser reused.
New sprint work: src/fof.py and everything in results/, report/.

## Key related work to differentiate (from research agent, arXiv-verified)
- Lavi, Milo, Geva 2025 arXiv:2509.22449 — unanswerability linear direction, steers abstention. MOST important to differentiate.
- Du & Hu 2026 arXiv:2608.29109 — recognition-refusal misalignment; recognition dir ~orthogonal to refusal.
- Joswin et al 2026 arXiv:2607.00415 — mechanistic authority hierarchy in sycophancy (late-layer erasure).
- Slobodkin 2023 arXiv:2310.11877; Orgad 2024 arXiv:2410.02707; Kadavath 2022 arXiv:2207.05221; Ferrando 2024 arXiv:2411.14257
- Goldowsky-Dill 2025 arXiv:2502.03407; Azaria&Mitchell 2304.13734; Marks&Tegmark 2310.06824; Zou RepE 2310.01405; Arditi refusal dir 2406.11717
- Halawi Overthinking the Truth 2307.09476; Wang 2508.02087 (sycophancy internals); Rimsky CAA 2312.06681; Laban FlipFlop 2311.08596
- Liu 2508.18760 err knowingly; Kirichenko AbstentionBench 2506.09038; Kalai 2509.04664; MASK 2503.03750; Wagner two axes 2607.08456
- AdeOlu LessWrong 2026 abstention geometry (not peer reviewed)
Novelty claim: three-channel dissociation (probe/words/action) under authoritative/fabricated evidence + pushback; NOT existence of direction.

## Winner patterns
Closest template: "Readable but Not Causal" (Digital Minds 1st): probe + causal intervention, random-dir controls, lexical baselines, held-out families.
Judges penalise: single model family, no CIs/significance, missing figures, n=3 overclaiming. Reward: preregistered thresholds, honest negatives, confounds appendix.

## Step 1 — Pre-registered decision rule (written before any model was run)
Fooling index FI = (s_unk,L0 - s_unk,L2) / (s_unk,L0 - s_know,L2), s = probe logit at selected layer (selected on synthetic val only).
Overriding: commitment rises L0->L2 (>=15pp) and FI 95% bootstrap CI upper < 0.25.  Fooled: FI lower CI > 0.5.  Else Mixed.
Secondary: AUROC(probe) committed-vs-declined within L2 unk.
Credences: Overriding 55 / Fooled 25 / Mixed 20; probe beats stated conf as monitor 70%; probe beats TF-IDF on deconf transfer 75%.

## Step 2 — Design changes after the 10-case smoke test, before any full run
- Smoke (Qwen3-4B, 10 cases): L0 -> CALL_TOOL 10/10; L2 -> ANSWER mostly (often PROBABILITY_YES 50). Parser bug: models write "DECISION: <ANSWER>"; fixed by stripping placeholder brackets (applied to all cells uniformly, disclosed).
- Layer rule: earliest layer within 0.005 of best synthetic-val AUROC among layers in [NL/4, 3NL/4] (layer 1 won on val because the synthetic set is lexically separable).
- TF-IDF on QUESTION TEXT ALONE gives AUROC 1.00 on NSE L2 and 0.99 on transfer L2 -> detection on these test sets is lexically trivial. Therefore: (i) "probe beats TF-IDF" is not a meaningful claim here; we report it honestly; (ii) the Fooled/Overriding test is WITHIN-QUESTION across contexts, where a lexical-question classifier is flat by construction -> a flat probe could be an artifact.
- Added POSITIVE CONTROL know/L0: the knowable NSE question "Based ONLY on the data shown, is the current close higher ..." with NO data shown. Context alone makes it unanswerable-from-given-data. A context-sensitive probe must move know/L0 vs know/L2. Overriding claim requires: probe moves on positive control (bootstrap CI excludes 0) AND stays flat on unk arm.
- Probe shifts reported in units of the train-set class gap (mean s_unk - mean s_ans on train).
- Authors: Samrudh Jain + Pranav Aggarwal (Pranav = author of 2608.27167 -> describe as team's own prior work, marked pre-existing). Affiliations TBD (Pranav: independent researcher per README). Public repo: user will create; I prepare clean folder.

## Step 3 — First full runs (v1) seen; v2 designed and launched
- Synthetic-trained probe FAILS NSE validity for qwen25-3b (AUROC .22), llama (.39), qwen3-8b (.49); OK for gemma (1.0), gate (.96). => v1 "Fooled" verdicts for those are probe artifacts; disclosed.
- POST-HOC (disclosed) probes: X = cross-domain diff-of-means on crypto/sports/weather L2 (no NSE data); N = NSE L2 cross-fitted (20 half-splits). Validity gate (post-hoc): NSE L2 AUROC >= .8 AND positive-control shift CI > 0.
- At 4 sampled layers: mid/deep layers mostly Overriding (FI<.25) for llama/gemma/qwen25; early layers partly move (FI .3-.55); depth-dependent.
- v2: all-layer scan (X_dm + N_dm), steering along X direction at layer NL//2 (fixed a priori), pushback X-scores.
- PRE-SPECIFIED v2 aggregation (written before v2 data): per model, verdict = median FI_L2 over VALID layers with depth >= 0.5 (X_dm and N_dm separately); Overriding if median < .25, Fooled if > .5, else Mixed. Also report the early-half median.

## Step 4 — v2 results seen; matched-control steering (v3) designed and launched
- v2 deep-layer verdicts: Overriding for all 6 under cross-fitted probe (median FI -0.14..0.23); cross-domain probe: Overriding llama/gemma/qwen25 (0.01..0.21), Mixed-borderline qwen3-4b (.26), qwen3-8b (.28), gate (.28).
- Steering (v2): Qwen2.5-3B clean (47.5->0% commit, knowable 100%, random raises). Qwen3-8B 25->2.5% but random a=8 lowers log-odds more -> specificity unclear. Llama: format breaks. Qwen3-4B: no effect. Reverse (a=-8) increases commit but random a=16 also does -> may be generic.
- v3: matched generation controls at a=+-8 for xdir and 3 random dirs (same norm) on llama, qwen25, qwen3-8b, gate, qwen3-4b. Claims about steering will be limited to what survives this control.

## Step 5 — External review; post-review experiments (all added after Steps 1–4, disclosed as post-hoc)
- Review points: no "fooled" reference on the FI scale; probe sensitivity tracks the verdict; pushback wording names the probed concept; steering layer invalid for Qwen3-14B and the gate.
- Added: leaked-answer anchor (L2post: panel + realised day+10 close, "Today" = target date; L2leak: same, "Today" unchanged); graded leakage (range half-width 0–25% of price, deep.py); matched date-only pairs; activation patching L0 -> L2 at the decision token; read-out gain along X; neutral pushback ("Are you sure? Please give your final decision…"); steering at the first X-valid layer >= n_layers//2 where n_layers//2 failed (Qwen3-14B, gate: layer 21); three more models (Qwen2.5-7B, Mistral-7B-v0.3, Llama-3.2-3B) with the unchanged pipeline.
- Expectation written before the anchor results: if the probes track knowability, FI(answer shown) should approach 1.
- Outcome: models commit on and answer the anchor items, but FI(answer shown) is only ~0.2–0.5 and the ask channel still says "unknowable". The probes and the self-report mainly encode question form, so the Overriding verdict from Steps 3–4 is withdrawn as not identifiable.
