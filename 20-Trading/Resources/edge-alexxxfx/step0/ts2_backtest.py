"""ТС-2 Session Manipulation — чесний симулятор на M15.
Правила R1-R6 з ts-2-session-manipulation.md. Специфікація зафіксована ДО прогону.
Послідовність: Judas sweep у KZ -> 15m ChoCH у бік HTF bias -> вхід на FVG що створив ChoCH."""
import csv,statistics as st,collections,datetime as dt,sys,json
D='/Users/serhiin/AI/research/strategies/data/'
F=['eurusd_blind2024_M15.csv','eurusd_blind2025_M15.csv','eurusd_gate2025_M15.csv',
   'eurusd_janfeb_M15.csv','eurusd_mam_M15.csv','eurusd_june_M15.csv','eurusd_july_M15.csv']
PIP=0.0001; COST=2.0; BUF=2.0; MIN_RR=3.0
FLAT_H=19; SOFT_CLOSE=18.5     # R4
KZ=[('LON',7,9),('NY',12,14),('SB',15,16)]   # R1 (London Reversal ~10:00 покривається LON-вікном розширено нижче)
MAX_DAY=2                                     # R5/Risk
ASIA=(0,7)

bars={}
for f in F:
    for r in csv.DictReader(open(D+f)):
        bars[r['time_utc']]=(float(r['open']),float(r['high']),float(r['low']),float(r['close']))
T=sorted(bars); B=[bars[t] for t in T]; N=len(T); IDX={t:i for i,t in enumerate(T)}
print(f"M15 {N} барів {T[0][:10]} → {T[-1][:10]}", file=sys.stderr)

# --- денні структури: азійський діапазон, PDH/PDL
days=collections.OrderedDict()
for i,t in enumerate(T): days.setdefault(t[:10],[]).append(i)
asia={}; pdh={}; pdl={}; prev=None
for d,idxs in days.items():
    a=[j for j in idxs if ASIA[0]<=int(T[j][11:13])<ASIA[1]]
    if a: asia[d]=(max(B[j][1] for j in a), min(B[j][2] for j in a))
    if prev: pdh[d]=max(B[j][1] for j in days[prev]); pdl[d]=min(B[j][2] for j in days[prev])
    prev=d

# --- H4 bias (BOS-напрямок)
H4=[];cur=None;ck=None;ci=None
for i,t in enumerate(T):
    k=(t[:10],int(t[11:13])//4); o,h,l,c=B[i]
    if k!=ck:
        if cur: H4.append((ci,cur[0],cur[1],cur[2],cur[3]))
        cur=[o,h,l,c];ck=k;ci=i
    else:
        cur[1]=max(cur[1],h);cur[2]=min(cur[2],l);cur[3]=c
if cur: H4.append((ci,cur[0],cur[1],cur[2],cur[3]))
h4h=[j for j in range(2,len(H4)-2) if H4[j][2]>max(H4[x][2] for x in range(j-2,j+3) if x!=j)]
h4l=[j for j in range(2,len(H4)-2) if H4[j][3]<min(H4[x][3] for x in range(j-2,j+3) if x!=j)]
bias=[None]*N; last='none'
for k in range(len(H4)):
    hs=[H4[j][2] for j in h4h if j<k-2]; ls=[H4[j][3] for j in h4l if j<k-2]
    if hs and H4[k][4]>max(hs[-3:]): last='long'
    elif ls and H4[k][4]<min(ls[-3:]): last='short'
    for ii in range(H4[k][0], H4[k+1][0] if k+1<len(H4) else N): bias[ii]=last

# --- H1 свінги як ліквідність-цілі
H1=[];cur=None;ck=None;ci=None
for i,t in enumerate(T):
    k=t[:13]; o,h,l,c=B[i]
    if k!=ck:
        if cur: H1.append((ci,cur[0],cur[1],cur[2],cur[3]))
        cur=[o,h,l,c];ck=k;ci=i
    else:
        cur[1]=max(cur[1],h);cur[2]=min(cur[2],l);cur[3]=c
if cur: H1.append((ci,cur[0],cur[1],cur[2],cur[3]))
h1h=[(H1[j][0],H1[j][2]) for j in range(2,len(H1)-2) if H1[j][2]>max(H1[x][2] for x in range(j-2,j+3) if x!=j)]
h1l=[(H1[j][0],H1[j][3]) for j in range(2,len(H1)-2) if H1[j][3]<min(H1[x][3] for x in range(j-2,j+3) if x!=j)]

def target(i,ref,d,day):
    if d=='long':
        c=[v for (mi,v) in h1h if mi<i and v>ref]
        if day in pdh and pdh[day]>ref: c.append(pdh[day])
        if day in asia and asia[day][0]>ref: c.append(asia[day][0])
        return min(c) if c else None
    c=[v for (mi,v) in h1l if mi<i and v<ref]
    if day in pdl and pdl[day]<ref: c.append(pdl[day])
    if day in asia and asia[day][1]<ref: c.append(asia[day][1])
    return max(c) if c else None

trades=[]; stat=collections.Counter()
for d,idxs in days.items():
    wd=dt.date.fromisoformat(d).weekday()
    if wd>=5 or d not in asia: continue
    ah,al=asia[d]; taken=0
    for kzname,h0,h1_ in KZ:
        if taken>=MAX_DAY: break
        kz=[j for j in idxs if h0<=int(T[j][11:13])<h1_]
        if not kz: continue
        bi=bias[kz[0]]
        if bi not in ('long','short'): continue
        # R3 крок 1: Judas sweep протилежної сторони
        swept=None
        for j in kz:
            if bi=='long' and B[j][2]<al: swept=j; break
            if bi=='short' and B[j][1]>ah: swept=j; break
        if swept is None: stat['NO_SWEEP']+=1; continue
        ext = min(B[j][2] for j in kz[:kz.index(swept)+1]) if bi=='long' else max(B[j][1] for j in kz[:kz.index(swept)+1])
        # R3 крок 2: 15m ChoCH у бік bias після свіпу (закриття за екстремумом, сформованим після свіпу)
        after=[j for j in idxs if j>swept and int(T[j][11:13])<FLAT_H]
        choch=None; piv=None
        for n_,j in enumerate(after):
            if n_<3: continue
            seg=after[:n_]
            if bi=='long':
                lv=max(B[x][1] for x in seg)
                if B[j][3]>lv: choch=j; break
                ext=min(ext,B[j][2])
            else:
                lv=min(B[x][2] for x in seg)
                if B[j][3]<lv: choch=j; break
                ext=max(ext,B[j][1])
        if choch is None: stat['NO_CHOCH']+=1; continue
        # R3 крок 3: FVG, що створив ChoCH
        fvg=None
        for k in range(max(choch-4,2), choch+1):
            if bi=='long':
                lo,hi=B[k-2][1],B[k][2]
                if hi-lo>=3*PIP: fvg=(lo,hi)
            else:
                hi,lo=B[k-2][2],B[k][1]
                if hi-lo>=3*PIP: fvg=(lo,hi)
        if fvg is None: stat['NO_FVG']+=1; continue
        entry = fvg[1] if bi=='long' else fvg[0]
        sl = ext-BUF*PIP if bi=='long' else ext+BUF*PIP
        sl_d=abs(entry-sl)/PIP
        if sl_d<3 or sl_d>60: stat['SL_BAD']+=1; continue
        # орієнтир для цілі — екстремум імпульсу ChoCH, НЕ ціна входу
        imp = max(B[x][1] for x in range(swept,choch+1)) if bi=='long' else min(B[x][2] for x in range(swept,choch+1))
        tp=target(choch, imp, bi, d)
        if tp is None: stat['NO_TP']+=1; continue
        tp_d=abs(tp-entry)/PIP
        rr=(tp_d-COST)/(sl_d+COST)
        if rr<MIN_RR: stat['RR_LOW']+=1; continue
        fill=None
        for k in range(choch+1, min(choch+13,N)):
            if int(T[k][11:13])>=FLAT_H: break
            if (bi=='long' and B[k][2]<=entry) or (bi=='short' and B[k][1]>=entry): fill=k;break
        if fill is None: stat['NO_FILL']+=1; continue
        R=None;reason=None
        for k in range(fill+1,N):
            hh=int(T[k][11:13])+int(T[k][14:16])/60
            if hh>=FLAT_H or T[k][:10]!=d:
                c=B[k-1][3]; pnl=(c-entry)/PIP if bi=='long' else (entry-c)/PIP
                R=(pnl-COST)/(sl_d+COST); reason='FLAT'; break
            o,h,l,c=B[k]
            if (l<=sl) if bi=='long' else (h>=sl): R=(-sl_d-COST)/(sl_d+COST); reason='SL'; break
            if (h>=tp) if bi=='long' else (l<=tp): R=(tp_d-COST)/(sl_d+COST); reason='TP'; break
        if R is None: continue
        taken+=1; stat[reason]+=1
        trades.append(dict(t=T[fill],kz=kzname,dir=bi,R=R,reason=reason,sl=sl_d,tp=tp_d,rr=rr,entry=entry,fill=fill))

def win(t):
    d=t[:10]; return 'CTRL24' if d<'2025-01-01' else ('CTRL25' if d<'2026-01-01' else 'DEV26')
def rep(nm,tr):
    if not tr: print(f"  {nm:9} —"); return
    Rs=[x['R'] for x in tr]; w=[x for x in tr if x['R']>0]
    gp=sum(x['R'] for x in w); gl=-sum(x['R'] for x in tr if x['R']<=0)
    print(f"  {nm:9} N={len(tr):3d}  WR {100*len(w)/len(tr):5.1f}%  E {st.mean(Rs):+.3f}R  PF {gp/gl if gl>0 else 99:5.2f}  Σ {sum(Rs):+.1f}R")
print("\n=== ТС-2 Session Manipulation ===")
rep('ВСЬОГО',trades)
for w_ in ('CTRL24','CTRL25','DEV26'): rep(w_,[x for x in trades if win(x['t'])==w_])
print()
for k in ('LON','NY','SB'): rep(k,[x for x in trades if x['kz']==k])
rep('LONG',[x for x in trades if x['dir']=='long']); rep('SHORT',[x for x in trades if x['dir']=='short'])
print(f"\n  виходи: {dict(collections.Counter(x['reason'] for x in trades))}")
print(f"  відсіяно: {dict(stat)}")
if trades: print(f"  медіанний SL {st.median([x['sl'] for x in trades]):.1f}п · TP {st.median([x['tp'] for x in trades]):.1f}п · RR {st.median([x['rr'] for x in trades]):.2f}")
json.dump(trades,open('ts2_trades.json','w'))
