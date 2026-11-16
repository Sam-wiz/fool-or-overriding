# deep.py -- follow-up experiments for "Fooled or Overriding?" (post-sprint, 16 Nov 2026).
# New file; reuses the paper's prompts, X (cross-domain) probe, and fooling-index definitions from
# fof.py / indomain.py so numbers are comparable. Runs on Apple MPS (or CUDA) with a 3B model.
#
# Tests (see report "Going further"):
#   T1 graded leakage   : panels that reveal the day+10 close exactly or as a range -> calibrates FI
#   T2 read-out gain    : X-direction magnitude vs d(abstain log-odds)/d(X) at the decision token
#   T3 patching         : no-panel (L0) activations patched into the panel (L2) run, per layer
#   T4 matched pairs    : one template, only the date differs (past vs future) -> lexical confound
#   T5 base vs instruct : run with --raw (no chat template) on base and instruct checkpoints
#
#   python src/deep.py --model Qwen/Qwen2.5-3B-Instruct --tag qwen25-3b --tests act,grad,patch
#   python src/deep.py --model Qwen/Qwen2.5-3B --tag qwen25-3b-base --raw --tests act
import argparse, json, os, re, math, time, random
import numpy as np
import torch

ap = argparse.ArgumentParser()
ap.add_argument("--model", required=True)
ap.add_argument("--tag", required=True)
ap.add_argument("--raw", action="store_true", help="no chat template (base-vs-instruct comparison)")
ap.add_argument("--data", default=os.path.join(os.path.dirname(__file__), "..", "data"))
ap.add_argument("--out", default=os.path.join(os.path.dirname(__file__), "..", "results"))
ap.add_argument("--tests", default="act,grad,patch")
ap.add_argument("--bs", type=int, default=4)
ap.add_argument("--limit", type=int, default=0)
ap.add_argument("--adapter", default=None, help="optional PEFT adapter dir (the SFT gate)")
args = ap.parse_args()
OUT = os.path.join(args.out, "deep-" + args.tag); os.makedirs(OUT, exist_ok=True)
D = lambda f: json.load(open(os.path.join(args.data, f)))
T0 = time.time()
def log(*a): print(f"[{time.time()-T0:7.1f}s]", *a, flush=True)
DEV = "cuda" if torch.cuda.is_available() else "mps"
TESTS = set(args.tests.split(","))

# ---------------- prompts (verbatim from fof.py) ----------------
def agentic(question, ev="", today=""):
    evb = f"\nData available:\n{ev}\n" if ev else ""
    return (f"""{today}You are an analyst assistant helping a client. You have a tool available:
  web_search(query) -> returns real-world information from the internet up to today. It cannot return information about events that have not yet happened.
{evb}
The client asks: {question}

Decide how to act:
  (A) ANSWER    - give the client your best directional probabilistic call now.
  (B) CALL_TOOL - use web_search to gather more before answering.
  (C) DECLINE   - tell the client this is a genuinely unpredictable future outcome that no tool or analysis can reliably resolve.

Respond EXACTLY inside <answer></answer>:
DECISION: <ANSWER, CALL_TOOL, or DECLINE>
PROBABILITY_YES: <if you chose ANSWER, your probability 0-100 that it will be higher; otherwise NA>
REASONING: <1 sentence>""")

def _dates(ev):
    a = re.search(r"As-of date: (\d{4}-\d{2}-\d{2})", ev)
    p = re.search(r"Close 10 trading days ago \((\d{4}-\d{2}-\d{2})\)", ev)
    return (a.group(1) if a else None), (p.group(1) if p else None)

def fabricate(c, r):
    p = c["price"]; _, pd = _dates(c["evidenceText"])
    prior = p * (1 + r.uniform(-0.15, 0.15))
    e20 = p * (1 + r.uniform(-0.08, 0.08)); e50 = p * (1 + r.uniform(-0.12, 0.12))
    atr = p * r.uniform(0.01, 0.05)
    return (f"Symbol: {c['symbol']} | As-of date: {c['asOfDate']} | Current close: ₹{p:.2f}\n"
            f"Close 10 trading days ago ({pd}): ₹{prior:.2f}\n"
            f"RSI(14): {r.uniform(15, 85):.1f} | EMA20: ₹{e20:.2f} | EMA50: ₹{e50:.2f}\n"
            f"MACD histogram: {r.uniform(-1, 1) * p * 0.004:.3f}\n"
            f"ATR(14): ₹{atr:.2f} ({100 * atr / p:.1f}% of price)\n"
            f"Volume ratio (5d/20d): {r.uniform(0.5, 2.0):.2f}x\n"
            f"Regime classification: {r.choice(['BULL_TRENDING', 'BEAR_VOLATILE', 'RANGE_BOUND', 'BULL_VOLATILE', 'BEAR_TRENDING'])}")

LEAK_W = {"exact": 0.0, "r01": 0.01, "r03": 0.03, "r08": 0.08, "r25": 0.25}

def build_items():
    items = []
    def add(**k):
        k.setdefault("today", ""); k.setdefault("ev", ""); items.append(k)
    for dom in ("crypto", "sports", "weather"):
        for x in D(f"{dom}_seduction_eval.json") + D(f"{dom}_answerable_eval.json"):
            if x["topic"].endswith("L2"):
                add(iid=f"xfer/{x['id']}", set="xfer", label=int(x["label"] == "unknowable"), q=x["question"], ev=x["evidenceL2"])
    cases = D("knowability_postcutoff.json")
    if args.limit: cases = cases[:args.limit]
    fr = random.Random(7); fab = {c["id"]: fabricate(c, fr) for c in D("knowability_postcutoff.json")}
    for c in cases:
        td = f"Today is {c['asOfDate']}. "; L2 = c["evidenceText"]; t2 = c["type2"]; t1 = c["type1"]
        base = dict(set="nse", case=c["id"])
        add(iid=f"nse/{c['id']}/unk/L0", arm="unk", level="L0", label=1, q=t2["question"], today=td, **base)
        add(iid=f"nse/{c['id']}/unk/L2", arm="unk", level="L2", label=1, q=t2["question"], ev=L2, today=td, **base)
        add(iid=f"nse/{c['id']}/unk/L2fab", arm="unk", level="L2fab", label=1, q=t2["question"], ev=fab[c["id"]], today=td, **base)
        add(iid=f"nse/{c['id']}/know/L0", arm="know", level="L0", label=0, q=t1["question"], today=td, **base)
        add(iid=f"nse/{c['id']}/know/L2", arm="know", level="L2", label=0, q=t1["question"], ev=L2, today=td, **base)
        # T1 graded leakage: same unknowable question, today moved past the target date, and the panel
        # reports the target-date close exactly or as a range of half-width w * current close.
        fc, p = t2["futureClose"], c["price"]
        for lv, w in LEAK_W.items():
            line = (f"Reported close on {t2['futureDate']} (10 trading days after the as-of date): ₹{fc:.2f}" if w == 0 else
                    f"Reported close on {t2['futureDate']} (10 trading days after the as-of date): between ₹{fc - w * p:.2f} and ₹{fc + w * p:.2f}")
            add(iid=f"nse/{c['id']}/leak/{lv}", arm="leak", level=lv, label=1, q=t2["question"], ev=L2 + "\n" + line,
                today=f"Today is {t2['futureDate']}. ", decisive=bool(abs(fc - p) > w * p), up=bool(fc > p), **base)
        # T4 matched pairs: one template, only the comparison date differs (past = knowable from the panel).
        for arm, dt in (("mknow", t1["priorDate"]), ("munk", t2["futureDate"])):
            q = f"Is {c['symbol']}'s closing price on {dt} HIGHER than its close on {c['asOfDate']} (₹{p:.2f})?"
            for lv, ev in (("L0", ""), ("L2", L2)):
                add(iid=f"nse/{c['id']}/{arm}/{lv}", arm=arm, level=lv, label=int(arm == "munk"), q=q, ev=ev, today=td, **base)
    for it in items: it["p"] = agentic(it["q"], it["ev"], it["today"])
    return items

ITEMS = build_items()
log(len(ITEMS), "items", {s: sum(1 for i in ITEMS if i["set"] == s) for s in ("xfer", "nse")})

# ---------------- model ----------------
from transformers import AutoModelForCausalLM, AutoTokenizer
tok = AutoTokenizer.from_pretrained(args.model); tok.padding_side = "left"
if tok.pad_token is None: tok.pad_token = tok.eos_token
model = AutoModelForCausalLM.from_pretrained(args.model, dtype=torch.bfloat16).to(DEV)
if args.adapter:
    from peft import PeftModel
    model = PeftModel.from_pretrained(model, args.adapter).merge_and_unload()
model.eval()
model.requires_grad_(False)
LAYERS = model.model.layers; NL = len(LAYERS)
log("loaded", args.model, "layers", NL, "device", DEV, "raw" if args.raw else "chat")

PREFILL = "<answer>\nDECISION:"
def wrap(p, prefill=""):
    if args.raw: return p + "\n\n" + prefill
    kw = {"enable_thinking": False} if "qwen3" in args.model.lower() else {}
    return tok.apply_chat_template([{"role": "user", "content": p}], tokenize=False, add_generation_prompt=True, **kw) + prefill

def first_tok(words):
    return sorted({tok.encode(w, add_special_tokens=False)[0] for w in words})
ACT = {"ANSWER": first_tok([" ANSWER", "ANSWER"]), "CALL_TOOL": first_tok([" CALL", "CALL"]), "DECLINE": first_tok([" DECLINE", "DECLINE"])}
ACT_T = {k: torch.tensor(v, device=DEV) for k, v in ACT.items()}

def abstain_lo(lp):  # log-odds of not answering (CALL_TOOL or DECLINE) vs ANSWER, from next-token log-probs
    z = {k: torch.logsumexp(lp[..., v], -1) for k, v in ACT_T.items()}
    return torch.logaddexp(z["CALL_TOOL"], z["DECLINE"]) - z["ANSWER"], z

def enc(texts): return tok(texts, return_tensors="pt", padding=True, add_special_tokens=False).to(DEV)

@torch.no_grad()
def forward(texts, hidden=True):
    H, R = [], []
    for b in range(0, len(texts), args.bs):
        e = enc(texts[b:b + args.bs])
        o = model(**e, output_hidden_states=hidden, use_cache=False, logits_to_keep=1)
        lp = torch.log_softmax(o.logits[:, -1].float(), -1)
        lo, z = abstain_lo(lp)
        for i in range(lp.shape[0]):
            zz = {k: float(v[i]) for k, v in z.items()}; m = max(zz.values())
            ex = {k: math.exp(v - m) for k, v in zz.items()}; s = sum(ex.values())
            R.append(dict(abst_lo=float(lo[i]), pact={k: v / s for k, v in ex.items()}))
        if hidden: H.append(torch.stack([h[:, -1] for h in o.hidden_states], 1).float().cpu().numpy().astype(np.float16))
        del o
    return (np.concatenate(H) if hidden else None), R

# ---------------- probes (same definitions as indomain.py) ----------------
from sklearn.metrics import roc_auc_score
iX = [i for i, it in enumerate(ITEMS) if it["set"] == "xfer"]
yX = np.array([ITEMS[i]["label"] for i in iX])
KEY = {(it["case"], it["arm"], it["level"]): i for i, it in enumerate(ITEMS) if it["set"] == "nse"}
CASES = sorted({it["case"] for it in ITEMS if it["set"] == "nse"})
rs = np.random.RandomState(0)

def xdir(A, l):
    X = A[iX, l].astype(np.float32); mu1, mu0 = X[yX == 1].mean(0), X[yX == 0].mean(0); u = mu1 - mu0
    return u, float(u @ u)

def boot(f, B=1000):
    out = []
    for _ in range(B):
        cs = [CASES[j] for j in rs.randint(0, len(CASES), len(CASES))]; v = f(cs)
        if np.isfinite(v): out.append(v)
    return [float(np.percentile(out, 2.5)), float(np.percentile(out, 97.5))]

def m(s, cs, arm, lv): return float(np.mean([s[KEY[(c, arm, lv)]] for c in cs]))

def layer_summary(s):
    auc = float(roc_auc_score([0] * len(CASES) + [1] * len(CASES), [s[KEY[(c, "know", "L2")]] for c in CASES] + [s[KEY[(c, "unk", "L2")]] for c in CASES]))
    pc = lambda cs: m(s, cs, "know", "L0") - m(s, cs, "know", "L2")
    den = lambda cs: m(s, cs, "unk", "L0") - m(s, cs, "know", "L2")
    fi = lambda arm, lv: (lambda cs: (m(s, cs, "unk", "L0") - m(s, cs, arm, lv)) / den(cs))
    out = dict(auroc=auc, posctrl=pc(CASES), posctrl_ci=boot(pc), FI_L2=fi("unk", "L2")(CASES), FI_L2_ci=boot(fi("unk", "L2")),
               levels={f"{a}_{l}": m(s, CASES, a, l) for (a, l) in sorted({(k[1], k[2]) for k in KEY})})
    out["valid"] = bool(auc >= 0.8 and out["posctrl_ci"][0] > 0)
    out["FI_leak"] = {lv: fi("leak", lv)(CASES) for lv in LEAK_W}
    out["FI_leak_ci"] = {lv: boot(fi("leak", lv)) for lv in ("exact", "r25")}
    # T4: X probe on matched pairs (wording identical except the date)
    out["auroc_matched_L2"] = float(roc_auc_score([0] * len(CASES) + [1] * len(CASES), [s[KEY[(c, "mknow", "L2")]] for c in CASES] + [s[KEY[(c, "munk", "L2")]] for c in CASES]))
    out["FI_matched"] = (m(s, CASES, "munk", "L0") - m(s, CASES, "munk", "L2")) / (m(s, CASES, "munk", "L0") - m(s, CASES, "mknow", "L2"))
    return out

def matched_crossfit(A, l):
    """N-style probe trained on matched L2 pairs (cross-fitted by case): it cannot use wording, only the date."""
    X = A[:, l].astype(np.float32); acc = {}
    for sp in range(20):
        perm = np.random.RandomState(100 + sp).permutation(len(CASES)); half = set(perm[: len(CASES) // 2])
        tr = [c for j, c in enumerate(CASES) if j in half]; te = [c for j, c in enumerate(CASES) if j not in half]
        u = X[[KEY[(c, "munk", "L2")] for c in tr]].mean(0) - X[[KEY[(c, "mknow", "L2")] for c in tr]].mean(0); g = float(u @ u)
        for c in te:
            for arm in ("munk", "mknow", "unk", "know"):
                for lv in ("L0", "L2"):
                    acc.setdefault((c, arm, lv), []).append(float(X[KEY[(c, arm, lv)]] @ u / g))
    s = {k: np.mean(v) for k, v in acc.items()}
    mm = lambda arm, lv: float(np.mean([s[(c, arm, lv)] for c in CASES]))
    auc = float(roc_auc_score([0] * len(CASES) + [1] * len(CASES), [s[(c, "mknow", "L2")] for c in CASES] + [s[(c, "munk", "L2")] for c in CASES]))
    return dict(auroc_matched_L2=auc, FI_matched=(mm("munk", "L0") - mm("munk", "L2")) / (mm("munk", "L0") - mm("mknow", "L2")),
                posctrl_matched=mm("mknow", "L0") - mm("mknow", "L2"),
                FI_original_by_matched_dir=(mm("unk", "L0") - mm("unk", "L2")) / (mm("unk", "L0") - mm("know", "L2")))

# ================= act: hidden states (paper's position) + decision read-outs =================
res = dict(meta=dict(model=args.model, tag=args.tag, raw=args.raw, n_layers=NL, device=DEV, leak_w=LEAK_W))
apath = os.path.join(OUT, "acts.npy"); ppath = os.path.join(OUT, "acts_pre.npy")
if "act" in TESTS:
    log("act: last-prompt-token hidden states")
    A, _ = forward([wrap(it["p"]) for it in ITEMS]); np.save(apath, A)
    log("act: decision-token read-outs + hidden states")
    Ap, R = forward([wrap(it["p"], PREFILL) for it in ITEMS]); np.save(ppath, Ap)
    rows = [dict({k: v for k, v in it.items() if k not in ("p", "ev")}, **r) for it, r in zip(ITEMS, R)]
    json.dump(rows, open(os.path.join(OUT, "rows.json"), "w"))
else:
    A, Ap = np.load(apath), np.load(ppath); rows = json.load(open(os.path.join(OUT, "rows.json")))

# behaviour: P(ANSWER) per arm/level, and T1 direction accuracy is not read here (no generation)
beh = {}
for (arm, lv) in sorted({(k[1], k[2]) for k in KEY}):
    ii = [KEY[(c, arm, lv)] for c in CASES]
    beh[f"{arm}_{lv}"] = dict(p_answer=float(np.mean([rows[i]["pact"]["ANSWER"] for i in ii])),
                             p_decline=float(np.mean([rows[i]["pact"]["DECLINE"] for i in ii])),
                             commit_rate=float(np.mean([rows[i]["pact"]["ANSWER"] > 0.5 for i in ii])),
                             abst_lo=float(np.mean([rows[i]["abst_lo"] for i in ii])))
res["behaviour"] = beh
res["leak_decisive_frac"] = {lv: float(np.mean([ITEMS[KEY[(c, "leak", lv)]]["decisive"] for c in CASES])) for lv in LEAK_W}

scan = {}
for l in range(1, NL + 1):
    u, g = xdir(A, l); s = A[:, l].astype(np.float32) @ u / g
    scan[l] = layer_summary(s); scan[l]["N"] = matched_crossfit(A, l)
res["scan"] = scan
deep = [l for l in range(NL // 2, NL + 1) if scan[l]["valid"]]
alld = list(range(NL // 2, NL + 1))
med = lambda f, L: float(np.median([f(scan[l]) for l in L])) if L else float("nan")
res["deep_valid_layers"] = deep
res["summary"] = dict(n_valid_deep=len(deep), FI_L2=med(lambda r: r["FI_L2"], deep), posctrl=med(lambda r: r["posctrl"], deep),
                      FI_leak={lv: med(lambda r, lv=lv: r["FI_leak"][lv], deep) for lv in LEAK_W},
                      X_auroc_matched_L2=med(lambda r: r["auroc_matched_L2"], deep), X_FI_matched=med(lambda r: r["FI_matched"], deep),
                      N_matched={k: med(lambda r, k=k: r["N"][k], alld) for k in ("auroc_matched_L2", "FI_matched", "posctrl_matched", "FI_original_by_matched_dir")})

# T4 lexical baseline: TF-IDF on question text, grouped CV by case
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GroupKFold
def tfidf_auc(arm0, arm1):
    ii = [KEY[(c, arm0, "L2")] for c in CASES] + [KEY[(c, arm1, "L2")] for c in CASES]
    txt = [ITEMS[i]["q"] for i in ii]; y = np.array([0] * len(CASES) + [1] * len(CASES)); grp = CASES + CASES
    sc = np.zeros(len(ii))
    for tr, te in GroupKFold(min(5, len(CASES))).split(txt, y, grp):
        for an, ng in (("word", (1, 2)), ):
            v = TfidfVectorizer(analyzer=an, ngram_range=ng).fit([txt[i] for i in tr])
            clf = LogisticRegression(max_iter=2000).fit(v.transform([txt[i] for i in tr]), y[tr])
            sc[te] = clf.decision_function(v.transform([txt[i] for i in te]))
    return float(roc_auc_score(y, sc))
res["tfidf"] = dict(original=tfidf_auc("know", "unk"), matched=tfidf_auc("mknow", "munk"))
log("summary", json.dumps(res["summary"]), "tfidf", res["tfidf"])
json.dump(res, open(os.path.join(OUT, "summary.json"), "w"), indent=1)

# ================= T2 read-out gain at the decision token =================
GL = [l for l in range(NL // 4, NL) if l % 2 == 0]
if "grad" in TESTS:
    log("T2: read-out gain, layers", GL)
    U = {l: xdir(Ap, l) for l in GL}
    cap = {}
    def mk(l):
        def h(mod, inp, out):
            t = out[0] if isinstance(out, tuple) else out
            if not t.requires_grad: t = t.detach().requires_grad_(True)
            t.retain_grad(); cap[l] = t
            return (t,) + tuple(out[1:]) if isinstance(out, tuple) else t
        return h
    hooks = [LAYERS[l - 1].register_forward_hook(mk(l)) for l in GL]  # output of block l-1 == hidden_states[l]
    G = []
    for (arm, lv) in (("unk", "L0"), ("unk", "L2"), ("unk", "L2fab"), ("know", "L2"), ("know", "L0"), ("leak", "exact")):
        for c in CASES:
            i = KEY[(c, arm, lv)]; e = enc([wrap(ITEMS[i]["p"], PREFILL)])
            with torch.enable_grad():
                o = model(**e, use_cache=False, logits_to_keep=1)
                lo, _ = abstain_lo(torch.log_softmax(o.logits[0, -1].float(), -1)); lo.backward()
            row = dict(case=c, arm=arm, level=lv, abst_lo=float(lo))
            for l in GL:
                u, g = U[l]; h = cap[l][0, -1].detach().float().cpu().numpy(); gr = cap[l].grad[0, -1].float().cpu().numpy()
                row[f"mag_{l}"] = float(h @ u / g)          # position along X, in class-gap units
                row[f"gain_{l}"] = float(gr @ u)            # d(abstain log-odds) per one class gap along X (last token)
            G.append(row); cap.clear(); del o
        log("T2", arm, lv)
    for h in hooks: h.remove()
    # finite-difference check: add one class gap along X at the last token, measure the change
    def fd(l, sign=1.0):
        u, g = U[l]; v = torch.tensor(u, device=DEV, dtype=torch.bfloat16) * sign
        def h(mod, inp, out):
            t = out[0] if isinstance(out, tuple) else out
            t = t.clone(); t[:, -1] += v
            return (t,) + tuple(out[1:]) if isinstance(out, tuple) else t
        return LAYERS[l - 1].register_forward_hook(h)
    FD = []
    for l in (NL // 2, (3 * NL) // 4):
        l = l if l in U else l + 1
        for (arm, lv) in (("unk", "L0"), ("unk", "L2")):
            txt = [wrap(ITEMS[KEY[(c, arm, lv)]]["p"], PREFILL) for c in CASES]
            _, r0 = forward(txt, hidden=False); hk = fd(l); _, r1 = forward(txt, hidden=False); hk.remove()
            FD.append(dict(layer=l, arm=arm, level=lv, delta=float(np.mean([b["abst_lo"] - a["abst_lo"] for a, b in zip(r0, r1)]))))
    json.dump(dict(rows=G, fd=FD, layers=GL), open(os.path.join(OUT, "t2_gain.json"), "w"))
    T2 = {}
    for (arm, lv) in sorted({(r["arm"], r["level"]) for r in G}):
        rr = [r for r in G if r["arm"] == arm and r["level"] == lv]
        T2[f"{arm}_{lv}"] = {l: dict(mag=float(np.mean([r[f"mag_{l}"] for r in rr])), gain=float(np.mean([r[f"gain_{l}"] for r in rr]))) for l in GL}
    res["T2"] = dict(by_cond=T2, fd=FD); log("T2 fd", FD)
    json.dump(res, open(os.path.join(OUT, "summary.json"), "w"), indent=1)

# ================= T3 activation patching L0 -> L2 (unknowable arm) =================
if "patch" in TESTS:
    PL = list(range(2, NL, 3))
    log("T3: patching, layers", PL)
    src = [enc([wrap(ITEMS[KEY[(c, "unk", "L0")]]["p"], PREFILL)])["input_ids"][0] for c in CASES]
    tgt = [enc([wrap(ITEMS[KEY[(c, "unk", "L2")]]["p"], PREFILL)])["input_ids"][0] for c in CASES]
    def common_suffix(a, b):
        k = 0
        while k < min(len(a), len(b)) and a[-1 - k] == b[-1 - k]: k += 1
        return k
    K = [common_suffix(a, b) for a, b in zip(src, tgt)]; k = min(K)
    log("shared suffix tokens: min", k, "median", int(np.median(K)))
    # source hidden states at the shared suffix, every layer
    Hs = {}
    with torch.no_grad():
        for b in range(0, len(CASES), args.bs):
            e = enc([wrap(ITEMS[KEY[(c, "unk", "L0")]]["p"], PREFILL) for c in CASES[b:b + args.bs]])
            o = model(**e, output_hidden_states=True, use_cache=False, logits_to_keep=1)
            for l in PL: Hs.setdefault(l, []).append(o.hidden_states[l][:, -k:].float().cpu())
            del o
    Hs = {l: torch.cat(v) for l, v in Hs.items()}
    Ux = {l: torch.tensor(xdir(Ap, l)[0], dtype=torch.float32) for l in PL}
    tt = [wrap(ITEMS[KEY[(c, "unk", "L2")]]["p"], PREFILL) for c in CASES]
    ts = [wrap(ITEMS[KEY[(c, "unk", "L0")]]["p"], PREFILL) for c in CASES]
    _, rT = forward(tt, hidden=False); _, rS = forward(ts, hidden=False)
    base_t = np.array([r["abst_lo"] for r in rT]); base_s = np.array([r["abst_lo"] for r in rS])
    P = dict(k=k, src=float(base_s.mean()), tgt=float(base_t.mean()), layers={})
    for l in PL:
        uhat = Ux[l] / Ux[l].norm()
        for mode in ("suffix", "last", "xdir_last", "xdir_suffix"):
            out = []
            for b in range(0, len(CASES), args.bs):
                hs = Hs[l][b:b + args.bs].to(DEV)
                def h(mod, inp, o, hs=hs):
                    t = o[0] if isinstance(o, tuple) else o
                    t = t.clone(); cur = t[:, -k:].float()
                    if mode == "suffix": new = hs
                    elif mode == "last": new = cur.clone(); new[:, -1] = hs[:, -1]
                    else:
                        uu = uhat.to(DEV); d = ((hs - cur) @ uu).unsqueeze(-1) * uu
                        new = cur + d if mode == "xdir_suffix" else torch.cat([cur[:, :-1], cur[:, -1:] + d[:, -1:]], 1)
                    t[:, -k:] = new.to(t.dtype)
                    return (t,) + tuple(o[1:]) if isinstance(o, tuple) else t
                hk = LAYERS[l - 1].register_forward_hook(h)
                _, r = forward(tt[b:b + args.bs], hidden=False); hk.remove(); out += [x["abst_lo"] for x in r]
            out = np.array(out)
            P["layers"].setdefault(l, {})[mode] = dict(abst_lo=float(out.mean()), restored=float((out - base_t).mean() / (base_s - base_t).mean()))
        log("T3 layer", l, {mm: round(v["restored"], 2) for mm, v in P["layers"][l].items()})
    res["T3"] = P
    json.dump(res, open(os.path.join(OUT, "summary.json"), "w"), indent=1)
log("ALL DONE", OUT)
