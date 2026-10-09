#!/usr/bin/env python3
"""v5 backtest — правила з реплею 16–20.02, без змін, на всій базі M5.

Напрямок:  тижневий біас (базова модель D1 на W1) → сценарій A/B при H1-закритті
           за PWL/PWH → «межа тижня», коли діапазон тижня ≥ медіани 8 попередніх.
Карта:     H1-півоти за 10 днів до дня + PDH/PDL + AsiaH/L + PWH/PWL.
Вхід:      ліміт на рівні карти, 09:00–17:00 UTC, Premium/Discount за діапазоном сесії.
Стоп:      екстремум сесії ± 0.5 п.  Ціль: перший рівень із RR_net ≥ 2.0.
Ліміти:    2 угоди/день, дедуп 60 хв, flat 19:00, стоп перевіряється першим.
"""
import csv, sys, random, datetime as dt
from collections import defaultdict
from statistics import median, mean

PATH = "/Users/serhiin/AI/research/strategies/data_dukascopy/duka_eurusd_m5cache_mid_M5.csv"
PIP = 0.0001; COST = 2.0*PIP; BUF = 0.5*PIP; OFF = 0.2*PIP; MINRR = 2.0
FROM_H, LAST_H, FLAT_H = 9, 17, 19
MAX_TR = 2; DEDUP_MIN = 60; PIV_DAYS = 10

bars = []
for r in csv.DictReader(open(PATH)):
    bars.append((dt.datetime.strptime(r["time_utc"], "%Y-%m-%dT%H:%M:%SZ"),
                 float(r["open"]), float(r["high"]), float(r["low"]), float(r["close"])))
bars.sort(key=lambda x: x[0])

days = defaultdict(list)
for i, x in enumerate(bars): days[x[0].date()].append(i)
full = [d for d in sorted(days) if len(days[d]) >= 200]          # без недільних сесій
dhi = {d: max(bars[i][2] for i in days[d]) for d in full}
dlo = {d: min(bars[i][3] for i in days[d]) for d in full}
dcl = {d: bars[days[d][-1]][4] for d in full}
prevday = {full[k]: full[k-1] for k in range(1, len(full))}

wks = defaultdict(list)
for d in full: wks[d.isocalendar()[:2]].append(d)
wk = [w for w in sorted(wks) if len(wks[w]) >= 4]
whi = {w: max(dhi[x] for x in wks[w]) for w in wk}
wlo = {w: min(dlo[x] for x in wks[w]) for w in wk}
wcl = {w: dcl[wks[w][-1]] for w in wk}
pw = {wk[k]: wk[k-1] for k in range(1, len(wk))}

# H1-півоти
h1 = defaultdict(lambda: [0.0, 9.0, None])
for i, x in enumerate(bars):
    k = x[0].replace(minute=0, second=0)
    h = h1[k]; h[0] = max(h[0], x[2]); h[1] = min(h[1], x[3]); h[2] = k
h1k = sorted(h1)
pivots = []  # (time, price)
for j in range(1, len(h1k)-1):
    a, b, c = h1[h1k[j-1]], h1[h1k[j]], h1[h1k[j+1]]
    if b[0] >= a[0] and b[0] >= c[0]: pivots.append((h1k[j], b[0]))
    if b[1] <= a[1] and b[1] <= c[1]: pivots.append((h1k[j], b[1]))

def weekly_bias(w):
    """Базова модель D1, застосована до W1: +1/-1/0."""
    if w not in pw: return 0
    p = pw[w]; H, L, C = whi[w], wlo[w], wcl[w]; PH, PL = whi[p], wlo[p]
    tookH, tookL = H > PH, L < PL
    if tookH and not tookL: return 1 if C > PH else -1
    if tookL and not tookH: return -1 if C < PL else 1
    if tookH and tookL: return 1 if C > (H+L)/2 else -1
    # нічого не зняло → структура за 3 тижні
    if p not in pw: return 0
    pp = pw[p]
    hh = whi[w] < whi[p] < whi[pp]; ll = wlo[w] < wlo[p] < wlo[pp]
    HH = whi[w] > whi[p] > whi[pp]; HL = wlo[w] > wlo[p] > wlo[pp]
    if HH and HL: return 1
    if hh and ll: return -1
    return 0

def run(direction_fn, seed=None):
    rng = random.Random(seed)
    trades = []
    for wi, w in enumerate(wk):
        if w not in pw: continue
        dir0 = direction_fn(w, rng)
        if dir0 == 0: continue
        P = pw[w]; PWH, PWL = whi[P], wlo[P]
        hist = [whi[x]-wlo[x] for x in wk[max(0, wi-8):wi]]
        WKFULL = median(hist) if hist else 0.011
        cur = dir0; scen = 'bias'; wkH, wkL = 0.0, 9.0
        for d in wks[w]:
            if d not in prevday: continue
            pd = prevday[d]
            complete = (wkH - wkL) >= WKFULL
            idx = days[d]
            asia = [i for i in idx if bars[i][0].hour < 6]
            if not asia: continue
            asH = max(bars[i][2] for i in asia); asL = min(bars[i][3] for i in asia)
            t0 = bars[idx[0]][0].replace(hour=6, minute=0)
            cut = t0 - dt.timedelta(days=PIV_DAYS)
            lv = {round(p, 5) for (t, p) in pivots if cut <= t < t0}
            lv |= {round(dhi[pd], 5), round(dlo[pd], 5), round(asH, 5), round(asL, 5), round(PWH, 5), round(PWL, 5)}
            LV = sorted(lv)
            sH, sL = 0.0, 9.0; opn = None; used = 0; lastT = -999
            day_dir = cur
            if complete:
                day_dir = 1 if (asL - wkL) < (wkH - asL) else -1
            for i in idx:
                t, o, h, l, c = bars[i]
                if t.hour < 6: continue
                if t.hour > FLAT_H: break
                sH = max(sH, h); sL = min(sL, l)
                mins = t.hour*60 + t.minute
                # сценарії на H1-закритті
                if t.minute == 55 and not complete:
                    if c < PWL and cur != -1: cur = -1; scen = 'A'; day_dir = -1
                    if c > PWH and cur != 1: cur = 1; scen = 'B'; day_dir = 1
                if opn:
                    dd, E, SL, TP, te = opn
                    R = None; ex = None
                    if dd < 0:
                        if h >= SL: R, ex = -1.0, 'SL'
                        elif l <= TP: R, ex = (E-TP-COST)/(SL-E+COST), 'TP'
                    else:
                        if l <= SL: R, ex = -1.0, 'SL'
                        elif h >= TP: R, ex = (TP-E-COST)/(E-SL+COST), 'TP'
                    if R is None and t.hour == FLAT_H and t.minute == 0:
                        R = (E-c-COST)/(SL-E+COST) if dd < 0 else (c-E-COST)/(E-SL+COST); ex = 'flat'
                    if R is not None:
                        trades.append(dict(w=w, d=d, t=te, dir=dd, E=E, SL=SL, TP=TP, R=R, ex=ex, risk=abs(SL-E)/PIP))
                        opn = None
                    continue
                if used >= MAX_TR or t.hour < FROM_H or t.hour > LAST_H or mins - lastT < DEDUP_MIN: continue
                dd = day_dir
                if dd < 0:
                    cands = [L for L in LV if h >= L + OFF and L >= o]
                    if not cands: continue
                    L = min(cands); E = L + OFF
                else:
                    cands = [L for L in LV if l <= L - OFF and L <= o]
                    if not cands: continue
                    L = max(cands); E = L - OFF
                rH, rL = max(sH, h), min(sL, l)
                if rH - rL <= 0: continue
                pos = (E - rL) / (rH - rL)
                if (dd < 0 and pos < 0.5) or (dd > 0 and pos > 0.5): continue
                SL = rH + BUF if dd < 0 else rL - BUF
                if (dd < 0 and SL <= E) or (dd > 0 and SL >= E): continue
                risk = abs(SL - E)
                if dd < 0:
                    tps = [L2 for L2 in LV if L2 < E and (E-L2-COST)/(risk+COST) >= MINRR]
                    if not tps: continue
                    TP = max(tps)
                else:
                    tps = [L2 for L2 in LV if L2 > E and (L2-E-COST)/(risk+COST) >= MINRR]
                    if not tps: continue
                    TP = min(tps)
                opn = (dd, E, SL, TP, t); used += 1; lastT = mins
            if d in dhi:
                wkH = max(wkH, dhi[d]); wkL = min(wkL, dlo[d])
    return trades

def stats(tr, label):
    if not tr: print(f"{label}: 0 угод"); return
    Rs = [x['R'] for x in tr]; n = len(Rs); w = sum(1 for r in Rs if r > 0)
    tot = sum(Rs); m = mean(Rs)
    # bootstrap CI на середнє
    rng = random.Random(1); ms = []
    for _ in range(2000):
        s = [Rs[rng.randrange(n)] for _ in range(n)]; ms.append(mean(s))
    ms.sort(); lo, hi = ms[50], ms[1950]
    print(f"{label}: n={n}  WR={100*w/n:.1f}%  E[R]={m:+.3f}  CI95=[{lo:+.3f};{hi:+.3f}]  ΣR={tot:+.1f}  "
          f"сер.виграш={mean([r for r in Rs if r>0]) if w else 0:+.2f}  сер.ризик={mean(x['risk'] for x in tr):.1f}п")
    return m, tot

real = run(lambda w, rng: weekly_bias(w))
print("=== v5, реальний напрямок ===")
m_real, tot_real = stats(real, "ВСЬОГО")
# по місяцях
bym = defaultdict(list)
for x in real: bym[x['d'].strftime('%Y-%m')].append(x['R'])
print("по місяцях:")
for k in sorted(bym):
    Rs = bym[k]; print(f"  {k}  n={len(Rs):3d}  WR={100*sum(1 for r in Rs if r>0)/len(Rs):5.1f}%  ΣR={sum(Rs):+6.1f}")
# розподіл по тижнях
byw = defaultdict(float)
for x in real: byw[x['w']] += x['R']
ws = list(byw.values()); ws.sort()
print(f"тижнів з угодами: {len(ws)}  прибуткових: {sum(1 for v in ws if v>0)}  медіана тижня: {median(ws):+.2f}R  гірший: {ws[0]:+.1f}  кращий: {ws[-1]:+.1f}")
# контроль: вхід ЛИШЕ 09:00 vs без фільтра — окремо не рахуємо тут
# нульова модель: випадковий напрямок на тиждень
print("\n=== нульова модель: випадковий напрямок (120 прогонів) ===")
tots = []; means = []
for s in range(120):
    tr = run(lambda w, rng: rng.choice([-1, 1]), seed=s)
    if tr: tots.append(sum(x['R'] for x in tr)); means.append(mean(x['R'] for x in tr))
tots.sort(); means.sort()
pct = sum(1 for v in tots if v < tot_real) / len(tots)
print(f"ΣR нульової: медіана {median(tots):+.1f}  5%={tots[int(0.05*len(tots))]:+.1f}  95%={tots[int(0.95*len(tots))]:+.1f}")
print(f"E[R] нульової: медіана {median(means):+.3f}")
print(f"реальний ΣR={tot_real:+.1f} → перцентиль серед нульових: {100*pct:.0f}%")
