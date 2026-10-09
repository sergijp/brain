#!/usr/bin/env python3
"""Null model for sweep_mss_m5: same entry times, same SL/TP distances, direction = coin flip."""
import csv, sys, datetime as dt, random, runpy, io, contextlib
from statistics import median

PIP=0.0001; COST=2.0*PIP; FLAT_H=19
PATH="/Users/serhiin/AI/research/strategies/data_dukascopy/duka_eurusd_m5cache_mid_M5.csv"
bars=[]
with open(PATH) as f:
    for r in csv.DictReader(f):
        bars.append((dt.datetime.strptime(r["time_utc"],"%Y-%m-%dT%H:%M:%SZ"),
                     float(r["open"]),float(r["high"]),float(r["low"]),float(r["close"])))
bars.sort(key=lambda x:x[0])
idx_of={b[0]:i for i,b in enumerate(bars)}

# re-import the detector's trade list
import importlib.util
spec=importlib.util.spec_from_file_location("det","sweep_mss_m5_v2.py")
m=importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()):
    sys.argv=["det"]; spec.loader.exec_module(m)
T=m.trades
print(f"Реальних трейдів: {len(T)}  E[R]={sum(t['R'] for t in T)/len(T):+.3f}")

def sim(seed):
    rnd=random.Random(seed); rs=[]
    for t in T:
        d=rnd.choice((1,-1))
        e=t["entry"]; risk=t["risk"]; tpd=abs(t["tp"]-t["entry"])
        sl=e-d*risk; tp=e+d*tpd
        i0=idx_of[t["t"]]; out=None
        for k in range(i0,len(bars)):
            _,_,h,l,c=bars[k]
            if bars[k][0].date()!=t["date"]: break
            if (l<=sl if d==1 else h>=sl): out=sl; break
            if (h>=tp if d==1 else l<=tp): out=tp; break
            if bars[k][0].hour>=FLAT_H: out=c; break
        if out is None: out=bars[k-1][4]
        rs.append((d*(out-e)-COST)/(risk+COST))
    return sum(rs)/len(rs)

E=[sim(20260916+s) for s in range(200)]
E.sort()
real=sum(t['R'] for t in T)/len(T)
print(f"Нуль (200 реплікацій): E[R] медіана={median(E):+.3f}  CI95=[{E[4]:+.3f}; {E[194]:+.3f}]")
print(f"Надлишок над нулем: {real-median(E):+.3f}")
print(f"Частка реплікацій нуля, що кращі за реальний: {sum(1 for e in E if e>=real)/len(E):.1%}")
