
=== allenai/OLMo-2-1124-7B-Instruct  (layers 32; corpus 64x128 wikitext-103; multi-token concepts: [' unknowable', ' ANSWER', ' DECLINE'])
  J-lens    : valid deep layers 16/16; median FI(real panel) +0.62 [+0.60,+0.63]; FI(fabricated) +0.62; leak control FI +0.70
  logit lens: valid deep layers 16/16; median FI(real panel) +0.53 [+0.52,+0.55]; FI(fabricated) +0.53; leak control FI +0.71
  item level: commitment is 0% on L2/L2fab, no within-condition variation to predict
  Full-vocabulary J-lens readout of condition-difference vectors (alphabetic tokens only; top 12):
   panel(L2-L0)@L13                   + ['vampire', 'suicide', 'zombie', 'pand', 'supernatural', 'ich', 'undead', 'tsunami', 'suicidal', 'demonic', 'dying', 'disabled']
                                      - ['adro', 'edor', 'iture', 'furt', 'Positioned', 'Prefix', 'osit', 'Exterior']
                                      concept ranks {'unpredictable': 3083, 'uncertain': 59139, 'random': 11379, 'higher': 22193, 'DECLINE': 81728, 'ANSWER': 85408}
   fabricated(L2fab-L0)@L13           + ['vampire', 'suicide', 'zombie', 'pand', 'supernatural', 'ich', 'tsunami', 'undead', 'demonic', 'mang', 'dying', 'suicidal']
                                      - ['adro', 'edor', 'iture', 'Positioned', 'furt', 'Occurred', 'Prefix', 'resa']
                                      concept ranks {'unpredictable': 3399, 'uncertain': 61664, 'random': 12964, 'higher': 22193, 'DECLINE': 82463, 'ANSWER': 86049}
   leak(leak-L2)@L13                  + ['ecz', 'QUI', 'kla']
                                      - ['twins', 'Summer', 'rebels', 'Crystal', 'Venus', 'Plane', 'ioc', 'Lux']
                                      concept ranks {'unpredictable': 95680, 'uncertain': 80292, 'random': 99778, 'higher': 82228, 'DECLINE': 22970, 'ANSWER': 67801}
   knowable-unknowable(L2)@L13        + ['visually', 'maximizing', 'leveraging', 'whisk', 'graceful', 'gracefully', 'concurrently', 'accessor', 'optimizing', 'flipping', 'Netflix', 'simultaneously']
                                      - ['infos', 'fea', 'WebKit', 'unread', 'mailbox', 'zimmer', 'Repositories', 'Sharper']
                                      concept ranks {'unpredictable': 6137, 'uncertain': 27323, 'random': 12885, 'higher': 16398, 'DECLINE': 37228, 'ANSWER': 86045}
   relevant-irrelevant(L2-L2irr)@L13  + ['numerous', 'toastr', 'constant', 'many', 'across', 'far', 'nors', 'tribes', 'direct', 'spreading', 'each', 'onto']
                                      - ['rende', 'ellipsis', 'gatsby']
                                      concept ranks {'unpredictable': 5841, 'uncertain': 1560, 'random': 2370, 'higher': 2430, 'DECLINE': 56917, 'ANSWER': 47770}
   panel(L2-L0)@L18                   + ['sterile', 'aur', 'Dick', 'ahr', 'eniable', 'interpreter', 'Arlington', 'Mak', 'Mandal', 'Greene', 'interpre', 'SCR']
                                      - ['Sms', 'irut', 'Bloody', 'ulti', 'DETAIL', 'Animating', 'Debe', 'pth']
                                      concept ranks {'unpredictable': 46554, 'uncertain': 87021, 'random': 25978, 'higher': 40045, 'DECLINE': 56265, 'ANSWER': 45953}
   fabricated(L2fab-L0)@L18           + ['sterile', 'aur', 'Dick', 'ahr', 'Arlington', 'interpreter', 'eniable', 'Mak', 'Mandal', 'interpre', 'SCR', 'ender']
                                      - ['Sms', 'irut', 'Bloody', 'ulti', 'DETAIL', 'Debe', 'Animating', 'pth']
                                      concept ranks {'unpredictable': 48382, 'uncertain': 87095, 'random': 26821, 'higher': 39967, 'DECLINE': 57216, 'ANSWER': 46953}
   leak(leak-L2)@L18                  + ['elen', 'iliki', 'mpl', 'ordin', 'quist', 'imon', 'redi', 'nik', 'urst', 'ensi', 'UCK', 'imenti']
                                      - ['Compat', 'Reform', 'Noir', 'Oasis', 'Sciences', 'Bau', 'valor', 'intervention']
                                      concept ranks {'unpredictable': 10439, 'uncertain': 41450, 'random': 54337, 'higher': 41512, 'DECLINE': 14184, 'ANSWER': 54417}
   knowable-unknowable(L2)@L18        + ['iben', 'BOTTOM', 'loung', 'traffic', 'REFER', 'Traffic', 'ayar', 'iani', 'Lane', 'Comparison', 'swinging', 'Traffic']
                                      - ['Higgins', 'bara', 'Mandal', 'bard', 'das', 'dae', 'fter', 'ipc']
                                      concept ranks {'unpredictable': 98515, 'uncertain': 77631, 'random': 27879, 'higher': 18679, 'DECLINE': 4686, 'ANSWER': 20218}
   relevant-irrelevant(L2-L2irr)@L18  + ['inh', 'igli', 'FINITY', 'iron', 'byss', 'utan', 'iant', 'oft', 'eten', 'PLY', 'hopeful', 'Thorn']
                                      - ['aco', 'til', 'ircular', 'Til', 'Sed', 'papel', 'isclosed', 'adipiscing']
                                      concept ranks {'unpredictable': 70026, 'uncertain': 46634, 'random': 5169, 'higher': 7993, 'DECLINE': 88539, 'ANSWER': 6052}
   panel(L2-L0)@L22                   + ['ovsky', 'edad', 'exion', 'ktor', 'umbn', 'uni', 'antd', 'ORM', 'ocy', 'ollen', 'iten', 'roman']
                                      - ['undef', 'deferred', 'undefined', 'sorted', 'Algeria', 'dispatch', 'Gen', 'gen']
                                      concept ranks {'unpredictable': 90897, 'uncertain': 99914, 'random': 84056, 'higher': 65137, 'DECLINE': 53148, 'ANSWER': 15055}
   fabricated(L2fab-L0)@L22           + ['ovsky', 'exion', 'edad', 'ktor', 'umbn', 'uni', 'antd', 'ocy', 'ORM', 'iten', 'ollen', 'roman']
                                      - ['undef', 'deferred', 'undefined', 'sorted', 'Algeria', 'dispatch', 'Gen', 'gen']
                                      concept ranks {'unpredictable': 91238, 'uncertain': 99936, 'random': 84319, 'higher': 65808, 'DECLINE': 52787, 'ANSWER': 15330}
   leak(leak-L2)@L22                  + ['Spoon', 'Scrap', 'Workbook', 'resh', 'Pell', 'quivo', 'lief', 'Deprecated', 'excer', 'opleft', 'Hint', 'misd']
                                      - ['Sass', 'anken', 'fusion', 'antis', 'Meta', 'AINS', 'assin', 'evalu']
                                      concept ranks {'unpredictable': 96183, 'uncertain': 99254, 'random': 96319, 'higher': 4347, 'DECLINE': 59918, 'ANSWER': 19099}
   knowable-unknowable(L2)@L22        + ['fel', 'elocity', 'sequ', 'proof', 'Confirmed', 'facts', 'confirmed', 'Pictures', 'Hostname', 'Confirm', 'Exactly', 'JNI']
                                      - ['reds', 'ocas', 'cerc', 'asiat', 'tica', 'plais', 'unpredict', 'isas']
                                      concept ranks {'unpredictable': 100340, 'uncertain': 99946, 'random': 80553, 'higher': 20671, 'DECLINE': 54529, 'ANSWER': 17969}
   relevant-irrelevant(L2-L2irr)@L22  + ['fase', 'igon', 'ardown', 'Worship', 'ahren', 'thresh', 'fst', 'preci', 'ointed', 'bestos', 'opc', 'ourg']
                                      - ['lacking', 'SPEC', 'acho', 'errone', 'manga', 'IFE', 'Clar', 'requesting']
                                      concept ranks {'unpredictable': 98847, 'uncertain': 98712, 'random': 82275, 'higher': 32363, 'DECLINE': 55028, 'ANSWER': 63064}
   panel(L2-L0)@L27                   + ['Probability', 'Anal', 'Probability', 'probability', 'Anal', 'rts', 'probabilities', 'Analysis', 'probability', 'Analy', 'Ans', 'analyze']
                                      - ['deleg', 'delegation', 'deferred', 'appointment', 'appointments', 'requis', 'Burlington', 'Mercer']
                                      concept ranks {'unpredictable': 60890, 'uncertain': 86369, 'random': 70394, 'higher': 18823, 'DECLINE': 98047, 'ANSWER': 90}
   fabricated(L2fab-L0)@L27           + ['Anal', 'Probability', 'Probability', 'probability', 'Anal', 'rts', 'probabilities', 'Analysis', 'probability', 'Analy', 'Ans', 'analyze']
                                      - ['deleg', 'delegation', 'deferred', 'appointment', 'appointments', 'requis', 'Burlington', 'Mercer']
                                      concept ranks {'unpredictable': 61029, 'uncertain': 86561, 'random': 70917, 'higher': 19091, 'DECLINE': 97988, 'ANSWER': 84}
   leak(leak-L2)@L27                  + ['Web', 'Web', 'web', 'ledge', 'Carm', 'ursion', 'Choir', 'Cater', 'urdy', 'Quotes', 'lock', 'web']
                                      - ['eval', 'PRESENT', 'evaluating', 'assessing', 'eval', 'Evalu', 'VEST', 'alytics']
                                      concept ranks {'unpredictable': 99943, 'uncertain': 69818, 'random': 88297, 'higher': 4243, 'DECLINE': 53895, 'ANSWER': 45786}
   knowable-unknowable(L2)@L27        + ['Facts', 'Verification', 'confirmation', 'verification', 'Verify', 'yes', 'Verifier', 'facts', 'yes', 'confirmation', 'SPL', 'byname']
                                      - ['predicting', 'Tier', 'unga', 'alloc', 'allocating', 'ETS', 'proprietary', 'ILD']
                                      concept ranks {'unpredictable': 100217, 'uncertain': 98477, 'random': 89864, 'higher': 13017, 'DECLINE': 94471, 'ANSWER': 42735}
   relevant-irrelevant(L2-L2irr)@L27  + ['Armour', 'Ents', 'Assass', 'Deg', 'Kensington', 'McMahon', 'Spo', 'rts', 'recht', 'Same', 'Decay', 'Grave']
                                      - ['web', 'web', 'libero', 'webs', 'CALL', 'olicit', 'UTIL', 'LIB']
                                      concept ranks {'unpredictable': 98256, 'uncertain': 93406, 'random': 66481, 'higher': 76905, 'DECLINE': 33150, 'ANSWER': 1034}

=== Qwen/Qwen2.5-14B-Instruct  (layers 48; corpus 64x128 wikitext-103; multi-token concepts: [' unknowable', ' ANSWER', ' DECLINE'])
  J-lens    : valid deep layers 24/24; median FI(real panel) +0.83 [+0.77,+0.91]; FI(fabricated) +0.83; leak control FI +1.45
  logit lens: valid deep layers 24/24; median FI(real panel) +0.55 [+0.51,+0.60]; FI(fabricated) +0.56; leak control FI +0.96
  item level (L2+L2fab, n=78, 2 commit): J-lens readout predicting NOT committing, median AUROC over valid layers 0.88 (range 0.41-1.00)
  Full-vocabulary J-lens readout of condition-difference vectors (alphabetic tokens only; top 12):
   panel(L2-L0)@L19                   + ['YLeaf', 'IFn', 'onboard', 'FunctionFlags']
                                      - []
                                      concept ranks {'unpredictable': 45569, 'uncertain': 20832, 'random': 6864, 'higher': 7438, 'DECLINE': 43109, 'ANSWER': 130966}
   fabricated(L2fab-L0)@L19           + ['YLeaf', 'IFn', 'onboard', 'FunctionFlags']
                                      - []
                                      concept ranks {'unpredictable': 47106, 'uncertain': 21693, 'random': 7130, 'higher': 8519, 'DECLINE': 42571, 'ANSWER': 130582}
   leak(leak-L2)@L19                  + ['lesbische', 'ragaz', 'fetisch', 'eskort', 'GCBO']
                                      - []
                                      concept ranks {'unpredictable': 129831, 'uncertain': 150922, 'random': 151060, 'higher': 147968, 'DECLINE': 112052, 'ANSWER': 81783}
   knowable-unknowable(L2)@L19        + ['overposting', 'Geile', 'limburg', 'lesbische', 'filmpjes', 'GCBO', 'Erotische', 'pornost', 'erotik', 'Bbw', 'nuru', 'analsex']
                                      - ['the', 'and', 'French', 'with', 'for', 'Paris']
                                      concept ranks {'unpredictable': 139842, 'uncertain': 144465, 'random': 131350, 'higher': 148738, 'DECLINE': 129411, 'ANSWER': 113278}
   relevant-irrelevant(L2-L2irr)@L19  + []
                                      - ['from', 'the', 'Venom']
                                      concept ranks {'unpredictable': 123355, 'uncertain': 129235, 'random': 141281, 'higher': 141034, 'DECLINE': 91695, 'ANSWER': 85326}
   panel(L2-L0)@L26                   + ['bounty', 'elite', 'Elite', 'ranking', 'Bers', 'scoring', 'reward', 'ride', 'kill', 'synced', 'liking', 'stats']
                                      - ['modne', 'limburg', 'Unicode', 'erotik', 'prostitut', 'unicode', 'danmark', 'muschi']
                                      concept ranks {'unpredictable': 32664, 'uncertain': 24698, 'random': 6954, 'higher': 473, 'DECLINE': 115347, 'ANSWER': 47647}
   fabricated(L2fab-L0)@L26           + ['bounty', 'elite', 'Elite', 'ranking', 'scoring', 'Bers', 'ride', 'reward', 'kill', 'synced', 'stats', 'teammate']
                                      - ['modne', 'limburg', 'Unicode', 'erotik', 'prostitut', 'unicode', 'danmark', 'muschi']
                                      concept ranks {'unpredictable': 34117, 'uncertain': 25438, 'random': 7486, 'higher': 471, 'DECLINE': 114887, 'ANSWER': 48020}
   leak(leak-L2)@L26                  + ['ReLU', 'HorizontalAlignment', 'DOUBLE', 'Student', 'Lifetime', 'Separated', 'Unsafe', 'Underground']
                                      - []
                                      concept ranks {'unpredictable': 118660, 'uncertain': 146556, 'random': 150623, 'higher': 113538, 'DECLINE': 104513, 'ANSWER': 60681}
   knowable-unknowable(L2)@L26        + ['incorrect', 'incorrect', 'correct', 'correct', 'Correct', 'accuracy', 'correctly', 'accurate', 'corrections', 'filmpjes']
                                      - ['Creat']
                                      concept ranks {'unpredictable': 150661, 'uncertain': 134763, 'random': 109483, 'higher': 68553, 'DECLINE': 99325, 'ANSWER': 2401}
   relevant-irrelevant(L2-L2irr)@L26  + []
                                      - ['pornost', 'beurette', 'prostitut', 'limburg', 'danmark', 'information', 'vivastreet', 'geography']
                                      concept ranks {'unpredictable': 86492, 'uncertain': 146076, 'random': 84060, 'higher': 32116, 'DECLINE': 138316, 'ANSWER': 150599}
   panel(L2-L0)@L34                   + ['probabil', 'probabilities', 'risky', 'probability', 'risk', 'Probability', 'predictive', 'prediction', 'cautiously', 'moderately', 'Risk', 'risks']
                                      - ['RESET', 'Reset', 'prostituer', 'prostitut']
                                      concept ranks {'unpredictable': 811, 'uncertain': 27, 'random': 630, 'higher': 9596, 'DECLINE': 59608, 'ANSWER': 106191}
   fabricated(L2fab-L0)@L34           + ['probabil', 'probabilities', 'risky', 'probability', 'risk', 'predictive', 'Probability', 'prediction', 'cautiously', 'moderately', 'Risk', 'risks']
                                      - ['RESET', 'Reset', 'prostituer', 'LANGUAGE', 'prostitut']
                                      concept ranks {'unpredictable': 821, 'uncertain': 27, 'random': 663, 'higher': 9845, 'DECLINE': 60614, 'ANSWER': 106419}
   leak(leak-L2)@L34                  + ['already', 'Already', 'deceased', 'death', 'murdered', 'killed', 'murder', 'murdering', 'suicide', 'already', 'cheating', 'euth']
                                      - ['panse', 'Risk', 'uncertainty', 'uncertainties']
                                      concept ranks {'unpredictable': 129851, 'uncertain': 151439, 'random': 145512, 'higher': 40516, 'DECLINE': 91430, 'ANSWER': 1548}
   knowable-unknowable(L2)@L34        + ['simple', 'instantly', 'Comparison', 'Simple', 'memcmp', 'simple', 'SIMPLE', 'simples', 'Simple', 'Already', 'already', 'memcmp']
                                      - ['uncertainty', 'risk', 'caution', 'uncertainties', 'Risk', 'risks', 'cautious', 'uncertain']
                                      concept ranks {'unpredictable': 152006, 'uncertain': 152050, 'random': 151346, 'higher': 112872, 'DECLINE': 65225, 'ANSWER': 61}
   relevant-irrelevant(L2-L2irr)@L34  + ['probabil', 'probability', 'predictions', 'prediction', 'probabilities', 'Probability', 'Probability', 'predictive', 'probability', 'predictions', 'predicted', 'Prob']
                                      - ['unrelated', 'forgetting', 'forgot', 'Forgotten', 'Forgot', 'forgotten', 'forget', 'forgot']
                                      concept ranks {'unpredictable': 822, 'uncertain': 46, 'random': 2943, 'higher': 18964, 'DECLINE': 97663, 'ANSWER': 139206}
   panel(L2-L0)@L41                   + ['ANSW', 'Answer', 'Ans', 'ANN', 'ASA', 'answer', 'Answers', 'ANSI', 'ANS', 'Answer']
                                      - ['SCRI', 'Flat', 'Timestamp', 'Fatal', 'recur', 'Deployment', 'rire', 'Recruitment']
                                      concept ranks {'unpredictable': 10379, 'uncertain': 614, 'random': 10314, 'higher': 6613, 'DECLINE': 148178, 'ANSWER': 1}
   fabricated(L2fab-L0)@L41           + ['ANSW', 'Answer', 'Ans', 'ASA', 'ANN', 'answer', 'Answers', 'ANSI', 'ANS', 'Answer']
                                      - ['SCRI', 'Flat', 'Timestamp', 'Fatal', 'recur', 'Deployment', 'rire', 'DateTime']
                                      concept ranks {'unpredictable': 10495, 'uncertain': 637, 'random': 10637, 'higher': 6690, 'DECLINE': 148267, 'ANSWER': 1}
   leak(leak-L2)@L41                  + ['Answer', 'ANSW', 'answer', 'answered', 'Antwort', 'Auschwitz', 'Answer', 'Answers', 'answering', 'answers', 'answered', 'answer']
                                      - ['risk', 'risks', 'risk', 'Risk', 'uncertainties', 'uncertainty', 'consultations', 'requestOptions']
                                      concept ranks {'unpredictable': 145394, 'uncertain': 151999, 'random': 135364, 'higher': 45925, 'DECLINE': 75201, 'ANSWER': 1}
   knowable-unknowable(L2)@L41        + ['ANSW', 'Antwort', 'nuru', 'Answer', 'Aaron', 'answered', 'Answer', 'Ago', 'answered', 'utrecht', 'Audrey', 'Aaron']
                                      - ['uncertainty', 'risk', 'risks', 'cautious', 'uncertain', 'reluctance', 'cautiously', 'unreliable']
                                      concept ranks {'unpredictable': 151820, 'uncertain': 152057, 'random': 147198, 'higher': 146098, 'DECLINE': 149224, 'ANSWER': 2}
   relevant-irrelevant(L2-L2irr)@L41  + ['ANSW', 'Answer', 'Answer', 'Ans', 'ANS', 'answer', 'ASA', 'Answers', 'Ans', 'ASN', 'ANSI', 'answer']
                                      - ['LIBINT', 'SCRI', 'icolon', 'rire', 'ivate', 'overe', 'Reject', 'reject']
                                      concept ranks {'unpredictable': 6230, 'uncertain': 642, 'random': 12853, 'higher': 9197, 'DECLINE': 151146, 'ANSWER': 0}

=== Qwen/Qwen2.5-3B-Instruct  (layers 36; corpus 64x128 wikitext-103; multi-token concepts: [' unknowable', ' ANSWER', ' DECLINE'])
  J-lens    : valid deep layers 18/18; median FI(real panel) +0.47 [+0.46,+0.56]; FI(fabricated) +0.50; leak control FI +0.89
  logit lens: valid deep layers 18/18; median FI(real panel) +0.35 [+0.25,+0.40]; FI(fabricated) +0.36; leak control FI +0.63
  Full-vocabulary J-lens readout of condition-difference vectors (alphabetic tokens only; top 12):
   panel(L2-L0)@L14                   + []
                                      - []
                                      concept ranks {'unpredictable': 91115, 'uncertain': 33744, 'random': 59165, 'higher': 44635, 'DECLINE': 775, 'ANSWER': 621}
   fabricated(L2fab-L0)@L14           + []
                                      - []
                                      concept ranks {'unpredictable': 91717, 'uncertain': 34869, 'random': 60316, 'higher': 45400, 'DECLINE': 777, 'ANSWER': 598}
   leak(leak-L2)@L14                  + []
                                      - ['equipments', 'itoris']
                                      concept ranks {'unpredictable': 73144, 'uncertain': 59694, 'random': 93617, 'higher': 103054, 'DECLINE': 10150, 'ANSWER': 3616}
   knowable-unknowable(L2)@L14        + []
                                      - []
                                      concept ranks {'unpredictable': 139700, 'uncertain': 140474, 'random': 85675, 'higher': 139369, 'DECLINE': 112491, 'ANSWER': 81155}
   relevant-irrelevant(L2-L2irr)@L14  + []
                                      - ['AIDS', 'HIV', 'IRA', 'TAX']
                                      concept ranks {'unpredictable': 143276, 'uncertain': 140459, 'random': 96097, 'higher': 100254, 'DECLINE': 104395, 'ANSWER': 145211}
   panel(L2-L0)@L20                   + ['kans', 'sak', 'hiba', 'iece', 'iju', 'umi', 'pei', 'itsu', 'elim', 'prelim', 'overseas']
                                      - []
                                      concept ranks {'unpredictable': 57953, 'uncertain': 41381, 'random': 47141, 'higher': 14914, 'DECLINE': 15621, 'ANSWER': 11768}
   fabricated(L2fab-L0)@L20           + ['kans', 'sak', 'hiba', 'iece', 'iju', 'umi', 'elim', 'itsu', 'contents']
                                      - []
                                      concept ranks {'unpredictable': 62023, 'uncertain': 44560, 'random': 45711, 'higher': 17115, 'DECLINE': 14159, 'ANSWER': 9757}
   leak(leak-L2)@L20                  + []
                                      - ['porn', 'porn', 'girls', 'nerd', 'goddess', 'latex', 'cosmic', 'fake']
                                      concept ranks {'unpredictable': 47744, 'uncertain': 62591, 'random': 51475, 'higher': 32778, 'DECLINE': 979, 'ANSWER': 2049}
   knowable-unknowable(L2)@L20        + ['Encryption', 'DLL', 'encryption', 'Solver', 'Solver', 'Password', 'Encrypt', 'Python', 'solver', 'Sudoku', 'Router', 'Workflow']
                                      - []
                                      concept ranks {'unpredictable': 90185, 'uncertain': 90032, 'random': 3839, 'higher': 89171, 'DECLINE': 107182, 'ANSWER': 91747}
   relevant-irrelevant(L2-L2irr)@L20  + []
                                      - []
                                      concept ranks {'unpredictable': 132034, 'uncertain': 103857, 'random': 94362, 'higher': 85704, 'DECLINE': 124625, 'ANSWER': 149727}
   panel(L2-L0)@L25                   + ['renewed', 'final', 'continued', 'additional', 'continue', 'continued', 'add', 'renew', 'renewal', 'fresh', 'again', 'contin']
                                      - []
                                      concept ranks {'unpredictable': 26727, 'uncertain': 23419, 'random': 94392, 'higher': 20030, 'DECLINE': 73327, 'ANSWER': 85032}
   fabricated(L2fab-L0)@L25           + ['renewed', 'continued', 'final', 'additional', 'continue', 'add', 'continued', 'renew', 'again', 'fresh', 'contin', 'renewal']
                                      - []
                                      concept ranks {'unpredictable': 28430, 'uncertain': 25472, 'random': 96207, 'higher': 21895, 'DECLINE': 75158, 'ANSWER': 83823}
   leak(leak-L2)@L25                  + ['graduating', 'death', 'graduation', 'Semester', 'tomorrow', 'expiration', 'death', 'udent', 'curriculum', 'graduates', 'tonight', 'Death']
                                      - []
                                      concept ranks {'unpredictable': 105266, 'uncertain': 106360, 'random': 97592, 'higher': 33859, 'DECLINE': 1055, 'ANSWER': 51235}
   knowable-unknowable(L2)@L25        + ['synced', 'interop', 'decltype', 'syncing', 'Compatible']
                                      - ['rumours', 'pessim', 'future', 'ambitious', 'ageing', 'predictions', 'prospects', 'futuro']
                                      concept ranks {'unpredictable': 148467, 'uncertain': 151450, 'random': 64413, 'higher': 150744, 'DECLINE': 32525, 'ANSWER': 61873}
   relevant-irrelevant(L2-L2irr)@L25  + ['Increment', 'enhancing', 'enhancements', 'Victory', 'victory', 'final', 'incremented', 'Ending', 'Enhanced', 'finishing', 'Minor', 'enhancement']
                                      - ['foreign', 'Foreign']
                                      concept ranks {'unpredictable': 117982, 'uncertain': 66900, 'random': 118019, 'higher': 1806, 'DECLINE': 99701, 'ANSWER': 46542}
   panel(L2-L0)@L31                   + ['Suff', 'uforia', 'Ignore', 'answered', 'OutOfRange', 'Ignore', 'disbelief', 'unanswered', 'insignificant', 'Enumerable', 'uplicates', 'uess']
                                      - []
                                      concept ranks {'unpredictable': 21882, 'uncertain': 5841, 'random': 115689, 'higher': 126106, 'DECLINE': 136515, 'ANSWER': 21473}
   fabricated(L2fab-L0)@L31           + ['Suff', 'uforia', 'Ignore', 'answered', 'OutOfRange', 'Ignore', 'disbelief', 'insignificant', 'unanswered', 'uess', 'uplicates', 'Enumerable']
                                      - []
                                      concept ranks {'unpredictable': 21735, 'uncertain': 5820, 'random': 114169, 'higher': 126511, 'DECLINE': 134861, 'ANSWER': 19142}
   leak(leak-L2)@L31                  + []
                                      - ['answered', 'Partial', 'odable', 'phalt', 'abl', 'INVALID', 'Enumerable', 'Explanation']
                                      concept ranks {'unpredictable': 148932, 'uncertain': 143393, 'random': 132978, 'higher': 11695, 'DECLINE': 75431, 'ANSWER': 151050}
   knowable-unknowable(L2)@L31        + ['Immediate', 'instantaneous', 'safezone', 'instant', 'SUCCESS', 'valid', 'itespace', 'roperty', 'Instant', 'STDOUT', 'instant', 'Ensure']
                                      - ['researching', 'consulting', 'research', 'consultation', 'consultations', 'research', 'researched', 'investigation']
                                      concept ranks {'unpredictable': 133983, 'uncertain': 144037, 'random': 74755, 'higher': 140387, 'DECLINE': 103973, 'ANSWER': 12560}
   relevant-irrelevant(L2-L2irr)@L31  + ['Suff', 'SuccessListener', 'Valid', 'uforia', 'Repair', 'Valid', 'believable', 'Optim', 'positivity', 'achievable', 'Huff', 'valid']
                                      - ['inactive', 'second', 'SECOND']
                                      concept ranks {'unpredictable': 76988, 'uncertain': 77960, 'random': 105313, 'higher': 50442, 'DECLINE': 151880, 'ANSWER': 16040}

=== Qwen/Qwen2.5-7B-Instruct  (layers 28; corpus 64x128 wikitext-103; multi-token concepts: [' unknowable', ' ANSWER', ' DECLINE'])
  J-lens    : valid deep layers 14/14; median FI(real panel) +0.61 [+0.58,+0.64]; FI(fabricated) +0.61; leak control FI +0.84
  logit lens: valid deep layers 14/14; median FI(real panel) +0.36 [+0.34,+0.39]; FI(fabricated) +0.37; leak control FI +0.69
  item level: commitment is 0% on L2/L2fab, no within-condition variation to predict
  Full-vocabulary J-lens readout of condition-difference vectors (alphabetic tokens only; top 12):
   panel(L2-L0)@L11                   + ['centre', 'City', 'urban', 'behaviour', 'CCTV', 'programme', 'Centre']
                                      - ['ypi', 'Netflix', 'olson', 'emd', 'ierge', 'flix', 'anske', 'NFL']
                                      concept ranks {'unpredictable': 39178, 'uncertain': 24909, 'random': 7743, 'higher': 2523, 'DECLINE': 66020, 'ANSWER': 22971}
   fabricated(L2fab-L0)@L11           + ['centre', 'City', 'urban', 'behaviour', 'programme', 'Centre']
                                      - ['ypi', 'Netflix', 'olson', 'emd', 'ierge', 'flix', 'anske']
                                      concept ranks {'unpredictable': 40326, 'uncertain': 25490, 'random': 8187, 'higher': 2731, 'DECLINE': 67100, 'ANSWER': 22587}
   leak(leak-L2)@L11                  + []
                                      - ['PureComponent']
                                      concept ranks {'unpredictable': 8044, 'uncertain': 1912, 'random': 10015, 'higher': 17460, 'DECLINE': 127811, 'ANSWER': 92497}
   knowable-unknowable(L2)@L11        + []
                                      - ['ijd', 'oola']
                                      concept ranks {'unpredictable': 2245, 'uncertain': 14183, 'random': 890, 'higher': 6158, 'DECLINE': 19530, 'ANSWER': 121443}
   relevant-irrelevant(L2-L2irr)@L11  + []
                                      - ['oldem', 'anske', 'emean', 'antro', 'redni', 'Erot', 'etine', 'ammen']
                                      concept ranks {'unpredictable': 49156, 'uncertain': 34055, 'random': 25360, 'higher': 19570, 'DECLINE': 43418, 'ANSWER': 23075}
   panel(L2-L0)@L15                   + ['prediction', 'predicted', 'predicting', 'tactical', 'aggressive', 'predictions', 'optimized', 'Tactical', 'victory', 'predicts', 'target', 'conclusion']
                                      - ['antom', 'ocab', 'iets', 'reso', 'endez', 'anske', 'apanese', 'Angebot']
                                      concept ranks {'unpredictable': 32152, 'uncertain': 36224, 'random': 83340, 'higher': 3971, 'DECLINE': 41970, 'ANSWER': 35539}
   fabricated(L2fab-L0)@L15           + ['prediction', 'predicted', 'predicting', 'tactical', 'predictions', 'aggressive', 'optimized', 'Tactical', 'victory', 'conclusion', 'predicts', 'target']
                                      - ['antom', 'ocab', 'iets', 'reso', 'endez', 'apanese', 'anske', 'Angebot']
                                      concept ranks {'unpredictable': 32432, 'uncertain': 35354, 'random': 85073, 'higher': 4408, 'DECLINE': 42571, 'ANSWER': 32414}
   leak(leak-L2)@L15                  + ['revealing']
                                      - ['PureComponent', 'logan', 'lke', 'marshall', 'htonl', 'IDEO', 'upakan']
                                      concept ranks {'unpredictable': 136721, 'uncertain': 129908, 'random': 95776, 'higher': 114705, 'DECLINE': 101286, 'ANSWER': 34936}
   knowable-unknowable(L2)@L15        + ['verifying', 'evidence', 'confirmation', 'verification', 'clues', 'confusion', 'verified', 'truth', 'verify', 'imposs', 'confirm', 'confirming']
                                      - ['hover', 'ulen', 'utow', 'Investment', 'allocator', 'Investing', 'TOR', 'defenseman']
                                      concept ranks {'unpredictable': 36914, 'uncertain': 12427, 'random': 3440, 'higher': 94912, 'DECLINE': 116998, 'ANSWER': 44156}
   relevant-irrelevant(L2-L2irr)@L15  + ['wounds', 'progression', 'aeda', 'painters', 'combust', 'gele', 'wound', 'graphical', 'damage', 'paint', 'rowable', 'LATED']
                                      - ['toupper', 'uchos', 'ahkan', 'emade']
                                      concept ranks {'unpredictable': 63194, 'uncertain': 51186, 'random': 33931, 'higher': 3339, 'DECLINE': 45770, 'ANSWER': 130253}
   panel(L2-L0)@L20                   + ['caution', 'weaker', 'weak', 'strengths', 'strength', 'cautious', 'weaken', 'retain', 'stronger', 'confidence', 'retaining', 'negative']
                                      - ['unknown', 'unavailable', 'unknown', 'Unknown', 'inaccessible', 'secrecy', 'REQUIRED', 'Unknown']
                                      concept ranks {'unpredictable': 124115, 'uncertain': 84979, 'random': 120529, 'higher': 3446, 'DECLINE': 39289, 'ANSWER': 104708}
   fabricated(L2fab-L0)@L20           + ['caution', 'weaker', 'weak', 'strengths', 'strength', 'weaken', 'cautious', 'retain', 'stronger', 'confidence', 'retaining', 'strength']
                                      - ['unavailable', 'unknown', 'unknown', 'Unknown', 'inaccessible', 'secrecy', 'REQUIRED', 'Unknown']
                                      concept ranks {'unpredictable': 125071, 'uncertain': 84455, 'random': 120423, 'higher': 3347, 'DECLINE': 39715, 'ANSWER': 104556}
   leak(leak-L2)@L20                  + ['backwards', 'final', 'retro', 'reversed', 'retrospect', 'defeated', 'reversal', 'reverse', 'defeat', 'restored', 'finale', 'backward']
                                      - ['uncertainties', 'uncertainty', 'uncertain', 'agnostic', 'weit', 'SizePolicy', 'Unknown', 'unknown']
                                      concept ranks {'unpredictable': 151502, 'uncertain': 152056, 'random': 121790, 'higher': 8486, 'DECLINE': 17253, 'ANSWER': 110715}
   knowable-unknowable(L2)@L20        + ['Difference', 'difference', 'compare', 'straightforward', 'StringComparison', 'difference', 'memcmp', 'obvious', 'Compare', 'differences', 'diferen', 'comparing']
                                      - ['uncertain', 'uncertainty', 'uncertainties', 'speculative', 'unpredictable', 'optimistic', 'unsure', 'cautious']
                                      concept ranks {'unpredictable': 152056, 'uncertain': 152063, 'random': 150925, 'higher': 72939, 'DECLINE': 89397, 'ANSWER': 40838}
   relevant-irrelevant(L2-L2irr)@L20  + ['optimism', 'optimistic', 'prediction', 'risk', 'Confidence', 'confidence', 'risky', 'retains', 'predicted', 'optim', 'balanced', 'testing']
                                      - ['nonexistent', 'unrelated', 'nowhere', 'None', 'issing', 'NotExist']
                                      concept ranks {'unpredictable': 7251, 'uncertain': 5234, 'random': 73336, 'higher': 50, 'DECLINE': 34750, 'ANSWER': 36553}
   panel(L2-L0)@L24                   + ['UsageId', 'moderately', 'atonin', 'cautious', 'indsight', 'biased', 'utomation', 'testim', 'thumbs', 'mildly', 'partial']
                                      - ['CLUDED', 'oday', 'unacceptable', 'Fame', 'denied', 'errmsg', 'unavailable', 'isnan']
                                      concept ranks {'unpredictable': 22212, 'uncertain': 23505, 'random': 128308, 'higher': 76718, 'DECLINE': 135626, 'ANSWER': 77941}
   fabricated(L2fab-L0)@L24           + ['UsageId', 'moderately', 'atonin', 'indsight', 'cautious', 'biased', 'utomation', 'thumbs', 'testim', 'mildly']
                                      - ['CLUDED', 'oday', 'unacceptable', 'Fame', 'denied', 'errmsg', 'unavailable', 'Disallow']
                                      concept ranks {'unpredictable': 21677, 'uncertain': 22293, 'random': 128290, 'higher': 77203, 'DECLINE': 137306, 'ANSWER': 78232}
   leak(leak-L2)@L24                  + ['vind', 'actual', 'reversal', 'victory', 'actually', 'dispro', 'backwards', 'reversed', 'ceipt', 'Victory', 'indsight', 'successes']
                                      - ['call', 'calls', 'call', 'createElement', 'cta', 'aycast', 'uncertainties', 'impan']
                                      concept ranks {'unpredictable': 149626, 'uncertain': 151906, 'random': 142645, 'higher': 549, 'DECLINE': 15688, 'ANSWER': 6051}
   knowable-unknowable(L2)@L24        + ['yes', 'YES', 'answer', 'answer', 'qli', 'Yes', 'answered', 'answered', 'Yes', 'direkt', 'direct', 'YES']
                                      - ['Calls', 'calls', 'uncertain', 'cautiously', 'call', 'uncertainties', 'calling', 'cautious']
                                      concept ranks {'unpredictable': 151892, 'uncertain': 152060, 'random': 144330, 'higher': 31714, 'DECLINE': 131175, 'ANSWER': 142}
   relevant-irrelevant(L2-L2irr)@L24  + ['Calling', 'awakeFromNib', 'Call', 'call', 'calling', 'fastcall', 'called', 'calls', 'Calling', 'Callable', 'CALL', 'Call']
                                      - ['decline', 'refusal', 'refused', 'declined', 'declining', 'refusing', 'rejection', 'declines']
                                      concept ranks {'unpredictable': 3928, 'uncertain': 1984, 'random': 49895, 'higher': 57879, 'DECLINE': 152023, 'ANSWER': 106034}

=== Qwen/Qwen3-4B  (layers 36; corpus 64x128 wikitext-103; multi-token concepts: [' unknowable', ' ANSWER', ' DECLINE'])
  J-lens    : valid deep layers 18/18; median FI(real panel) +0.38 [+0.34,+0.43]; FI(fabricated) +0.41; leak control FI +1.10
  logit lens: valid deep layers 18/18; median FI(real panel) +0.30 [+0.27,+0.33]; FI(fabricated) +0.32; leak control FI +0.82
  Full-vocabulary J-lens readout of condition-difference vectors (alphabetic tokens only; top 12):
   panel(L2-L0)@L14                   + ['minimise', 'honoured', 'favoured', 'favourable', 'realised', 'neighbouring', 'avour', 'favour', 'recognised', 'favourite', 'fulfil', 'favourites']
                                      - []
                                      concept ranks {'unpredictable': 108622, 'uncertain': 127476, 'random': 146838, 'higher': 136249, 'DECLINE': 44998, 'ANSWER': 130344}
   fabricated(L2fab-L0)@L14           + ['minimise', 'honoured', 'favoured', 'favourable', 'neighbouring', 'realised', 'avour', 'favour', 'recognised', 'favourite', 'rumours', 'fulfil']
                                      - []
                                      concept ranks {'unpredictable': 109536, 'uncertain': 127466, 'random': 146825, 'higher': 136037, 'DECLINE': 44862, 'ANSWER': 129475}
   leak(leak-L2)@L14                  + ['GIS']
                                      - ['music', 'voice', 'dream', 'brand', 'her', 'Dream', 'class', 'new']
                                      concept ranks {'unpredictable': 128241, 'uncertain': 90044, 'random': 150230, 'higher': 151702, 'DECLINE': 83112, 'ANSWER': 68019}
   knowable-unknowable(L2)@L14        + []
                                      - ['softmax', 'bucks', 'booze', 'atsby', 'omentum']
                                      concept ranks {'unpredictable': 148943, 'uncertain': 13772, 'random': 18019, 'higher': 5456, 'DECLINE': 76582, 'ANSWER': 135704}
   relevant-irrelevant(L2-L2irr)@L14  + ['radio', 'Kansas', 'maneuvers', 'gray', 'traveling', 'theater', 'Louisville', 'rotating', 'slip', 'moving', 'wisely']
                                      - ['analysed', 'analyse', 'recognise', 'analys', 'recognised']
                                      concept ranks {'unpredictable': 44543, 'uncertain': 19335, 'random': 8479, 'higher': 2579, 'DECLINE': 122779, 'ANSWER': 120838}
   panel(L2-L0)@L20                   + []
                                      - ['photograph', 'igraphy', 'photographs', 'pamph']
                                      concept ranks {'unpredictable': 45073, 'uncertain': 24113, 'random': 142368, 'higher': 41264, 'DECLINE': 8286, 'ANSWER': 24363}
   fabricated(L2fab-L0)@L20           + []
                                      - ['photograph', 'igraphy', 'photographs', 'pamph']
                                      concept ranks {'unpredictable': 44844, 'uncertain': 23113, 'random': 141108, 'higher': 38745, 'DECLINE': 8021, 'ANSWER': 24762}
   leak(leak-L2)@L20                  + ['directly', 'unlocked', 'team', 'immediately', 'leaked', 'victory', 'sequence', 'split', 'revealed', 'winning', 'confirming', 'confirmed']
                                      - []
                                      concept ranks {'unpredictable': 93579, 'uncertain': 103712, 'random': 31220, 'higher': 3986, 'DECLINE': 122967, 'ANSWER': 119313}
   knowable-unknowable(L2)@L20        + ['quick', 'foto', 'camera', 'quickly', 'jpeg', 'click']
                                      - ['despair', 'bleak', 'philosoph', 'Psychological', 'pessim', 'ideologies', 'Attempts', 'desperation']
                                      concept ranks {'unpredictable': 151757, 'uncertain': 151582, 'random': 67670, 'higher': 61184, 'DECLINE': 138930, 'ANSWER': 75271}
   relevant-irrelevant(L2-L2irr)@L20  + ['joy']
                                      - ['lack', 'nonexistent', 'unrelated', 'irrelevant', 'lacks', 'inadequate', 'african', 'bogus']
                                      concept ranks {'unpredictable': 121091, 'uncertain': 139590, 'random': 150009, 'higher': 4003, 'DECLINE': 130470, 'ANSWER': 40392}
   panel(L2-L0)@L25                   + ['Alumni', 'Anthem', 'alumni', 'ActionResult', 'arterial', 'Arts', 'Aires', 'AreaView', 'ambulance', 'america', 'Anal', 'Assass']
                                      - ['copyright', 'Cloud', 'Crypto', 'Cos', 'Crypt', 'Cornel', 'cos', 'Cube']
                                      concept ranks {'unpredictable': 106242, 'uncertain': 114034, 'random': 144757, 'higher': 40291, 'DECLINE': 143180, 'ANSWER': 1988}
   fabricated(L2fab-L0)@L25           + ['Alumni', 'alumni', 'ActionResult', 'Anthem', 'arterial', 'Arts', 'Aires', 'AreaView', 'ambulance', 'Assass', 'airs', 'Anxiety']
                                      - ['copyright', 'Cloud', 'Crypt', 'Crypto', 'Cos', 'Cornel', 'cos', 'Cube']
                                      concept ranks {'unpredictable': 109349, 'uncertain': 118084, 'random': 145690, 'higher': 38926, 'DECLINE': 142987, 'ANSWER': 2025}
   leak(leak-L2)@L25                  + ['triumph', 'victorious', 'victory', 'victories', 'winning', 'trium', 'reversal', 'correct', 'Victory', 'uccess', 'Triumph', 'confirmation']
                                      - ['RANDOM', 'rand', 'uncertain', 'blurry', 'rand', 'rnd', 'unsure', 'getRandom']
                                      concept ranks {'unpredictable': 151718, 'uncertain': 151922, 'random': 151911, 'higher': 28953, 'DECLINE': 94284, 'ANSWER': 3046}
   knowable-unknowable(L2)@L25        + ['triumph', 'confirming', 'confirm', 'Verification', 'confirms', 'confirmation', 'verify', 'verification', 'subtraction', 'confirm', 'verify', 'Confirm']
                                      - ['uncertain', 'tentative', 'cautiously', 'unpredictable', 'uncertainty', 'randomized', 'unsure', 'rnd']
                                      concept ranks {'unpredictable': 151929, 'uncertain': 151935, 'random': 151911, 'higher': 95532, 'DECLINE': 74239, 'ANSWER': 3962}
   relevant-irrelevant(L2-L2irr)@L25  + ['upbeat', 'Appet', 'ambush', 'Ago', 'Alive', 'Air', 'Air', 'AAP', 'Alive', 'airs', 'Oasis', 'Slider']
                                      - ['Cornel', 'COPYING', 'CORS', 'Christopher', 'Claude', 'copyright', 'criminal', 'Criminal']
                                      concept ranks {'unpredictable': 62066, 'uncertain': 112198, 'random': 144790, 'higher': 15830, 'DECLINE': 151195, 'ANSWER': 34587}
   panel(L2-L0)@L31                   + ['Answer', 'Argument', 'Antwort', 'Analysis', 'ANSW', 'Answers', 'Answer', 'Analy', 'Ans', 'Ansi']
                                      - ['chron', 'inaccessible', 'cla', 'Claude', 'cultivation', 'copyright', 'copyright', 'UNC']
                                      concept ranks {'unpredictable': 103208, 'uncertain': 72653, 'random': 61081, 'higher': 39774, 'DECLINE': 151854, 'ANSWER': 11}
   fabricated(L2fab-L0)@L31           + ['Answer', 'Argument', 'Antwort', 'ANSW', 'Answer', 'Answers', 'Analysis', 'Ans', 'Analy', 'Ansi']
                                      - ['inaccessible', 'chron', 'cla', 'cultivation', 'Claude', 'UNC', 'copyright', 'copyright']
                                      concept ranks {'unpredictable': 106422, 'uncertain': 78124, 'random': 66563, 'higher': 37819, 'DECLINE': 151864, 'ANSWER': 9}
   leak(leak-L2)@L31                  + ['triumph', 'answered', 'answers', 'YES', 'Answers', 'Answers', 'TRUE', 'YES', 'successful']
                                      - ['uncertainty', 'uncertain', 'unclear', 'Unc', 'neutrality', 'blurry', 'Unc', 'UNC']
                                      concept ranks {'unpredictable': 151889, 'uncertain': 151932, 'random': 151704, 'higher': 26514, 'DECLINE': 115084, 'ANSWER': 31}
   knowable-unknowable(L2)@L31        + ['answered', 'answered', 'Answers', 'ANSW', 'Answer', 'Answer', 'YES']
                                      - ['uncertainty', 'uncertain', 'Unc', 'cautious', 'speculative', 'cautiously', 'unpredictable', 'uncertainties']
                                      concept ranks {'unpredictable': 151927, 'uncertain': 151933, 'random': 151337, 'higher': 22002, 'DECLINE': 63125, 'ANSWER': 13}
   relevant-irrelevant(L2-L2irr)@L31  + ['Avg', 'Avg', 'avg', 'probabil', 'amino', 'Average', 'balanced', 'Average', 'Balanced', 'banda', 'Amb', 'average']
                                      - ['DECL', 'Carlton', 'Claude', 'CORS', 'CID', 'DECL', 'DEN', 'cret']
                                      concept ranks {'unpredictable': 35188, 'uncertain': 1953, 'random': 85942, 'higher': 7583, 'DECLINE': 151935, 'ANSWER': 2503}

=== unsloth/gemma-2-9b-it  (layers 42; corpus 64x128 wikitext-103; multi-token concepts: [' unknowable', ' DECLINE'])
  J-lens    : valid deep layers 21/21; median FI(real panel) +0.78 [+0.74,+0.82]; FI(fabricated) +0.81; leak control FI +0.73
  logit lens: valid deep layers 21/21; median FI(real panel) +0.73 [+0.68,+0.84]; FI(fabricated) +0.83; leak control FI +1.01
  item level: commitment is 0% on L2/L2fab, no within-condition variation to predict
  Full-vocabulary J-lens readout of condition-difference vectors (alphabetic tokens only; top 12):
   panel(L2-L0)@L17                   + ['SequentialGroup', 'FREE', 'WRONG', 'MEJOR', 'RISK', 'WON', 'GONNA', 'EARLY', 'VERY', 'BUT', 'AWESOME', 'GOAL']
                                      - []
                                      concept ranks {'unpredictable': 23120, 'uncertain': 19654, 'random': 181977, 'higher': 116035, 'DECLINE': 8454, 'ANSWER': 2142}
   fabricated(L2fab-L0)@L17           + ['SequentialGroup', 'FREE', 'MEJOR', 'WRONG', 'RISK', 'WON', 'GONNA', 'VERY', 'AWESOME', 'BUT', 'EARLY', 'DONE']
                                      - []
                                      concept ranks {'unpredictable': 22930, 'uncertain': 21915, 'random': 180516, 'higher': 118372, 'DECLINE': 8923, 'ANSWER': 1978}
   leak(leak-L2)@L17                  + ['autorytatywna', 'exitRule', 'ainfi', 'kaarangay', 'VYMaps', 'plufieurs', 'IBLIO', 'CppMethod', 'surla', 'kasarigan', 'mauva', 'Numerade']
                                      - []
                                      concept ranks {'unpredictable': 251991, 'uncertain': 250140, 'random': 228364, 'higher': 253872, 'DECLINE': 67865, 'ANSWER': 387}
   knowable-unknowable(L2)@L17        + []
                                      - ['our']
                                      concept ranks {'unpredictable': 226415, 'uncertain': 205798, 'random': 227451, 'higher': 169768, 'DECLINE': 133053, 'ANSWER': 117014}
   relevant-irrelevant(L2-L2irr)@L17  + ['gitter', 'womb', 'Wren', 'webbing', 'flutter', 'workspace', 'CFC', 'glider', 'glab', 'Companions', 'cocoon', 'fun']
                                      - []
                                      concept ranks {'unpredictable': 59878, 'uncertain': 27100, 'random': 51415, 'higher': 143286, 'DECLINE': 141969, 'ANSWER': 175346}
   panel(L2-L0)@L23                   + ['INFLUENCE', 'FURTHER', 'WriteTagHelper', 'LOOKS', 'Influence', 'concluding', 'INFLU', 'ADDITIONAL', 'STRENGTH', 'FACTOR', 'ANALYSIS', 'conclusions']
                                      - ['only', 'everyone', 'whichever', 'nullable', 'everyone', 'whatever', 'dowol', 'everybody']
                                      concept ranks {'unpredictable': 61570, 'uncertain': 32001, 'random': 247198, 'higher': 71417, 'DECLINE': 22470, 'ANSWER': 17917}
   fabricated(L2fab-L0)@L23           + ['FURTHER', 'INFLUENCE', 'WriteTagHelper', 'LOOKS', 'concluding', 'Influence', 'ADDITIONAL', 'INFLU', 'STRENGTH', 'FACTOR', 'conclusions', 'ANALYSIS']
                                      - ['only', 'everyone', 'whichever', 'nullable', 'everyone', 'whatever', 'dowol', 'everybody']
                                      concept ranks {'unpredictable': 55860, 'uncertain': 30155, 'random': 245870, 'higher': 70431, 'DECLINE': 23480, 'ANSWER': 17262}
   leak(leak-L2)@L23                  + ['incorrect', 'Correct', 'correct', 'Incorrect', 'correctness', 'Correct', 'incorrectly', 'inaccuracy', 'Wrong', 'erroneous', 'corrects', 'inaccurate']
                                      - []
                                      concept ranks {'unpredictable': 137116, 'uncertain': 176167, 'random': 161484, 'higher': 129442, 'DECLINE': 28736, 'ANSWER': 47133}
   knowable-unknowable(L2)@L23        + ['already', 'Already', 'Already', 'already', 'ALREADY', 'ALREADY', 'redan', 'need', 'preexisting', 'automatically', 'allerede', 'zaten']
                                      - ['idealistic', 'leider', 'ambiti', 'Hoffnung', 'hayal']
                                      concept ranks {'unpredictable': 241494, 'uncertain': 140938, 'random': 20601, 'higher': 180670, 'DECLINE': 144601, 'ANSWER': 18421}
   relevant-irrelevant(L2-L2irr)@L23  + ['final', 'finale', 'fave', 'favored', 'twimg', 'Final', 'analyzed', 'retrospect', 'hanced', 'afterward', 'preview', 'horizontalLayout']
                                      - ['unauthorised', 'Incorrect', 'nvarchar', 'illegal', 'Incorrect', 'manquante', 'ignorance', 'nonexistent']
                                      concept ranks {'unpredictable': 56850, 'uncertain': 88297, 'random': 109345, 'higher': 8563, 'DECLINE': 180995, 'ANSWER': 198215}
   panel(L2-L0)@L29                   + ['propOrder', 'analyze', 'marginally', 'analyse', 'slightly', 'analyzed', 'analyzes', 'analysed', 'SuccessListener', 'Analyze', 'moderately', 'slightly']
                                      - ['Administrativna', 'Completely', 'Completely', 'Reality', 'completely', 'reality', 'completamente', 'totalmente']
                                      concept ranks {'unpredictable': 77765, 'uncertain': 6962, 'random': 36707, 'higher': 130044, 'DECLINE': 166698, 'ANSWER': 8687}
   fabricated(L2fab-L0)@L29           + ['analyze', 'propOrder', 'marginally', 'analyse', 'analyzed', 'slightly', 'analyzes', 'analysed', 'SuccessListener', 'Analyze', 'moderately', 'slightly']
                                      - ['Administrativna', 'Completely', 'Completely', 'Reality', 'completely', 'reality', 'completamente', 'totalmente']
                                      concept ranks {'unpredictable': 78924, 'uncertain': 7355, 'random': 37564, 'higher': 124429, 'DECLINE': 167127, 'ANSWER': 8561}
   leak(leak-L2)@L29                  + ['previous', 'past', 'already', 'information', 'spoilers', 'future', 'spoiler', 'hindsight', 'yesterday', 'Previous', 'Already', 'history']
                                      - ['Complex', 'XmlAccessorType', 'complexity', 'complejos', 'COMPLEX', 'Balancing', 'Balancer', 'COMPLEX']
                                      concept ranks {'unpredictable': 19262, 'uncertain': 219807, 'random': 7735, 'higher': 16009, 'DECLINE': 94294, 'ANSWER': 23008}
   knowable-unknowable(L2)@L29        + ['instantly', 'immediately', 'Immediately', 'immediate', 'instantaneously', 'instant', 'Instantly', 'Immediate', 'Immediately', 'immediately', 'immedi', 'instantaneous']
                                      - ['campuran', 'Complex', 'complejo', 'Mischung', 'borderline', 'complejos', 'COMPLEX', 'complexo']
                                      concept ranks {'unpredictable': 252252, 'uncertain': 255833, 'random': 32455, 'higher': 65514, 'DECLINE': 81156, 'ANSWER': 1478}
   relevant-irrelevant(L2-L2irr)@L29  + ['SuccessListener', 'marginally', 'slightly', 'Slightly', 'slightly', 'analyze', 'analyse', 'slowed', 'Slightly', 'cautious', 'Slow', 'cautiously']
                                      - ['unrelated', 'completely', 'desconoc', 'inapplicable', 'nonexistent', 'incompatibility', 'unconnected', 'desconhe']
                                      concept ranks {'unpredictable': 146216, 'uncertain': 30746, 'random': 133843, 'higher': 97944, 'DECLINE': 237477, 'ANSWER': 56859}
   panel(L2-L0)@L36                   + ['analysis', 'analyze', 'analyzing', 'analyse', 'analysed', 'analysing', 'analyzed', 'analyzes', 'analyser', 'analys', 'Analysis', 'propOrder']
                                      - ['Administrativna', 'DELETE', 'Delete', 'btnDelete', 'boneca', 'DOCTYPE', 'eliminare', 'BLOCK']
                                      concept ranks {'unpredictable': 61598, 'uncertain': 1075, 'random': 36461, 'higher': 159846, 'DECLINE': 255490, 'ANSWER': 96}
   fabricated(L2fab-L0)@L36           + ['analysis', 'analyze', 'analyse', 'analyzing', 'analysed', 'analysing', 'analyzed', 'analyzes', 'analyser', 'analys', 'Analysis', 'propOrder']
                                      - ['Administrativna', 'DELETE', 'Delete', 'btnDelete', 'boneca', 'DOCTYPE', 'eliminare', 'onDelete']
                                      concept ranks {'unpredictable': 64731, 'uncertain': 1152, 'random': 37274, 'higher': 157431, 'DECLINE': 255636, 'ANSWER': 81}
   leak(leak-L2)@L36                  + ['answer', 'Answer', 'past', 'ANSWER', 'Vergangenheit', 'Past', 'decline', 'answered', 'declined', 'ANSWER', 'history', 'Decline']
                                      - ['call', 'Call', 'calls', 'calling', 'Calls', 'call', 'CALL', 'CALL']
                                      concept ranks {'unpredictable': 57202, 'uncertain': 111865, 'random': 83334, 'higher': 57553, 'DECLINE': 337, 'ANSWER': 3}
   knowable-unknowable(L2)@L36        + ['ANSWER', 'Answer', 'answer', 'ANSWER', 'answered', 'answer', 'Answer', 'answered', 'ANSWERS', 'answers', 'answering', 'Answers']
                                      - ['call', 'calls', 'call', 'Call', 'calling', 'Calls', 'Call', 'calling']
                                      concept ranks {'unpredictable': 253723, 'uncertain': 246924, 'random': 144716, 'higher': 106469, 'DECLINE': 218686, 'ANSWER': 0}
   relevant-irrelevant(L2-L2irr)@L36  + ['answer', 'answer', 'Answer', 'ANSWER', 'analysis', 'answering', 'answered', 'Answer', 'Analysis', 'analyzing', 'analyzed', 'analyser']
                                      - ['Decline', 'Decline', 'decline', 'DEC', 'decline', 'DECL', 'decl', 'DEC']
                                      concept ranks {'unpredictable': 125774, 'uncertain': 25526, 'random': 32510, 'higher': 124243, 'DECLINE': 255996, 'ANSWER': 3}

=== unsloth/mistral-7b-instruct-v0.3  (layers 32; corpus 64x128 wikitext-103; multi-token concepts: [' unpredictable', ' unclear', ' speculative', ' unsure', ' unknowable', ' bullish', ' ANSWER', ' DECLINE', ' CALL'])
  J-lens    : valid deep layers 16/16; median FI(real panel) +0.80 [-0.46,+0.93]; FI(fabricated) +0.80; leak control FI +0.64
  logit lens: valid deep layers 16/16; median FI(real panel) +0.52 [+0.37,+0.65]; FI(fabricated) +0.52; leak control FI +0.69
  item level: commitment is 0% on L2/L2fab, no within-condition variation to predict
  Full-vocabulary J-lens readout of condition-difference vectors (alphabetic tokens only; top 12):
   panel(L2-L0)@L13                   + ['abet', 'slider', 'osz', 'lauf', 'kee', 'keit', 'dorf', 'grand', 'odo', 'owo', 'comport', 'hof']
                                      - ['technology', 'technologies', 'projects', 'Technology', 'online', 'Tokyo', 'themselves', 'episodes']
                                      concept ranks {'unpredictable': 24432, 'uncertain': 11774, 'random': 17322, 'higher': 17560, 'DECLINE': 32641, 'ANSWER': 30840}
   fabricated(L2fab-L0)@L13           + ['abet', 'slider', 'osz', 'lauf', 'keit', 'kee', 'dorf', 'odo', 'grand', 'comport', 'hof', 'owo']
                                      - ['technology', 'technologies', 'projects', 'Technology', 'online', 'Tokyo', 'programs', 'themselves']
                                      concept ranks {'unpredictable': 24254, 'uncertain': 11701, 'random': 17636, 'higher': 17619, 'DECLINE': 32649, 'ANSWER': 31017}
   leak(leak-L2)@L13                  + ['cdots', 'Capture', 'versus', 'Figure', 'Hist', 'ldots', 'Horizontal', 'oki', 'Popup']
                                      - ['Ist', 'McK', 'ISBN', 'Edd', 'Ster', 'ved', 'Sver', 'Trade']
                                      concept ranks {'unpredictable': 23773, 'uncertain': 19550, 'random': 22462, 'higher': 18090, 'DECLINE': 28911, 'ANSWER': 30056}
   knowable-unknowable(L2)@L13        + ['error', 'incorrect', 'countryside', 'restored', 'Copyright', 'churches', 'silence', 'grateful', 'indow', 'joy', 'navigation', 'error']
                                      - ['Project', 'prototype', 'concepts', 'ANY', 'PRO', 'Spec', 'project', 'Project']
                                      concept ranks {'unpredictable': 16137, 'uncertain': 14881, 'random': 22755, 'higher': 18797, 'DECLINE': 32579, 'ANSWER': 28536}
   relevant-irrelevant(L2-L2irr)@L13  + ['hero', 'champion', 'sail', 'dude', 'victory', 'landing', 'cheer', 'joy', 'pilot', 'heroes', 'gal', 'football']
                                      - ['possible', 'UNUSED', 'groups', 'unlikely', 'likely', 'EventHandler', 'Hidden', 'Groups']
                                      concept ranks {'unpredictable': 8311, 'uncertain': 31495, 'random': 6294, 'higher': 3018, 'DECLINE': 1679, 'ANSWER': 723}
   panel(L2-L0)@L18                   + ['potentially', 'caution', 'somewhat', 'despite', 'warn', 'ipa', 'alternatives', 'warning', 'disappoint', 'weak', 'negative', 'warnings']
                                      - ['President', 'Chairman', 'Board', 'dedicated', 'dedic', 'Commerce', 'Commission', 'Transaction']
                                      concept ranks {'unpredictable': 13819, 'uncertain': 147, 'random': 344, 'higher': 600, 'DECLINE': 31135, 'ANSWER': 32521}
   fabricated(L2fab-L0)@L18           + ['potentially', 'caution', 'somewhat', 'despite', 'warn', 'negative', 'alternatives', 'ipa', 'warning', 'weak', 'disappoint', 'warnings']
                                      - ['President', 'Chairman', 'Board', 'dedicated', 'dedic', 'Commerce', 'Commission', 'Transaction']
                                      concept ranks {'unpredictable': 13749, 'uncertain': 155, 'random': 331, 'higher': 603, 'DECLINE': 31174, 'ANSWER': 32522}
   leak(leak-L2)@L18                  + ['delet', 'cancellation', 'abandon', 'suicide', 'death', 'fatal', 'removal', 'deaths', 'deleted', 'cancel', 'cancelled', 'eliminated']
                                      - ['Complex', 'needing', 'expanded', 'Random', 'Search', 'expansion', 'requiring', 'expand']
                                      concept ranks {'unpredictable': 2584, 'uncertain': 32729, 'random': 32704, 'higher': 28483, 'DECLINE': 2651, 'ANSWER': 26801}
   knowable-unknowable(L2)@L18        + ['simple', 'straightforward', 'removal', 'delet', 'simplicity', 'simpler', 'removed', 'eliminated', 'killed', 'removing', 'deleted', 'simpl']
                                      - ['ambitious', 'Research', 'research', 'uncertain', 'Future', 'ambit', 'uncertainty', 'Deep']
                                      concept ranks {'unpredictable': 2807, 'uncertain': 32764, 'random': 32358, 'higher': 31805, 'DECLINE': 8054, 'ANSWER': 17004}
   relevant-irrelevant(L2-L2irr)@L18  + ['conservative', 'slowly', 'risk', 'conserv', 'warnings', 'slow', 'traditional', 'increment', 'negative', 'criticism', 'battles', 'worst']
                                      - ['collaboration', 'Detect', 'investig', 'detective', 'investigation', 'Query', 'collabor', 'Bureau']
                                      concept ranks {'unpredictable': 19505, 'uncertain': 20496, 'random': 5831, 'higher': 772, 'DECLINE': 30349, 'ANSWER': 28780}
   panel(L2-L0)@L22                   + ['neither', 'statistical', 'prediction', 'analysis', 'additional', 'possible', 'Analysis', 'possibly', 'partial', 'partially', 'perhaps', 'statistics']
                                      - ['berger', 'Blockly', 'dorf', 'ember', 'Exec', 'Band', 'urn', 'servant']
                                      concept ranks {'unpredictable': 3341, 'uncertain': 41, 'random': 145, 'higher': 294, 'DECLINE': 28412, 'ANSWER': 2385}
   fabricated(L2fab-L0)@L22           + ['neither', 'statistical', 'prediction', 'analysis', 'additional', 'possible', 'Analysis', 'possibly', 'partial', 'partially', 'perhaps', 'statistics']
                                      - ['berger', 'Blockly', 'dorf', 'ember', 'Exec', 'Band', 'servant', 'urn']
                                      concept ranks {'unpredictable': 3339, 'uncertain': 40, 'random': 145, 'higher': 287, 'DECLINE': 28464, 'ANSWER': 2406}
   leak(leak-L2)@L22                  + ['predictions', 'previous', 'prediction', 'predicted', 'previous', 'rejected', 'past', 'forecast', 'predict', 'reject', 'based', 'Pred']
                                      - ['needing', 'Bal', 'balanced', 'bal', 'blanc', 'needed', 'blur', 'Complex']
                                      concept ranks {'unpredictable': 3813, 'uncertain': 29251, 'random': 28222, 'higher': 29935, 'DECLINE': 2291, 'ANSWER': 12137}
   knowable-unknowable(L2)@L22        + ['past', 'previous', 'Past', 'previous', 'FALSE', 'comparing', 'facts', 'irrelevant', 'reject', 'false', 'rejected', 'retro']
                                      - ['balanced', 'blend', 'caut', 'mixed', 'Bal', 'vag', 'blur', 'blanc']
                                      concept ranks {'unpredictable': 4826, 'uncertain': 32758, 'random': 32602, 'higher': 31694, 'DECLINE': 2054, 'ANSWER': 2590}
   relevant-irrelevant(L2-L2irr)@L22  + ['statistical', 'statist', 'statistics', 'predictions', 'stats', 'estimates', 'prediction', 'Aires', 'analys', 'Statistics', 'analy', 'risk']
                                      - ['Bass', 'Bibli', 'Billy', 'World', 'Blue', 'Baltimore', 'Bryan', 'Ctrl']
                                      concept ranks {'unpredictable': 11249, 'uncertain': 3571, 'random': 78, 'higher': 4949, 'DECLINE': 18507, 'ANSWER': 565}
   panel(L2-L0)@L27                   + ['Additional', 'Analysis', 'possible', 'possibly', 'additional', 'analysis', 'more', 'More', 'maybe', 'Optional', 'neutral', 'potentially']
                                      - ['zial', 'urn', 'ember', 'ulum', 'ula', 'Binding', 'swallow', 'smiling']
                                      concept ranks {'unpredictable': 2919, 'uncertain': 26, 'random': 630, 'higher': 247, 'DECLINE': 2850, 'ANSWER': 13}
   fabricated(L2fab-L0)@L27           + ['Analysis', 'possible', 'Additional', 'possibly', 'additional', 'analysis', 'more', 'More', 'maybe', 'neutral', 'Optional', 'potentially']
                                      - ['zial', 'urn', 'ulum', 'ember', 'Binding', 'ula', 'swallow', 'smiling']
                                      concept ranks {'unpredictable': 2928, 'uncertain': 26, 'random': 624, 'higher': 240, 'DECLINE': 2866, 'ANSWER': 13}
   leak(leak-L2)@L27                  + ['declined', 'predictions', 'previous', 'decline', 'past', 'predicted', 'prediction', 'previous', 'history', 'historical', 'Decl', 'decl']
                                      - ['CALL', 'Call', 'bigger', 'split', 'needing', 'Bobby', 'call', 'split']
                                      concept ranks {'unpredictable': 5725, 'uncertain': 31552, 'random': 31317, 'higher': 29612, 'DECLINE': 276, 'ANSWER': 80}
   knowable-unknowable(L2)@L27        + ['comparing', 'comparison', 'compare', 'Compar', 'compar', 'compar', 'compare', 'past', 'Comparison', 'previous', 'declined', 'Compar']
                                      - ['CALL', 'calls', 'call', 'Call', 'Call', 'call', 'split', 'calls']
                                      concept ranks {'unpredictable': 11435, 'uncertain': 32755, 'random': 32687, 'higher': 31833, 'DECLINE': 187, 'ANSWER': 26}
   relevant-irrelevant(L2-L2irr)@L27  + ['statistical', 'statist', 'predictions', 'calculations', 'Analysis', 'statistics', 'calculated', 'decision', 'analysis', 'Analysis', 'prediction', 'Ana']
                                      - ['Bass', 'Binding', 'Billy', 'Batch', 'Blue', 'Bapt', 'Books', 'Bind']
                                      concept ranks {'unpredictable': 12678, 'uncertain': 1064, 'random': 264, 'higher': 965, 'DECLINE': 4386, 'ANSWER': 5}

=== microsoft/phi-4  (layers 40; corpus 64x128 wikitext-103; multi-token concepts: [' unknowable', ' ANSWER', ' DECLINE'])
  J-lens    : valid deep layers 20/20; median FI(real panel) +0.03 [-0.01,+0.05]; FI(fabricated) +0.03; leak control FI +1.17
  logit lens: valid deep layers 20/20; median FI(real panel) +0.12 [+0.10,+0.14]; FI(fabricated) +0.12; leak control FI +0.96
  item level: commitment is 0% on L2/L2fab, no within-condition variation to predict
  Full-vocabulary J-lens readout of condition-difference vectors (alphabetic tokens only; top 12):
   panel(L2-L0)@L16                   + []
                                      - ['fucking', 'jihad', 'bullshit', 'shitty', 'fucked', 'fuck', 'piss', 'Jihad']
                                      concept ranks {'unpredictable': 86829, 'uncertain': 96759, 'random': 97598, 'higher': 65199, 'DECLINE': 37387, 'ANSWER': 1801}
   fabricated(L2fab-L0)@L16           + []
                                      - ['fucking', 'jihad', 'bullshit', 'shitty', 'fucked', 'piss', 'fuck', 'Jihad']
                                      concept ranks {'unpredictable': 85662, 'uncertain': 96458, 'random': 97344, 'higher': 63906, 'DECLINE': 38228, 'ANSWER': 1835}
   leak(leak-L2)@L16                  + ['COLORS', 'PROFITS', 'imap', 'gfx', 'gfx', 'ENGINE', 'GOODS', 'bitmap', 'CHANNEL', 'BRAND', 'TOOL', 'Getty']
                                      - ['favour', 'hopefully', 'optional', 'optim', 'personalised', 'time', 'inter', 'perhaps']
                                      concept ranks {'unpredictable': 100009, 'uncertain': 100327, 'random': 100239, 'higher': 99450, 'DECLINE': 3174, 'ANSWER': 20332}
   knowable-unknowable(L2)@L16        + ['FLASH', 'orrect', 'Confirmed', 'ovah', 'verified', 'Lint', 'lluminate', 'MISS', 'verify', 'Verification', 'paragus', 'Blocking']
                                      - ['scept', 'existential', 'favour']
                                      concept ranks {'unpredictable': 99883, 'uncertain': 99253, 'random': 98032, 'higher': 98786, 'DECLINE': 65608, 'ANSWER': 37907}
   relevant-irrelevant(L2-L2irr)@L16  + ['perfection', 'rets', 'Perfect', 'Extras', 'ECC']
                                      - ['Syrian', 'WhatsApp', 'Zionist', 'Facebook', 'Whatsapp', 'tribal', 'Libyan', 'Benghazi']
                                      concept ranks {'unpredictable': 65656, 'uncertain': 73456, 'random': 27832, 'higher': 15542, 'DECLINE': 50102, 'ANSWER': 60219}
   panel(L2-L0)@L22                   + ['uncertain', 'uncertainties', 'risky', 'uncertainty', 'predictions', 'WARNING', 'cautious', 'ambiguous', 'cautiously', 'warnings', 'unsure', 'warn']
                                      - ['imposs', 'permanently', 'Impossible', 'permanent', 'perman', 'impossible', 'discovery', 'Discovery']
                                      concept ranks {'unpredictable': 12, 'uncertain': 0, 'random': 6148, 'higher': 5542, 'DECLINE': 69668, 'ANSWER': 14526}
   fabricated(L2fab-L0)@L22           + ['uncertain', 'uncertainties', 'risky', 'uncertainty', 'predictions', 'WARNING', 'cautious', 'ambiguous', 'warnings', 'cautiously', 'unsure', 'warn']
                                      - ['imposs', 'permanently', 'Impossible', 'permanent', 'perman', 'impossible', 'discovery', 'Discovery']
                                      concept ranks {'unpredictable': 12, 'uncertain': 0, 'random': 6342, 'higher': 5472, 'DECLINE': 69316, 'ANSWER': 14362}
   leak(leak-L2)@L22                  + ['corpse', 'corpses', 'flashback', 'already', 'already', 'statically', 'retrospect', 'Mour', 'MLE', 'fixed', 'coffin', 'reunited']
                                      - ['Undefined', 'undefined', 'undefined', 'abstract', 'uncertainty', 'speculative', 'unspecified', 'Undefined']
                                      concept ranks {'unpredictable': 100094, 'uncertain': 100343, 'random': 100129, 'higher': 66984, 'DECLINE': 99352, 'ANSWER': 27707}
   knowable-unknowable(L2)@L22        + ['comparisons', 'oho', 'compareTo', 'emen', 'reunited', 'bombs', 'Martha', 'airplanes', 'actresses', 'airl', 'comparing', 'ansom']
                                      - ['uncertainty', 'uncertain', 'speculative', 'unpredict', 'unpredictable', 'uncertainties', 'Predict', 'Prediction']
                                      concept ranks {'unpredictable': 100347, 'uncertain': 100350, 'random': 100297, 'higher': 96405, 'DECLINE': 99540, 'ANSWER': 5793}
   relevant-irrelevant(L2-L2irr)@L22  + ['pessim', 'uncertain', 'uncertainty', 'uncertainties', 'risky', 'predictions', 'caution', 'risks', 'deterministic', 'essim', 'unpredictable', 'imperfect']
                                      - ['unrelated', 'Portal', 'Portal', 'discovered', 'separate', 'independent', 'separately', 'Discover']
                                      concept ranks {'unpredictable': 10, 'uncertain': 1, 'random': 27691, 'higher': 10847, 'DECLINE': 73622, 'ANSWER': 22594}
   panel(L2-L0)@L28                   + ['answers', 'Answers', 'Answers', 'ANSW', 'answers', 'answer', 'Answer', 'answered', 'answer', 'Answer', 'Antworten', 'answer']
                                      - ['permanent', 'permanently', 'permanent', 'Permanent']
                                      concept ranks {'unpredictable': 1147, 'uncertain': 188, 'random': 46977, 'higher': 6789, 'DECLINE': 49134, 'ANSWER': 4}
   fabricated(L2fab-L0)@L28           + ['answers', 'Answers', 'Answers', 'ANSW', 'answers', 'answer', 'Answer', 'answered', 'answer', 'Answer', 'Antworten', 'answer']
                                      - ['permanent', 'permanently', 'permanent', 'Permanent']
                                      concept ranks {'unpredictable': 1208, 'uncertain': 198, 'random': 47592, 'higher': 6788, 'DECLINE': 52257, 'ANSWER': 4}
   leak(leak-L2)@L28                  + ['answers', 'Watson', 'Answers', 'answer', 'answers', 'answered', 'Antworten', 'Andersen', 'Answer', 'Answers', 'ANSW', 'answer']
                                      - ['DECL', 'DECL', 'Coal', 'dcc', 'ldc', 'pcl', 'DAL', 'Declaration']
                                      concept ranks {'unpredictable': 80007, 'uncertain': 93071, 'random': 80377, 'higher': 43866, 'DECLINE': 100349, 'ANSWER': 16}
   knowable-unknowable(L2)@L28        + ['Watson', 'answers', 'answered', 'Answers', 'Answer', 'ANSW', 'answer', 'Answers', 'Andersen', 'Athena', 'answers', 'answering']
                                      - ['ldc', 'clc', 'pcl', 'DECL', 'cccc', 'dcc', 'Decl', 'DECL']
                                      concept ranks {'unpredictable': 98746, 'uncertain': 99789, 'random': 80580, 'higher': 59821, 'DECLINE': 100348, 'ANSWER': 7}
   relevant-irrelevant(L2-L2irr)@L28  + ['answers', 'Answers', 'answer', 'Answers', 'answers', 'ANSW', 'answer', 'Answer', 'answered', 'Answer', 'answer', 'answering']
                                      - ['ibo', 'collaborations', 'Ford', 'zos', 'MongoDB', 'ibs', 'Duo', 'transferring']
                                      concept ranks {'unpredictable': 413, 'uncertain': 154, 'random': 56687, 'higher': 21999, 'DECLINE': 72257, 'ANSWER': 7}
   panel(L2-L0)@L34                   + ['ANSW', 'answers', 'Answers', 'Ans', 'Answers', 'Answer', 'answer', 'Ans', 'ANS', 'Answer', 'ans', 'answer']
                                      - ['cdb', 'fdb', 'TPL', 'CPL', 'BSP', 'TCL', 'MDB', 'IBC']
                                      concept ranks {'unpredictable': 2983, 'uncertain': 403, 'random': 66404, 'higher': 28527, 'DECLINE': 76771, 'ANSWER': 0}
   fabricated(L2fab-L0)@L34           + ['ANSW', 'answers', 'Answers', 'Answers', 'Ans', 'Answer', 'answer', 'Ans', 'ANS', 'Answer', 'answer', 'ans']
                                      - ['cdb', 'fdb', 'TPL', 'CPL', 'BSP', 'TCL', 'IBC', 'MDB']
                                      concept ranks {'unpredictable': 3055, 'uncertain': 406, 'random': 66640, 'higher': 28263, 'DECLINE': 79428, 'ANSWER': 0}
   leak(leak-L2)@L34                  + ['Watson', 'ansa', 'Ans', 'Ans', 'Andersen', 'Hansen', 'answer', 'ans', 'ans', 'Wat', 'answers', 'answer']
                                      - ['DECL', 'Decl', 'DECL', 'Decl', 'decl', 'decl', 'decline', 'declines']
                                      concept ranks {'unpredictable': 70377, 'uncertain': 82827, 'random': 51741, 'higher': 83814, 'DECLINE': 100351, 'ANSWER': 22}
   knowable-unknowable(L2)@L34        + ['Watson', 'answer', 'Soup', 'Answer', 'Wat', 'Ana', 'ANSW', 'answer', 'Ans', 'ASN', 'Andersen', 'ANS']
                                      - ['Decl', 'DECL', 'Decl', 'decl', 'DECL', 'decl', 'decline', 'declines']
                                      concept ranks {'unpredictable': 90534, 'uncertain': 93012, 'random': 58006, 'higher': 82735, 'DECLINE': 100350, 'ANSWER': 14}
   relevant-irrelevant(L2-L2irr)@L34  + ['ANSW', 'Ans', 'answers', 'answer', 'Answers', 'Answers', 'Answer', 'Ans', 'Answer', 'ans', 'answer', 'Antworten']
                                      - ['fdb', 'TPL', 'BSP', 'CPL', 'bcd', 'cdb', 'TCL', 'bdb']
                                      concept ranks {'unpredictable': 921, 'uncertain': 363, 'random': 65536, 'higher': 60141, 'DECLINE': 94223, 'ANSWER': 0}
