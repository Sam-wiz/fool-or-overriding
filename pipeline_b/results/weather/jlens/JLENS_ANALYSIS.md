
=== unsloth/Meta-Llama-3.1-8B-Instruct  (layers 32; corpus 64x128 wikitext-103; multi-token concepts: [' unknowable', ' ANSWER', ' DECLINE'])
  J-lens    : valid deep layers 16/16; median FI(real panel) -0.03 [-0.05,-0.01]; FI(fabricated) -0.05; leak control FI +0.42
  logit lens: valid deep layers 16/16; median FI(real panel) +0.14 [+0.13,+0.15]; FI(fabricated) +0.14; leak control FI +0.41
  item level (L2+L2fab, n=80, 33 commit): J-lens readout predicting NOT committing, median AUROC over valid layers 0.70 (range 0.59-0.80)
  Full-vocabulary J-lens readout of condition-difference vectors (alphabetic tokens only; top 12):
   panel(L2-L0)@L13                   + ['unfolding', 'COVID', 'COVID', 'unfore', 'covid', 'impactful', 'crowdfunding', 'Prediction']
                                      - []
                                      concept ranks {'unpredictable': 26, 'uncertain': 54, 'random': 92748, 'higher': 45695, 'DECLINE': 15590, 'ANSWER': 99387}
   fabricated(L2fab-L0)@L13           + ['unfolding', 'COVID', 'COVID', 'unfore', 'covid', 'impactful', 'unpredictable', 'Covid']
                                      - []
                                      concept ranks {'unpredictable': 23, 'uncertain': 59, 'random': 90161, 'higher': 43349, 'DECLINE': 14484, 'ANSWER': 101013}
   leak(leak-L2)@L13                  + ['exampleInputEmail', 'vocab', 'exampleInput', 'EObject', 'jumbotron', 'codegen', 'frauen']
                                      - ['https', 'https', 'http']
                                      concept ranks {'unpredictable': 124693, 'uncertain': 123147, 'random': 127901, 'higher': 94232, 'DECLINE': 98931, 'ANSWER': 76723}
   knowable-unknowable(L2)@L13        + ['ndern', 'ported', 'azzi', 'retty', 'umably', 'ungan', 'curacy', 'pcf', 'upal', 'ancellable', 'ukan', 'rename']
                                      - ['countless', 'many', 'vast', 'world', 'intricate', 'deep', 'deeply', 'narrative']
                                      concept ranks {'unpredictable': 127136, 'uncertain': 126647, 'random': 117399, 'higher': 126141, 'DECLINE': 97473, 'ANSWER': 31434}
   relevant-irrelevant(L2-L2irr)@L13  + ['afterwards', 'lenght', 'intros', 'balancing', 'balances', 'pretty', 'basically', 'thereafter', 'programme', 'initialised', 'jvu', 'really']
                                      - ['Chinese', 'China', 'Iranian', 'Korean', 'French', 'Fortnite', 'Chinese', 'Cuban']
                                      concept ranks {'unpredictable': 28070, 'uncertain': 32812, 'random': 66036, 'higher': 67282, 'DECLINE': 37925, 'ANSWER': 34966}
   panel(L2-L0)@L18                   + ['Valk', 'Alpha', 'Archie', 'Apprent', 'Aristotle', 'Vanilla', 'Avalanche', 'ALPHA', 'Antique', 'Armor', 'alpha', 'anarchist']
                                      - ['bloggers', 'bilingual', 'buses', 'blogger', 'ihan', 'billions', 'BCHP', 'coop']
                                      concept ranks {'unpredictable': 1531, 'uncertain': 1119, 'random': 1815, 'higher': 77178, 'DECLINE': 59158, 'ANSWER': 29616}
   fabricated(L2fab-L0)@L18           + ['Valk', 'Alpha', 'Archie', 'Apprent', 'Vanilla', 'Aristotle', 'Avalanche', 'Antique', 'Armor', 'ALPHA', 'anarchist', 'predictions']
                                      - ['bloggers', 'bilingual', 'buses', 'blogger', 'ihan', 'bisexual', 'BCHP', 'bip']
                                      concept ranks {'unpredictable': 1768, 'uncertain': 1400, 'random': 2406, 'higher': 80102, 'DECLINE': 53553, 'ANSWER': 31378}
   leak(leak-L2)@L18                  + ['elim', 'Elim', 'elimination', 'final', 'eliminated', 'Absolute', 'finale', 'finally', 'triumph', 'nostalgia', 'absolute', 'trium']
                                      - ['random', 'ricerca', 'Unknown', 'unknown', 'randomly', 'generic', 'random', 'Unknown']
                                      concept ranks {'unpredictable': 128190, 'uncertain': 128230, 'random': 128254, 'higher': 21238, 'DECLINE': 6544, 'ANSWER': 79}
   knowable-unknowable(L2)@L18        + ['Ogre', 'Awards', 'straightforward', 'Athletics', 'victorious', 'Assass', 'Assy', 'ArgumentOutOfRangeException', 'Winners', 'Athletic', 'Automatic', 'triumph']
                                      - ['uncertain', 'brainstorm', 'crypt', 'unsure', 'Cipher', 'Crypt', 'Cipher', 'unknown']
                                      concept ranks {'unpredictable': 128244, 'uncertain': 128255, 'random': 127453, 'higher': 62973, 'DECLINE': 7995, 'ANSWER': 79}
   relevant-irrelevant(L2-L2irr)@L18  + ['Autof', 'arithmetic', 'Haupt', 'assault', 'Arithmetic', 'Audi', 'immunity', 'Automotive', 'Andersen', 'autof', 'Auto', 'Assault']
                                      - ['globalization', 'CNN', 'CrossRef', 'international', 'extern', 'external', 'foreign', 'Global']
                                      concept ranks {'unpredictable': 2298, 'uncertain': 233, 'random': 93071, 'higher': 92255, 'DECLINE': 87209, 'ANSWER': 16898}
   panel(L2-L0)@L22                   + ['Anti', 'predictions', 'anarch', 'anarchist', 'Acceler', 'analysis', 'absence', 'predicted', 'anon', 'Analy', 'anticip', 'acceleration']
                                      - ['onica', 'bib', 'ubby', 'hub', 'ika', 'InterruptedException', 'oku', 'BOTH']
                                      concept ranks {'unpredictable': 588, 'uncertain': 1917, 'random': 93, 'higher': 5086, 'DECLINE': 58249, 'ANSWER': 26421}
   fabricated(L2fab-L0)@L22           + ['Anti', 'predictions', 'anarch', 'anarchist', 'Acceler', 'analysis', 'absence', 'predicted', 'Anxiety', 'Analy', 'anticip', 'anticipation']
                                      - ['onica', 'ubby', 'bib', 'hub', 'oku', 'ika', 'InterruptedException', 'BOTH']
                                      concept ranks {'unpredictable': 532, 'uncertain': 1701, 'random': 97, 'higher': 5942, 'DECLINE': 51074, 'ANSWER': 29423}
   leak(leak-L2)@L22                  + ['answers', 'answer', 'answering', 'correct', 'confident', 'answered', 'confirmed', 'elimination', 'victory', 'confidence', 'parallel', 'bold']
                                      - ['memberOf', 'metavar', 'Unknown', 'probe', 'Randall', 'tesy', 'unread', 'LEM']
                                      concept ranks {'unpredictable': 122392, 'uncertain': 124958, 'random': 127247, 'higher': 8463, 'DECLINE': 7266, 'ANSWER': 190}
   knowable-unknowable(L2)@L22        + ['comparisons', 'straightforward', 'comparison', 'easy', 'Comparison', 'answers', 'Automatic', 'autom', 'automatic', 'simple', 'True', 'simplicity']
                                      - ['uncertain', 'unsure', 'uncertainty', 'uncertainties', 'probe', 'Probe', 'ubern', 'probe']
                                      concept ranks {'unpredictable': 128210, 'uncertain': 128255, 'random': 127735, 'higher': 50782, 'DECLINE': 14038, 'ANSWER': 94}
   relevant-irrelevant(L2-L2irr)@L22  + ['Anti', 'Army', 'anti', 'Attack', 'Action', 'attent', 'balanced', 'army', 'Audio', 'anx', 'moderately', 'annoyance']
                                      - ['Luke', 'Luke', 'Chronic', 'Lucas', 'ublik', 'chron', 'Ritch', 'utos']
                                      concept ranks {'unpredictable': 4498, 'uncertain': 5158, 'random': 22026, 'higher': 25937, 'DECLINE': 119676, 'ANSWER': 6798}
   panel(L2-L0)@L27                   + ['ANSW', 'Answer', 'answer', 'Ans', 'ANS', 'answers', 'Answers', 'answering', 'Ans', 'ans', 'ANSI', 'Answer']
                                      - ['ide', 'ilar', 'alic', 'lom', 'rika', 'olve', 'acia', 'getC']
                                      concept ranks {'unpredictable': 18902, 'uncertain': 1191, 'random': 3789, 'higher': 30003, 'DECLINE': 6149, 'ANSWER': 0}
   fabricated(L2fab-L0)@L27           + ['ANSW', 'Answer', 'answer', 'Ans', 'ANS', 'answers', 'Answers', 'answering', 'Ans', 'ans', 'ANSI', 'Answer']
                                      - ['ide', 'ilar', 'alic', 'olve', 'rika', 'lom', 'acia', 'getC']
                                      concept ranks {'unpredictable': 18330, 'uncertain': 1104, 'random': 3937, 'higher': 33652, 'DECLINE': 1960, 'ANSWER': 0}
   leak(leak-L2)@L27                  + ['Answer', 'ANSW', 'answer', 'answered', 'answers', 'Answers', 'decline', 'answering', 'declined', 'Answer', 'declining', 'ANS']
                                      - ['Call', 'Calls', 'Calling', 'calls', 'Call', 'CALL', 'CALL', 'call']
                                      concept ranks {'unpredictable': 123780, 'uncertain': 107944, 'random': 124882, 'higher': 26064, 'DECLINE': 22, 'ANSWER': 1}
   knowable-unknowable(L2)@L27        + ['answer', 'ANS', 'Answer', 'comparisons', 'ANSW', 'asn', 'Comparison', 'comparison', 'answered', 'compares', 'answer', 'comparing']
                                      - ['Call', 'call', 'CALL', 'Call', 'Calls', 'call', 'calls', 'Calls']
                                      concept ranks {'unpredictable': 126247, 'uncertain': 126622, 'random': 114387, 'higher': 1498, 'DECLINE': 78279, 'ANSWER': 4}
   relevant-irrelevant(L2-L2irr)@L27  + ['ANSW', 'Answer', 'ANS', 'answer', 'answers', 'Ans', 'Answers', 'Answer', 'answering', 'answered', 'ans', 'ans']
                                      - ['Decl', 'Decl', 'decl', 'decl', 'decline', 'DECL', 'DECL', 'declaration']
                                      concept ranks {'unpredictable': 50283, 'uncertain': 2166, 'random': 40284, 'higher': 93359, 'DECLINE': 128250, 'ANSWER': 0}

=== Qwen/Qwen3-14B  (layers 40; corpus 64x128 wikitext-103; multi-token concepts: [' unknowable', ' ANSWER', ' DECLINE'])
  J-lens    : valid deep layers 20/20; median FI(real panel) -0.50 [-0.55,-0.46]; FI(fabricated) -0.52; leak control FI +1.02
  logit lens: valid deep layers 20/20; median FI(real panel) -0.50 [-0.57,-0.43]; FI(fabricated) -0.51; leak control FI +1.25
  item level: commitment is 0% on L2/L2fab, no within-condition variation to predict
  Full-vocabulary J-lens readout of condition-difference vectors (alphabetic tokens only; top 12):
   panel(L2-L0)@L16                   + ['benchmark']
                                      - ['mPid', 'PropertyParams']
                                      concept ranks {'unpredictable': 27261, 'uncertain': 103565, 'random': 39922, 'higher': 1176, 'DECLINE': 69348, 'ANSWER': 140501}
   fabricated(L2fab-L0)@L16           + ['benchmark', 'modelling']
                                      - ['mPid', 'PropertyParams', 'FilterWhere', 'principalColumn']
                                      concept ranks {'unpredictable': 28271, 'uncertain': 105132, 'random': 35415, 'higher': 1080, 'DECLINE': 70496, 'ANSWER': 137197}
   leak(leak-L2)@L16                  + ['programmes']
                                      - ['handjob']
                                      concept ranks {'unpredictable': 28328, 'uncertain': 72168, 'random': 95092, 'higher': 18752, 'DECLINE': 101846, 'ANSWER': 74555}
   knowable-unknowable(L2)@L16        + ['manoe', 'kilometres', 'armour', 'rumours', 'defence', 'rather', 'offence']
                                      - []
                                      concept ranks {'unpredictable': 1197, 'uncertain': 6283, 'random': 5612, 'higher': 47452, 'DECLINE': 150676, 'ANSWER': 150753}
   relevant-irrelevant(L2-L2irr)@L16  + []
                                      - ['wars', 'freq', 'viet']
                                      concept ranks {'unpredictable': 119877, 'uncertain': 111050, 'random': 150005, 'higher': 105694, 'DECLINE': 29485, 'ANSWER': 105902}
   panel(L2-L0)@L22                   + ['Mongo', 'confidence', 'assertFalse']
                                      - ['camera', 'iPhone', 'photography', 'photographers', 'video', 'photographer', 'internet', 'photos']
                                      concept ranks {'unpredictable': 95764, 'uncertain': 38268, 'random': 149538, 'higher': 137389, 'DECLINE': 56793, 'ANSWER': 85841}
   fabricated(L2fab-L0)@L22           + ['confidence', 'Mongo', 'assertFalse']
                                      - ['camera', 'iPhone', 'photography', 'video', 'photographers', 'internet', 'smartphone', 'photographer']
                                      concept ranks {'unpredictable': 95719, 'uncertain': 35817, 'random': 149791, 'higher': 137820, 'DECLINE': 56323, 'ANSWER': 90194}
   leak(leak-L2)@L22                  + ['victories', 'successful', 'triumph', 'victorious', 'senal', 'correctness', 'assertTrue', 'PostalCodes']
                                      - ['ugin']
                                      concept ranks {'unpredictable': 131747, 'uncertain': 128761, 'random': 144172, 'higher': 129029, 'DECLINE': 60198, 'ANSWER': 106209}
   knowable-unknowable(L2)@L22        + ['tjejer', 'salopes', 'lesbische', 'Erotische']
                                      - ['deep', 'Deep', 'Abyss', 'Patreon', 'climate', 'Lord', 'visionary', 'ambition']
                                      concept ranks {'unpredictable': 147780, 'uncertain': 138860, 'random': 138158, 'higher': 151229, 'DECLINE': 50003, 'ANSWER': 4354}
   relevant-irrelevant(L2-L2irr)@L22  + ['Bezier']
                                      - ['espionage', 'spies', 'unknown', 'foreign', 'unknow', 'covert', 'indirect', 'suspected']
                                      concept ranks {'unpredictable': 151472, 'uncertain': 151728, 'random': 145202, 'higher': 146006, 'DECLINE': 55026, 'ANSWER': 87658}
   panel(L2-L0)@L28                   + ['abstract', 'extrapol', 'concept', 'prediction', 'conclusion', 'without', 'philosophical', 'interpretation', 'metaphor', 'Concept', 'lack', 'conceptual']
                                      - ['tjejer', 'nuru', 'pornofilm', 'prostitut', 'Cumhur', 'Bbw', 'erotisk', 'lesbische']
                                      concept ranks {'unpredictable': 13, 'uncertain': 484, 'random': 841, 'higher': 13529, 'DECLINE': 37011, 'ANSWER': 21118}
   fabricated(L2fab-L0)@L28           + ['extrapol', 'abstract', 'prediction', 'concept', 'without', 'conclusion', 'interpretation', 'philosophical', 'lack', 'Concept', 'metaphor', 'conceptual']
                                      - ['tjejer', 'nuru', 'pornofilm', 'prostitut', 'Cumhur', 'Bbw', 'erotisk', 'Geile']
                                      concept ranks {'unpredictable': 13, 'uncertain': 386, 'random': 1003, 'higher': 12827, 'DECLINE': 36819, 'ANSWER': 22546}
   leak(leak-L2)@L28                  + ['compare', 'comparing', 'compare', 'already', 'already', 'comparison', 'Comparison', 'comparisons', 'compares', 'Compar', 'Compare', 'comparison']
                                      - ['unknown', 'Unknown', 'uncertain', 'inability', 'UNKNOWN', 'uncertainty', 'unspecified', 'unpredict']
                                      concept ranks {'unpredictable': 151903, 'uncertain': 151930, 'random': 150657, 'higher': 39242, 'DECLINE': 115712, 'ANSWER': 115481}
   knowable-unknowable(L2)@L28        + ['Immediate', 'simple', 'immediate', 'thumbs', 'instantly']
                                      - ['uncertain', 'unknown', 'uncertainty', 'speculative', 'unpredict', 'Unknown', 'unpredictable', 'uncertainties']
                                      concept ranks {'unpredictable': 151925, 'uncertain': 151935, 'random': 144150, 'higher': 102802, 'DECLINE': 79456, 'ANSWER': 3228}
   relevant-irrelevant(L2-L2irr)@L28  + ['prediction', 'predictions', 'Prediction', 'predicting', 'forecast', 'Predict', 'predictive', 'predicted', 'predict', 'Predict', 'Prediction', 'predicts']
                                      - ['prostitut', 'lesbische', 'tjejer', 'najb']
                                      concept ranks {'unpredictable': 90, 'uncertain': 3144, 'random': 2448, 'higher': 20844, 'DECLINE': 138227, 'ANSWER': 111070}
   panel(L2-L0)@L34                   + ['decl', 'Decl', 'DECL', 'decl', 'Decl', 'decline', 'uncertainty', 'DECL', 'declines', 'declaration', 'unable', 'Unable']
                                      - ['pios', 'ballot', 'updated', 'obutton', 'obar']
                                      concept ranks {'unpredictable': 3978, 'uncertain': 26, 'random': 142992, 'higher': 110359, 'DECLINE': 3, 'ANSWER': 1562}
   fabricated(L2fab-L0)@L34           + ['decl', 'DECL', 'Decl', 'decl', 'Decl', 'decline', 'uncertainty', 'DECL', 'declines', 'declaration', 'unable', 'Unable']
                                      - ['obutton', 'ballot', 'pios', 'updated', 'obar']
                                      concept ranks {'unpredictable': 3801, 'uncertain': 24, 'random': 143357, 'higher': 109544, 'DECLINE': 1, 'ANSWER': 1542}
   leak(leak-L2)@L34                  + ['ACE', 'Arthur', 'Aleks', 'adders', 'alpha', 'Alberta']
                                      - ['inability', 'uncertainty', 'unable', 'uncertain', 'cannot', 'unknown', 'unclear', 'descon']
                                      concept ranks {'unpredictable': 151792, 'uncertain': 151928, 'random': 110450, 'higher': 84112, 'DECLINE': 119720, 'ANSWER': 1383}
   knowable-unknowable(L2)@L34        + ['erotisk', 'spath', 'authenticate', 'adders']
                                      - ['inability', 'uncertainty', 'unable', 'uncertain', 'cannot', 'incap', 'incapable', 'Unable']
                                      concept ranks {'unpredictable': 151547, 'uncertain': 151930, 'random': 53980, 'higher': 86672, 'DECLINE': 148111, 'ANSWER': 462}
   relevant-irrelevant(L2-L2irr)@L34  + ['decl', 'Decl', 'Predict', 'Declared', 'forecasts', 'Decl', 'forecast', 'uncertainty', 'Predict', 'DECLARE', 'predict', 'forecast']
                                      - ['invalid', 'missing', 'transferring', 'transfer', 'cross', 'untrue', 'foreign', 'invalid']
                                      concept ranks {'unpredictable': 1613, 'uncertain': 38, 'random': 130976, 'higher': 103732, 'DECLINE': 25, 'ANSWER': 5599}

=== Qwen/Qwen3-8B  (layers 36; corpus 64x128 wikitext-103; multi-token concepts: [' unknowable', ' ANSWER', ' DECLINE'])
  J-lens    : valid deep layers 18/18; median FI(real panel) -0.11 [-0.14,-0.09]; FI(fabricated) -0.11; leak control FI +0.63
  logit lens: valid deep layers 18/18; median FI(real panel) -0.05 [-0.08,-0.02]; FI(fabricated) -0.01; leak control FI +0.66
  item level (L2+L2fab, n=80, 14 commit): J-lens readout predicting NOT committing, median AUROC over valid layers 0.66 (range 0.45-0.88)
  Full-vocabulary J-lens readout of condition-difference vectors (alphabetic tokens only; top 12):
   panel(L2-L0)@L14                   + []
                                      - []
                                      concept ranks {'unpredictable': 809, 'uncertain': 90368, 'random': 2356, 'higher': 30457, 'DECLINE': 62247, 'ANSWER': 118526}
   fabricated(L2fab-L0)@L14           + []
                                      - []
                                      concept ranks {'unpredictable': 852, 'uncertain': 100178, 'random': 2974, 'higher': 33599, 'DECLINE': 67473, 'ANSWER': 121040}
   leak(leak-L2)@L14                  + []
                                      - ['REALLY', 'crappy', 'doesnt']
                                      concept ranks {'unpredictable': 71500, 'uncertain': 12566, 'random': 26939, 'higher': 5651, 'DECLINE': 97810, 'ANSWER': 99404}
   knowable-unknowable(L2)@L14        + ['members', 'French', 'Canadian', 'language', 'different', 'memory', 'records', 'mistake', 'official', 'police', 'episode', 'British']
                                      - []
                                      concept ranks {'unpredictable': 61339, 'uncertain': 12116, 'random': 3428, 'higher': 2339, 'DECLINE': 94635, 'ANSWER': 123439}
   relevant-irrelevant(L2-L2irr)@L14  + ['Colour', 'initialise']
                                      - []
                                      concept ranks {'unpredictable': 110333, 'uncertain': 57777, 'random': 41746, 'higher': 137297, 'DECLINE': 116555, 'ANSWER': 148318}
   panel(L2-L0)@L20                   + ['only', 'nothing', 'none', 'neither', 'remaining', 'not', 'lack', 'alone', 'missing', 'command', 'even', 'symbol']
                                      - ['pedia', 'twitter', 'Tweets', 'Craigslist']
                                      concept ranks {'unpredictable': 2181, 'uncertain': 8307, 'random': 9873, 'higher': 2250, 'DECLINE': 49976, 'ANSWER': 125684}
   fabricated(L2fab-L0)@L20           + ['only', 'nothing', 'none', 'neither', 'lack', 'remaining', 'not', 'alone', 'rejected', 'missing', 'command', 'even']
                                      - ['Tweets', 'pedia', 'twitter', 'Craigslist']
                                      concept ranks {'unpredictable': 2641, 'uncertain': 9784, 'random': 11032, 'higher': 2410, 'DECLINE': 50093, 'ANSWER': 124552}
   leak(leak-L2)@L20                  + ['amat', 'Duplicate', 'bonus', 'verbatim']
                                      - ['unreliable', 'uncertain', 'unpredict', 'failed', 'unpredictable', 'failures', 'failure', 'undefined']
                                      concept ranks {'unpredictable': 151930, 'uncertain': 151934, 'random': 151863, 'higher': 114786, 'DECLINE': 88166, 'ANSWER': 14809}
   knowable-unknowable(L2)@L20        + ['Simple', 'GetSize', 'seperate', 'ivial']
                                      - ['unpredict', 'unpredictable', 'uncertain', 'attempts', 'unreliable', 'mystical', 'cyber', 'forecasting']
                                      concept ranks {'unpredictable': 151934, 'uncertain': 151933, 'random': 149215, 'higher': 150773, 'DECLINE': 124924, 'ANSWER': 4404}
   relevant-irrelevant(L2-L2irr)@L20  + ['upgrade', 'upgraded', 'upgrades']
                                      - ['nonexistent', 'irrelevant', 'pointless', 'nonsense', 'absurd', 'bizarre']
                                      concept ranks {'unpredictable': 142092, 'uncertain': 127887, 'random': 130291, 'higher': 82, 'DECLINE': 123052, 'ANSWER': 138285}
   panel(L2-L0)@L25                   + ['neither', 'answers', 'Neither', 'answering', 'answer', 'unanswered', 'Undefined', 'denying', 'denies', 'Undefined', 'denial', 'Neither']
                                      - ['Google', 'Google', 'Bluetooth', 'Bike', 'Bluetooth', 'Bible', 'CrossRef', 'BILL']
                                      concept ranks {'unpredictable': 21932, 'uncertain': 3656, 'random': 135205, 'higher': 113819, 'DECLINE': 4118, 'ANSWER': 3702}
   fabricated(L2fab-L0)@L25           + ['answers', 'neither', 'answering', 'Neither', 'answer', 'unanswered', 'denying', 'denies', 'Undefined', 'Neither', 'denial']
                                      - ['Google', 'Google', 'Bluetooth', 'Bike', 'Bluetooth', 'CrossRef', 'Bible', 'HTTPRequest']
                                      concept ranks {'unpredictable': 25736, 'uncertain': 4270, 'random': 137384, 'higher': 115498, 'DECLINE': 4649, 'ANSWER': 2845}
   leak(leak-L2)@L25                  + []
                                      - ['uncertainty', 'uncertain', 'Crypt', 'Clim', 'unavailable', 'Chlor', 'III', 'BCHP']
                                      concept ranks {'unpredictable': 151848, 'uncertain': 151934, 'random': 137998, 'higher': 76199, 'DECLINE': 149558, 'ANSWER': 47977}
   knowable-unknowable(L2)@L25        + ['affirmative', 'Positive', 'Accessories']
                                      - ['uncertain', 'uncertainty', 'neither', 'predicting', 'unpredict', 'doubtful', 'progn', 'conject']
                                      concept ranks {'unpredictable': 151890, 'uncertain': 151935, 'random': 135837, 'higher': 71235, 'DECLINE': 150730, 'ANSWER': 24491}
   relevant-irrelevant(L2-L2irr)@L25  + ['Analytics', 'Prediction', 'Predict', 'undecided', 'Prediction', 'analysts', 'predictive', 'Analysis', 'Predict', 'predictions', 'Analy', 'Beat']
                                      - ['ColumnType', 'cocci', 'chapters', 'Cristina', 'Constantin', 'continents', 'CrLf', 'Chapter']
                                      concept ranks {'unpredictable': 589, 'uncertain': 41, 'random': 11042, 'higher': 33676, 'DECLINE': 141605, 'ANSWER': 45023}
   panel(L2-L0)@L31                   + ['decline', 'declines', 'answering', 'Decl', 'declined', 'Decl', 'declining', 'decl', 'DECL', 'answer', 'decl', 'decay']
                                      - ['CALL', 'calls', 'calls', 'call', 'CALL', 'calling', 'Call', 'Calls']
                                      concept ranks {'unpredictable': 37448, 'uncertain': 50633, 'random': 58304, 'higher': 83968, 'DECLINE': 39, 'ANSWER': 792}
   fabricated(L2fab-L0)@L31           + ['decline', 'answering', 'declines', 'declined', 'Decl', 'Decl', 'declining', 'answer', 'DECL', 'decl', 'answers', 'Answer']
                                      - ['CALL', 'calls', 'calls', 'call', 'calling', 'CALL', 'Call', 'Calls']
                                      concept ranks {'unpredictable': 40568, 'uncertain': 54643, 'random': 61378, 'higher': 84962, 'DECLINE': 44, 'ANSWER': 523}
   leak(leak-L2)@L31                  + ['answered', 'substring', 'answer', 'JSONArray', 'answers', 'Answer', 'answer']
                                      - ['BCHP', 'CRYPT', 'croft', 'Burk', 'CTYPE', 'classification', 'CAA', 'clist']
                                      concept ranks {'unpredictable': 151447, 'uncertain': 149705, 'random': 72431, 'higher': 34476, 'DECLINE': 151310, 'ANSWER': 39}
   knowable-unknowable(L2)@L31        + ['answer', 'answered', 'JSONArray', 'affirmative', 'JSONArray', 'Answer', 'answer', 'substring', 'answers', 'Answer', 'accumulator']
                                      - ['BCHP', 'Burk', 'Clim', 'Cbd', 'Decl', 'clist', 'CRYPT', 'ocale']
                                      concept ranks {'unpredictable': 151427, 'uncertain': 151131, 'random': 69587, 'higher': 33996, 'DECLINE': 151873, 'ANSWER': 55}
   relevant-irrelevant(L2-L2irr)@L31  + ['Answer', 'answering', 'Answer', 'answer', 'answer', 'ANSW', 'calculate', 'analytics', 'predictive', 'Analytics', 'Analytics', 'analyze']
                                      - ['definitely', 'legality', 'phans', 'permission', 'Disallow', 'confiscated', 'restrictions', 'certainly']
                                      concept ranks {'unpredictable': 945, 'uncertain': 763, 'random': 1710, 'higher': 29685, 'DECLINE': 36155, 'ANSWER': 7}
