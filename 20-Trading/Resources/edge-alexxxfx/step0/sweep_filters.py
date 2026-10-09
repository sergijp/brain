#!/usr/bin/env python3
"""Two PRE-DECLARED filters on the sweep_mss_m5 trade list. Bonferroni alpha=0.05/2=0.025.
 F-A  Premium/Discount: short only if sweep sits in upper half of prev-day range (mirror for long)
 F-B  Killzone: entry within London 07:00-10:00 or NY 12:00-15:00 UTC
"""
import sys, io, contextlib, importlib.util, csv, datetime as dt
from statistics import median
from collections import defaultdict
spec=importlib.util.spec_from_file_location("det","sweep_mss_m5.py")
m=importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()):
    sys.argv=["det"]; spec.loader.exec_module(m)
T=m.trades; dhi=m.dhi; dlo=m.dlo; daykeys=m.daykeys
prev={daykeys[i]:daykeys[i-1] for i in range(1,len(daykeys))}

def boot(rs,n=2000,seed=7):
    import random; r=random.Random(seed); out=[]
    for _ in range(n): out.append(sum(r.choice(rs) for _ in rs)/len(rs))
    out.sort(); return out[int(n*0.0125)], out[int(n*0.9875)]   # 97.5% CI (Bonferroni)

def rep(ts,label):
    if len(ts)<10: print(f"{label:<30} n={len(ts)} — замало"); return
    rs=[t["R"] for t in ts]; e=sum(rs)/len(rs); lo,hi=boot(rs)
    print(f"{label:<30} n={len(rs):<4} E[R]={e:+.3f}  CI97.5=[{lo:+.3f}; {hi:+.3f}]  WR={sum(1 for r in rs if r>0)/len(rs):.1%}")

rep(T,"Базова (без фільтрів)")
print()
fa=[]
for t in T:
    p=prev.get(t["date"]);  mid=(dhi[p]+dlo[p])/2 if p else None
    if mid is None: continue
    ref=t["sl"]
    if (t["dir"]==-1 and ref>mid) or (t["dir"]==1 and ref<mid): fa.append(t)
rep(fa,"F-A Premium/Discount")
rep([t for t in T if t not in fa],"F-A відрізане")
print()
KZ=lambda h: 7<=h<10 or 12<=h<15
fb=[t for t in T if KZ(t["t"].hour)]
rep(fb,"F-B Killzone LDN/NY")
rep([t for t in T if not KZ(t["t"].hour)],"F-B відрізане")
print()
rep([t for t in fa if KZ(t["t"].hour)],"F-A + F-B разом")
