#!/usr/bin/env python3
"""Абляція v6 на всій базі: що прибрати, що додати."""
import csv, random, datetime as dt
from collections import defaultdict
from statistics import median, mean

PATH = "/Users/serhiin/AI/research/strategies/data_dukascopy/duka_eurusd_m5cache_mid_M5.csv"
PIP = 0.0001; COST = 2.0*PIP; BUF = 0.5*PIP; OFF = 0.2*PIP
FLAT_H = 19

bars = []
for r in csv.DictReader(open(PATH)):
    bars.append((dt.datetime.strptime(r["time_utc"], "%Y-%m-%dT%H:%M:%SZ"),
                 float(r["open"]), float(r["high"]), float(r["low"]), float(r["close"])))
bars.sort(key=lambda x: x[0])
days = defaultdict(list)
for i, x in enumerate(bars): days[x[0].date()].append(i)
full = [d for d in sorted(days) if len(days[d]) >= 200]
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
h1 = defaultdict(lambda: [0.0, 9.0])
for x in bars:
    k = x[0].replace(minute=0, second=0)
    h1[k][0] = max(h1[k][0], x[2]); h1[k][1] = min(h1[k][1], x[3])
h1k = sorted(h1); pivots = []
for j in range(1, len(h1k)-1):
    a, b, c = h1[h1k[j-1]], h1[h1k[j]], h1[h1k[j+1]]
    if b[0] >= a[0] and b[0] >= c[0]: pivots.append((h1k[j], b[0]))
    if b[1] <= a[1] and b[1] <= c[1]: pivots.append((h1k[j], b[1]))

def weekly_bias(w):
    if w not in pw: return 0
    p = pw[w]; H, L, C = whi[w], wlo[w], wcl[w]; PH, PL = whi[p], wlo[p]
    tH, tL = H > PH, L < PL
    if tH and not tL: return 1 if C > PH else -1
    if tL and not tH: return -1 if C < PL else 1
    if tH and tL: return 1 if C > (H+L)/2 else -1
    if p not in pw: return 0
    pp = pw[p]
    if whi[w] > whi[p] > whi[pp] and wlo[w] > wlo[p] > wlo[pp]: return 1
    if whi[w] < whi[p] < whi[pp] and wlo[w] < wlo[p] < wlo[pp]: return -1
    return 0

D = dict(shift=True, minbody=2.0*PIP, from_h=9, last_h=17, prem=True, maxtr=2,
         dedup=60, minrr=2.0, maxrisk=0.0, scen=True, boundary=True, piv=10,
         fresh=False, dirfn=None)

def run(**kw):
    P = dict(D); P.update(kw)
    dirfn = P['dirfn'] or (lambda w, r: weekly_bias(w))
    rng = random.Random(P.get('seed'))
    trades = []
    for wi, w in enumerate(wk):
        if w not in pw: continue
        d0 = dirfn(w, rng)
        if d0 == 0: continue
        PW = pw[w]; PWH, PWL = whi[PW], wlo[PW]
        hist = [whi[x]-wlo[x] for x in wk[max(0, wi-8):wi]]
        WKFULL = median(hist) if hist else 0.011
        cur = d0; wkH, wkL = 0.0, 9.0
        for d in wks[w]:
            if d not in prevday: continue
            pdd = prevday[d]
            complete = P['boundary'] and (wkH - wkL) >= WKFULL
            idx = days[d]
            asia = [i for i in idx if bars[i][0].hour < 6]
            if not asia: continue
            asH = max(bars[i][2] for i in asia); asL = min(bars[i][3] for i in asia)
            t0 = bars[idx[0]][0].replace(hour=6, minute=0)
            cut = t0 - dt.timedelta(days=P['piv'])
            lv = {round(p, 5) for (t, p) in pivots if cut <= t < t0}
            lv |= {round(dhi[pdd],5), round(dlo[pdd],5), round(asH,5), round(asL,5), round(PWH,5), round(PWL,5)}
            LV = sorted(lv)
            sH, sL = 0.0, 9.0; extIdx = None; shift = False
            opn = None; used = 0; lastT = -999; touched = set()
            day_dir = cur
            if complete: day_dir = 1 if (asL - wkL) < (wkH - asL) else -1
            seq = [i for i in idx if 6 <= bars[i][0].hour <= FLAT_H]
            for k, i in enumerate(seq):
                t, o, h, l, c = bars[i]
                dd = day_dir
                if dd < 0:
                    if h > sH: sH = h; extIdx = k; shift = False
                else:
                    if l < sL: sL = l; extIdx = k; shift = False
                sH = max(sH, h); sL = min(sL, l)
                if P['scen'] and t.minute == 55 and not complete:
                    if c < PWL and cur != -1: cur = -1; day_dir = -1; shift = False; extIdx = None
                    if c > PWH and cur != 1: cur = 1; day_dir = 1; shift = False; extIdx = None
                if extIdx is not None and k >= extIdx + 2 and not shift:
                    p1 = bars[seq[k-1]]; pb = abs(p1[4]-p1[1])
                    if dd < 0:
                        sw = min(bars[seq[j]][3] for j in range(extIdx, k)); body = o - c
                        if c < sw and body >= P['minbody'] and body > pb: shift = True
                    else:
                        sw = max(bars[seq[j]][2] for j in range(extIdx, k)); body = c - o
                        if c > sw and body >= P['minbody'] and body > pb: shift = True
                if opn:
                    ddo, E, SL, TP, te, lvl = opn
                    R = ex = None
                    if ddo < 0:
                        if h >= SL: R, ex = -1.0, 'SL'
                        elif l <= TP: R, ex = (E-TP-COST)/(SL-E+COST), 'TP'
                    else:
                        if l <= SL: R, ex = -1.0, 'SL'
                        elif h >= TP: R, ex = (TP-E-COST)/(E-SL+COST), 'TP'
                    if R is None and t.hour == FLAT_H and t.minute == 0:
                        R = (E-c-COST)/(SL-E+COST) if ddo < 0 else (c-E-COST)/(E-SL+COST); ex = 'flat'
                    if R is not None:
                        trades.append(dict(d=d, R=R, risk=abs(SL-E)/PIP, ex=ex, t=te, dir=ddo)); opn = None
                    continue
                mins = t.hour*60 + t.minute
                if used >= P['maxtr'] or t.hour < P['from_h'] or t.hour > P['last_h'] or mins - lastT < P['dedup']: continue
                if P['shift'] and not shift: continue
                if dd < 0:
                    cands = [L for L in LV if h >= L + OFF and L >= o]
                    if P['fresh']: cands = [L for L in cands if L not in touched]
                    if not cands: continue
                    L = min(cands); E = L + OFF
                else:
                    cands = [L for L in LV if l <= L - OFF and L <= o]
                    if P['fresh']: cands = [L for L in cands if L not in touched]
                    if not cands: continue
                    L = max(cands); E = L - OFF
                rH, rL = max(sH, h), min(sL, l)
                if rH - rL <= 0: continue
                pos = (E - rL) / (rH - rL)
                if P['prem'] and ((dd < 0 and pos < 0.5) or (dd > 0 and pos > 0.5)): continue
                SL = rH + BUF if dd < 0 else rL - BUF
                if (dd < 0 and SL <= E) or (dd > 0 and SL >= E): continue
                risk = abs(SL - E)
                if P['maxrisk'] and risk > P['maxrisk']: continue
                if dd < 0:
                    tps = [x for x in LV if x < E and (E-x-COST)/(risk+COST) >= P['minrr']]
                    if not tps: continue
                    TP = max(tps)
                else:
                    tps = [x for x in LV if x > E and (x-E-COST)/(risk+COST) >= P['minrr']]
                    if not tps: continue
                    TP = min(tps)
                opn = (dd, E, SL, TP, t, L); used += 1; lastT = mins; touched.add(L)
            if d in dhi: wkH = max(wkH, dhi[d]); wkL = min(wkL, dlo[d])
    return trades

def st(tr, label):
    if not tr or len(tr) < 5:
        print(f"{label:34s} n={len(tr):4d}  —"); return
    Rs = [x['R'] for x in tr]; n = len(Rs); wn = sum(1 for r in Rs if r > 0)
    m = mean(Rs)
    rng = random.Random(1); ms = sorted(mean([Rs[rng.randrange(n)] for _ in range(n)]) for _ in range(1500))
    aw = mean([r for r in Rs if r > 0]) if wn else 0
    be = 100/(1+aw) if aw else 99
    print(f"{label:34s} n={n:4d}  WR={100*wn/n:5.1f}%  E[R]={m:+.3f}  CI=[{ms[37]:+.3f};{ms[1462]:+.3f}]  "
          f"ΣR={sum(Rs):+7.1f}  вигр={aw:+.2f}  беззб.WR={be:4.1f}%")

print("=== БАЗА v6 ===")
st(run(), "v6 базова")

print("\n=== ПРИБРАТИ (по одному) ===")
st(run(shift=False),    "− Shift")
st(run(prem=False),     "− Premium/Discount")
st(run(from_h=6),       "− година 09:00")
st(run(scen=False),     "− сценарії A/B")
st(run(boundary=False), "− межа тижня")
st(run(dedup=0),        "− дедуплікація")

print("\n=== ДОДАТИ: обмеження ризику ===")
for r in [5, 8, 10, 12, 15, 20]:
    st(run(maxrisk=r*PIP), f"+ ризик ≤ {r} п")

print("\n=== ДОДАТИ: сила Shift (тіло) ===")
for b in [1.0, 2.0, 3.0, 4.0]:
    st(run(minbody=b*PIP), f"+ тіло Shift ≥ {b} п")

print("\n=== ДОДАТИ: нетестований рівень (fresh POI) ===")
st(run(fresh=True), "+ тільки нетестовані рівні")

print("\n=== ЦІЛЬ / КІЛЬКІСТЬ ===")
for r in [1.5, 2.0, 2.5, 3.0, 4.0]:
    st(run(minrr=r), f"MINRR {r}")
for m in [1, 2, 3]:
    st(run(maxtr=m), f"макс {m} угод/день")
print("\n=== ВІКНО ВХОДУ ===")
for a, b in [(9,17),(9,14),(9,12),(10,17),(12,17),(7,17)]:
    st(run(from_h=a, last_h=b), f"вхід {a:02d}:00–{b:02d}:00")

print("\n=== КАРТА: глибина півотів ===")
for p in [5, 10, 20, 40]:
    st(run(piv=p), f"H1-півоти за {p} днів")

print("\n=== НАЙКРАЩА КОМБІНАЦІЯ (перевірка) ===")
best = run(maxrisk=10*PIP, minbody=3.0*PIP, fresh=True)
st(best, "v7 = ризик≤10 + тіло≥3 + fresh")
bym = defaultdict(list)
for x in best: bym[x['d'].strftime('%Y-%m')].append(x['R'])
print("  по місяцях: " + "  ".join(f"{k[-2:]}:{sum(v):+.0f}" for k, v in sorted(bym.items())))
print("\n  нульова модель для v7 (60 прогонів):")
tots = sorted(sum(x['R'] for x in run(maxrisk=10*PIP, minbody=3.0*PIP, fresh=True,
                                      dirfn=lambda w, r: r.choice([-1,1]), seed=s)) for s in range(60))
tr = sum(x['R'] for x in best)
print(f"  медіана нульової {median(tots):+.1f}  5%={tots[3]:+.1f}  95%={tots[56]:+.1f}  "
      f"→ реальний {tr:+.1f} = перцентиль {100*sum(1 for v in tots if v < tr)/len(tots):.0f}%")

print("\n\n=== КОМБІНАЦІЯ ДВОХ ЗНАХІДОК ===")
st(run(scen=False), "− сценарії")
st(run(maxrisk=5*PIP), "+ ризик ≤5")
c = run(scen=False, maxrisk=5*PIP)
st(c, "− сценарії + ризик ≤5")
st(run(scen=False, maxrisk=5*PIP, prem=False), "  той самий − Premium")
st(run(scen=False, maxrisk=8*PIP), "− сценарії + ризик ≤8")
st(run(scen=False, maxrisk=6*PIP), "− сценарії + ризик ≤6")

print("\n=== WALK-FORWARD: підбір на 1-й половині, перевірка на 2-й ===")
CUT = dt.date(2026, 2, 1)
def split(tr):
    return [x for x in tr if x['d'] < CUT], [x for x in tr if x['d'] >= CUT]
variants = [("v6 базова", {}), ("− сценарії", dict(scen=False)),
            ("ризик≤5", dict(maxrisk=5*PIP)), ("− сцен + ризик≤5", dict(scen=False, maxrisk=5*PIP)),
            ("− сцен + ризик≤8", dict(scen=False, maxrisk=8*PIP)),
            ("− сцен + ризик≤5 − prem", dict(scen=False, maxrisk=5*PIP, prem=False))]
print(f"{'варіант':28s} {'IS (вер25–січ26)':>22s}   {'OOS (лют–лип26)':>22s}")
for nm, kw in variants:
    a, b = split(run(**kw))
    fa = f"n={len(a):3d} E[R]={mean(x['R'] for x in a):+.3f} Σ{sum(x['R'] for x in a):+6.1f}" if len(a) > 4 else "мало"
    fb = f"n={len(b):3d} E[R]={mean(x['R'] for x in b):+.3f} Σ{sum(x['R'] for x in b):+6.1f}" if len(b) > 4 else "мало"
    print(f"{nm:28s} {fa:>22s}   {fb:>22s}")

print("\n=== ФІНАЛ: − сценарії + ризик ≤5, помісячно ===")
f = run(scen=False, maxrisk=5*PIP)
bym = defaultdict(list)
for x in f: bym[x['d'].strftime('%Y-%m')].append(x['R'])
for k in sorted(bym):
    v = bym[k]
    print(f"  {k}  n={len(v):3d}  WR={100*sum(1 for r in v if r>0)/len(v):5.1f}%  ΣR={sum(v):+6.1f}")
print("\n  нульова (60 прогонів):")
tt = sorted(sum(x['R'] for x in run(scen=False, maxrisk=5*PIP, dirfn=lambda w,r: r.choice([-1,1]), seed=s)) for s in range(60))
rr = sum(x['R'] for x in f)
print(f"  медіана {median(tt):+.1f}  5%={tt[3]:+.1f}  95%={tt[56]:+.1f}  → реальний {rr:+.1f} = перцентиль {100*sum(1 for v in tt if v<rr)/len(tt):.0f}%")
