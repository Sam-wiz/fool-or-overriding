# Pre-registration: Fooled or Overriding?

Written 16 Nov 2026, 01:47 IST, before any smoke or main result was inspected
(the smoke run had been launched but no output read). File hash recorded in git/zip at submission.

## Question
When an authoritative-looking evidence panel raises an open-weight model's commitment on an unknowable
question, does the model's internal knowability signal collapse (FOOLED) or persist while the action
commits anyway (OVERRIDING)?

## Design (fixed before results)
- Items: 40 post-cutoff NSE cases; arms unk (will close be higher in 10 trading days, sealed outcome) and
  ans (was close higher than 10 trading days ago, same panel); levels L0 none, L1 thin, L2 rich real,
  L2irr another stock's panel, L2fab same stock, all numbers from another date (nothing true).
- Prompt: the published paper's natural agentic prompt, verbatim.
- Action: forced-choice P(ANSWER) over {ANSWER, CALL_TOOL, DECLINE}; greedy generation as secondary.
  Commitment on unk = ANSWER.
- Inside: logistic probe (unknowable vs answerable), trained on synthetic v3 items only, layer and position
  chosen only by AUROC on the crypto/sports/weather transfer set. NSE never used for any selection.
- Words-when-asked: forced-choice P(category 3 = IRREDUCIBLE) on the same context.
- Causal: add +/- alpha x diff-of-means direction at the chosen layer; 8 norm-matched random directions.

## Primary contrasts (per model, case-clustered bootstrap CIs)
1. Behavioural lift: P(ANSWER | unk, L2) - P(ANSWER | unk, L0).
2. Inside shift on unk: probe(unk, L2) - probe(unk, L0).
3. Inside separation at L2: AUROC(probe; unk vs ans at L2) and the same at L0.
Verdict rule for a model with a behavioural lift of at least 10pp:
- OVERRIDING if the L2 probe separation AUROC >= 0.75 and probe(unk, L2) stays above the Youden threshold
  on a majority of committed unk items.
- FOOLED if L2 separation AUROC < 0.65 or the majority of committed unk items fall below threshold.
- MIXED otherwise.

## Predictions (credences)
- P1: Majority verdict across responsive models is OVERRIDING: 55%. FOOLED: 25%. MIXED: 20%.
- P2: Probe separation (unk vs ans) on NSE at L0 >= 0.75 in at least half the models: 65%.
- P3: Probe beats a shuffled-label probe and stated/forced-choice action confidence as a detector of
  unknowable items among committed L2 rows: 70%.
- P4: The fabricated panel (L2fab) lifts commitment about as much as the real panel (|diff| < 10pp) in most
  responsive models: 60%.
- P5: Steering along +knowability raises P(DECLINE) on unk L2 items more than any of 8 random directions of
  equal norm: 70%; it also raises P(DECLINE) on ans L2 items (i.e. it is not selective): 60%.
- P6: Models classify unk items as IRREDUCIBLE when asked (P(3) > 0.5) on most L2 rows even when they
  commit: 50% (lower than the 90% seen in frontier models, as small models are weaker classifiers).

## Known risks stated in advance
Small models may commit at L0 already (no behavioural gradient); probe may not transfer from synthetic to
stocks (then the inside channel is reported as unreliable, not reinterpreted); tense differs between arms
(the transfer set and training set are tense-balanced, so the probe cannot rely on "will").

## Addendum A (01:52 IST, after reading ONE smoke model, Qwen2.5-7B, 10 items/cell; before any main run)
Observed: Qwen2.5-7B never chooses ANSWER on unk; it chooses CALL_TOOL at every level although the tool
description says it cannot see the future, while classifying the same items IRREDUCIBLE with P(3) ~ 1.0 when asked.
Changes, decided now and applied to all models:
- Secondary action outcome added: ACT = 1 - P(DECLINE) (ANSWER or CALL_TOOL; the paper's "tool fallacy" counts as
  acting on an unknowable question). Primary stays P(ANSWER). Verdicts are reported for both.
- Surface-text caveat: unk and ans questions differ in wording, so unk-vs-ans separation AUROC on NSE is weak
  evidence (a random direction may separate them). Primary inside measures become (i) within-arm probe shift across
  evidence levels (same question text, only the panel changes) and (ii) the probe's calibrated score relative to the
  transfer-set Youden threshold. Separation AUROC is reported against a random-direction baseline.

## Addendum B (02:32 IST, after smoke only; no main-run result inspected)
Smoke showed the transfer-set Youden threshold does not carry over to the NSE format (Llama probe ~0.00 on every NSE
row vs threshold 0.06; Qwen3 threshold 0.96 never crossed even at L0), so the absolute-threshold arm of the verdict
rule would label models FOOLED for a calibration reason, not a representational one. Changes:
- The threshold-based "knows-inside" fraction is recomputed with a threshold refit on NSE L0 rows only (Youden on
  unk-L0 vs ans-L0). L0 is not part of the L2-vs-L0 behavioural contrast's outcome, but this is a use of NSE data
  and is labelled as such. The original transfer-threshold numbers are still reported.
- Primary inside readout becomes the paired per-case unk-minus-ans gap on the normalised diff-of-means projection
  (projn), and its change L0->L2 and L1->L2 / L1->L2fab. FOOLED = gap shrinks by more than half with CI excluding 0;
  OVERRIDING = gap retained (change CI includes 0 or is positive) while commitment rises >= 10pp; MIXED otherwise.
- The TF-IDF control is interpreted as: wording separates the arms on NSE with the wrong sign (AUROC 0.00-0.34),
  so a correct-sign probe separation cannot come from synthetic-trained wording cues.
- Added follow-ups (exploratory, labelled as such): L0->L2 activation patching at the decision token (full vector
  and knowability-axis-only), the paper's triage system prompt with a matched-length placebo, logit-lens decision
  timeline, panel-push direction geometry cos(u, mean(unk L2) - mean(unk L0)).

## Addendum C (03:50 IST, POST-HOC, after Llama/Qwen3/OLMo main + phase-2 results were seen)
A devil's-advocate review found that in Qwen3-8B the diff-of-means knowability direction u is almost the model's own
decline direction on the synthetic training items (Qwen3 declines 62% of synthetic unknowables vs 8% of answerables;
cos(u, within-class decline direction) = 0.94). A probe trained on labels that the model's behaviour tracks can read the
decision instead of the knowledge. Post-hoc analysis, labelled as such in the report: a decision-orthogonalised
direction u_perp = u minus its component on the within-class decline direction c (c = mean over classes of
mean(declined) - mean(not declined) on synthetic train). We report z and the Addendum-B gap change on u_perp next to u,
and the transfer AUROC of u_perp (Qwen3 0.85, Llama 0.98) to show it still reads knowability. Interpretation rule fixed
now: a model is called FOOLED only if the gap shrinks on BOTH u and u_perp. Plus a GPU follow-up (phase 3): patch L0->L2
along c only, along u_perp only, and along norm-matched random directions.
