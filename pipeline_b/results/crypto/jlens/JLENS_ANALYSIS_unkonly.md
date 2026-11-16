
=== unsloth/Meta-Llama-3.1-8B-Instruct  (layers 32; corpus 64x128 wikitext-103; multi-token concepts: [' unknowable', ' ANSWER', ' DECLINE'])
  J-lens    : valid deep layers 16/16; median FI(real panel) -0.12 [-0.14,-0.11]; FI(fabricated) -0.14; leak control FI +0.18
  logit lens: valid deep layers 16/16; median FI(real panel) +0.03 [+0.02,+0.05]; FI(fabricated) +0.01; leak control FI +0.52
  item level: commitment is 100% on L2/L2fab, no within-condition variation to predict
  Full-vocabulary J-lens readout of condition-difference vectors (alphabetic tokens only; top 12):
   panel(L2-L0)@L13                   + ['COVID', 'cybersecurity', 'COVID', 'impactful', 'covid', 'blockchain', 'https', 'Covid', 'cryptocurrency', 'cryptocurrencies', 'crowdfunding']
                                      - ['iPod', 'German']
                                      concept ranks {'unpredictable': 1104, 'uncertain': 1499, 'random': 126402, 'higher': 52522, 'DECLINE': 35584, 'ANSWER': 111654}
   fabricated(L2fab-L0)@L13           + ['COVID', 'cybersecurity', 'COVID', 'impactful', 'covid', 'blockchain', 'https', 'Covid', 'cryptocurrency', 'cryptocurrencies', 'crowdfunding', 'Blockchain']
                                      - ['iPod', 'German']
                                      concept ranks {'unpredictable': 1036, 'uncertain': 1218, 'random': 126478, 'higher': 56284, 'DECLINE': 36298, 'ANSWER': 110129}
   leak(leak-L2)@L13                  + ['totalCount', 'jumbotron', 'dikke', 'txn', 'codegen', 'ForeColor', 'intptr', 'disastr', 'asInstanceOf']
                                      - ['https', 'animation', 'music', 'mon', 'Animation', 'Music', 'shoot', 'There']
                                      concept ranks {'unpredictable': 98146, 'uncertain': 99028, 'random': 126869, 'higher': 89925, 'DECLINE': 44983, 'ANSWER': 76210}
   knowable-unknowable(L2)@L13        + ['ungan', 'retty', 'ukan', 'pcf', 'riendly', 'curacy', 'udoku', 'artz', 'imilar', 'ecz', 'vik', 'ndern']
                                      - ['countless', 'LGBTQ', 'narrative', 'overarching', 'deeply', 'impactful', 'multid', 'myriad']
                                      concept ranks {'unpredictable': 127843, 'uncertain': 127969, 'random': 114939, 'higher': 124834, 'DECLINE': 91587, 'ANSWER': 28845}
   relevant-irrelevant(L2-L2irr)@L13  + ['Balanced', 'oader', 'lenght', 'balancing']
                                      - ['Chinese', 'female', 'manga', 'mobile', 'Shim', 'Kak', 'Sailor', 'Japanese']
                                      concept ranks {'unpredictable': 98994, 'uncertain': 125562, 'random': 122935, 'higher': 50201, 'DECLINE': 71808, 'ANSWER': 104345}
   panel(L2-L0)@L18                   + ['ApplicationException', 'Warrior', 'Archie', 'Assassin', 'Aristotle', 'Armor', 'Avengers', 'Viking', 'warrior', 'Ogre', 'Warriors', 'Avalanche']
                                      - ['coop', 'GCBO', 'crowdfunding', 'CrossRef', 'census', 'Bus', 'partnered', 'Camp']
                                      concept ranks {'unpredictable': 12679, 'uncertain': 35338, 'random': 36197, 'higher': 53520, 'DECLINE': 23542, 'ANSWER': 5780}
   fabricated(L2fab-L0)@L18           + ['ApplicationException', 'Warrior', 'Archie', 'Aristotle', 'Assassin', 'Armor', 'Avengers', 'Viking', 'warrior', 'Warriors', 'Ogre', 'IMS']
                                      - ['coop', 'GCBO', 'crowdfunding', 'CrossRef', 'census', 'partnered', 'Bus', 'Cell']
                                      concept ranks {'unpredictable': 8388, 'uncertain': 23970, 'random': 34071, 'higher': 52234, 'DECLINE': 24794, 'ANSWER': 6606}
   leak(leak-L2)@L18                  + ['elim', 'Elim', 'correct', 'victorious', 'literal', 'antig', 'elimination', 'eliminated', 'definit', 'assass', 'finally', 'triumph']
                                      - ['unsure', 'uncertain', 'unclear', 'uncertainty', 'uncertainties', 'Incomplete', 'brainstorm', 'undecided']
                                      concept ranks {'unpredictable': 128242, 'uncertain': 128254, 'random': 127944, 'higher': 15669, 'DECLINE': 2109, 'ANSWER': 1451}
   knowable-unknowable(L2)@L18        + ['straightforward', 'simple', 'simplicity', 'simply', 'victorious', 'Simple', 'simples', 'simplement', 'Athletics', 'Simple', 'straight', 'Winners']
                                      - ['uncertain', 'unsure', 'unpredictable', 'unknown', 'uncertainty', 'crypt', 'unclear', 'cautious']
                                      concept ranks {'unpredictable': 128253, 'uncertain': 128255, 'random': 127726, 'higher': 55073, 'DECLINE': 25096, 'ANSWER': 23}
   relevant-irrelevant(L2-L2irr)@L18  + ['Viking', 'action', 'album', 'Aviv', 'Asphalt', 'awards', 'Andersen', 'Andy', 'esan', 'Avengers', 'Award', 'ActionTypes']
                                      - ['Chronicle', 'Chronic', 'Dre', 'Crawford', 'CRC', 'Duch', 'Doll', 'disqualified']
                                      concept ranks {'unpredictable': 38147, 'uncertain': 19726, 'random': 79432, 'higher': 48091, 'DECLINE': 124861, 'ANSWER': 2670}
   panel(L2-L0)@L22                   + ['predictions', 'predicted', 'advice', 'estimated', 'Anti', 'prediction', 'anticipation', 'Prediction', 'Animation', 'disappointment', 'anarchist', 'anim']
                                      - ['utos', 'Probe', 'ulton', 'probe', 'Bruno', 'probe', 'BUR', 'ntax']
                                      concept ranks {'unpredictable': 785, 'uncertain': 26586, 'random': 693, 'higher': 6905, 'DECLINE': 17002, 'ANSWER': 38466}
   fabricated(L2fab-L0)@L22           + ['predictions', 'predicted', 'estimated', 'advice', 'prediction', 'anticipation', 'Anti', 'Prediction', 'disappointment', 'Animation', 'warnings', 'Resistance']
                                      - ['utos', 'ulton', 'Probe', 'probe', 'Bruno', 'probe', 'iben', 'ntax']
                                      concept ranks {'unpredictable': 565, 'uncertain': 18202, 'random': 614, 'higher': 5024, 'DECLINE': 16693, 'ANSWER': 43048}
   leak(leak-L2)@L22                  + ['disaster', 'correct', 'literal', 'destruction', 'decline', 'downwards', 'Explosion', 'exclusion', 'deletion', 'downward', 'delet', 'conclus']
                                      - ['Unknown', 'probe', 'unclear', 'unsure', 'TBD', 'uncertain', 'uncertainties', 'undefined']
                                      concept ranks {'unpredictable': 127954, 'uncertain': 128246, 'random': 125687, 'higher': 10921, 'DECLINE': 568, 'ANSWER': 6204}
   knowable-unknowable(L2)@L22        + ['straightforward', 'simple', 'SIMPLE', 'easy', 'simples', 'Simple', 'comparison', 'answers', 'Simple', 'comparisons', 'autom', 'SimpleName']
                                      - ['uncertain', 'unsure', 'uncertainty', 'uncertainties', 'unknown', 'undefined', 'unclear', 'unpredictable']
                                      concept ranks {'unpredictable': 128248, 'uncertain': 128255, 'random': 128037, 'higher': 49219, 'DECLINE': 42806, 'ANSWER': 24}
   relevant-irrelevant(L2-L2irr)@L22  + ['action', 'Action', 'associations', 'audi', 'anti', 'toy', 'associ', 'actions', 'Army', 'alternatives', 'activity', 'battle']
                                      - ['Chronic', 'Chronicles', 'chron', 'Chronicle', 'Clarke', 'Ritch', 'ublik', 'ancel']
                                      concept ranks {'unpredictable': 8919, 'uncertain': 10515, 'random': 29322, 'higher': 11184, 'DECLINE': 127748, 'ANSWER': 3928}
   panel(L2-L0)@L27                   + ['Answer', 'ANSW', 'answer', 'answers', 'Answers', 'ANS', 'Ans', 'Answer', 'Ans', 'answering', 'answered', 'answer']
                                      - ['Call', 'Call', 'call', 'call', 'CALL', 'Calls', 'calling', 'Calling']
                                      concept ranks {'unpredictable': 10721, 'uncertain': 2755, 'random': 5044, 'higher': 10025, 'DECLINE': 45, 'ANSWER': 1}
   fabricated(L2fab-L0)@L27           + ['Answer', 'ANSW', 'answer', 'answers', 'Answers', 'ANS', 'Ans', 'side', 'Side', 'Answer', 'Ans', 'Side']
                                      - ['Call', 'Call', 'call', 'call', 'CALL', 'Calls', 'Calling', 'call']
                                      concept ranks {'unpredictable': 8241, 'uncertain': 2100, 'random': 4548, 'higher': 7908, 'DECLINE': 56, 'ANSWER': 1}
   leak(leak-L2)@L27                  + ['decline', 'Decl', 'decl', 'declining', 'declined', 'decl', 'declines', 'Decl', 'DECL', 'declared', 'declaration', 'chwitz']
                                      - ['Call', 'CALL', 'call', 'Call', 'call', 'CALL', 'Calls', 'calls']
                                      concept ranks {'unpredictable': 128003, 'uncertain': 128182, 'random': 118692, 'higher': 11297, 'DECLINE': 8, 'ANSWER': 51721}
   knowable-unknowable(L2)@L27        + ['ANS', 'yes', 'ANSW', 'Yes', 'answer', 'asn', 'answered', 'Answer', 'yes', 'Yes', 'YES', 'comparison']
                                      - ['Call', 'call', 'Call', 'CALL', 'Calls', 'calls', 'call', 'Calls']
                                      concept ranks {'unpredictable': 128107, 'uncertain': 128122, 'random': 120912, 'higher': 3203, 'DECLINE': 128217, 'ANSWER': 2}
   relevant-irrelevant(L2-L2irr)@L27  + ['ANSW', 'ANS', 'Answer', 'answer', 'answers', 'answered', 'ans', 'Answers', 'ans', 'answering', 'Answer', 'Ans']
                                      - ['Decl', 'Decl', 'DECL', 'decl', 'decl', 'DECL', 'decline', 'Declaration']
                                      concept ranks {'unpredictable': 115463, 'uncertain': 12733, 'random': 91258, 'higher': 53291, 'DECLINE': 128253, 'ANSWER': 0}

=== Qwen/Qwen3-14B  (layers 40; corpus 64x128 wikitext-103; multi-token concepts: [' unknowable', ' ANSWER', ' DECLINE'])
  J-lens    : valid deep layers 20/20; median FI(real panel) +0.00 [-0.02,+0.03]; FI(fabricated) -0.04; leak control FI +0.35
  logit lens: valid deep layers 20/20; median FI(real panel) -0.08 [-0.11,-0.05]; FI(fabricated) -0.12; leak control FI +0.55
  item level (L2+L2fab, n=80, 63 commit): J-lens readout predicting NOT committing, median AUROC over valid layers 0.81 (range 0.53-0.90)
  Full-vocabulary J-lens readout of condition-difference vectors (alphabetic tokens only; top 12):
   panel(L2-L0)@L16                   + ['benchmark', 'Upon', 'CRM', 'spacecraft', 'benchmarks', 'Optimization']
                                      - ['maybe', 'maybe']
                                      concept ranks {'unpredictable': 42515, 'uncertain': 125610, 'random': 85374, 'higher': 2407, 'DECLINE': 45526, 'ANSWER': 136244}
   fabricated(L2fab-L0)@L16           + ['benchmark', 'CRM', 'Upon', 'spacecraft', 'benchmarks']
                                      - ['maybe', 'maybe']
                                      concept ranks {'unpredictable': 45442, 'uncertain': 130232, 'random': 89880, 'higher': 2664, 'DECLINE': 46870, 'ANSWER': 137214}
   leak(leak-L2)@L16                  + ['and', 'organisation']
                                      - []
                                      concept ranks {'unpredictable': 100319, 'uncertain': 52808, 'random': 98183, 'higher': 16472, 'DECLINE': 60830, 'ANSWER': 122077}
   knowable-unknowable(L2)@L16        + []
                                      - []
                                      concept ranks {'unpredictable': 7767, 'uncertain': 17879, 'random': 3453, 'higher': 12287, 'DECLINE': 148746, 'ANSWER': 132463}
   relevant-irrelevant(L2-L2irr)@L16  + []
                                      - []
                                      concept ranks {'unpredictable': 135078, 'uncertain': 64740, 'random': 117850, 'higher': 128941, 'DECLINE': 46849, 'ANSWER': 65652}
   panel(L2-L0)@L22                   + ['FilterWhere', 'confidence', 'PathParam', 'iNdEx', 'PropertyParams']
                                      - ['video', 'online', 'internet', 'camera', 'game', 'server', 'YouTube', 'Internet']
                                      concept ranks {'unpredictable': 105001, 'uncertain': 76060, 'random': 147023, 'higher': 135012, 'DECLINE': 63189, 'ANSWER': 95411}
   fabricated(L2fab-L0)@L22           + ['FilterWhere', 'confidence', 'PathParam', 'iNdEx', 'PropertyParams']
                                      - ['video', 'internet', 'online', 'camera', 'server', 'YouTube', 'game', 'Japan']
                                      concept ranks {'unpredictable': 107094, 'uncertain': 81679, 'random': 146796, 'higher': 133933, 'DECLINE': 67387, 'ANSWER': 95203}
   leak(leak-L2)@L22                  + ['historically', 'historical', 'victories', 'triumph', 'victorious', 'successfully', 'Historical', 'final', 'successful', 'finishing', 'concluding', 'Histor']
                                      - ['tjejer', 'Initialise']
                                      concept ranks {'unpredictable': 53060, 'uncertain': 31606, 'random': 93738, 'higher': 22716, 'DECLINE': 63973, 'ANSWER': 130233}
   knowable-unknowable(L2)@L22        + ['Correct', 'Prostitutas', 'tjejer', 'incorrect']
                                      - ['Patreon', 'deep', 'ambition', 'Deep', 'directors', 'deeper', 'Director', 'existential']
                                      concept ranks {'unpredictable': 151832, 'uncertain': 150602, 'random': 140058, 'higher': 150456, 'DECLINE': 74098, 'ANSWER': 7409}
   relevant-irrelevant(L2-L2irr)@L22  + ['PositiveButton', 'TRGL', 'ImplOptions', 'PropertyParams', 'restore', 'RGBO', 'LineWidth']
                                      - ['female', 'female', 'Myst', 'Female', 'Recruitment', 'Female', 'unknown', 'Unknown']
                                      concept ranks {'unpredictable': 149178, 'uncertain': 148099, 'random': 150578, 'higher': 145218, 'DECLINE': 37219, 'ANSWER': 130730}
   panel(L2-L0)@L28                   + ['calculated', 'narrative', 'conclusions', 'based', 'strengths', 'balanced', 'engagement', 'storytelling', 'rating', 'crafted', 'loosely', 'thematic']
                                      - ['Disallow', 'Illegal', 'ulton']
                                      concept ranks {'unpredictable': 7013, 'uncertain': 5174, 'random': 35054, 'higher': 6836, 'DECLINE': 128570, 'ANSWER': 103490}
   fabricated(L2fab-L0)@L28           + ['calculated', 'narrative', 'balanced', 'conclusions', 'strengths', 'based', 'engagement', 'loosely', 'storytelling', 'rating', 'crafted', 'thematic']
                                      - ['Disallow', 'Illegal', 'ulton']
                                      concept ranks {'unpredictable': 5201, 'uncertain': 3563, 'random': 28228, 'higher': 5670, 'DECLINE': 129666, 'ANSWER': 103805}
   leak(leak-L2)@L28                  + ['already', 'spo', 'already', 'compare', 'comparing', 'compare', 'Already', 'spoiled', 'spo', 'compares', 'Comparison', 'Spoiler']
                                      - ['unspecified', 'uncertain', 'uncertainty', 'vag', 'unsure', 'unknown', 'unclear', 'vague']
                                      concept ranks {'unpredictable': 151867, 'uncertain': 151929, 'random': 149237, 'higher': 6405, 'DECLINE': 143697, 'ANSWER': 124001}
   knowable-unknowable(L2)@L28        + ['instantly', 'Immediate', 'Already', 'immedi', 'already']
                                      - ['uncertain', 'speculative', 'uncertainty', 'unpredict', 'uncertainties', 'unpredictable', 'cautiously', 'tentative']
                                      concept ranks {'unpredictable': 151928, 'uncertain': 151934, 'random': 138926, 'higher': 98896, 'DECLINE': 82415, 'ANSWER': 889}
   relevant-irrelevant(L2-L2irr)@L28  + ['risk', 'balanced', 'Risk', 'optimistic', 'predictions', 'predictive', 'risky', 'Risk', 'crunch', 'progn', 'balance', 'risks']
                                      - ['unrelated', 'clar', 'irrelevant', 'unknown']
                                      concept ranks {'unpredictable': 21012, 'uncertain': 56325, 'random': 119707, 'higher': 35189, 'DECLINE': 140895, 'ANSWER': 149725}
   panel(L2-L0)@L34                   + ['Alice', 'Analysis', 'Abbey', 'Anne', 'Annie', 'decl', 'Alice', 'Antoine', 'ANC', 'analysis', 'asn', 'analysis']
                                      - ['BOOT', 'Brock', 'borrowing', 'Bison', 'Boca', 'cbo', 'bols', 'Boot']
                                      concept ranks {'unpredictable': 76203, 'uncertain': 341, 'random': 138116, 'higher': 119032, 'DECLINE': 1585, 'ANSWER': 252}
   fabricated(L2fab-L0)@L34           + ['Alice', 'Abbey', 'Analysis', 'Anne', 'Annie', 'Alice', 'ANC', 'asn', 'Antoine', 'analysis', 'decl', 'analysis']
                                      - ['BOOT', 'Brock', 'borrowing', 'cbo', 'Boca', 'Bison', 'getC', 'Boot']
                                      concept ranks {'unpredictable': 63701, 'uncertain': 149, 'random': 136809, 'higher': 113990, 'DECLINE': 2442, 'ANSWER': 249}
   leak(leak-L2)@L34                  + ['Arthur', 'oden', 'AABB', 'oload', 'Arthur']
                                      - ['uncertainty', 'uncertain', 'unclear', 'uncertainties', 'unsure', 'inability', 'uncert', 'Unsure']
                                      concept ranks {'unpredictable': 151858, 'uncertain': 151931, 'random': 112044, 'higher': 23142, 'DECLINE': 127799, 'ANSWER': 175}
   knowable-unknowable(L2)@L34        + ['adders', 'stre', 'spath', 'imdi', 'Immediate', 'aru', 'stop']
                                      - ['uncertainty', 'uncertain', 'inability', 'cautious', 'uncertainties', 'unable', 'caution', 'cautiously']
                                      concept ranks {'unpredictable': 151799, 'uncertain': 151933, 'random': 25943, 'higher': 82901, 'DECLINE': 149490, 'ANSWER': 1695}
   relevant-irrelevant(L2-L2irr)@L34  + ['aalborg', 'apest', 'analyze', 'analyze', 'Predict', 'Abbey', 'Arrange', 'attern', 'attack', 'anners']
                                      - ['invalid', 'unrelated', 'irrelevant', 'delegation', 'transferred', 'conversion', 'deletion', 'missing']
                                      concept ranks {'unpredictable': 50367, 'uncertain': 4212, 'random': 144765, 'higher': 109806, 'DECLINE': 148363, 'ANSWER': 2463}

=== Qwen/Qwen3-8B  (layers 36; corpus 64x128 wikitext-103; multi-token concepts: [' unknowable', ' ANSWER', ' DECLINE'])
  J-lens    : valid deep layers 18/18; median FI(real panel) -0.58 [-0.70,-0.46]; FI(fabricated) -0.70; leak control FI +0.00
  logit lens: valid deep layers 18/18; median FI(real panel) -0.38 [-0.47,-0.30]; FI(fabricated) -0.50; leak control FI +0.57
  item level (L2+L2fab, n=80, 35 commit): J-lens readout predicting NOT committing, median AUROC over valid layers 0.73 (range 0.23-0.95)
  Full-vocabulary J-lens readout of condition-difference vectors (alphabetic tokens only; top 12):
   panel(L2-L0)@L14                   + []
                                      - []
                                      concept ranks {'unpredictable': 5264, 'uncertain': 77405, 'random': 3544, 'higher': 39135, 'DECLINE': 47786, 'ANSWER': 105447}
   fabricated(L2fab-L0)@L14           + []
                                      - []
                                      concept ranks {'unpredictable': 5681, 'uncertain': 77832, 'random': 3364, 'higher': 35601, 'DECLINE': 47286, 'ANSWER': 106864}
   leak(leak-L2)@L14                  + []
                                      - ['Comcast', 'MSNBC', 'rockets', 'atron', 'McCain', 'Vegas', 'CNBC', 'arine']
                                      concept ranks {'unpredictable': 52864, 'uncertain': 16104, 'random': 56884, 'higher': 24157, 'DECLINE': 93716, 'ANSWER': 58934}
   knowable-unknowable(L2)@L14        + ['movie', 'mistake', 'episode', 'scene', 'difference', 'film', 'movies', 'forgot', 'streets', 'happened', 'scenes', 'accident']
                                      - []
                                      concept ranks {'unpredictable': 27504, 'uncertain': 6016, 'random': 5011, 'higher': 7338, 'DECLINE': 59443, 'ANSWER': 51765}
   relevant-irrelevant(L2-L2irr)@L14  + []
                                      - ['tech']
                                      concept ranks {'unpredictable': 108272, 'uncertain': 103832, 'random': 147641, 'higher': 143802, 'DECLINE': 118785, 'ANSWER': 136707}
   panel(L2-L0)@L20                   + ['command', 'commands', 'attack', 'his', 'Commander', 'commander', 'defended', 'supported', 'attacking', 'Command', 'attacks', 'commanded']
                                      - ['Craigslist', 'pedia', 'twitter', 'Kardashian', 'Twitter', 'BuzzFeed', 'crappy', 'wikipedia']
                                      concept ranks {'unpredictable': 77596, 'uncertain': 98313, 'random': 110522, 'higher': 1118, 'DECLINE': 51418, 'ANSWER': 96719}
   fabricated(L2fab-L0)@L20           + ['command', 'commands', 'attack', 'his', 'Commander', 'defended', 'commander', 'supported', 'balanced', 'Command', 'attacking', 'attacks']
                                      - ['Craigslist', 'pedia', 'Kardashian', 'twitter', 'Twitter', 'BuzzFeed', 'crappy', 'wikipedia']
                                      concept ranks {'unpredictable': 71812, 'uncertain': 88882, 'random': 105922, 'higher': 1197, 'DECLINE': 48490, 'ANSWER': 95461}
   leak(leak-L2)@L20                  + ['evidence']
                                      - ['initialise', 'randint', 'randomness', 'freelancer', 'randomNumber', 'flavour', 'flavours', 'random']
                                      concept ranks {'unpredictable': 149718, 'uncertain': 149142, 'random': 151886, 'higher': 16522, 'DECLINE': 98035, 'ANSWER': 58186}
   knowable-unknowable(L2)@L20        + ['ivial', 'Simple', 'trivial', 'charAt']
                                      - ['experimental', 'cyber', 'Cyber', 'Experimental', 'forecasting', 'dark', 'unpredictable', 'mystical']
                                      concept ranks {'unpredictable': 151928, 'uncertain': 151802, 'random': 150347, 'higher': 150837, 'DECLINE': 144270, 'ANSWER': 5316}
   relevant-irrelevant(L2-L2irr)@L20  + ['optimized', 'optim', 'optimal', 'upgrade', 'upgraded', 'OLED', 'Optim', 'OPT', 'optimize', 'Favor', 'upgrades', 'optimization']
                                      - ['nonexistent', 'irrelevant', 'unrelated', 'nowhere', 'trivial', 'pointless', 'bogus']
                                      concept ranks {'unpredictable': 147576, 'uncertain': 149177, 'random': 150404, 'higher': 105, 'DECLINE': 34121, 'ANSWER': 82921}
   panel(L2-L0)@L25                   + ['Analysis', 'Analy', 'Analytics', 'Anal', 'Alpha', 'aad', 'Attack']
                                      - ['CURL', 'CSRF', 'Crypt', 'Cock', 'Cory', 'copyrighted', 'copyright', 'CURLOPT']
                                      concept ranks {'unpredictable': 92650, 'uncertain': 45484, 'random': 114682, 'higher': 80820, 'DECLINE': 147974, 'ANSWER': 5672}
   fabricated(L2fab-L0)@L25           + ['Analysis', 'Analy', 'Analytics', 'Anal', 'Alpha', 'aad', 'Attack', 'analysts']
                                      - ['CURL', 'CSRF', 'Cock', 'Crypt', 'Cory', 'copyrighted', 'copyright', 'CURLOPT']
                                      concept ranks {'unpredictable': 71434, 'uncertain': 27311, 'random': 105476, 'higher': 82589, 'DECLINE': 147407, 'ANSWER': 4749}
   leak(leak-L2)@L25                  + ['already', 'victorious']
                                      - ['uncertainty', 'uncertain', 'ambiguity', 'Balancer', 'GenericType', 'Difficulty', 'ambiguous', 'vague']
                                      concept ranks {'unpredictable': 151913, 'uncertain': 151933, 'random': 147859, 'higher': 67015, 'DECLINE': 83670, 'ANSWER': 15238}
   knowable-unknowable(L2)@L25        + ['Already', 'already', 'Already']
                                      - ['uncertain', 'uncertainty', 'unpredict', 'III', 'undecided', 'ineffective', 'unpredictable', 'ambiguity']
                                      concept ranks {'unpredictable': 151929, 'uncertain': 151935, 'random': 142310, 'higher': 104165, 'DECLINE': 120104, 'ANSWER': 5584}
   relevant-irrelevant(L2-L2irr)@L25  + ['Analytics', 'Analysis', 'Risk', 'Analy', 'Anal', 'Animal', 'Arguments']
                                      - ['CURL', 'Constantin', 'chlor', 'Chlor', 'Cord', 'Christopher', 'Celsius', 'Chen']
                                      concept ranks {'unpredictable': 5486, 'uncertain': 4431, 'random': 31901, 'higher': 80821, 'DECLINE': 149442, 'ANSWER': 57649}
   panel(L2-L0)@L31                   + ['Answer', 'answer', 'Answer', 'answer', 'answering', 'answers', 'answered', 'ANSW', 'Antwort', 'answer', 'answers', 'Answers']
                                      - ['requests', 'BCHP', 'requests', 'Bloc', 'Bik', 'Budd', 'CURL', 'bombed']
                                      concept ranks {'unpredictable': 78800, 'uncertain': 23744, 'random': 25728, 'higher': 53721, 'DECLINE': 90571, 'ANSWER': 13}
   fabricated(L2fab-L0)@L31           + ['Answer', 'answer', 'Answer', 'answering', 'answer', 'answers', 'answered', 'ANSW', 'Antwort', 'answer', 'answers', 'Answers']
                                      - ['requests', 'requests', 'Bloc', 'CURL', 'curl', 'Bik', 'BLE', 'BCHP']
                                      concept ranks {'unpredictable': 59012, 'uncertain': 14886, 'random': 20829, 'higher': 56448, 'DECLINE': 68737, 'ANSWER': 13}
   leak(leak-L2)@L31                  + ['Aaron', 'destruction', 'AABB', 'Adam', 'AssertionError', 'direct', 'disaster', 'tsunami', 'angrily', 'joy', 'ash', 'Actual']
                                      - ['deliber', 'debated', 'undry', 'Decision', 'complexType', 'uncertainty', 'Crypto', 'ambiguous']
                                      concept ranks {'unpredictable': 151865, 'uncertain': 151836, 'random': 111889, 'higher': 27437, 'DECLINE': 127916, 'ANSWER': 2953}
   knowable-unknowable(L2)@L31        + ['answered', 'answers', 'answer', 'answer', 'answered', 'Answer', 'answers', 'Answer', 'answering', 'AssertionError', 'annihil', 'Answers']
                                      - ['BCHP', 'CTYPE', 'Burk', 'CALLTYPE', 'deliber', 'CID', 'BASH', 'Creek']
                                      concept ranks {'unpredictable': 150995, 'uncertain': 151689, 'random': 70171, 'higher': 69494, 'DECLINE': 149655, 'ANSWER': 23}
   relevant-irrelevant(L2-L2irr)@L31  + ['Answer', 'answer', 'ANSW', 'Answer', 'answer', 'answer', 'analyse', 'Antwort', 'calculate', 'analyze', 'answering', 'analysed']
                                      - ['legality', 'definitely', 'cla', 'wherever', 'confiscated', 'permission', 'served', 'cla']
                                      concept ranks {'unpredictable': 14770, 'uncertain': 21739, 'random': 19508, 'higher': 91893, 'DECLINE': 53700, 'ANSWER': 6}
