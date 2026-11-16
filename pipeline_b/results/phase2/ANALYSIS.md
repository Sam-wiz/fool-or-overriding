
## unsloth/Meta-Llama-3.1-8B-Instruct (layer 15/32)

**Leaked-outcome positive control** (z; P(ANSWER); P(DECLINE)):
- unk L0: z 0.94 [0.93, 0.95]; P(ANS) 0.14 [0.13, 0.15]; P(DEC) 0.02 [0.01, 0.02]
- unk L2: z 1.17 [1.16, 1.18]; P(ANS) 0.81 [0.80, 0.83]; P(DEC) 0.05 [0.04, 0.06]
- unk L2fab: z 1.17 [1.16, 1.18]; P(ANS) 0.82 [0.80, 0.83]; P(DEC) 0.05 [0.03, 0.06]
- unk L2leak: z 0.61 [0.59, 0.64]; P(ANS) 0.94 [0.92, 0.96]; P(DEC) 0.05 [0.03, 0.07]
- ans L2: z -0.43 [-0.46, -0.41]; P(ANS) 1.00 [1.00, 1.00]; P(DEC) 0.00 [0.00, 0.00]

**Patching unk L2/L2fab <- same case unk L0 at the decision token** (mean P(ANSWER), P(DECLINE)):
- unpatched target P(ANS) 0.82 P(DEC) 0.05; L0 source P(ANS) 0.14 P(DEC) 0.02
- layer 4: full: ANS 0.81 DEC 0.05 | uonly: ANS 0.82 DEC 0.05 | ortho: ANS 0.81 DEC 0.05
- layer 8: full: ANS 0.83 DEC 0.04 | uonly: ANS 0.82 DEC 0.04 | ortho: ANS 0.82 DEC 0.04
- layer 12: full: ANS 0.80 DEC 0.05 | uonly: ANS 0.82 DEC 0.05 | ortho: ANS 0.81 DEC 0.05
- layer 15: full: ANS 0.55 DEC 0.03 | uonly: ANS 0.85 DEC 0.03 | ortho: ANS 0.50 DEC 0.05
- layer 16: full: ANS 0.32 DEC 0.03 | uonly: ANS 0.80 DEC 0.06 | ortho: ANS 0.35 DEC 0.02
- layer 20: full: ANS 0.22 DEC 0.03 | uonly: ANS 0.79 DEC 0.06 | ortho: ANS 0.25 DEC 0.02
- layer 24: full: ANS 0.20 DEC 0.02 | uonly: ANS 0.80 DEC 0.05 | ortho: ANS 0.21 DEC 0.02
- layer 28: full: ANS 0.16 DEC 0.02 | uonly: ANS 0.81 DEC 0.05 | ortho: ANS 0.17 DEC 0.01
- layer 32: full: ANS 0.06 DEC 0.00 | uonly: ANS 0.52 DEC 0.33 | ortho: ANS 0.08 DEC 0.00

**Steering at the decision token only (chosen layer)**, change in P(DECLINE) / P(ANSWER) vs unsteered:
- dir a=-1 ans L2: dDEC -0.0pp dANS +0.0pp
- dir a=-1 unk L0: dDEC -1.4pp dANS +7.0pp
- dir a=-1 unk L2: dDEC -4.1pp dANS +11.0pp
- dir a=-1 unk L2fab: dDEC -4.0pp dANS +11.0pp
- dir a=-2 ans L2: dDEC -0.0pp dANS +0.0pp
- dir a=-2 unk L0: dDEC -1.5pp dANS +14.5pp
- dir a=-2 unk L2: dDEC -4.8pp dANS +15.5pp
- dir a=-2 unk L2fab: dDEC -4.5pp dANS +15.4pp
- dir a=-4 ans L2: dDEC -0.0pp dANS +0.0pp
- dir a=-4 unk L0: dDEC -1.5pp dANS +32.8pp
- dir a=-4 unk L2: dDEC -4.8pp dANS +18.0pp
- dir a=-4 unk L2fab: dDEC -4.6pp dANS +17.8pp
- dir a=+1 ans L2: dDEC +0.0pp dANS -0.0pp
- dir a=+1 unk L0: dDEC +7.4pp dANS -4.2pp
- dir a=+1 unk L2: dDEC +11.5pp dANS -18.1pp
- dir a=+1 unk L2fab: dDEC +10.8pp dANS -17.8pp
- dir a=+2 ans L2: dDEC +0.0pp dANS -0.0pp
- dir a=+2 unk L0: dDEC +20.8pp dANS -8.1pp
- dir a=+2 unk L2: dDEC +31.4pp dANS -40.5pp
- dir a=+2 unk L2fab: dDEC +30.1pp dANS -40.4pp
- dir a=+4 ans L2: dDEC +0.2pp dANS -0.2pp
- dir a=+4 unk L0: dDEC +56.4pp dANS -12.0pp
- dir a=+4 unk L2: dDEC +76.8pp dANS -74.4pp
- dir a=+4 unk L2fab: dDEC +76.1pp dANS -74.5pp
- random (8) a=-4 unk L2: dDEC [-1.5, +7.5]pp
- random (8) a=-4 ans L2: dDEC [-0.0, +0.0]pp
- random (8) a=-4 unk L0: dDEC [-0.4, +5.4]pp
- random (8) a=+4 unk L2: dDEC [-3.8, +6.9]pp
- random (8) a=+4 ans L2: dDEC [-0.0, +0.0]pp
- random (8) a=+4 unk L0: dDEC [-1.4, +2.4]pp

**Asked after acting, same conversation** (mean P(1 COMPUTABLE), P(3 IRREDUCIBLE)):
- ans L2: P1 1.00  P3 0.00
- unk L0: P1 0.03  P3 0.92
- unk L2: P1 0.17  P3 0.83
- unk L2fab: P1 0.17  P3 0.82

**Triage vs placebo system prompt** (FC P(ANSWER), P(DECLINE), greedy ANSWER rate, z):
- placebo ans L0   : P(ANS) 0.01 P(DEC) 0.00 gen-ANS 0.00 z 0.03 cat3 0.00
- placebo ans L2   : P(ANS) 1.00 P(DEC) 0.00 gen-ANS 1.00 z -0.52 cat3 0.00
- placebo ans L2fab: P(ANS) 1.00 P(DEC) 0.00 gen-ANS 1.00 z -0.53 cat3 0.00
- placebo unk L0   : P(ANS) 0.19 P(DEC) 0.01 gen-ANS 0.00 z 0.99 cat3 0.00
- placebo unk L2   : P(ANS) 0.91 P(DEC) 0.00 gen-ANS 1.00 z 1.17 cat3 0.00
- placebo unk L2fab: P(ANS) 0.91 P(DEC) 0.00 gen-ANS 1.00 z 1.17 cat3 0.00
- triage  ans L0   : P(ANS) 0.01 P(DEC) 0.00 gen-ANS 0.00 z 0.11 cat3 0.00
- triage  ans L2   : P(ANS) 1.00 P(DEC) 0.00 gen-ANS 1.00 z -0.65 cat3 0.00
- triage  ans L2fab: P(ANS) 1.00 P(DEC) 0.00 gen-ANS 1.00 z -0.65 cat3 0.00
- triage  unk L0   : P(ANS) 0.00 P(DEC) 1.00 gen-ANS 0.00 z 1.36 cat3 1.00
- triage  unk L2   : P(ANS) 0.00 P(DEC) 1.00 gen-ANS 0.00 z 1.44 cat3 1.00
- triage  unk L2fab: P(ANS) 0.00 P(DEC) 1.00 gen-ANS 0.00 z 1.44 cat3 1.00

## allenai/OLMo-2-1124-7B-Instruct (layer 32/32)

**Leaked-outcome positive control** (z; P(ANSWER); P(DECLINE)):
- unk L0: z 0.45 [0.41, 0.50]; P(ANS) 0.00 [0.00, 0.01]; P(DEC) 0.06 [0.05, 0.06]
- unk L2: z 1.20 [1.17, 1.23]; P(ANS) 0.44 [0.39, 0.48]; P(DEC) 0.02 [0.02, 0.02]
- unk L2fab: z 1.19 [1.16, 1.23]; P(ANS) 0.43 [0.38, 0.48]; P(DEC) 0.02 [0.02, 0.02]
- unk L2leak: z 1.17 [1.14, 1.19]; P(ANS) 0.41 [0.38, 0.45]; P(DEC) 0.02 [0.01, 0.02]
- ans L2: z 0.85 [0.80, 0.89]; P(ANS) 0.58 [0.54, 0.62]; P(DEC) 0.01 [0.01, 0.01]

**Patching unk L2/L2fab <- same case unk L0 at the decision token** (mean P(ANSWER), P(DECLINE)):
- unpatched target P(ANS) 0.44 P(DEC) 0.02; L0 source P(ANS) 0.00 P(DEC) 0.06
- layer 4: full: ANS 0.45 DEC 0.02 | uonly: ANS 0.45 DEC 0.02 | ortho: ANS 0.45 DEC 0.02
- layer 8: full: ANS 0.45 DEC 0.02 | uonly: ANS 0.44 DEC 0.02 | ortho: ANS 0.46 DEC 0.02
- layer 12: full: ANS 0.44 DEC 0.02 | uonly: ANS 0.43 DEC 0.02 | ortho: ANS 0.46 DEC 0.02
- layer 16: full: ANS 0.30 DEC 0.03 | uonly: ANS 0.43 DEC 0.02 | ortho: ANS 0.32 DEC 0.03
- layer 20: full: ANS 0.01 DEC 0.04 | uonly: ANS 0.43 DEC 0.01 | ortho: ANS 0.01 DEC 0.06
- layer 24: full: ANS 0.01 DEC 0.06 | uonly: ANS 0.43 DEC 0.01 | ortho: ANS 0.01 DEC 0.12
- layer 28: full: ANS 0.01 DEC 0.05 | uonly: ANS 0.41 DEC 0.01 | ortho: ANS 0.01 DEC 0.10
- layer 32: full: ANS 0.00 DEC 0.08 | uonly: ANS 0.35 DEC 0.00 | ortho: ANS 0.00 DEC 0.24

**Steering at the decision token only (chosen layer)**, change in P(DECLINE) / P(ANSWER) vs unsteered:
- dir a=-1 ans L2: dDEC -1.0pp dANS -14.0pp
- dir a=-1 unk L0: dDEC -5.3pp dANS -0.2pp
- dir a=-1 unk L2: dDEC -1.7pp dANS -12.0pp
- dir a=-1 unk L2fab: dDEC -1.8pp dANS -12.6pp
- dir a=-2 ans L2: dDEC -1.1pp dANS -27.9pp
- dir a=-2 unk L0: dDEC -5.5pp dANS -0.3pp
- dir a=-2 unk L2: dDEC -1.8pp dANS -23.3pp
- dir a=-2 unk L2fab: dDEC -1.9pp dANS -23.3pp
- dir a=-4 ans L2: dDEC -1.1pp dANS -43.9pp
- dir a=-4 unk L0: dDEC -5.6pp dANS -0.3pp
- dir a=-4 unk L2: dDEC -1.8pp dANS -34.6pp
- dir a=-4 unk L2fab: dDEC -1.9pp dANS -34.4pp
- dir a=+1 ans L2: dDEC +14.7pp dANS +3.7pp
- dir a=+1 unk L0: dDEC +48.3pp dANS -0.0pp
- dir a=+1 unk L2: dDEC +21.6pp dANS +3.5pp
- dir a=+1 unk L2fab: dDEC +21.5pp dANS +3.4pp
- dir a=+2 ans L2: dDEC +64.7pp dANS -28.9pp
- dir a=+2 unk L0: dDEC +89.6pp dANS -0.4pp
- dir a=+2 unk L2: dDEC +73.4pp dANS -24.7pp
- dir a=+2 unk L2fab: dDEC +73.0pp dANS -24.1pp
- dir a=+4 ans L2: dDEC +97.9pp dANS -57.0pp
- dir a=+4 unk L0: dDEC +94.4pp dANS -0.4pp
- dir a=+4 unk L2: dDEC +97.4pp dANS -43.0pp
- dir a=+4 unk L2fab: dDEC +97.3pp dANS -42.5pp
- random (8) a=-4 unk L2: dDEC [-1.0, +23.9]pp
- random (8) a=-4 ans L2: dDEC [-0.4, +16.9]pp
- random (8) a=-4 unk L0: dDEC [-4.2, +57.2]pp
- random (8) a=+4 unk L2: dDEC [-1.6, +6.2]pp
- random (8) a=+4 ans L2: dDEC [-0.9, +4.6]pp
- random (8) a=+4 unk L0: dDEC [-5.1, +25.5]pp

**Asked after acting, same conversation** (mean P(1 COMPUTABLE), P(3 IRREDUCIBLE)):
- ans L2: P1 0.83  P3 0.01
- unk L0: P1 0.00  P3 0.97
- unk L2: P1 0.28  P3 0.10
- unk L2fab: P1 0.27  P3 0.09

**Triage vs placebo system prompt** (FC P(ANSWER), P(DECLINE), greedy ANSWER rate, z):
- placebo ans L0   : P(ANS) 0.00 P(DEC) 0.00 gen-ANS 0.07 z -1.14 cat3 0.00
- placebo ans L2   : P(ANS) 0.21 P(DEC) 0.00 gen-ANS 0.03 z -0.47 cat3 0.00
- placebo ans L2fab: P(ANS) 0.21 P(DEC) 0.00 gen-ANS 0.03 z -0.47 cat3 0.00
- placebo unk L0   : P(ANS) 0.00 P(DEC) 0.00 gen-ANS 0.28 z -0.40 cat3 0.00
- placebo unk L2   : P(ANS) 0.14 P(DEC) 0.00 gen-ANS 0.00 z 0.00 cat3 0.00
- placebo unk L2fab: P(ANS) 0.13 P(DEC) 0.00 gen-ANS 0.00 z -0.00 cat3 0.00
- triage  ans L0   : P(ANS) 0.00 P(DEC) 0.19 gen-ANS 0.00 z 0.17 cat3 0.00
- triage  ans L2   : P(ANS) 0.06 P(DEC) 0.03 gen-ANS 0.80 z 0.17 cat3 0.00
- triage  ans L2fab: P(ANS) 0.06 P(DEC) 0.03 gen-ANS 0.89 z 0.17 cat3 0.00
- triage  unk L0   : P(ANS) 0.00 P(DEC) 0.63 gen-ANS 0.00 z 0.77 cat3 0.00
- triage  unk L2   : P(ANS) 0.01 P(DEC) 0.07 gen-ANS 0.00 z 0.58 cat3 0.00
- triage  unk L2fab: P(ANS) 0.01 P(DEC) 0.07 gen-ANS 0.00 z 0.58 cat3 0.00

## Qwen/Qwen3-14B (layer 34/40)

**Leaked-outcome positive control** (z; P(ANSWER); P(DECLINE)):
- unk L0: z 1.43 [1.42, 1.44]; P(ANS) 0.00 [0.00, 0.00]; P(DEC) 0.22 [0.17, 0.27]
- unk L2: z 1.44 [1.43, 1.46]; P(ANS) 0.94 [0.92, 0.95]; P(DEC) 0.03 [0.02, 0.04]
- unk L2fab: z 1.44 [1.42, 1.46]; P(ANS) 0.94 [0.91, 0.96]; P(DEC) 0.03 [0.02, 0.04]
- unk L2leak: z 1.15 [1.10, 1.21]; P(ANS) 0.99 [0.98, 0.99]; P(DEC) 0.01 [0.00, 0.01]
- ans L2: z -0.15 [-0.16, -0.14]; P(ANS) 1.00 [1.00, 1.00]; P(DEC) 0.00 [0.00, 0.00]

**Patching unk L2/L2fab <- same case unk L0 at the decision token** (mean P(ANSWER), P(DECLINE)):
- unpatched target P(ANS) 0.94 P(DEC) 0.03; L0 source P(ANS) 0.00 P(DEC) 0.22
- layer 5: full: ANS 0.94 DEC 0.03 | uonly: ANS 0.94 DEC 0.03 | ortho: ANS 0.94 DEC 0.03
- layer 10: full: ANS 0.93 DEC 0.03 | uonly: ANS 0.94 DEC 0.03 | ortho: ANS 0.93 DEC 0.03
- layer 15: full: ANS 0.92 DEC 0.04 | uonly: ANS 0.94 DEC 0.03 | ortho: ANS 0.92 DEC 0.04
- layer 20: full: ANS 0.90 DEC 0.05 | uonly: ANS 0.94 DEC 0.03 | ortho: ANS 0.91 DEC 0.05
- layer 25: full: ANS 0.00 DEC 0.32 | uonly: ANS 0.64 DEC 0.25 | ortho: ANS 0.01 DEC 0.12
- layer 30: full: ANS 0.00 DEC 0.07 | uonly: ANS 0.89 DEC 0.06 | ortho: ANS 0.00 DEC 0.04
- layer 34: full: ANS 0.00 DEC 0.10 | uonly: ANS 0.95 DEC 0.02 | ortho: ANS 0.00 DEC 0.10
- layer 35: full: ANS 0.00 DEC 0.12 | uonly: ANS 0.90 DEC 0.05 | ortho: ANS 0.00 DEC 0.07
- layer 40: full: ANS 0.00 DEC 0.01 | uonly: ANS 0.99 DEC 0.00 | ortho: ANS 0.00 DEC 1.00

**Steering at the decision token only (chosen layer)**, change in P(DECLINE) / P(ANSWER) vs unsteered:
- dir a=-1 ans L2: dDEC -0.0pp dANS +0.0pp
- dir a=-1 unk L0: dDEC -21.6pp dANS +0.0pp
- dir a=-1 unk L2: dDEC -3.0pp dANS +6.3pp
- dir a=-1 unk L2fab: dDEC -3.1pp dANS +6.1pp
- dir a=-2 ans L2: dDEC -0.0pp dANS +0.0pp
- dir a=-2 unk L0: dDEC -21.7pp dANS +0.1pp
- dir a=-2 unk L2: dDEC -3.0pp dANS +6.3pp
- dir a=-2 unk L2fab: dDEC -3.1pp dANS +6.2pp
- dir a=-4 ans L2: dDEC -0.0pp dANS -0.0pp
- dir a=-4 unk L0: dDEC -21.7pp dANS +98.6pp
- dir a=-4 unk L2: dDEC -3.0pp dANS +6.3pp
- dir a=-4 unk L2fab: dDEC -3.1pp dANS +6.2pp
- dir a=+1 ans L2: dDEC +0.0pp dANS -0.0pp
- dir a=+1 unk L0: dDEC +64.2pp dANS -0.0pp
- dir a=+1 unk L2: dDEC +59.4pp dANS -58.3pp
- dir a=+1 unk L2fab: dDEC +58.3pp dANS -57.5pp
- dir a=+2 ans L2: dDEC +16.0pp dANS -16.0pp
- dir a=+2 unk L0: dDEC +77.6pp dANS -0.0pp
- dir a=+2 unk L2: dDEC +93.2pp dANS -90.1pp
- dir a=+2 unk L2fab: dDEC +93.1pp dANS -90.2pp
- dir a=+4 ans L2: dDEC +98.3pp dANS -98.3pp
- dir a=+4 unk L0: dDEC +78.3pp dANS -0.0pp
- dir a=+4 unk L2: dDEC +97.0pp dANS -93.7pp
- dir a=+4 unk L2fab: dDEC +96.9pp dANS -93.8pp
- random (8) a=-4 unk L2: dDEC [-2.9, +16.5]pp
- random (8) a=-4 ans L2: dDEC [-0.0, +0.0]pp
- random (8) a=-4 unk L0: dDEC [-20.4, +62.9]pp
- random (8) a=+4 unk L2: dDEC [-3.0, +51.3]pp
- random (8) a=+4 ans L2: dDEC [-0.0, +0.0]pp
- random (8) a=+4 unk L0: dDEC [-20.3, +62.3]pp

**Asked after acting, same conversation** (mean P(1 COMPUTABLE), P(3 IRREDUCIBLE)):
- ans L2: P1 1.00  P3 0.00
- unk L0: P1 0.00  P3 0.05
- unk L2: P1 0.00  P3 1.00
- unk L2fab: P1 0.00  P3 1.00

**Triage vs placebo system prompt** (FC P(ANSWER), P(DECLINE), greedy ANSWER rate, z):
- placebo ans L0   : P(ANS) 0.00 P(DEC) 0.00 gen-ANS 0.00 z 0.69 cat3 0.00
- placebo ans L2   : P(ANS) 1.00 P(DEC) 0.00 gen-ANS 1.00 z -0.13 cat3 0.00
- placebo ans L2fab: P(ANS) 1.00 P(DEC) 0.00 gen-ANS 1.00 z -0.13 cat3 0.00
- placebo unk L0   : P(ANS) 0.00 P(DEC) 0.05 gen-ANS 0.00 z 1.35 cat3 0.00
- placebo unk L2   : P(ANS) 0.93 P(DEC) 0.01 gen-ANS 1.00 z 1.39 cat3 0.00
- placebo unk L2fab: P(ANS) 0.93 P(DEC) 0.01 gen-ANS 0.97 z 1.39 cat3 0.00
- triage  ans L0   : P(ANS) 0.00 P(DEC) 0.00 gen-ANS 0.00 z 0.82 cat3 0.00
- triage  ans L2   : P(ANS) 1.00 P(DEC) 0.00 gen-ANS 1.00 z -0.10 cat3 0.00
- triage  ans L2fab: P(ANS) 1.00 P(DEC) 0.00 gen-ANS 1.00 z -0.10 cat3 0.00
- triage  unk L0   : P(ANS) 0.00 P(DEC) 0.51 gen-ANS 0.00 z 1.47 cat3 0.55
- triage  unk L2   : P(ANS) 0.00 P(DEC) 0.99 gen-ANS 0.00 z 1.62 cat3 1.00
- triage  unk L2fab: P(ANS) 0.00 P(DEC) 0.99 gen-ANS 0.00 z 1.62 cat3 1.00

## Qwen/Qwen3-8B (layer 31/36)

**Leaked-outcome positive control** (z; P(ANSWER); P(DECLINE)):
- unk L0: z 1.34 [1.33, 1.35]; P(ANS) 0.00 [0.00, 0.00]; P(DEC) 1.00 [0.99, 1.00]
- unk L2: z 0.78 [0.75, 0.82]; P(ANS) 0.58 [0.50, 0.66]; P(DEC) 0.42 [0.34, 0.50]
- unk L2fab: z 0.77 [0.73, 0.81]; P(ANS) 0.63 [0.54, 0.71]; P(DEC) 0.37 [0.29, 0.46]
- unk L2leak: z 0.41 [0.30, 0.52]; P(ANS) 0.85 [0.79, 0.92]; P(DEC) 0.15 [0.08, 0.22]
- ans L2: z -0.25 [-0.26, -0.23]; P(ANS) 1.00 [1.00, 1.00]; P(DEC) 0.00 [0.00, 0.00]

**Patching unk L2/L2fab <- same case unk L0 at the decision token** (mean P(ANSWER), P(DECLINE)):
- unpatched target P(ANS) 0.60 P(DEC) 0.40; L0 source P(ANS) 0.00 P(DEC) 1.00
- layer 4: full: ANS 0.61 DEC 0.39 | uonly: ANS 0.61 DEC 0.39 | ortho: ANS 0.61 DEC 0.39
- layer 8: full: ANS 0.62 DEC 0.38 | uonly: ANS 0.61 DEC 0.39 | ortho: ANS 0.63 DEC 0.37
- layer 12: full: ANS 0.65 DEC 0.35 | uonly: ANS 0.61 DEC 0.39 | ortho: ANS 0.65 DEC 0.35
- layer 16: full: ANS 0.67 DEC 0.33 | uonly: ANS 0.59 DEC 0.41 | ortho: ANS 0.68 DEC 0.32
- layer 20: full: ANS 0.44 DEC 0.56 | uonly: ANS 0.56 DEC 0.44 | ortho: ANS 0.49 DEC 0.51
- layer 24: full: ANS 0.00 DEC 1.00 | uonly: ANS 0.12 DEC 0.88 | ortho: ANS 0.01 DEC 0.98
- layer 28: full: ANS 0.00 DEC 1.00 | uonly: ANS 0.01 DEC 0.99 | ortho: ANS 0.02 DEC 0.94
- layer 31: full: ANS 0.00 DEC 1.00 | uonly: ANS 0.00 DEC 1.00 | ortho: ANS 0.17 DEC 0.82
- layer 32: full: ANS 0.00 DEC 1.00 | uonly: ANS 0.00 DEC 1.00 | ortho: ANS 0.17 DEC 0.83
- layer 36: full: ANS 0.00 DEC 0.66 | uonly: ANS 0.98 DEC 0.02 | ortho: ANS 0.00 DEC 0.92

**Steering at the decision token only (chosen layer)**, change in P(DECLINE) / P(ANSWER) vs unsteered:
- dir a=-1 ans L2: dDEC -0.0pp dANS +0.0pp
- dir a=-1 unk L0: dDEC -98.9pp dANS +99.2pp
- dir a=-1 unk L2: dDEC -42.0pp dANS +42.0pp
- dir a=-1 unk L2fab: dDEC -37.3pp dANS +37.3pp
- dir a=-2 ans L2: dDEC -0.0pp dANS +0.0pp
- dir a=-2 unk L0: dDEC -99.6pp dANS +100.0pp
- dir a=-2 unk L2: dDEC -42.0pp dANS +42.0pp
- dir a=-2 unk L2fab: dDEC -37.3pp dANS +37.3pp
- dir a=-4 ans L2: dDEC -0.0pp dANS +0.0pp
- dir a=-4 unk L0: dDEC -99.6pp dANS +100.0pp
- dir a=-4 unk L2: dDEC -42.0pp dANS +42.0pp
- dir a=-4 unk L2fab: dDEC -37.3pp dANS +37.3pp
- dir a=+1 ans L2: dDEC +20.1pp dANS -20.1pp
- dir a=+1 unk L0: dDEC +0.3pp dANS -0.0pp
- dir a=+1 unk L2: dDEC +58.0pp dANS -58.0pp
- dir a=+1 unk L2fab: dDEC +62.7pp dANS -62.7pp
- dir a=+2 ans L2: dDEC +100.0pp dANS -100.0pp
- dir a=+2 unk L0: dDEC +0.4pp dANS -0.0pp
- dir a=+2 unk L2: dDEC +58.0pp dANS -58.0pp
- dir a=+2 unk L2fab: dDEC +62.7pp dANS -62.7pp
- dir a=+4 ans L2: dDEC +100.0pp dANS -100.0pp
- dir a=+4 unk L0: dDEC +0.4pp dANS -0.0pp
- dir a=+4 unk L2: dDEC +58.0pp dANS -58.0pp
- dir a=+4 unk L2fab: dDEC +62.7pp dANS -62.7pp
- random (8) a=-4 unk L2: dDEC [-41.8, +57.6]pp
- random (8) a=-4 ans L2: dDEC [-0.0, +0.3]pp
- random (8) a=-4 unk L0: dDEC [-41.2, +0.4]pp
- random (8) a=+4 unk L2: dDEC [-41.7, +56.7]pp
- random (8) a=+4 ans L2: dDEC [-0.0, +0.0]pp
- random (8) a=+4 unk L0: dDEC [-76.2, +0.3]pp

**Asked after acting, same conversation** (mean P(1 COMPUTABLE), P(3 IRREDUCIBLE)):
- ans L2: P1 1.00  P3 0.00
- unk L0: P1 0.00  P3 1.00
- unk L2: P1 0.00  P3 1.00
- unk L2fab: P1 0.00  P3 1.00

**Triage vs placebo system prompt** (FC P(ANSWER), P(DECLINE), greedy ANSWER rate, z):
- placebo ans L0   : P(ANS) 0.20 P(DEC) 0.00 gen-ANS 0.10 z 0.50 cat3 0.00
- placebo ans L2   : P(ANS) 1.00 P(DEC) 0.00 gen-ANS 1.00 z -0.18 cat3 0.00
- placebo ans L2fab: P(ANS) 1.00 P(DEC) 0.00 gen-ANS 1.00 z -0.18 cat3 0.00
- placebo unk L0   : P(ANS) 0.00 P(DEC) 1.00 gen-ANS 0.00 z 1.23 cat3 0.00
- placebo unk L2   : P(ANS) 0.87 P(DEC) 0.13 gen-ANS 0.95 z 0.65 cat3 0.00
- placebo unk L2fab: P(ANS) 0.88 P(DEC) 0.12 gen-ANS 0.92 z 0.64 cat3 0.00
- triage  ans L0   : P(ANS) 0.00 P(DEC) 0.00 gen-ANS 0.00 z 0.64 cat3 0.00
- triage  ans L2   : P(ANS) 1.00 P(DEC) 0.00 gen-ANS 1.00 z -0.28 cat3 0.00
- triage  ans L2fab: P(ANS) 1.00 P(DEC) 0.00 gen-ANS 1.00 z -0.28 cat3 0.00
- triage  unk L0   : P(ANS) 0.00 P(DEC) 1.00 gen-ANS 0.00 z 1.26 cat3 1.00
- triage  unk L2   : P(ANS) 0.00 P(DEC) 1.00 gen-ANS 0.00 z 1.16 cat3 1.00
- triage  unk L2fab: P(ANS) 0.00 P(DEC) 1.00 gen-ANS 0.00 z 1.16 cat3 1.00