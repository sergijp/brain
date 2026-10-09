import sys,io,contextlib,importlib.util,csv,datetime as dt,random
from statistics import median
PIP=0.0001; COST=2.0*PIP; FLAT_H=19
spec=importlib.util.spec_from_file_location("det","sweep_mss_m5_v2.py")
m=importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()):
    sys.argv=["det"]; spec.loader.exec_module(m)
T=m.trades; bars=m.bars; idx_of={b[0]:i for i,b in enumerate(bars)}

def null_for(ts,seed):
    rnd=random.Random(seed); rs=[]
    for t in ts:
        d=rnd.choice((1,-1)); e=t["entry"]; risk=t["risk"]; tpd=abs(t["tp"]-t["entry"])
        sl=e-d*risk; tp=e+d*tpd; i0=idx_of[t["t"]]; out=None
        for k in range(i0,len(bars)):
            _,_,h,l,c=bars[k]
            if bars[k][0].date()!=t["date"]: break
            if (l<=sl if d==1 else h>=sl): out=sl; break
            if (h>=tp if d==1 else l<=tp): out=tp; break
            if bars[k][0].hour>=FLAT_H: out=c; break
        if out is None: out=bars[k-1][4]
        rs.append((d*(out-e)-COST)/(risk+COST))
    return sum(rs)/len(rs)

W=[("W1 вер-гру 2025",dt.date(2025,9,1),dt.date(2025,12,31)),
   ("W2 січ-бер 2026",dt.date(2026,1,1),dt.date(2026,3,31)),
   ("W3 кві-лип 2026",dt.date(2026,4,1),dt.date(2026,7,31))]
print(f"{'вікно':<18} {'n':>4} {'E[R]':>8} {'нуль':>8} {'надлишок':>9} {'WR':>6} {'p':>6}")
for nm,a,b in W+[("ВСЕ",dt.date(2000,1,1),dt.date(2100,1,1))]:
    ts=[t for t in T if a<=t["date"]<=b]
    if not ts: continue
    e=sum(t["R"] for t in ts)/len(ts)
    E=sorted(null_for(ts,20260916+s) for s in range(200))
    p=sum(1 for x in E if x>=e)/len(E)
    wr=sum(1 for t in ts if t["R"]>0)/len(ts)
    print(f"{nm:<18} {len(ts):>4} {e:>+8.3f} {median(E):>+8.3f} {e-median(E):>+9.3f} {wr:>5.1%} {p:>6.3f}")

# bootstrap CI of excess on the full sample
rs=[t["R"] for t in T]
base_null=median(sorted(null_for(T,20260916+s) for s in range(200)))
rnd=random.Random(11); bs=[]
for _ in range(3000): bs.append(sum(rnd.choice(rs) for _ in rs)/len(rs)-base_null)
bs.sort()
print(f"\nCI95 надлишку: [{bs[75]:+.3f}; {bs[2924]:+.3f}]")
print(f"Беззбитковий WR при RR={median(t['rr'] for t in T):.2f}: {1/(1+median(t['rr'] for t in T)):.1%}  (фактичний {sum(1 for t in T if t['R']>0)/len(T):.1%})")
