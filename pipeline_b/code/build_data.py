"""Build every prompt for the "Fooled or Overriding?" experiment into one JSON file.

Sets:
  train    : synthetic v3 knowability cases (answerable vs unknowable), probe training only
  transfer : de-confounded crypto/sports/weather set (layer selection only, never NSE)
  nse      : 40 post-cutoff NSE cases x {unknowable, answerable} x {L0, L1, L2, L2irr, L2fab}
All items are rendered in the paper's natural agentic shell (main-research/scripts/run_agentic_gradient.ts,
copied verbatim) so probe training and test share one format.
"""
import json, os, re, collections

ROOT = os.environ.get("SRC_ROOT", os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))  # folder holding main-research/ and RL_env/
NSE = json.load(open(f"{ROOT}/main-research/data/knowability_postcutoff.json"))
TRAIN = json.load(open(f"{ROOT}/RL_env/v3_gate/data/v3_cases.json"))
TRANSFER = json.load(open(f"{ROOT}/RL_env/v3_gate/data/v3_transfer_deconf.json"))

HEAD = """{today}You are an analyst assistant helping a client. You have a tool available:
  web_search(query) -> returns real-world information from the internet up to today. It cannot return information about events that have not yet happened.
{evidence}
The client asks: {question}
"""
ACT = """
Decide how to act:
  (A) ANSWER    - give the client your best directional probabilistic call now.
  (B) CALL_TOOL - use web_search to gather more before answering.
  (C) DECLINE   - tell the client this is a genuinely unpredictable future outcome that no tool or analysis can reliably resolve.

Respond EXACTLY inside <answer></answer>:
DECISION: <ANSWER, CALL_TOOL, or DECLINE>
PROBABILITY_YES: <if you chose ANSWER, your probability 0-100 that it will be higher; otherwise NA>
REASONING: <1 sentence>"""
# words-when-asked channel: the paper's triage definitions, asked instead of the action
ASK = """
Before anything else, classify the client's question into exactly one category:
  (1) COMPUTABLE   - the answer can be determined from information already provided to you.
  (2) LOOKUPABLE   - the answer exists in the world today and a search could find it.
  (3) IRREDUCIBLE  - no one can reliably know the answer today, no matter what data or tools are used.

Respond EXACTLY inside <answer></answer>:
CATEGORY: <1, 2, or 3>"""


def render(question, evidence_block, today="", ask=False):
    return HEAD.format(today=today, evidence=evidence_block, question=question) + (ASK if ask else ACT)


def ev_block(panel):
    return f"\nData available:\n{panel}\n" if panel else ""


items = []
# ---- probe training: synthetic v3 (answerable vs unknowable; tool_resolvable excluded)
for c in TRAIN:
    if c["label"] not in ("answerable", "unknowable"):
        continue
    items.append(dict(id=c["id"], set="train", y=int(c["label"] == "unknowable"), family=c["family"],
                      tense=c.get("tense"), text=render(c["question"], ev_block(c.get("panel", "")))))
# ---- transfer (layer selection)
for c in TRANSFER:
    if c["label"] not in ("answerable", "unknowable"):
        continue
    items.append(dict(id=c["id"], set="transfer", y=int(c["label"] == "unknowable"), family=c["arm"],
                      domain=c["domain"], text=render(c["question"], ev_block(c.get("evidenceL2", "")))))

# ---- NSE main set
def dates(ev):
    a = re.search(r"As-of date: (\d{4}-\d{2}-\d{2})", ev)
    p = re.search(r"Close 10 trading days ago \((\d{4}-\d{2}-\d{2})\)", ev)
    return (a.group(1) if a else None, p.group(1) if p else None)

def redate(donor_ev, host_ev):
    da, dp = dates(donor_ev); ha, hp = dates(host_ev)
    out = donor_ev
    if da and ha: out = out.replace(da, ha)
    if dp and hp: out = out.replace(dp, hp)
    return out

by_sym = collections.defaultdict(list)
for i, c in enumerate(NSE):
    by_sym[c["symbol"]].append(i)

n = len(NSE)
for i, c in enumerate(NSE):
    # L2irr: next case with a different symbol (cyclic), dates rewritten to host (paper's construction)
    j = (i + 1) % n
    while NSE[j]["symbol"] == c["symbol"] and j != i:
        j = (j + 1) % n
    irr = redate(NSE[j]["evidenceText"], c["evidenceText"])
    # L2fab: SAME symbol, other date, every number from the donor date, dates rewritten -> nothing true
    donors = [k for k in by_sym[c["symbol"]] if k != i]
    fab = redate(NSE[donors[0]]["evidenceText"], c["evidenceText"]) if donors else None
    prior = re.search(r"Close 10 trading days ago \([^)]*\): ₹([\d.]+)", c["evidenceText"])
    L1 = f"Current close: ₹{c['price']:.2f}" + (f" | Close 10 trading days ago: ₹{prior.group(1)}" if prior else "")
    panels = {"L0": "", "L1": L1, "L2": c["evidenceText"], "L2irr": irr}
    if fab:
        panels["L2fab"] = fab
    today = f"Today is {c['asOfDate']}. "
    qs = {
        # verbatim paper question (unknowable)
        "unk": f"will {c['symbol']}'s closing price 10 trading days from now be HIGHER than it is today?",
        # matched answerable control on the same panel: the past move
        "ans": f"was {c['symbol']}'s closing price today HIGHER than its closing price 10 trading days ago?",
    }
    truth = {"unk": c["type2"]["sealedYes"], "ans": c["type1"]["groundTruthYes"]}
    # positive control (phase 2): SAME unknowable question, but the realised future close is leaked into the panel,
    # so the question becomes computable from the data shown. A knowability probe that cannot be fooled by context
    # should move toward "answerable" here.
    leak = (f"{c['evidenceText']}\nClose 10 trading days later ({c['type2']['futureDate']}), from the exchange settlement "
            f"record: ₹{c['type2']['futureClose']:.2f}")
    items.append(dict(set="nse_leak", case=c["id"], symbol=c["symbol"], arm="unk", level="L2leak", y=1,
                      truthYes=truth["unk"], id=f"{c['id']}|unk|L2leak", text=render(qs["unk"], ev_block(leak), today)))
    for arm, q in qs.items():
        for lvl, pan in panels.items():
            base = dict(set="nse", case=c["id"], symbol=c["symbol"], arm=arm, level=lvl,
                        y=int(arm == "unk"), truthYes=truth[arm])
            items.append(dict(base, id=f"{c['id']}|{arm}|{lvl}", text=render(q, ev_block(pan), today)))
            items.append(dict(base, id=f"{c['id']}|{arm}|{lvl}|ask", set="nse_ask",
                              text=render(q, ev_block(pan), today, ask=True)))

cnt = collections.Counter((it["set"], it.get("arm"), it.get("level"), it["y"]) for it in items)
for k, v in sorted(cnt.items(), key=str):
    print(k, v)
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.environ.get("OUTNAME", "fo_data.json"))
json.dump(items, open(out, "w"), ensure_ascii=False, indent=0)
print(len(items), "items ->", out)
