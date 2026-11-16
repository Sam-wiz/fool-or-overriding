
=== unsloth/Meta-Llama-3.1-8B-Instruct  (layers 32; corpus 64x128 wikitext-103; multi-token concepts: [' unknowable', ' ANSWER', ' DECLINE'])
  J-lens    : valid deep layers 16/16; median FI(real panel) -0.17 [-0.18,-0.15]; FI(fabricated) -0.17; leak control FI +0.07
  logit lens: valid deep layers 16/16; median FI(real panel) +0.01 [-0.00,+0.02]; FI(fabricated) +0.01; leak control FI +0.45
  item level: commitment is 100% on L2/L2fab, no within-condition variation to predict
  Full-vocabulary J-lens readout of condition-difference vectors (alphabetic tokens only; top 12):
   panel(L2-L0)@L13                   + ['COVID', 'COVID', 'covid', 'cybersecurity', 'Covid', 'impactful', 'blockchain', 'coronavirus', 'cryptocurrency', 'https', 'crowdfunding', 'Coronavirus']
                                      - ['iPod']
                                      concept ranks {'unpredictable': 1280, 'uncertain': 1842, 'random': 124940, 'higher': 56744, 'DECLINE': 29844, 'ANSWER': 106878}
   fabricated(L2fab-L0)@L13           + ['COVID', 'COVID', 'covid', 'cybersecurity', 'Covid', 'impactful', 'blockchain', 'coronavirus', 'cryptocurrency', 'https', 'crowdfunding', 'Coronavirus']
                                      - ['iPod']
                                      concept ranks {'unpredictable': 1404, 'uncertain': 1890, 'random': 125322, 'higher': 59461, 'DECLINE': 31363, 'ANSWER': 108213}
   leak(leak-L2)@L13                  + ['totalCount', 'EObject', 'codegen', 'txn', 'jumbotron', 'RTAL', 'strSQL']
                                      - ['https', 'mon', 'animation', 'None', 'There', 'ind', 'Minimal', 'limited']
                                      concept ranks {'unpredictable': 97668, 'uncertain': 110148, 'random': 126587, 'higher': 98437, 'DECLINE': 52212, 'ANSWER': 71997}
   knowable-unknowable(L2)@L13        + ['ungan', 'ukan', 'retty', 'pcf', 'riendly', 'artz', 'curacy', 'udoku', 'vik', 'imilar', 'ancellable', 'ndern']
                                      - ['countless', 'narrative', 'LGBTQ', 'overarching', 'myriad', 'deeply', 'multid', 'vast']
                                      concept ranks {'unpredictable': 127908, 'uncertain': 128035, 'random': 120058, 'higher': 125237, 'DECLINE': 95126, 'ANSWER': 28703}
   relevant-irrelevant(L2-L2irr)@L13  + ['initially', 'lenght', 'initial', 'initialise', 'initialised', 'progressively', 'balance', 'then', 'balancing', 'balanced', 'critics', 'gradually']
                                      - ['zas', 'Node', 'Chinese', 'node', 'Saras', 'kart', 'nod', 'female']
                                      concept ranks {'unpredictable': 11322, 'uncertain': 17525, 'random': 78685, 'higher': 18753, 'DECLINE': 28367, 'ANSWER': 57202}
   panel(L2-L0)@L18                   + ['Avengers', 'Warrior', 'ApplicationException', 'Archie', 'Assassin', 'Armor', 'adrenaline', 'warrior', 'Aristotle', 'Avalanche', 'Viking', 'warriors']
                                      - ['coop', 'Bus', 'bus', 'GCBO', 'census', 'blogging', 'Census', 'bloggers']
                                      concept ranks {'unpredictable': 6607, 'uncertain': 26688, 'random': 33604, 'higher': 48798, 'DECLINE': 19984, 'ANSWER': 10237}
   fabricated(L2fab-L0)@L18           + ['Avengers', 'Warrior', 'ApplicationException', 'Assassin', 'Archie', 'Armor', 'adrenaline', 'Aristotle', 'warrior', 'Avalanche', 'Viking', 'warriors']
                                      - ['coop', 'Bus', 'bus', 'GCBO', 'census', 'blogging', 'Census', 'BCHP']
                                      concept ranks {'unpredictable': 6811, 'uncertain': 26618, 'random': 33614, 'higher': 47678, 'DECLINE': 20591, 'ANSWER': 9668}
   leak(leak-L2)@L18                  + ['victorious', 'triumph', 'trium', 'victories', 'correct', 'finally', 'actual', 'affirm', 'finished', 'accurate', 'elim', 'literal']
                                      - ['unsure', 'uncertain', 'unclear', 'uncertainty', 'uncertainties', 'inadequate', 'Complexity', 'ricerca']
                                      concept ranks {'unpredictable': 128245, 'uncertain': 128254, 'random': 127935, 'higher': 12704, 'DECLINE': 16343, 'ANSWER': 278}
   knowable-unknowable(L2)@L18        + ['straightforward', 'simple', 'simplicity', 'simply', 'Simple', 'victorious', 'simples', 'simplement', 'Simple', 'Athletics', 'straight', 'Winners']
                                      - ['uncertain', 'unsure', 'unpredictable', 'unknown', 'crypt', 'uncertainty', 'Crypt', 'Chaos']
                                      concept ranks {'unpredictable': 128253, 'uncertain': 128255, 'random': 127401, 'higher': 57423, 'DECLINE': 38252, 'ANSWER': 41}
   relevant-irrelevant(L2-L2irr)@L18  + ['Viking', 'album', 'action', 'Avengers', 'Aviv', 'Asphalt', 'aerobic', 'averages', 'esan', 'Andersen', 'Angebot', 'Autof']
                                      - ['Chronicle', 'Chronic', 'Crawford', 'CRC', 'CNN', 'CrossRef', 'Casc', 'Clim']
                                      concept ranks {'unpredictable': 13936, 'uncertain': 2835, 'random': 69901, 'higher': 50305, 'DECLINE': 122330, 'ANSWER': 3789}
   panel(L2-L0)@L22                   + ['predictions', 'predicted', 'prediction', 'estimated', 'anticipation', 'Anti', 'anarch', 'warnings', 'anarchist', 'Prediction', 'precarious', 'warning']
                                      - ['utos', 'Probe', 'probe', 'Bruno', 'probe', 'BUR', 'ulton', 'Probe']
                                      concept ranks {'unpredictable': 252, 'uncertain': 10324, 'random': 749, 'higher': 9355, 'DECLINE': 13094, 'ANSWER': 64666}
   fabricated(L2fab-L0)@L22           + ['predictions', 'predicted', 'prediction', 'estimated', 'anticipation', 'Anti', 'anarchist', 'anarch', 'warnings', 'Prediction', 'advice', 'precarious']
                                      - ['utos', 'Probe', 'probe', 'Bruno', 'probe', 'ulton', 'BUR', 'Probe']
                                      concept ranks {'unpredictable': 258, 'uncertain': 10116, 'random': 725, 'higher': 9057, 'DECLINE': 14348, 'ANSWER': 61308}
   leak(leak-L2)@L22                  + ['affirmation', 'correct', 'affirm', 'straight', 'literal', 'assert', 'actually', 'facts', 'revelation', 'outright', 'deletion', 'banned']
                                      - ['Unknown', 'probe', 'unclear', 'uncertainties', 'TBD', 'unsure', 'uncertain', 'unsupported']
                                      concept ranks {'unpredictable': 127966, 'uncertain': 128245, 'random': 125892, 'higher': 4531, 'DECLINE': 9254, 'ANSWER': 880}
   knowable-unknowable(L2)@L22        + ['straightforward', 'simple', 'SIMPLE', 'simples', 'Simple', 'easy', 'Simple', 'SimpleName', 'comparison', 'answers', 'comparisons', 'simplest']
                                      - ['uncertain', 'unsure', 'uncertainty', 'uncertainties', 'undefined', 'unknown', 'unclear', 'unpredictable']
                                      concept ranks {'unpredictable': 128248, 'uncertain': 128255, 'random': 128033, 'higher': 42536, 'DECLINE': 70427, 'ANSWER': 27}
   relevant-irrelevant(L2-L2irr)@L22  + ['action', 'Action', 'average', 'battling', 'audi', 'battle', 'anti', 'air', 'alternatives', 'balanced', 'associ', 'bug']
                                      - ['Chronic', 'Chronicles', 'chron', 'Ritch', 'ublik', 'Chronicle', 'Clarke', 'utos']
                                      concept ranks {'unpredictable': 2681, 'uncertain': 2415, 'random': 28674, 'higher': 5957, 'DECLINE': 127531, 'ANSWER': 7764}
   panel(L2-L0)@L27                   + ['Answer', 'ANSW', 'decline', 'answer', 'answers', 'Answers', 'ANS', 'Ans', 'decl', 'declining', 'declines', 'DECL']
                                      - ['Call', 'call', 'Call', 'call', 'CALL', 'Calls', 'calls', 'calling']
                                      concept ranks {'unpredictable': 4216, 'uncertain': 1175, 'random': 5710, 'higher': 11916, 'DECLINE': 11, 'ANSWER': 1}
   fabricated(L2fab-L0)@L27           + ['Answer', 'ANSW', 'answer', 'answers', 'decline', 'Answers', 'ANS', 'Ans', 'decl', 'declining', 'declines', 'Ans']
                                      - ['Call', 'call', 'Call', 'call', 'CALL', 'Calls', 'calls', 'calling']
                                      concept ranks {'unpredictable': 4331, 'uncertain': 1066, 'random': 5752, 'higher': 11530, 'DECLINE': 14, 'ANSWER': 1}
   leak(leak-L2)@L27                  + ['confirmed', 'affirmation', 'chwitz', 'Abe', 'confirmation', 'spoiler', 'confirm', 'iana', 'aes', 'ActionResult', 'correct', 'yes']
                                      - ['CALL', 'Call', 'call', 'Call', 'call', 'Calls', 'calls', 'CALL']
                                      concept ranks {'unpredictable': 128031, 'uncertain': 128172, 'random': 117688, 'higher': 6231, 'DECLINE': 122296, 'ANSWER': 659}
   knowable-unknowable(L2)@L27        + ['ANS', 'yes', 'Yes', 'ANSW', 'asn', 'comparison', 'answer', 'yes', 'answered', 'simple', 'Yes', 'Simple']
                                      - ['Call', 'call', 'Call', 'CALL', 'Decl', 'Calls', 'Decl', 'calls']
                                      concept ranks {'unpredictable': 128127, 'uncertain': 128140, 'random': 120682, 'higher': 2228, 'DECLINE': 128232, 'ANSWER': 3}
   relevant-irrelevant(L2-L2irr)@L27  + ['ANSW', 'ANS', 'Answer', 'answer', 'answers', 'ans', 'answered', 'answering', 'Ans', 'Answers', 'ans', 'Answer']
                                      - ['Decl', 'Decl', 'DECL', 'decl', 'decl', 'DECL', 'decline', 'Declaration']
                                      concept ranks {'unpredictable': 94869, 'uncertain': 3416, 'random': 88493, 'higher': 34408, 'DECLINE': 128253, 'ANSWER': 0}

=== Qwen/Qwen3-14B  (layers 40; corpus 64x128 wikitext-103; multi-token concepts: [' unknowable', ' ANSWER', ' DECLINE'])
  J-lens    : valid deep layers 20/20; median FI(real panel) -0.07 [-0.13,-0.05]; FI(fabricated) -0.07; leak control FI +0.20
  logit lens: valid deep layers 20/20; median FI(real panel) -0.10 [-0.14,-0.06]; FI(fabricated) -0.08; leak control FI +0.32
  item level: commitment is 100% on L2/L2fab, no within-condition variation to predict
  Full-vocabulary J-lens readout of condition-difference vectors (alphabetic tokens only; top 12):
   panel(L2-L0)@L16                   + ['benchmark', 'benchmarks', 'Benchmark', 'Upon', 'nuru', 'Optimization', 'pobli', 'Evalu', 'optimal', 'CRM', 'wida']
                                      - ['maybe', 'maybe']
                                      concept ranks {'unpredictable': 43863, 'uncertain': 130858, 'random': 97762, 'higher': 4922, 'DECLINE': 37168, 'ANSWER': 139002}
   fabricated(L2fab-L0)@L16           + ['benchmark', 'nuru', 'Benchmark', 'benchmarks', 'Upon', 'pobli', 'Evalu', 'wida', 'Optimization', 'optimal', 'CRM']
                                      - ['maybe', 'maybe']
                                      concept ranks {'unpredictable': 44681, 'uncertain': 130705, 'random': 98601, 'higher': 5221, 'DECLINE': 39171, 'ANSWER': 140080}
   leak(leak-L2)@L16                  + ['licence', 'organisations', 'defence', 'organisation', 'organisers', 'honoured', 'uminium', 'honour', 'organising', 'licences', 'organisation', 'authorised']
                                      - ['shemale']
                                      concept ranks {'unpredictable': 70986, 'uncertain': 44681, 'random': 128178, 'higher': 6945, 'DECLINE': 79068, 'ANSWER': 97553}
   knowable-unknowable(L2)@L16        + ['organised', 'manoe', 'armour', 'defence', 'specialised', 'rumours', 'kilometres', 'offence', 'recognised']
                                      - ['gonna', 'YES']
                                      concept ranks {'unpredictable': 28839, 'uncertain': 76244, 'random': 17748, 'higher': 35561, 'DECLINE': 149054, 'ANSWER': 131941}
   relevant-irrelevant(L2-L2irr)@L16  + []
                                      - ['councill', 'limburg', 'modx', 'NdEx', 'TRGL', 'Initialise', 'drFc', 'neighbourhood']
                                      concept ranks {'unpredictable': 44991, 'uncertain': 24471, 'random': 52421, 'higher': 69351, 'DECLINE': 78220, 'ANSWER': 61415}
   panel(L2-L0)@L22                   + ['confidence', 'PathParam', 'FilterWhere', 'positive', 'PropertyParams', 'strength']
                                      - ['internet', 'video', 'computer', 'camera', 'server', 'game', 'Internet', 'online']
                                      concept ranks {'unpredictable': 98322, 'uncertain': 81561, 'random': 147300, 'higher': 137889, 'DECLINE': 75478, 'ANSWER': 117870}
   fabricated(L2fab-L0)@L22           + ['confidence', 'PathParam', 'FilterWhere', 'positive', 'PropertyParams', 'PositiveButton', 'strength']
                                      - ['internet', 'video', 'computer', 'camera', 'server', 'online', 'game', 'Internet']
                                      concept ranks {'unpredictable': 99672, 'uncertain': 82772, 'random': 147561, 'higher': 138109, 'DECLINE': 76879, 'ANSWER': 116481}
   leak(leak-L2)@L22                  + ['historically', 'victories', 'ending', 'corrupt', 'triumph', 'endings', 'finishing', 'historical', 'retro', 'final', 'based', 'successfully']
                                      - ['tjejer', 'filmpjes', 'lesbische', 'erotisk', 'Erotische']
                                      concept ranks {'unpredictable': 17787, 'uncertain': 10615, 'random': 20384, 'higher': 13152, 'DECLINE': 62085, 'ANSWER': 118526}
   knowable-unknowable(L2)@L22        + ['incorrect', 'Correct', 'correct']
                                      - ['deep', 'ambition', 'existential', 'Philosophy', 'Patreon', 'directors', 'philosophical', 'Deep']
                                      concept ranks {'unpredictable': 151858, 'uncertain': 150737, 'random': 128431, 'higher': 149884, 'DECLINE': 84528, 'ANSWER': 7212}
   relevant-irrelevant(L2-L2irr)@L22  + ['PositiveButton', 'Argb']
                                      - ['translation', 'female', 'unknown', 'translator', 'Unknown', 'unknow', 'information', 'detectives']
                                      concept ranks {'unpredictable': 150648, 'uncertain': 149643, 'random': 149501, 'higher': 140180, 'DECLINE': 50049, 'ANSWER': 117494}
   panel(L2-L0)@L28                   + ['calculated', 'based', 'balanced', 'strengths', 'crafted', 'analysis', 'favorable', 'engagement', 'loosely', 'conclusions', 'bold', 'rating']
                                      - ['Disallow', 'Illegal', 'ulton', 'Illegal', 'PROCUREMENT', 'illegal']
                                      concept ranks {'unpredictable': 3605, 'uncertain': 2145, 'random': 48732, 'higher': 5942, 'DECLINE': 131565, 'ANSWER': 124864}
   fabricated(L2fab-L0)@L28           + ['calculated', 'based', 'balanced', 'strengths', 'crafted', 'analysis', 'favorable', 'engagement', 'conclusions', 'loosely', 'bold', 'rating']
                                      - ['Disallow', 'Illegal', 'ulton', 'Illegal', 'PROCUREMENT', 'illegal']
                                      concept ranks {'unpredictable': 3632, 'uncertain': 2128, 'random': 50163, 'higher': 6006, 'DECLINE': 132244, 'ANSWER': 125133}
   leak(leak-L2)@L28                  + ['spo', 'compare', 'comparing', 'already', 'compares', 'compare', 'comparison', 'Preview', 'spoilers', 'countdown', 'spoiled', 'spo']
                                      - ['vag', 'humility', 'Lack', 'INCREMENT', 'Unsure', 'uncertain', 'fuzzy', 'uncertainty']
                                      concept ranks {'unpredictable': 151775, 'uncertain': 151917, 'random': 145773, 'higher': 2478, 'DECLINE': 142388, 'ANSWER': 92895}
   knowable-unknowable(L2)@L28        + ['instantly', 'Already', 'Immediate', 'immedi', 'immediate']
                                      - ['uncertain', 'speculative', 'uncertainty', 'unpredict', 'uncertainties', 'unpredictable', 'cautiously', 'tentative']
                                      concept ranks {'unpredictable': 151928, 'uncertain': 151934, 'random': 140085, 'higher': 99115, 'DECLINE': 82569, 'ANSWER': 1446}
   relevant-irrelevant(L2-L2irr)@L28  + ['risk', 'predictions', 'optimistic', 'balanced', 'nuanced', 'lookahead', 'predictive', 'risky', 'CurrentValue', 'strengths', 'predicted', 'Risk']
                                      - ['unrelated', 'unknown', 'irrelevant', 'UNKNOWN', 'Unknown', 'unknown', 'clar']
                                      concept ranks {'unpredictable': 56665, 'uncertain': 122791, 'random': 133824, 'higher': 32012, 'DECLINE': 147083, 'ANSWER': 149890}
   panel(L2-L0)@L34                   + ['Abbey', 'Analysis', 'Annie', 'Alice', 'Anne', 'Alice', 'analysis', 'AdapterFactory', 'Avenue', 'Antoine', 'ANC', 'analysis']
                                      - ['BOOT', 'CALE', 'getC', 'cbo', 'borrowing', 'Cub', 'cyl', 'Brock']
                                      concept ranks {'unpredictable': 64304, 'uncertain': 109, 'random': 139865, 'higher': 114674, 'DECLINE': 9913, 'ANSWER': 537}
   fabricated(L2fab-L0)@L34           + ['Abbey', 'Annie', 'Analysis', 'Alice', 'Anne', 'Alice', 'AdapterFactory', 'Avenue', 'analysis', 'Antoine', 'ANC', 'Anna']
                                      - ['BOOT', 'getC', 'cbo', 'CALE', 'borrowing', 'Cub', 'cyl', 'CSC']
                                      concept ranks {'unpredictable': 65141, 'uncertain': 116, 'random': 139969, 'higher': 113902, 'DECLINE': 10954, 'ANSWER': 575}
   leak(leak-L2)@L34                  + ['AABB', 'computed', 'Arthur', 'oden', 'oload']
                                      - ['uncertainty', 'uncertain', 'unclear', 'uncertainties', 'unsure', 'inability', 'uncert', 'cautious']
                                      concept ranks {'unpredictable': 151802, 'uncertain': 151931, 'random': 79378, 'higher': 14744, 'DECLINE': 140037, 'ANSWER': 399}
   knowable-unknowable(L2)@L34        + ['stre', 'adders', 'spath', 'imdi', 'coded', 'Immediate', 'aru', 'Payload']
                                      - ['uncertainty', 'uncertain', 'cautious', 'inability', 'uncertainties', 'caution', 'cautiously', 'limited']
                                      concept ranks {'unpredictable': 151801, 'uncertain': 151933, 'random': 22971, 'higher': 72909, 'DECLINE': 145524, 'ANSWER': 2671}
   relevant-irrelevant(L2-L2irr)@L34  + ['attack', 'armor', 'armor', 'analyze', 'Abbey', 'analyze', 'attern', 'apest', 'Armor', 'Arrange', 'Austria', 'aalborg']
                                      - ['delegation', 'delegate', 'unrelated', 'invalid', 'transferred', 'delegated', 'transfer', 'irrelevant']
                                      concept ranks {'unpredictable': 98494, 'uncertain': 52152, 'random': 145317, 'higher': 112002, 'DECLINE': 149149, 'ANSWER': 2470}

=== Qwen/Qwen3-8B  (layers 36; corpus 64x128 wikitext-103; multi-token concepts: [' unknowable', ' ANSWER', ' DECLINE'])
  J-lens    : valid deep layers 18/18; median FI(real panel) -0.16 [-0.22,-0.07]; FI(fabricated) -0.16; leak control FI +0.18
  logit lens: valid deep layers 18/18; median FI(real panel) -0.57 [-0.71,-0.43]; FI(fabricated) -0.57; leak control FI +0.35
  item level (L2+L2fab, n=78, 30 commit): J-lens readout predicting NOT committing, median AUROC over valid layers 0.36 (range 0.20-0.95)
  Full-vocabulary J-lens readout of condition-difference vectors (alphabetic tokens only; top 12):
   panel(L2-L0)@L14                   + []
                                      - ['Jessica', 'Emily', 'Crystal', 'Dresden']
                                      concept ranks {'unpredictable': 3806, 'uncertain': 52132, 'random': 10404, 'higher': 59649, 'DECLINE': 35822, 'ANSWER': 74633}
   fabricated(L2fab-L0)@L14           + []
                                      - ['Jessica', 'Crystal', 'Emily']
                                      concept ranks {'unpredictable': 3767, 'uncertain': 51572, 'random': 10246, 'higher': 53819, 'DECLINE': 36515, 'ANSWER': 77406}
   leak(leak-L2)@L14                  + []
                                      - ['Comcast', 'elsif']
                                      concept ranks {'unpredictable': 27488, 'uncertain': 5373, 'random': 9635, 'higher': 2350, 'DECLINE': 81974, 'ANSWER': 95293}
   knowable-unknowable(L2)@L14        + ['movie', 'episode', 'scene', 'mistake', 'crossword', 'film', 'recording', 'streets', 'recorded', 'accident', 'forgot', 'oficial']
                                      - []
                                      concept ranks {'unpredictable': 24550, 'uncertain': 7568, 'random': 5548, 'higher': 8963, 'DECLINE': 54719, 'ANSWER': 45059}
   relevant-irrelevant(L2-L2irr)@L14  + []
                                      - ['anguard', 'Hezbollah']
                                      concept ranks {'unpredictable': 60762, 'uncertain': 5764, 'random': 1058, 'higher': 7639, 'DECLINE': 136815, 'ANSWER': 148250}
   panel(L2-L0)@L20                   + ['command', 'commands', 'attack', 'Commander', 'defended', 'commander', 'reinforced', 'Command', 'attacking', 'commanding', 'supported', 'leadership']
                                      - ['pedia', 'wikipedia', 'Craigslist']
                                      concept ranks {'unpredictable': 69729, 'uncertain': 106587, 'random': 136347, 'higher': 922, 'DECLINE': 62705, 'ANSWER': 104819}
   fabricated(L2fab-L0)@L20           + ['command', 'commands', 'attack', 'Commander', 'defended', 'commander', 'Command', 'reinforced', 'commanding', 'attacking', 'supported', 'leadership']
                                      - ['pedia', 'wikipedia', 'Craigslist']
                                      concept ranks {'unpredictable': 69898, 'uncertain': 108674, 'random': 136951, 'higher': 947, 'DECLINE': 62962, 'ANSWER': 105253}
   leak(leak-L2)@L20                  + []
                                      - ['randint', 'rand', 'initialise', 'randomness', 'freelancer', 'random', 'randomly', 'srand']
                                      concept ranks {'unpredictable': 151239, 'uncertain': 151230, 'random': 151918, 'higher': 50275, 'DECLINE': 72201, 'ANSWER': 58702}
   knowable-unknowable(L2)@L20        + ['trivial', 'Simple', 'ivial', 'charAt']
                                      - ['cyber', 'experimental', 'Cyber', 'Experimental', 'mystical', 'dark', 'ranked', 'forecasting']
                                      concept ranks {'unpredictable': 151926, 'uncertain': 151813, 'random': 148833, 'higher': 151199, 'DECLINE': 139507, 'ANSWER': 4638}
   relevant-irrelevant(L2-L2irr)@L20  + ['optimized', 'optim']
                                      - ['nonexistent', 'irrelevant', 'unrelated', 'nowhere']
                                      concept ranks {'unpredictable': 149229, 'uncertain': 150659, 'random': 150944, 'higher': 707, 'DECLINE': 41518, 'ANSWER': 84225}
   panel(L2-L0)@L25                   + ['Analy', 'Analysis', 'Analytics', 'Anal', 'Alpha', 'Attack']
                                      - ['CURL', 'Cock', 'CSRF', 'legality', 'copyright', 'Colbert', 'copyrighted', 'CORS']
                                      concept ranks {'unpredictable': 21911, 'uncertain': 7401, 'random': 95028, 'higher': 78526, 'DECLINE': 147927, 'ANSWER': 3570}
   fabricated(L2fab-L0)@L25           + ['Analy', 'Analysis', 'Analytics', 'Anal', 'Alpha', 'Attack']
                                      - ['CURL', 'Cock', 'CSRF', 'legality', 'copyright', 'CORS', 'chlor', 'copyrighted']
                                      concept ranks {'unpredictable': 22322, 'uncertain': 7583, 'random': 94579, 'higher': 77679, 'DECLINE': 147946, 'ANSWER': 3644}
   leak(leak-L2)@L25                  + ['victorious', 'surprise', 'victory', 'already', 'outraged', 'winners']
                                      - ['uncertainty', 'uncertain', 'ambiguity', 'GenericType', 'Balancer', 'neither', 'ambiguous', 'Difficulty']
                                      concept ranks {'unpredictable': 151919, 'uncertain': 151932, 'random': 148785, 'higher': 48885, 'DECLINE': 83830, 'ANSWER': 44017}
   knowable-unknowable(L2)@L25        + ['Already']
                                      - ['uncertain', 'uncertainty', 'unpredict', 'III', 'unpredictable', 'undecided', 'neither', 'ineffective']
                                      concept ranks {'unpredictable': 151931, 'uncertain': 151935, 'random': 143431, 'higher': 106211, 'DECLINE': 112984, 'ANSWER': 8472}
   relevant-irrelevant(L2-L2irr)@L25  + ['Analytics', 'Risk', 'Analysis', 'Animal', 'Army', 'Analy']
                                      - ['Constantin', 'CURL', 'Corinthians', 'chlor', 'Christopher', 'Cos', 'Cord', 'Cory']
                                      concept ranks {'unpredictable': 10837, 'uncertain': 6769, 'random': 45465, 'higher': 75528, 'DECLINE': 149023, 'ANSWER': 65634}
   panel(L2-L0)@L31                   + ['Answer', 'Answer', 'answer', 'answer', 'answering', 'ANSW', 'answers', 'answer', 'answered', 'Antwort', 'answers', 'Answers']
                                      - ['requests', 'requests', 'CURL', 'curl', 'disappearing', 'Cla', 'definitely', 'removal']
                                      concept ranks {'unpredictable': 70333, 'uncertain': 29215, 'random': 39090, 'higher': 85837, 'DECLINE': 108353, 'ANSWER': 10}
   fabricated(L2fab-L0)@L31           + ['Answer', 'Answer', 'answer', 'answer', 'answering', 'ANSW', 'answers', 'answer', 'answered', 'Antwort', 'answers', 'Answers']
                                      - ['requests', 'requests', 'CURL', 'curl', 'disappearing', 'Cla', 'definitely', 'Curl']
                                      concept ranks {'unpredictable': 71383, 'uncertain': 29823, 'random': 39600, 'higher': 86737, 'DECLINE': 109539, 'ANSWER': 10}
   leak(leak-L2)@L31                  + ['destruction', 'disaster', 'Aaron', 'tsunami', 'birthday', 'negatively', 'Press', 'Destroy', 'disasters', 'joy', 'AABB', 'rush']
                                      - ['deliber', 'complexType', 'Decision', 'debated', 'ponder', 'undry', 'Thinking']
                                      concept ranks {'unpredictable': 151782, 'uncertain': 151258, 'random': 120951, 'higher': 19226, 'DECLINE': 119162, 'ANSWER': 66144}
   knowable-unknowable(L2)@L31        + ['answered', 'answers', 'answer', 'unary', 'answer', 'annihil', 'answered', 'AssertionError', 'substring', 'tam', 'Answer', 'answers']
                                      - ['BCHP', 'deliber', 'Creek', 'clist', 'Burk', 'debated', 'CALLTYPE', 'CTYPE']
                                      concept ranks {'unpredictable': 151163, 'uncertain': 151573, 'random': 76430, 'higher': 74138, 'DECLINE': 147335, 'ANSWER': 58}
   relevant-irrelevant(L2-L2irr)@L31  + ['Answer', 'answer', 'ANSW', 'Answer', 'answer', 'answer', 'Antwort', 'analyse', 'answering', 'calculate', 'analysed', 'answered']
                                      - ['legality', 'definitely', 'wherever', 'cla', 'permission', 'served', 'confiscated', 'division']
                                      concept ranks {'unpredictable': 28584, 'uncertain': 34614, 'random': 28652, 'higher': 80013, 'DECLINE': 90144, 'ANSWER': 5}
