"""Narrative Layer — механічна перевірка компонента Market State.
   Питання: чи дні Compression справді дають менше руху, доступного інтрадей-трейдеру?
   Специфікація зафіксована в коді ДО перегляду результатів."""
import csv,statistics as st,collections,datetime as dt
D='/Users/serhiin/AI/research/strategies/data/'
FILES=['eurusd_blind2024_M15.csv','eurusd_blind2025_M15.csv','eurusd_gate2025_M15.csv',
       'eurusd_janfeb_M15.csv','eurusd_mam_M15.csv','eurusd_june_M15.csv','eurusd_july_M15.csv']
PIP=0.0001; START_H=7; FLAT_H=19
bars={}
for f in FILES:
    for r in csv.DictReader(open(D+f)):
        bars[r['time_utc']]=(float(r['open']),float(r['high']),float(r['low']),float(r['close']))
T=sorted(bars)
days=collections.OrderedDict()
for t in T:
    d=t[:10]; o,h,l,c=bars[t]
    if d not in days: days[d]=[o,h,l,c]
    else:
        days[d][1]=max(days[d][1],h); days[d][2]=min(days[d][2],l); days[d][3]=c
dl=[d for d in days if dt.date.fromisoformat(d).weekday()<5]
print(f"торгових днів {len(dl)}  {dl[0]} → {dl[-1]}")

# ATR_D(14) і його ковзна медіана за 60 днів
atr={}
for i,d in enumerate(dl):
    if i<14: continue
    trs=[]
    for j in range(i-14,i):
        o,h,l,c=days[dl[j]]; pc=days[dl[j-1]][3]
        trs.append(max(h-l,abs(h-pc),abs(l-pc)))
    atr[d]=sum(trs)/14
med60={}
ks=[d for d in dl if d in atr]
for i,d in enumerate(ks):
    if i<60: continue
    med60[d]=st.median([atr[x] for x in ks[i-60:i]])

# --- класифікація стану (на відкритті дня, тільки з минулих даних)
def state(i):
    d=dl[i]
    if d not in atr or d not in med60: return None
    po,ph,pl,pc = days[dl[i-1]]
    ppo,pph,ppl,ppc = days[dl[i-2]]
    inside = ph<=pph and pl>=ppl                 # вчора inside day
    prev_rng=(ph-pl)
    low_atr = atr[d] < med60[d]
    narrow  = prev_rng < 0.7*atr[d]
    over    = prev_rng > 1.5*atr[d]              # вчора здутий рух
    if over: return 'overextension'
    if inside or (low_atr and narrow): return 'compression'
    return 'expansion'

# --- доступний рух: від 07:00 UTC до 19:00, більша з двох сторін
def avail(d):
    o=None;hi=None;lo=None
    for t in T:
        if t[:10]!=d: continue
        hh=int(t[11:13])
        if hh<START_H or hh>=FLAT_H: continue
        oo,h,l,c=bars[t]
        if o is None: o=oo
        hi=h if hi is None else max(hi,h); lo=l if lo is None else min(lo,l)
    if o is None: return None
    return max(hi-o, o-lo)/PIP, (hi-lo)/PIP

res=collections.defaultdict(list); rng=collections.defaultdict(list)
for i in range(2,len(dl)):
    s=state(i)
    if s is None: continue
    a=avail(dl[i])
    if a is None: continue
    res[s].append(a[0]); rng[s].append(a[1])
def q(v,p):
    z=sorted(v); return z[int(p*(len(z)-1))]
print(f"\n{'стан':14} {'N':>5} {'доступний рух 07-19 UTC (п)':>34}   {'діапазон вікна':>22}")
print(f"{'':14} {'':>5} {'медіана':>10} {'p25':>8} {'p75':>8}   {'медіана':>10} {'p25':>8}")
for s in ('expansion','compression','overextension'):
    v=res[s]; r=rng[s]
    if not v: continue
    print(f"{s:14} {len(v):5d} {st.median(v):10.1f} {q(v,.25):8.1f} {q(v,.75):8.1f}   {st.median(r):10.1f} {q(r,.25):8.1f}")
allv=[x for s in res for x in res[s]]
print(f"{'ВСІ':14} {len(allv):5d} {st.median(allv):10.1f} {q(allv,.25):8.1f} {q(allv,.75):8.1f}")

# bootstrap різниці медіан compression vs expansion
import random
r=random.Random(20260916)
A=res['expansion']; B=res['compression']
d0=st.median(A)-st.median(B)
boot=[]
for _ in range(2000):
    a=[r.choice(A) for _ in A]; b=[r.choice(B) for _ in B]
    boot.append(st.median(a)-st.median(b))
print(f"\nΔ медіан (expansion − compression) = {d0:+.1f} п   95% CI [{q(boot,.025):+.1f}; {q(boot,.975):+.1f}]")
C=res['overextension']
d1=st.median(A)-st.median(C)
boot2=[]
for _ in range(2000):
    a=[r.choice(A) for _ in A]; c=[r.choice(C) for _ in C]
    boot2.append(st.median(a)-st.median(c))
print(f"Δ медіан (expansion − overextension) = {d1:+.1f} п   95% CI [{q(boot2,.025):+.1f}; {q(boot2,.975):+.1f}]")
print(f"\nЦіна фільтра: Compression = {100*len(B)/len(allv):.1f}% днів. "
      f"Їхня медіана {st.median(B):.1f} п проти {st.median(A):.1f} п у expansion.")
