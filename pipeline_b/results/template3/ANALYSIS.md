# Results: t3_res

| model | layer (pos) | transfer AUROC | lift FC P(ANSWER) L0->L2 (pp) | lift gen ANSWER (pp) | fab-real FC (pp) | probe sep L0 | probe sep L2 | probe sep L2fab | shuf sep L2 | ask-P3 sep L2 | L2 committed n | knows-inside | says-irreducible | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Qwen3-14B | 34/40 (DEC) | 0.997 | 0.0 [0.0, 0.0] | 0.0 [0.0, 0.0] | -0.0 [-0.0, 0.0] | 1.00 | 1.000 [1.000, 1.000] | 1.00 | 1.00 | 1.00 | 0 | nan | nan | **NO-LIFT** |
| Qwen3-8B | 31/36 (DEC) | 0.994 | 1.8 [1.2, 2.4] | 0.0 [0.0, 0.0] | 0.1 [-0.6, 0.7] | 1.00 | 1.000 [1.000, 1.000] | 1.00 | 0.00 | 1.00 | 0 | nan | nan | **NO-LIFT** |

### Addendum-B verdicts (paired projn gap, L1 anchor)

| model | target | lift (pp) | gap L1 | change | rel | verdict |
|---|---|---|---|---|---|---|
| Qwen3-14B | L2 | 0.0 | 0.98 | 0.707 [0.604, 0.822] | +0.72 | **NO-LIFT** |
| Qwen3-14B | L2fab | 0.0 | 0.98 | 0.703 [0.594, 0.817] | +0.72 | **NO-LIFT** |
| Qwen3-8B | L2 | 1.8 | 1.03 | -0.140 [-0.159, -0.123] | -0.14 | **NO-LIFT** |
| Qwen3-8B | L2fab | 1.9 | 1.03 | -0.140 [-0.156, -0.121] | -0.14 | **NO-LIFT** |

## Qwen/Qwen3-14B  (thr 0.19; best {'pos': 'DEC', 'layer': 34, 'transfer_auroc': 0.9974922839506173})

| arm | lvl | n | FC ans | FC tool | FC decl | gen ANS | gen TOOL | gen DECL | unparsed | probe | probe>thr | ask P3 | ask mass | fc mass |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| unk | L0 | 40 | 0.00 | 0.29 | 0.71 | 0.00 | 0.00 | 1.00 | 0.00 | 0.96 | 1.00 | 1.00 | 1.00 | 1.00 |
| unk | L1 | 40 | 0.00 | 0.29 | 0.71 | 0.00 | 0.00 | 1.00 | 0.00 | 0.96 | 1.00 | 1.00 | 1.00 | 1.00 |
| unk | L2 | 40 | 0.00 | 0.08 | 0.92 | 0.00 | 0.00 | 1.00 | 0.00 | 0.94 | 1.00 | 1.00 | 1.00 | 1.00 |
| unk | L2fab | 38 | 0.00 | 0.08 | 0.92 | 0.00 | 0.00 | 1.00 | 0.00 | 0.93 | 1.00 | 1.00 | 1.00 | 1.00 |
| ans | L0 | 40 | 0.00 | 1.00 | 0.00 | 0.00 | 1.00 | 0.00 | 0.00 | 0.25 | 0.97 | 0.00 | 1.00 | 1.00 |
| ans | L1 | 40 | 0.67 | 0.32 | 0.00 | 0.70 | 0.30 | 0.00 | 0.00 | 0.02 | 0.00 | 0.00 | 1.00 | 1.00 |
| ans | L2 | 40 | 1.00 | 0.00 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 1.00 |
| ans | L2fab | 38 | 1.00 | 0.00 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 1.00 |

Separation AUROC (unk vs ans) by level: L0: probe 1.00, shuf 1.00, ask 1.00, fc_decl 1.00; L1: probe 1.00, shuf 1.00, ask 1.00, fc_decl 1.00; L2: probe 1.00, shuf 1.00, ask 1.00, fc_decl 1.00; L2fab: probe 1.00, shuf 1.00, ask 1.00, fc_decl 1.00

probe shift unk L0->L2 -0.027 [-0.031, -0.024]; ans -0.250 [-0.262, -0.239]; ask P3 shift unk 0.000 [0.000, 0.000]
groups: {'L2': {'n_committed': 0, 'knows_inside': nan, 'says_irreducible_when_asked': nan}, 'L2fab': {'n_committed': 0, 'knows_inside': nan, 'says_irreducible_when_asked': nan}, 'L1': {'n_committed': 0, 'knows_inside': nan, 'says_irreducible_when_asked': nan}}
paired gap probe(unk-ans) by level: L0 0.712 [0.698, 0.725]; L1 0.939 [0.923, 0.952]; L2 0.935 [0.932, 0.938]; L2fab 0.934 [0.930, 0.937]
gap change probe L1->L2 -0.004 [-0.016, 0.010]; L0->L2 0.223 [0.209, 0.238]; L1->L2fab -0.005 [-0.017, 0.009]
paired gap projn(unk-ans) by level: L0 0.602 [0.594, 0.610]; L1 0.982 [0.880, 1.083]; L2 1.689 [1.673, 1.705]; L2fab 1.686 [1.669, 1.704]
gap change projn L1->L2 0.707 [0.604, 0.822]; L0->L2 1.087 [1.068, 1.106]; L1->L2fab 0.703 [0.594, 0.817]
gap change ask-P3 L1->L2 0.000 [0.000, 0.000]; FC P(ANSWER) lift L1->L2 0.0 [0.0, 0.0]pp; ACT (1-P(decl)) lift L0->L2 -21.1 [-27.4, -14.9]pp
z (0=synthetic answerable mean, 1=synthetic unknowable mean): unk_L0 1.358 [1.350, 1.367]; unk_L1 1.420 [1.414, 1.425]; unk_L2 1.507 [1.505, 1.509]; unk_L2fab 1.507 [1.505, 1.510]; ans_L0 0.756 [0.748, 0.765]; ans_L1 0.437 [0.343, 0.543]; ans_L2 -0.182 [-0.199, -0.165]; ans_L2fab -0.178 [-0.197, -0.161]
Addendum C decline check: {'cos_u_decline': 0.5895533561706543, 'transfer_auroc_u': 0.9780414094650206, 'transfer_auroc_uperp': 0.979295267489712}
gap change z  L1->L2 0.707 [0.596, 0.815] (gap L1 0.98); L1->L2fab 0.703 [0.594, 0.823]
gap change zperp L1->L2 0.616 [0.547, 0.682] (gap L1 0.73); L1->L2fab 0.613 [0.543, 0.682]
route of lift from L0: L2 {'d_answer': 1.288347999507095e-05, 'd_decline': 0.21074412131072684, 'd_tool': -0.21075700479072168}; L2fab {'d_answer': 1.2397034681619688e-05, 'd_decline': 0.21245522592518795, 'd_tool': -0.21246762295986948}
Brier on committed unk (always-50 = 0.25): L1 None; L2 None; L2fab None
critical subset (unk&committed vs ans): {'L2': {'n': 0, 'probe': nan, 'ask': nan}, 'L2fab': {'n': 0, 'probe': nan, 'ask': nan}}
act-intent (unk, L1/L2/L2fab): {'L2': {'n': 40, 'n_commit': 0, 'auc_probe_predicts_commit': nan, 'auc_ask_predicts_commit': nan, 'auc_fc_predicts_commit': nan, 'spearman_projn_vs_fcanswer': -0.0013133208255159477}, 'L2fab': {'n': 38, 'n_commit': 0, 'auc_probe_predicts_commit': nan, 'auc_ask_predicts_commit': nan, 'auc_fc_predicts_commit': nan, 'spearman_projn_vs_fcanswer': -0.029871977240398292}, 'L1': {'n': 40, 'n_commit': 0, 'auc_probe_predicts_commit': nan, 'auc_ask_predicts_commit': nan, 'auc_fc_predicts_commit': nan, 'spearman_projn_vs_fcanswer': -0.15365853658536588}}
random-direction |AUROC| baseline (unk vs ans): {'L0': {'median': 1.0, 'p95': 1.0}, 'L2': {'median': 1.0, 'p95': 1.0}}

## Qwen/Qwen3-8B  (thr 0.02; best {'pos': 'DEC', 'layer': 31, 'transfer_auroc': 0.9936664094650205})

| arm | lvl | n | FC ans | FC tool | FC decl | gen ANS | gen TOOL | gen DECL | unparsed | probe | probe>thr | ask P3 | ask mass | fc mass |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| unk | L0 | 40 | 0.00 | 0.74 | 0.26 | 0.00 | 0.70 | 0.30 | 0.00 | 0.44 | 1.00 | 1.00 | 1.00 | 1.00 |
| unk | L1 | 40 | 0.00 | 0.10 | 0.90 | 0.00 | 0.05 | 0.95 | 0.00 | 0.68 | 1.00 | 1.00 | 1.00 | 1.00 |
| unk | L2 | 40 | 0.02 | 0.27 | 0.71 | 0.00 | 0.23 | 0.78 | 0.00 | 0.22 | 0.97 | 1.00 | 1.00 | 1.00 |
| unk | L2fab | 38 | 0.02 | 0.29 | 0.70 | 0.00 | 0.26 | 0.74 | 0.00 | 0.20 | 0.97 | 1.00 | 1.00 | 1.00 |
| ans | L0 | 40 | 0.00 | 1.00 | 0.00 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 1.00 |
| ans | L1 | 40 | 1.00 | 0.00 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 1.00 |
| ans | L2 | 40 | 1.00 | 0.00 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 1.00 |
| ans | L2fab | 38 | 1.00 | 0.00 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 1.00 |

Separation AUROC (unk vs ans) by level: L0: probe 1.00, shuf 0.00, ask 1.00, fc_decl 1.00; L1: probe 1.00, shuf 0.00, ask 1.00, fc_decl 1.00; L2: probe 1.00, shuf 0.00, ask 1.00, fc_decl 1.00; L2fab: probe 1.00, shuf 0.00, ask 1.00, fc_decl 1.00

probe shift unk L0->L2 -0.221 [-0.303, -0.135]; ans 0.001 [0.001, 0.001]; ask P3 shift unk -0.000 [-0.000, -0.000]
groups: {'L2': {'n_committed': 0, 'knows_inside': nan, 'says_irreducible_when_asked': nan}, 'L2fab': {'n_committed': 0, 'knows_inside': nan, 'says_irreducible_when_asked': nan}, 'L1': {'n_committed': 0, 'knows_inside': nan, 'says_irreducible_when_asked': nan}}
paired gap probe(unk-ans) by level: L0 0.441 [0.378, 0.505]; L1 0.675 [0.636, 0.712]; L2 0.219 [0.167, 0.278]; L2fab 0.204 [0.152, 0.262]
gap change probe L1->L2 -0.456 [-0.505, -0.405]; L0->L2 -0.222 [-0.308, -0.139]; L1->L2fab -0.472 [-0.522, -0.419]
paired gap projn(unk-ans) by level: L0 0.333 [0.326, 0.339]; L1 1.028 [1.014, 1.040]; L2 0.887 [0.870, 0.903]; L2fab 0.888 [0.873, 0.903]
gap change projn L1->L2 -0.140 [-0.159, -0.123]; L0->L2 0.554 [0.539, 0.569]; L1->L2fab -0.140 [-0.156, -0.121]
gap change ask-P3 L1->L2 -0.000 [-0.000, -0.000]; FC P(ANSWER) lift L1->L2 1.8 [1.2, 2.4]pp; ACT (1-P(decl)) lift L0->L2 -45.8 [-58.1, -31.8]pp
z (0=synthetic answerable mean, 1=synthetic unknowable mean): unk_L0 1.094 [1.083, 1.103]; unk_L1 1.097 [1.093, 1.100]; unk_L2 0.915 [0.901, 0.927]; unk_L2fab 0.912 [0.900, 0.924]; ans_L0 0.761 [0.754, 0.767]; ans_L1 0.069 [0.057, 0.083]; ans_L2 0.028 [0.015, 0.040]; ans_L2fab 0.024 [0.011, 0.036]
Addendum C decline check: {'cos_u_decline': 0.9354298114776611, 'transfer_auroc_u': 0.8830054012345678, 'transfer_auroc_uperp': 0.8446502057613169}
gap change z  L1->L2 -0.140 [-0.158, -0.122] (gap L1 1.03); L1->L2fab -0.140 [-0.156, -0.122]
gap change zperp L1->L2 0.173 [0.143, 0.202] (gap L1 0.70); L1->L2fab 0.183 [0.153, 0.214]
route of lift from L0: L2 {'d_answer': 0.01818866752088098, 'd_decline': 0.45804413258033827, 'd_tool': -0.4762328001012194}; L2fab {'d_answer': 0.01925146981088505, 'd_decline': 0.4400364925686573, 'd_tool': -0.45928796237954245}
Brier on committed unk (always-50 = 0.25): L1 None; L2 None; L2fab None
critical subset (unk&committed vs ans): {'L2': {'n': 0, 'probe': nan, 'ask': nan}, 'L2fab': {'n': 0, 'probe': nan, 'ask': nan}}
act-intent (unk, L1/L2/L2fab): {'L2': {'n': 40, 'n_commit': 0, 'auc_probe_predicts_commit': nan, 'auc_ask_predicts_commit': nan, 'auc_fc_predicts_commit': nan, 'spearman_projn_vs_fcanswer': -0.9598499061913698}, 'L2fab': {'n': 38, 'n_commit': 0, 'auc_probe_predicts_commit': nan, 'auc_ask_predicts_commit': nan, 'auc_fc_predicts_commit': nan, 'spearman_projn_vs_fcanswer': -0.9474778422146842}, 'L1': {'n': 40, 'n_commit': 0, 'auc_probe_predicts_commit': nan, 'auc_ask_predicts_commit': nan, 'auc_fc_predicts_commit': nan, 'spearman_projn_vs_fcanswer': -0.6607251754536404}}
random-direction |AUROC| baseline (unk vs ans): {'L0': {'median': 1.0, 'p95': 1.0}, 'L2': {'median': 1.0, 'p95': 1.0}}