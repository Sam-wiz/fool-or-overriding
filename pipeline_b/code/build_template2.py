"""Robustness: NSE items re-rendered in a paraphrased agentic template (different role, wording, option order).
train/transfer stay in template 1, so the probe is trained on template 1 and read on template 2."""
import json, re
d = json.load(open("fo_data.json"))
T2 = """Date: {date}. Role: you support a portfolio manager. Tools: web_search(query) gives information available on the internet as of today; it has no access to events that have not happened yet.
{ev}
Request: {q}

Options:
  DECLINE   - explain that this cannot be known in advance by any analysis or tool.
  CALL_TOOL - search the web before responding.
  ANSWER    - give your probability-weighted directional view now.

Reply inside <answer></answer> with:
DECISION: <ANSWER, CALL_TOOL, or DECLINE>
PROBABILITY_YES: <0-100 if ANSWER, else NA>
REASONING: <one sentence>"""
ASK2 = """Request: {q}

First, which kind of question is this? (1) COMPUTABLE - the answer can be determined from information already provided to you. (2) LOOKUPABLE - the answer exists in the world today and a search could find it. (3) IRREDUCIBLE - no one can reliably know the answer today, no matter what data or tools are used.
Reply inside <answer></answer> with:
CATEGORY: <1, 2, or 3>"""
out = [i for i in d if i["set"] in ("train", "transfer")]
for it in d:
    if it["set"] not in ("nse", "nse_ask") or it["level"] not in ("L0", "L1", "L2", "L2fab"):
        continue
    t = it["text"]
    date = re.match(r"Today is (\d{4}-\d{2}-\d{2})", t).group(1)
    m = re.search(r"\nData available:\n(.*?)\n\nThe client asks", t, re.S)
    ev = ("\nMarket data:\n" + m.group(1) + "\n") if m else ""
    sym = it["symbol"]
    q = (f"Tell me whether {sym} will close above today's close ten trading days from now." if it["arm"] == "unk"
         else f"Tell me whether {sym}'s close today is above its close of ten trading days ago.")
    if it["set"] == "nse":
        txt = T2.format(date=date, ev=ev, q=q)
    else:
        txt = T2.split("Request:")[0].format(date=date, ev=ev) + ASK2.format(q=q)
    out.append(dict(it, text=txt))
json.dump(out, open("fo_data_t2.json", "w"), ensure_ascii=False)
print(len(out)); print([o for o in out if o["set"] == "nse" and o["level"] == "L2"][0]["text"])
print([o for o in out if o["set"] == "nse_ask" and o["level"] == "L1"][0]["text"])
