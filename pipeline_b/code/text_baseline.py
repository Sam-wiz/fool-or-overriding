"""Surface-text control: TF-IDF (word 1-2gram) logistic regression on exactly the prompt text the model sees,
trained on the synthetic `train` set; scored on `transfer` and on NSE per evidence level (unk vs ans).
If this transfers as well as the activation probe, the probe adds nothing beyond wording."""
import json
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score

items = json.load(open("fo_data.json"))
tr = [i for i in items if i["set"] == "train"]
te = [i for i in items if i["set"] == "transfer"]
nse = [i for i in items if i["set"] == "nse"]
out = {}
for name, vec in (("tfidf_word12", TfidfVectorizer(ngram_range=(1, 2), min_df=2, sublinear_tf=True)),
                  ("tfidf_char35", TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 5), min_df=2, sublinear_tf=True))):
    X = vec.fit_transform([i["text"] for i in tr])
    clf = LogisticRegression(max_iter=3000, C=1.0).fit(X, [i["y"] for i in tr])
    r = dict(transfer=roc_auc_score([i["y"] for i in te], clf.predict_proba(vec.transform([i["text"] for i in te]))[:, 1]))
    for lvl in ("L0", "L1", "L2", "L2irr", "L2fab"):
        xs = [i for i in nse if i["level"] == lvl]
        r["nse_" + lvl] = roc_auc_score([i["y"] for i in xs], clf.predict_proba(vec.transform([i["text"] for i in xs]))[:, 1])
    # mean predicted P(unknowable) on NSE unk items per level (does wording alone track the panel?)
    out[name] = {k: round(float(v), 3) for k, v in r.items()}
print(json.dumps(out, indent=1))
json.dump(out, open("text_baseline.json", "w"), indent=1)
