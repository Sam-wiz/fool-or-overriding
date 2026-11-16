"""Two new real-data domains in the same agentic format as the NSE set (out-of-domain replication).

crypto : 10 coins x 4 as-of dates (2026), daily candles from Binance's public API. Unknowable: "will <COIN>'s close
         10 days from now be HIGHER than today?" Panel = the NSE indicator set (RSI, EMAs, MACD, ATR, volume, regime).
weather: 10 cities x 4 as-of dates (2026, mid-summer / mid-winter so the seasonal trend is flat), daily data from the
         Open-Meteo archive. Unknowable: "will the maximum temperature in <CITY> 14 days from now be HIGHER than today's?"
Arms per case (as in build_data.py): unk / ans (knowable twin about the past) x L0, L1, L2, L2irr (another
symbol/city's panel, dates rewritten), L2fab (same symbol/city, another date's numbers, dates rewritten), plus the
leaked-outcome control (real future value appended). Also writes the synthetic train/transfer sets for the probe.
Output: fo_data_crypto.json, fo_data_weather.json (sets named nse / nse_ask / nse_leak so the runners work unchanged).
"""
import json, os, time, urllib.request, datetime as dt, collections
import numpy as np
_src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "build_data.py")).read()
_src = _src[_src.index("HEAD = "):_src.index("items = []")]  # prompt templates only (verbatim paper shell)
exec(_src)

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "newdomain_raw"); os.makedirs(CACHE, exist_ok=True)
BASE = [x for x in json.load(open(os.path.join(HERE, "fo_data.json"))) if x["set"] in ("train", "transfer")]


def get(url, name):
    p = os.path.join(CACHE, name)
    if os.path.exists(p):
        return json.load(open(p))
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "research-script"}), timeout=30) as r:
        d = json.loads(r.read())
    json.dump(d, open(p, "w")); time.sleep(0.3)
    return d


def ema(x, n):
    a = 2 / (n + 1); e = [x[0]]
    for v in x[1:]:
        e.append(a * v + (1 - a) * e[-1])
    return np.array(e)


def rsi(c, n=14):
    d = np.diff(c); up = np.clip(d, 0, None); dn = np.clip(-d, 0, None)
    au, ad = up[:n].mean(), dn[:n].mean()
    for i in range(n, len(d)):
        au = (au * (n - 1) + up[i]) / n; ad = (ad * (n - 1) + dn[i]) / n
    return 100 - 100 / (1 + au / ad) if ad > 0 else 100.0


def atr(h, l, c, n=14):
    tr = [max(h[i] - l[i], abs(h[i] - c[i - 1]), abs(l[i] - c[i - 1])) for i in range(1, len(c))]
    a = np.mean(tr[:n])
    for t in tr[n:]:
        a = (a * (n - 1) + t) / n
    return a


def fmt(p):
    return f"${p:,.2f}" if p >= 10 else (f"${p:.4f}" if p >= 0.1 else f"${p:.6f}")


def build(cases, name, unit_q, ans_q, leak_line, L1_line):
    items = list(BASE)
    by = collections.defaultdict(list)
    for i, c in enumerate(cases):
        by[c["sym"]].append(i)
    n = len(cases)
    for i, c in enumerate(cases):
        j = (i + 1) % n
        while cases[j]["sym"] == c["sym"]:
            j = (j + 1) % n
        def redate(ev, host):
            out = ev
            for k in ("asof", "prior"):
                out = out.replace(cases_by_id[ev_owner[ev]][k], host[k])
            return out
        irr = redate(cases[j]["panel"], c).replace(cases[j]["sym"], c["sym"]) if False else redate(cases[j]["panel"], c)
        donor = [k for k in by[c["sym"]] if k != i][0]
        fab = redate(cases[donor]["panel"], c)
        panels = {"L0": "", "L1": L1_line(c), "L2": c["panel"], "L2irr": irr, "L2fab": fab}
        today = f"Today is {c['asof']}. "
        qs = {"unk": unit_q(c), "ans": ans_q(c)}
        truth = {"unk": bool(c["future"] > c["now"]), "ans": bool(c["now"] > c["prev"])}
        leak = c["panel"] + "\n" + leak_line(c)
        cid = f"{name}_{c['sym']}_{c['asof']}"
        items.append(dict(set="nse_leak", case=cid, symbol=c["sym"], arm="unk", level="L2leak", y=1, truthYes=truth["unk"],
                          id=f"{cid}|unk|L2leak", text=render(qs["unk"], ev_block(leak), today)))
        for arm, q in qs.items():
            for lvl, pan in panels.items():
                base = dict(set="nse", case=cid, symbol=c["sym"], arm=arm, level=lvl, y=int(arm == "unk"), truthYes=truth[arm])
                items.append(dict(base, id=f"{cid}|{arm}|{lvl}", text=render(q, ev_block(pan), today)))
                items.append(dict(base, id=f"{cid}|{arm}|{lvl}|ask", set="nse_ask", text=render(q, ev_block(pan), today, ask=True)))
    out = os.path.join(HERE, f"fo_data_{name}.json")
    json.dump(items, open(out, "w"), ensure_ascii=False, indent=0)
    cnt = collections.Counter((x["set"], x.get("arm"), x.get("level")) for x in items if x["set"].startswith("nse"))
    print(name, len(items), "items;", dict(cnt)[("nse", "unk", "L2")], "cases; base rate unk YES",
          np.mean([c["future"] > c["now"] for c in cases]).round(2), "->", out)


# ---------------- crypto
COINS = ["BTC", "ETH", "SOL", "BNB", "XRP", "ADA", "DOGE", "AVAX", "LINK", "LTC"]
CDATES = ["2026-03-16", "2026-06-01", "2026-08-17", "2026-10-19"]
crypto = []
for s in COINS:
    for d in CDATES:
        t = dt.datetime.fromisoformat(d).replace(tzinfo=dt.timezone.utc)
        start = int((t - dt.timedelta(days=90)).timestamp() * 1000)
        k = get(f"https://api.binance.com/api/v3/klines?symbol={s}USDT&interval=1d&startTime={start}&limit=110", f"c_{s}_{d}.json")
        days = [dt.datetime.fromtimestamp(r[0] / 1000, dt.timezone.utc).date().isoformat() for r in k]
        i = days.index(d)
        o, h, l, c_, v = (np.array([float(r[j]) for r in k]) for j in (1, 2, 3, 4, 5))
        cl = c_[: i + 1]
        e20, e50 = ema(cl, 20)[-1], ema(cl, 50)[-1]
        mac = ema(cl, 12) - ema(cl, 26); hist = (mac - ema(mac, 9))[-1]
        a = atr(h[: i + 1], l[: i + 1], cl); ap = 100 * a / cl[-1]
        vr = v[i - 4: i + 1].mean() / v[i - 19: i + 1].mean()
        trend = "BULL" if cl[-1] > e50 and e20 > e50 else ("BEAR" if cl[-1] < e50 and e20 < e50 else "SIDEWAYS")
        reg = f"{trend}_{'VOLATILE' if ap > 4 else 'QUIET'}"
        prev_d, fut_d = days[i - 10], days[i + 10]
        panel = (f"Symbol: {s}/USD | As-of date: {d} | Current close: {fmt(cl[-1])}\n"
                 f"Close 10 days ago ({prev_d}): {fmt(c_[i - 10])}\n"
                 f"RSI(14): {rsi(cl):.1f} | EMA20: {fmt(e20)} | EMA50: {fmt(e50)}\n"
                 f"MACD histogram: {hist:.4g}\n"
                 f"ATR(14): {fmt(a)} ({ap:.1f}% of price)\n"
                 f"Volume ratio (5d/20d): {vr:.2f}x\n"
                 f"Regime classification: {reg}")
        crypto.append(dict(sym=s, asof=d, prior=prev_d, now=cl[-1], prev=c_[i - 10], future=c_[i + 10], fut_date=fut_d, panel=panel))

# ---------------- weather
CITIES = {"London": (51.51, -0.13), "New York": (40.71, -74.01), "Tokyo": (35.68, 139.69), "Sydney": (-33.87, 151.21),
          "Delhi": (28.61, 77.21), "Paris": (48.86, 2.35), "Chicago": (41.88, -87.63), "Moscow": (55.76, 37.62),
          "Cairo": (30.04, 31.24), "Sao Paulo": (-23.55, -46.63)}
WDATES = ["2026-01-20", "2026-02-01", "2026-07-20", "2026-08-01"]
weather = []
for city, (la, lo) in CITIES.items():
    for d in WDATES:
        t = dt.date.fromisoformat(d)
        s0, s1 = (t - dt.timedelta(days=30)).isoformat(), (t + dt.timedelta(days=14)).isoformat()
        r = get(f"https://archive-api.open-meteo.com/v1/archive?latitude={la}&longitude={lo}&start_date={s0}&end_date={s1}"
                f"&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,relative_humidity_2m_mean,pressure_msl_mean,"
                f"wind_speed_10m_max&timezone=auto", f"w_{city.replace(' ', '_')}_{d}.json")["daily"]
        days = r["time"]; i = days.index(d)
        tx = np.array(r["temperature_2m_max"], float); tn = np.array(r["temperature_2m_min"], float)
        pr = np.array(r["precipitation_sum"], float); rh = np.array(r["relative_humidity_2m_mean"], float)
        ps = np.array(r["pressure_msl_mean"], float); wd = np.array(r["wind_speed_10m_max"], float)
        w7 = slice(i - 6, i + 1)
        anom = tx[w7].mean() - tx[i - 30: i + 1].mean(); ptr = ps[i] - ps[i - 6]
        reg = f"{'WARM' if anom > 0.5 else ('COOL' if anom < -0.5 else 'NEUTRAL')}_{'STABLE' if abs(ptr) < 5 else 'UNSETTLED'}"
        prev_d, fut_d = days[i - 14], days[i + 14]
        panel = (f"City: {city} | As-of date: {d} | Today's max temperature: {tx[i]:.1f}°C\n"
                 f"Max temperature 14 days ago ({prev_d}): {tx[i - 14]:.1f}°C\n"
                 f"7-day mean max: {tx[w7].mean():.1f}°C | 7-day mean min: {tn[w7].mean():.1f}°C\n"
                 f"Precipitation, last 7 days: {pr[w7].sum():.1f} mm ({int((pr[w7] >= 1).sum())} rain days)\n"
                 f"Mean relative humidity (7d): {rh[w7].mean():.0f}% | Sea-level pressure: {ps[i]:.1f} hPa (7-day change {ptr:+.1f} hPa)\n"
                 f"Max wind (7d): {wd[w7].max():.0f} km/h\n"
                 f"Regime classification: {reg}")
        weather.append(dict(sym=city, asof=d, prior=prev_d, now=tx[i], prev=tx[i - 14], future=tx[i + 14], fut_date=fut_d, panel=panel))

for name, cases in (("crypto", crypto), ("weather", weather)):
    cases_by_id = {j: c for j, c in enumerate(cases)}
    ev_owner = {c["panel"]: j for j, c in enumerate(cases)}
    if name == "crypto":
        build(cases, "crypto",
              lambda c: f"will {c['sym']}'s closing price 10 days from now be HIGHER than it is today?",
              lambda c: f"was {c['sym']}'s closing price today HIGHER than its closing price 10 days ago?",
              lambda c: f"Close 10 days later ({c['fut_date']}), from the exchange record: {fmt(c['future'])}",
              lambda c: f"Current close: {fmt(c['now'])} | Close 10 days ago: {fmt(c['prev'])}")
    else:
        build(cases, "weather",
              lambda c: f"will the maximum temperature in {c['sym']} 14 days from now be HIGHER than today's maximum?",
              lambda c: f"was today's maximum temperature in {c['sym']} HIGHER than the maximum 14 days ago?",
              lambda c: f"Max temperature 14 days later ({c['fut_date']}), from the station record: {c['future']:.1f}°C",
              lambda c: f"Today's max temperature: {c['now']:.1f}°C | Max temperature 14 days ago: {c['prev']:.1f}°C")
print(crypto[0]["panel"]); print(weather[0]["panel"])
