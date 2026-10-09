"""«Просто логіка і сетапи»: без RR-гейта, TP до найближчої зони АБО ліквідності,
   БЕЗ EOD-flat — тримаємо до TP чи SL. Порівняння з нульовою моделлю."""
import csv,statistics as st,collections,datetime as dt,random,sys,json
D='/Users/serhiin/AI/research/strategies/data/'
F=['eurusd_blind2024_M15.csv','eurusd_blind2025_M15.csv','eurusd_gate2025_M15.csv',
   'eurusd_janfeb_M15.csv','eurusd_mam_M15.csv','eurusd_june_M15.csv','eurusd_july_M15.csv']
PIP=0.0001; COST=2.0; BUF=2.0; MAXDAYS=10; SEED=20260916; NREP=300
bars={}
for f in F:
    for r in csv.DictReader(open(D+f)):
        bars[r['time_utc']]=(float(r['open']),float(r['high']),float(r['low']),float(r['close']))
T=sorted(bars); B=[bars[t] for t in T]; N=len(T)
def agg(key):
    out=[];cur=None;ck=None;ci=None
    for i,t in enumerate(T):
        k=key(t); o,h,l,c=B[i]
        if k!=ck:
            if cur: out.append((ci,cur[0],cur[1],cur[2],cur[3]))
            cur=[o,h,l,c];ck=k;ci=i
        else:
            cur[1]=max(cur[1],h);cur[2]=min(cur[2],l);cur[3]=c
    if cur: out.append((ci,cur[0],cur[1],cur[2],cur[3]))
    return out
H1=agg(lambda t:t[:13]); H4=agg(lambda t:(t[:10],int(t[11:13])//4))
def fr(x):
    H=[j for j in range(2,len(x)-2) if x[j][2]>max(x[y][2] for y in range(j-2,j+3) if y!=j)]
    L=[j for j in range(2,len(x)-2) if x[j][3]<min(x[y][3] for y in range(j-2,j+3) if y!=j)]
    return H,L
h1H,h1L=fr(H1); h4H,h4L=fr(H4)
# --- незаповнені H1 FVG як «зони»
zonesU=[];zonesD=[]   # (idx, lo, hi)
for k in range(2,len(H1)):
    lo,hi=H1[k-2][2],H1[k][3]
    if hi>lo: zonesU.append((H1[k][0],lo,hi))      # бичачий розрив (підтримка знизу)
    hi2,lo2=H1[k-2][3],H1[k][2]
    if hi2>lo2: zonesD.append((H1[k][0],lo2,hi2))  # ведмежий розрив (опір зверху)
# --- H4 bias
bias=[None]*N; last='none'
for k in range(len(H4)):
    hs=[H4[j][2] for j in h4H if j<k-2]; ls=[H4[j][3] for j in h4L if j<k-2]
    if hs and H4[k][4]>max(hs[-3:]): last='long'
    elif ls and H4[k][4]<min(ls[-3:]): last='short'
    for ii in range(H4[k][0], H4[k+1][0] if k+1<len(H4) else N): bias[ii]=last

def target(i,ref,d):
    """найближча ЗОНА або ЛІКВІДНІСТЬ у бік угоди, за орієнтиром ref"""
    c=[]
    if d=='long':
        c+=[H1[j][2] for j in h1H if H1[j][0]<i and H1[j][2]>ref]
        c+=[H4[j][2] for j in h4H if H4[j][0]<i and H4[j][2]>ref]
        c+=[z[1] for z in zonesD if z[0]<i and z[1]>ref]      # нижній край ведмежого FVG зверху
        return min(c) if c else None
    c+=[H1[j][3] for j in h1L if H1[j][0]<i and H1[j][3]<ref]
    c+=[H4[j][3] for j in h4L if H4[j][0]<i and H4[j][3]<ref]
    c+=[z[2] for z in zonesU if z[0]<i and z[2]<ref]
    return max(c) if c else None

def run(fi,d,entry,sl_d,tp_d):
    sl=entry-sl_d*PIP if d=='long' else entry+sl_d*PIP
    tp=entry+tp_d*PIP if d=='long' else entry-tp_d*PIP
    lim=min(fi+1+MAXDAYS*96,N)
    for k in range(fi+1,lim):
        o,h,l,c=B[k]
        if (l<=sl) if d=='long' else (h>=sl): return (-sl_d-COST)/(sl_d+COST),'SL'
        if (h>=tp) if d=='long' else (l<=tp): return (tp_d-COST)/(sl_d+COST),'TP'
    c=B[lim-1][3]; pnl=(c-entry)/PIP if d=='long' else (entry-c)/PIP
    return (pnl-COST)/(sl_d+COST),'TIME'

# ---------- сетапи ТС-3: свіжий 15m BOS у бік bias -> inner FVG
sw_h=[j for j in range(2,N-2) if B[j][1]>max(B[y][1] for y in range(j-2,j+3) if y!=j)]
sw_l=[j for j in range(2,N-2) if B[j][2]<min(B[y][2] for y in range(j-2,j+3) if y!=j)]
setups=[]
busy=-1
for i in range(200,N-1):
    if i<busy: continue
    bi=bias[i]
    if bi not in ('long','short'): continue
    if bi=='long':
        prior=[B[j][1] for j in sw_h if j<i-2]
        if not prior or B[i][3]<=max(prior[-3:]): continue
        base=[j for j in sw_l if j<i]
        if not base: continue
        lo=B[base[-1]][2]; hi=max(B[j][1] for j in range(base[-1],i+1))
    else:
        prior=[B[j][2] for j in sw_l if j<i-2]
        if not prior or B[i][3]>=min(prior[-3:]): continue
        base=[j for j in sw_h if j<i]
        if not base: continue
        hi=B[base[-1]][1]; lo=min(B[j][2] for j in range(base[-1],i+1))
    fvg=None
    for k in range(max(base[-1]+2,2), i+1):
        if bi=='long':
            a,b=B[k-2][1],B[k][2]
            if b-a>=5*PIP and b<lo+0.5*(hi-lo): fvg=(a,b)
        else:
            b,a=B[k-2][2],B[k][1]
            if b-a>=5*PIP and a>lo+0.5*(hi-lo): fvg=(a,b)
    if fvg is None: continue
    entry=fvg[1] if bi=='long' else fvg[0]
    strong=lo if bi=='long' else hi
    sl_d=abs(entry-strong)/PIP+BUF
    if not (5<=sl_d<=45): continue
    ref=hi if bi=='long' else lo
    tp=target(i,ref,bi)
    if tp is None: continue
    tp_d=abs(tp-entry)/PIP
    if tp_d<=COST: continue
    fill=None
    for k in range(i+1,min(i+25,N)):
        if (bi=='long' and B[k][2]<=entry) or (bi=='short' and B[k][1]>=entry): fill=k;break
    if fill is None: continue
    R,why=run(fill,bi,entry,sl_d,tp_d)
    busy=fill+96
    setups.append(dict(t=T[fill],dir=bi,R=R,why=why,sl=sl_d,tp=tp_d,entry=entry,fill=fill,
                       rr=(tp_d-COST)/(sl_d+COST)))
def q(v,p):
    z=sorted(v); return z[int(p*(len(z)-1))]
def show(nm,tr):
    if not tr: print(f"  {nm:8} —"); return
    Rs=[x['R'] for x in tr]; w=[x for x in tr if x['R']>0]
    gp=sum(x['R'] for x in w); gl=-sum(x['R'] for x in tr if x['R']<=0)
    print(f"  {nm:8} N={len(tr):3d}  WR {100*len(w)/len(tr):5.1f}%  E {st.mean(Rs):+.3f}R  PF {gp/gl if gl>0 else 99:5.2f}  Σ {sum(Rs):+7.1f}R")
print(f"\n=== Тільки логіка: без RR-гейта, без EOD-flat, TP = зона/ліквідність, max {MAXDAYS} дн ===")
show('ВСЬОГО',setups)
for y in ('2024','2025','2026'): show(y,[x for x in setups if x['t'][:4]==y])
show('LONG',[x for x in setups if x['dir']=='long']); show('SHORT',[x for x in setups if x['dir']=='short'])
print(f"\n  виходи: {dict(collections.Counter(x['why'] for x in setups))}")
print(f"  SL медіана {st.median([x['sl'] for x in setups]):.1f}п · TP {st.median([x['tp'] for x in setups]):.1f}п · RR {st.median([x['rr'] for x in setups]):.2f}")
# нуль
Es=[];WRs=[]
for r_ in range(NREP):
    rg=random.Random(SEED+r_); Rs=[]
    for x in setups:
        R,_=run(x['fill'],rg.choice(('long','short')),x['entry'],x['sl'],x['tp'])
        Rs.append(R)
    Es.append(st.mean(Rs)); WRs.append(100*sum(1 for r in Rs if r>0)/len(Rs))
e=st.mean([x['R'] for x in setups]); w=100*sum(1 for x in setups if x['R']>0)/len(setups)
print(f"\n  нуль:   WR {st.mean(WRs):5.1f}%  E {st.mean(Es):+.3f}R   CI WR [{q(WRs,.025):.1f}; {q(WRs,.975):.1f}]  CI E [{q(Es,.025):+.3f}; {q(Es,.975):+.3f}]")
print(f"  надлишок WR {w-st.mean(WRs):+.1f} пп CI [{w-q(WRs,.975):+.1f}; {w-q(WRs,.025):+.1f}]")
print(f"  надлишок E  {e-st.mean(Es):+.3f}R CI [{e-q(Es,.975):+.3f}; {e-q(Es,.025):+.3f}]")
print(f"\n  {'✅ КРАЩЕ за випадковий' if w>q(WRs,.975) else ('❌ гірше' if w<q(WRs,.025) else '⚪ нерозрізнимо')}")
json.dump(setups,open('logic_only.json','w'))
