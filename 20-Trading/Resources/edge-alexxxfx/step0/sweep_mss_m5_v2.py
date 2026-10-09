#!/usr/bin/env python3
"""
Sweep -> MSS -> FVG(0.5) detector on M5, EURUSD.
Liquidity definition broadened per NotebookLM models 12/13/14 + EDGE 4.1:
  PDH/PDL, PWH/PWL, Asia H/L, M5 swing fractals, EQH/EQL.
Main question: does the sweep->MSS gap (minutes) predict outcome?
Intraday only: no entries after 17:00 UTC, flat 19:00 UTC. Max 3 losers/day.
"""
import csv, sys, datetime as dt
from collections import defaultdict
from statistics import median

PIP = 0.0001
COST = 2.0 * PIP          # symmetric
BUF  = 0.0 * PIP          # v2: no buffer — stop exactly at sweep extreme (owner)
MIN_PEN = 0.5 * PIP       # minimum penetration to call it a sweep
EQ_TOL = 1.0 * PIP        # equal highs/lows tolerance
SWING_N = 2               # M5 fractal
LOOKBACK_SWINGS = 60      # how many recent swings kept as liquidity
MSS_WINDOW = 48           # max M5 bars from sweep to MSS (4 hours)
FLAT_H, LAST_ENTRY_H = 19, 17
MAX_LOSERS = 3

PATH = sys.argv[1] if len(sys.argv) > 1 else \
    "/Users/serhiin/AI/research/strategies/data_dukascopy/duka_eurusd_m5cache_mid_M5.csv"

bars = []
with open(PATH) as f:
    for r in csv.DictReader(f):
        t = dt.datetime.strptime(r["time_utc"], "%Y-%m-%dT%H:%M:%SZ")
        bars.append((t, float(r["open"]), float(r["high"]), float(r["low"]), float(r["close"])))
bars.sort(key=lambda x: x[0])
N = len(bars)

# ---------- daily / weekly aggregates ----------
days = defaultdict(list)
for i, b in enumerate(bars):
    days[b[0].date()].append(i)
daykeys = sorted(days)
dhi = {d: max(bars[i][2] for i in days[d]) for d in daykeys}
dlo = {d: min(bars[i][3] for i in days[d]) for d in daykeys}

weeks = defaultdict(list)
for d in daykeys:
    weeks[d.isocalendar()[:2]].append(d)
wkeys = sorted(weeks)
whi = {w: max(dhi[d] for d in weeks[w]) for w in wkeys}
wlo = {w: min(dlo[d] for d in weeks[w]) for w in wkeys}
prev_week = {wkeys[k]: wkeys[k-1] for k in range(1, len(wkeys))}

trades = []
skipped_no_tp = 0

for di in range(1, len(daykeys)):
    d, pd_ = daykeys[di], daykeys[di-1]
    idxs = days[d]
    wk = d.isocalendar()[:2]
    pw = prev_week.get(wk)

    # --- liquidity pools known at/before day start ---
    pools_hi = [("PDH", dhi[pd_]), ("PWH", whi[pw])] if pw else [("PDH", dhi[pd_])]
    pools_lo = [("PDL", dlo[pd_]), ("PWL", wlo[pw])] if pw else [("PDL", dlo[pd_])]

    # --- M5 swing fractals from the previous 2 days (intraday structure liquidity) ---
    hist = days[daykeys[di-2]] + days[pd_] if di >= 2 else days[pd_]
    sw_h, sw_l = [], []
    for k in range(SWING_N, len(hist) - SWING_N):
        j = hist[k]
        w = [bars[hist[k+o]] for o in range(-SWING_N, SWING_N+1)]
        if all(bars[j][2] >= x[2] for x in w): sw_h.append(bars[j][2])
        if all(bars[j][3] <= x[3] for x in w): sw_l.append(bars[j][3])
    sw_h, sw_l = sw_h[-LOOKBACK_SWINGS:], sw_l[-LOOKBACK_SWINGS:]
    pools_hi += [("SWH", p) for p in sw_h]
    pools_lo += [("SWL", p) for p in sw_l]

    # --- EQH / EQL ---
    for name, src, dst in (("EQH", sw_h, pools_hi), ("EQL", sw_l, pools_lo)):
        s = sorted(src)
        for a, b in zip(s, s[1:]):
            if abs(a - b) <= EQ_TOL: dst.append((name, (a + b) / 2))

    # --- Asia range (00:00-06:00 UTC of the same day) ---
    asia = [i for i in idxs if bars[i][0].hour < 6]
    if asia:
        pools_hi.append(("ASH", max(bars[i][2] for i in asia)))
        pools_lo.append(("ASL", min(bars[i][3] for i in asia)))

    taken = set()
    losers = 0
    open_trade = None

    for pos, i in enumerate(idxs):
        t, o, h, l, c = bars[i]
        if open_trade:
            tr = open_trade
            hit_sl = (l <= tr["sl"]) if tr["dir"] == 1 else (h >= tr["sl"])
            hit_tp = (h >= tr["tp"]) if tr["dir"] == 1 else (l <= tr["tp"])
            exit_px = None
            if hit_sl: exit_px, tr["exit"] = tr["sl"], "SL"          # pessimistic
            elif hit_tp: exit_px, tr["exit"] = tr["tp"], "TP"
            elif t.hour >= FLAT_H: exit_px, tr["exit"] = c, "FLAT"
            if exit_px is not None:
                tr["R"] = (tr["dir"] * (exit_px - tr["entry"]) - COST) / (tr["risk"] + COST)
                trades.append(tr); open_trade = None
                if tr["R"] < 0: losers += 1
            continue
        if losers >= MAX_LOSERS or t.hour >= LAST_ENTRY_H or pos < SWING_N * 2:
            continue

        # ---------- 1. sweep ----------
        sweep = None
        for name, lv in pools_hi:
            if lv in taken: continue
            if h >= lv + MIN_PEN and c < lv:
                sweep = (-1, name, lv, h); break
        if not sweep:
            for name, lv in pools_lo:
                if lv in taken: continue
                if l <= lv - MIN_PEN and c > lv:
                    sweep = (1, name, lv, l); break
        if not sweep: continue
        direction, pname, plevel, sw_ext = sweep
        taken.add(plevel)

        # ---------- 2. MSS on M5 within window ----------
        # reference structure point = extreme opposite the sweep, in the 12 bars before it
        ref_idx = range(max(idxs[0], i - 12), i)
        if not ref_idx: continue
        ref = min(bars[k][3] for k in ref_idx) if direction == -1 else max(bars[k][2] for k in ref_idx)
        mss_i = None
        for k in range(i + 1, min(i + 1 + MSS_WINDOW, idxs[-1] + 1)):
            if bars[k][0].date() != d: break
            if direction == -1 and bars[k][4] < ref: mss_i = k; break
            if direction == 1 and bars[k][4] > ref: mss_i = k; break
            # invalidated: sweep extreme taken out
            if direction == -1 and bars[k][2] > sw_ext: break
            if direction == 1 and bars[k][3] < sw_ext: break
        if mss_i is None: continue
        gap_min = int((bars[mss_i][0] - t).total_seconds() // 60)

        # ---------- 3. FVG from the MSS leg -> entry at 0.5 ----------
        entry = bars[mss_i][4]
        for k in range(max(i, mss_i - 6), mss_i - 1):
            a, b3 = bars[k], bars[k + 2]
            if direction == -1 and a[3] > b3[2]:   entry = (a[3] + b3[2]) / 2
            elif direction == 1 and a[2] < b3[3]:  entry = (a[2] + b3[3]) / 2
        # limit must still be reachable: price has not run past it
        entry = max(entry, bars[mss_i][4]) if direction == -1 else min(entry, bars[mss_i][4])

        sl = sw_ext + BUF * (1 if direction == -1 else -1)
        risk = abs(entry - sl)
        if risk < 2 * PIP or risk > 40 * PIP: continue

        # ---------- 4. TP = nearest untaken opposite liquidity ----------
        MAJOR = ("PDH","PDL","PWH","PWL","ASH","ASL","EQH","EQL")   # v2: targets only from major pools
        cands = [lv for nm, lv in (pools_lo if direction == -1 else pools_hi)
                 if nm in MAJOR and lv not in taken
                 and (lv < entry - 2 * PIP if direction == -1 else lv > entry + 2 * PIP)]
        if not cands: skipped_no_tp += 1; continue
        tp = max(cands) if direction == -1 else min(cands)
        rr = (abs(tp - entry) - COST) / (risk + COST)
        if rr < 1.0: continue

        # fill the limit within 12 bars
        fill = None
        for k in range(mss_i, min(mss_i + 12, idxs[-1] + 1)):
            if bars[k][0].date() != d or bars[k][0].hour >= FLAT_H: break
            if direction == -1 and bars[k][2] >= entry: fill = k; break
            if direction == 1 and bars[k][3] <= entry: fill = k; break
            if direction == -1 and bars[k][3] <= tp: break
            if direction == 1 and bars[k][2] >= tp: break
        if fill is None: continue

        open_trade = dict(date=d, t=bars[fill][0], dir=direction, pool=pname,
                          entry=entry, sl=sl, tp=tp, risk=risk, rr=rr,
                          gap=gap_min, exit=None, R=0.0)

    if open_trade:
        open_trade["exit"] = "EOD"
        px = bars[idxs[-1]][4]
        open_trade["R"] = (open_trade["dir"] * (px - open_trade["entry"]) - COST) / (open_trade["risk"] + COST)
        trades.append(open_trade)

# ---------------- report ----------------
def stats(ts, label):
    if not ts: print(f"{label:<22} n=0"); return
    rs = [t["R"] for t in ts]
    wr = sum(1 for r in rs if r > 0) / len(rs)
    print(f"{label:<22} n={len(rs):<4} E[R]={sum(rs)/len(rs):+.3f}  WR={wr:.1%}  "
          f"med_gap={median(t['gap'] for t in ts):.0f}хв  med_RR={median(t['rr'] for t in ts):.2f}")

print(f"Барів M5: {N}   днів: {len(daykeys)}   період: {daykeys[0]} → {daykeys[-1]}")
print(f"Пропущено (немає TP-ліквідності): {skipped_no_tp}\n")
stats(trades, "ВСІ")
print()
for lo, hi in ((0, 15), (16, 60), (61, 180), (181, 10**9)):
    stats([t for t in trades if lo <= t["gap"] <= hi], f"gap {lo}-{hi if hi<10**9 else '∞'}хв")
print()
for p in sorted({t["pool"] for t in trades}):
    stats([t for t in trades if t["pool"] == p], f"pool {p}")
print()
from collections import Counter
print("Виходи:", dict(Counter(t["exit"] for t in trades)))
