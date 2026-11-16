
=== unsloth/Llama-3.3-70B-Instruct-bnb-4bit  (layers 80; corpus 32x128 wikitext-103; multi-token concepts: [' unknowable', ' ANSWER', ' DECLINE'])
  J-lens    : valid deep layers 40/40; median FI(real panel) -0.74 [-0.80,-0.68]; FI(fabricated) -0.74; leak control FI -0.28
  logit lens: valid deep layers 40/40; median FI(real panel) -0.24 [-0.28,-0.21]; FI(fabricated) -0.25; leak control FI +0.21
  item level (L2+L2fab, n=78, 2 commit): J-lens readout predicting NOT committing, median AUROC over valid layers 0.95 (range 0.25-1.00)
  Full-vocabulary J-lens readout of condition-difference vectors (alphabetic tokens only; top 12):
   panel(L2-L0)@L32                   + ['combat', 'offensive', 'victory', 'attack', 'somewhat', 'speed', 'power']
                                      - ['Placeholder', 'Prostitutas', 'Pending', 'Scheduled', 'Waiting', 'Until', 'Blank', 'Pending']
                                      concept ranks {'unpredictable': 15846, 'uncertain': 18592, 'random': 2527, 'higher': 1663, 'DECLINE': 41737, 'ANSWER': 81494}
   fabricated(L2fab-L0)@L32           + ['combat', 'offensive', 'victory', 'attack', 'somewhat', 'speed', 'power', 'tactics']
                                      - ['Placeholder', 'Prostitutas', 'Pending', 'Scheduled', 'Until', 'Waiting', 'Blank', 'GOODMAN']
                                      concept ranks {'unpredictable': 16143, 'uncertain': 18626, 'random': 2523, 'higher': 1681, 'DECLINE': 42397, 'ANSWER': 80348}
   leak(leak-L2)@L32                  + ['Exceptions', 'victorious', 'reun', 'reunited', 'Opp', 'restored', 'Exceptions', 'formerly', 'regained', 'exceptions', 'Japanese', 'data']
                                      - ['Cic', 'Proto', 'Witch', 'Barbar', 'Viking', 'brainstorm', 'prot', 'Wild']
                                      concept ranks {'unpredictable': 127444, 'uncertain': 120644, 'random': 125233, 'higher': 83473, 'DECLINE': 24651, 'ANSWER': 24754}
   knowable-unknowable(L2)@L32        + ['Opp', 'Savings', 'animator', 'homer', 'IDA', 'PCA', 'Duplicate', 'DVDs', 'animate', 'DVD', 'Platt', 'Celebr']
                                      - ['strategic', 'experimentation', 'overall', 'experimental', 'experiments', 'strategy', 'ambitious', 'complex']
                                      concept ranks {'unpredictable': 127642, 'uncertain': 123243, 'random': 118763, 'higher': 127739, 'DECLINE': 1855, 'ANSWER': 7190}
   relevant-irrelevant(L2-L2irr)@L32  + []
                                      - []
                                      concept ranks {'unpredictable': 0, 'uncertain': 0, 'random': 0, 'higher': 0, 'DECLINE': 0, 'ANSWER': 0}
   panel(L2-L0)@L44                   + ['Analysis', 'confidence', 'analysis', 'opinion', 'Analytics', 'risk', 'lik', 'subjective', 'optimism', 'prediction', 'Confidence', 'predictions']
                                      - ['Bra', 'spacer', 'Bram', 'IRT', 'Reality', 'Jerry', 'Pap', 'Fruit']
                                      concept ranks {'unpredictable': 5439, 'uncertain': 29, 'random': 32566, 'higher': 37678, 'DECLINE': 57516, 'ANSWER': 1021}
   fabricated(L2fab-L0)@L44           + ['Analysis', 'confidence', 'analysis', 'risk', 'opinion', 'Analytics', 'lik', 'optimism', 'subjective', 'prediction', 'Confidence', 'predictions']
                                      - ['Bra', 'spacer', 'Bram', 'IRT', 'Reality', 'Jerry', 'Pap', 'Fruit']
                                      concept ranks {'unpredictable': 5572, 'uncertain': 32, 'random': 34444, 'higher': 38116, 'DECLINE': 59019, 'ANSWER': 979}
   leak(leak-L2)@L44                  + ['reverse', 'already', 'retrospective', 'retro', 'Reverse', 'retrospect', 'reversed', 'Retro', 'vict', 'spo', 'literal', 'forbidden']
                                      - ['uncertain', 'Incomplete', 'Tobias', 'undecided', 'agnostic', 'subjective', 'undefined', 'agus']
                                      concept ranks {'unpredictable': 123482, 'uncertain': 128255, 'random': 128068, 'higher': 46850, 'DECLINE': 40000, 'ANSWER': 62728}
   knowable-unknowable(L2)@L44        + ['Safe', 'straightforward', 'easy', 'easy', 'utra', 'Easy', 'NEG', 'simple', 'facil', 'NEG', 'afe', 'SAFE']
                                      - ['uncertain', 'incomplete', 'insufficient', 'unfinished', 'undecided', 'Lambert', 'semi', 'unsure']
                                      concept ranks {'unpredictable': 128086, 'uncertain': 128255, 'random': 127600, 'higher': 112536, 'DECLINE': 7591, 'ANSWER': 1005}
   relevant-irrelevant(L2-L2irr)@L44  + []
                                      - []
                                      concept ranks {'unpredictable': 0, 'uncertain': 0, 'random': 0, 'higher': 0, 'DECLINE': 0, 'ANSWER': 0}
   panel(L2-L0)@L56                   + ['prediction', 'predictions', 'answer', 'progn', 'subjective', 'answers', 'speculation', 'educated', 'Gut', 'uncertain', 'Prediction', 'guess']
                                      - ['Fetch', 'spacer', 'Trit', 'Pink', 'Fetching', 'iteral', 'Jerry', 'EFA']
                                      concept ranks {'unpredictable': 23762, 'uncertain': 9, 'random': 12714, 'higher': 67001, 'DECLINE': 66372, 'ANSWER': 465}
   fabricated(L2fab-L0)@L56           + ['prediction', 'predictions', 'answer', 'progn', 'subjective', 'answers', 'speculation', 'educated', 'Gut', 'uncertain', 'Prediction', 'speculative']
                                      - ['Fetch', 'spacer', 'Trit', 'Pink', 'Fetching', 'iteral', 'Jerry', 'EFA']
                                      concept ranks {'unpredictable': 25004, 'uncertain': 9, 'random': 12926, 'higher': 67450, 'DECLINE': 67747, 'ANSWER': 449}
   leak(leak-L2)@L56                  + ['retro', 'preview', 'previews', 'retrospective', 'reverse', 'Retro', 'retrospect', 'Reverse', 'already', 'viewer', 'archival', 'Preview']
                                      - ['uncertainty', 'uncertain', 'uncertainties', 'subjective', 'chio', 'unde', 'opinion', 'unsure']
                                      concept ranks {'unpredictable': 114715, 'uncertain': 128254, 'random': 126274, 'higher': 5440, 'DECLINE': 21770, 'ANSWER': 56541}
   knowable-unknowable(L2)@L56        + ['Safe', 'easy', 'straightforward', 'uluk', 'Easy', 'massage', 'lian', 'iggs', 'easy', 'izzes', 'dez', 'answer']
                                      - ['uncertain', 'Spec', 'speculative', 'speculation', 'incomplete', 'forecasts', 'predictions', 'forecast']
                                      concept ranks {'unpredictable': 128049, 'uncertain': 128255, 'random': 126327, 'higher': 92029, 'DECLINE': 27537, 'ANSWER': 263}
   relevant-irrelevant(L2-L2irr)@L56  + []
                                      - []
                                      concept ranks {'unpredictable': 0, 'uncertain': 0, 'random': 0, 'higher': 0, 'DECLINE': 0, 'ANSWER': 0}
   panel(L2-L0)@L68                   + ['Ans', 'Answer', 'ANSW', 'ans', 'answer', 'ANS', 'answers', 'Answer', 'Ans', 'answered', 'answer', 'answering']
                                      - ['Retrie', 'Calgary', 'Banner', 'SEM', 'egrity', 'Calvin', 'Bowman', 'Fruit']
                                      concept ranks {'unpredictable': 66815, 'uncertain': 785, 'random': 47796, 'higher': 122308, 'DECLINE': 34016, 'ANSWER': 2}
   fabricated(L2fab-L0)@L68           + ['Ans', 'Answer', 'ANSW', 'ans', 'answer', 'ANS', 'Ans', 'Answer', 'answers', 'answered', 'answer', 'answering']
                                      - ['Retrie', 'Calgary', 'Banner', 'SEM', 'Bowman', 'egrity', 'Calvin', 'Fruit']
                                      concept ranks {'unpredictable': 69329, 'uncertain': 846, 'random': 48717, 'higher': 122458, 'DECLINE': 38181, 'ANSWER': 2}
   leak(leak-L2)@L68                  + ['already', 'previews', 'preview', 'retrospective', 'viewer', 'decl', 'flashback', 'Retro', 'peek', 'Abbott', 'Jonah', 'opposite']
                                      - ['uncertain', 'uncertainty', 'uncertainties', 'probabil', 'opinion', 'inde', 'Tar', 'tar']
                                      concept ranks {'unpredictable': 92709, 'uncertain': 128254, 'random': 114935, 'higher': 5435, 'DECLINE': 99, 'ANSWER': 75}
   knowable-unknowable(L2)@L68        + ['straightforward', 'ANS', 'ANSW', 'lian', 'AFP', 'AFP', 'datab', 'easy', 'NEG', 'answer', 'utzer', 'answer']
                                      - ['Cant', 'Weber', 'Predict', 'Canton', 'Salem', 'BCE', 'predictive', 'Clement']
                                      concept ranks {'unpredictable': 128015, 'uncertain': 128182, 'random': 105152, 'higher': 46728, 'DECLINE': 118347, 'ANSWER': 2}
   relevant-irrelevant(L2-L2irr)@L68  + []
                                      - []
                                      concept ranks {'unpredictable': 0, 'uncertain': 0, 'random': 0, 'higher': 0, 'DECLINE': 0, 'ANSWER': 0}
