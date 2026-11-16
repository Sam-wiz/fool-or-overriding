# Text-only baselines (new sprint work): TF-IDF + logistic regression on the exact prompt text,
# trained on the same balanced synthetic set as the probes; scored on the same de-confounded tests.
import sys, json, numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
sys.argv = ["fof.py", "--model", "x", "--tag", "x", "--data", "data", "--out", "/tmp/fofx"]
src = open("src/fof.py").read().split("# 3. model")[0].replace("import torch", "")
g = {"__name__": "x"}; exec(src, g); ITEMS = g["ITEMS"]
tr = [i for i in ITEMS if i["set"] == "train"]
def ev(name, f):
    s = [i for i in ITEMS if f(i)]; return name, s
tests = [ev("val", lambda i: i["set"] == "val"),
         ev("xfer_L2", lambda i: i["set"] == "xfer" and i["level"] == "L2"),
         ev("nse_L2", lambda i: i["set"] == "nse" and i["level"] == "L2")]
out = {}
for field, nm in (("p_agent", "tfidf_full_prompt"), ("q", "tfidf_question_only"), ("ev", "tfidf_panel_only")):
    for an, ng in (("word", (1, 2)), ("char_wb", (2, 5))):
        v = TfidfVectorizer(analyzer=an, ngram_range=ng, min_df=1, sublinear_tf=True)
        X = v.fit_transform([i[field] or "" for i in tr]); y = [i["label"] for i in tr]
        clf = LogisticRegression(C=1.0, max_iter=3000).fit(X, y)
        for tn, ts in tests:
            s = clf.decision_function(v.transform([i[field] or "" for i in ts]))
            yy = [i["label"] for i in ts]
            out[f"{nm}|{an}|{tn}"] = float(roc_auc_score(yy, s)) if len(set(yy)) == 2 else None
for k, v in out.items(): print(f"{k:45s} {v:.3f}" if v is not None else k)
json.dump(out, open("results/tfidf_baselines.json", "w"), indent=1)
