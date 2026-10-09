"""ТС-3 Inner FVG Sniper — чесний симулятор на M15 (без lookahead).
СПЕЦИФІКАЦІЯ ЗАФІКСОВАНА ДО ПРОГОНУ. Правила з ts-3-inner-fvg-sniper.md, R1-R5.
Головний фальсифікований тест із плану доопрацювання: ОБИДВІ сторони, не shorts-only."""
import csv,statistics as st,collections,datetime as dt,sys,json,math
D='/Users/serhiin/AI/research/strategies/data/'
F=['eurusd_blind2024_M15.csv','eurusd_blind2025_M15.csv','eurusd_gate2025_M15.csv',
   'eurusd_janfeb_M15.csv','eurusd_mam_M15.csv','eurusd_june_M15.csv','eurusd_july_M15.csv']
PIP=0.0001; COST=2.0
SL_MAX=20.0; SL_BUF=2.5; FVG_MIN=5.0; MIN_RR=0.0
BOS_FRESH=2          # R1: BOS у межах 30 хв = 2 бари M15
MAXHOLD_BARS=16       # R4: max 2 години = 8 барів M15
FLAT_H=19; ASIA_END=7   # R5
MAX_TRADES_DAY=3

bars={}
for f in F:
    for r in csv.DictReader(open(D+f)):
        bars[r['time_utc']]=(float(r['open']),float(r['high']),float(r['low']),float(r['close']))
T=sorted(bars); B=[bars[t] for t in T]; N=len(T)
print(f"M15 барів {N}  {T[0][:10]} → {T[-1][:10]}", file=sys.stderr)

# ---- ATR(14) на M15 + ковзна медіана 30 днів (R5)
atr=[None]*N
for i in range(14,N):
    trs=[]
    for j in range(i-14,i):
        o,h,l,c=B[j]; pc=B[j-1][3]
        trs.append(max(h-l,abs(h-pc),abs(l-pc)))
    atr[i]=sum(trs)/14
W=30*96
med=[None]*N          # медіана перераховується раз на день (оптимізація, не зміна правила)
_last=-10**9; _cur=None
for i in range(W+14,N):
    if i-_last>=96:
        v=[x for x in atr[i-W:i] if x]
        _cur=st.median(v) if v else None; _last=i
    med[i]=_cur

# ---- свінги M15 (n=2)
sw_h=[];sw_l=[]
for i in range(2,N-2):
    if B[i][1]>max(B[j][1] for j in range(i-2,i+3) if j!=i): sw_h.append(i)
    if B[i][2]<min(B[j][2] for j in range(i-2,i+3) if j!=i): sw_l.append(i)
SH=set(sw_h); SL_=set(sw_l)

# ---- H1 bias: напрямок останнього H1 BOS
H1=[]; cur=None; ct=None
for i,t in enumerate(T):
    k=t[:13]; o,h,l,c=B[i]
    if k!=ct:
        if cur: H1.append((ci,cur[0],cur[1],cur[2],cur[3]))
        cur=[o,h,l,c]; ct=k; ci=i
    else:
        cur[1]=max(cur[1],h); cur[2]=min(cur[2],l); cur[3]=c
if cur: H1.append((ci,cur[0],cur[1],cur[2],cur[3]))
h1h=[];h1l=[]
for i in range(2,len(H1)-2):
    if H1[i][2]>max(H1[j][2] for j in range(i-2,i+3) if j!=i): h1h.append(i)
    if H1[i][3]<min(H1[j][3] for j in range(i-2,i+3) if j!=i): h1l.append(i)
bias_at={}            # індекс M15 -> bias
last='none'
ev=sorted([(H1[j][0],'h',H1[j][2]) for j in h1h]+[(H1[j][0],'l',H1[j][3]) for j in h1l])
hi_lv=None; lo_lv=None
for k in range(len(H1)):
    mi=H1[k][0]
    hs=[H1[j][2] for j in h1h if j<k-2]
    ls=[H1[j][3] for j in h1l if j<k-2]
    if hs and H1[k][4]>max(hs[-3:]): last='long'
    elif ls and H1[k][4]<min(ls[-3:]): last='short'
    for ii in range(mi, H1[k+1][0] if k+1<len(H1) else N): bias_at[ii]=last

# H1-свінги як HTF-ліквідність (специфікація R4: «наступна ліквідність, часто session H/L», «HTF target»)
H1SH=[(H1[j][0],H1[j][2]) for j in h1h]
H1SL=[(H1[j][0],H1[j][3]) for j in h1l]
# PDH/PDL
pdh={};pdl={}
_d=None;_h=None;_l=None;_prev=None
for _i,_t in enumerate(T):
    d=_t[:10]
    if d!=_d:
        if _d is not None: _prev=(_h,_l)
        if _prev: pdh[d]=_prev[0]; pdl[d]=_prev[1]
        _d=d;_h=B[_i][1];_l=B[_i][2]
    else:
        _h=max(_h,B[_i][1]); _l=min(_l,B[_i][2])

def nearest_liq(i,ref,d):
    """наступна НЕЗНЯТА HTF-ліквідність за піком імпульсу: H1-свінг або PDH/PDL"""
    day=T[i][:10]
    if d=='long':
        c=[v for (mi,v) in H1SH if mi<i and v>ref]
        if day in pdh and pdh[day]>ref: c.append(pdh[day])
        return min(c) if c else None
    c=[v for (mi,v) in H1SL if mi<i and v<ref]
    if day in pdl and pdl[day]<ref: c.append(pdl[day])
    return max(c) if c else None

trades=[]; stat=collections.Counter(); perday=collections.Counter(); busy_until=-1
for i in range(W+20, N-1):
    t=T[i]; hh=int(t[11:13]); day=t[:10]
    wd=dt.date.fromisoformat(day).weekday()
    if wd>=5: continue
    if hh<ASIA_END or hh>=FLAT_H: continue                    # R5
    if med[i] is None or atr[i] is None or atr[i]<med[i]: stat['LOW_ATR']+=1; continue   # R5
    if perday[day]>=MAX_TRADES_DAY: stat['DAY_LIMIT']+=1; continue
    if i<busy_until: continue
    bias=bias_at.get(i,'none')
    if bias=='none': continue
    # R1: свіжий 15m BOS у бік bias протягом BOS_FRESH барів
    bos=None
    for k in range(i-BOS_FRESH, i+1):
        if k<3: continue
        if bias=='long':
            prior=[B[j][1] for j in sw_h if j<k-2]
            if prior and B[k][3]>max(prior[-3:]): bos=k
        else:
            prior=[B[j][2] for j in sw_l if j<k-2]
            if prior and B[k][3]<min(prior[-3:]): bos=k
    if bos is None: continue
    # нога імпульсу: від останнього протилежного свінгу до бара BOS
    if bias=='long':
        base=[j for j in sw_l if j<bos]
        if not base: continue
        leg0=base[-1]; leg_lo=B[leg0][2]; leg_hi=max(B[j][1] for j in range(leg0,bos+1))
    else:
        base=[j for j in sw_h if j<bos]
        if not base: continue
        leg0=base[-1]; leg_hi=B[leg0][1]; leg_lo=min(B[j][2] for j in range(leg0,bos+1))
    leg=(leg_hi-leg_lo)/PIP
    if leg<=0: continue
    # R2: FVG усередині ноги (3-барова), не порушений, ≥5 п, у discount/premium
    fvg=None
    for k in range(leg0+2, bos+1):
        if bias=='long':
            gap_lo=B[k-2][1]; gap_hi=B[k][2]
            if gap_hi-gap_lo < FVG_MIN*PIP: continue
            rngk=list(range(k+1,i+1))
            if rngk and min(B[j][2] for j in rngk) <= gap_lo: continue     # порушений
            mid=(gap_lo+gap_hi)/2
            if mid > leg_lo+0.5*(leg_hi-leg_lo): continue                    # має бути discount
            fvg=(gap_lo,gap_hi)
        else:
            gap_hi=B[k-2][2]; gap_lo=B[k][1]
            if gap_hi-gap_lo < FVG_MIN*PIP: continue
            rngk=list(range(k+1,i+1))
            if rngk and max(B[j][1] for j in rngk) >= gap_hi: continue
            mid=(gap_lo+gap_hi)/2
            if mid < leg_lo+0.5*(leg_hi-leg_lo): continue                    # має бути premium
            fvg=(gap_lo,gap_hi)
    if fvg is None: stat['NO_FVG']+=1; continue
    gap_lo,gap_hi=fvg
    entry = gap_hi if bias=='long' else gap_lo                # proximal edge
    eq    = (gap_lo+gap_hi)/2
    swing = leg_lo if bias=='long' else leg_hi
    # R3: SL за 50% FVG АБО за свінг — що далі
    sl = min(eq, swing)-SL_BUF*PIP if bias=='long' else max(eq, swing)+SL_BUF*PIP
    sl_d=abs(entry-sl)/PIP
    if sl_d>SL_MAX: stat['SL_WIDE']+=1; continue              # R3
    if sl_d<3: stat['SL_TINY']+=1; continue
    # R4: min RR 1:3 до найближчої ліквідності
    liq=nearest_liq(i, leg_hi if bias=='long' else leg_lo, bias)
    if liq is None: stat['NO_LIQ']+=1; continue
    tp2_d=abs(liq-entry)/PIP
    rr=(tp2_d-COST)/(sl_d+COST)
    if rr<MIN_RR: stat['RR_LOW']+=1; continue
    # вхід лімітом, живий 4 бари
    fill=None
    for k in range(i+1, min(i+5,N)):
        if (bias=='long' and B[k][2]<=entry) or (bias=='short' and B[k][1]>=entry): fill=k;break
    if fill is None: stat['NO_FILL']+=1; continue
    tp1=None  # ТС-3.2: одна ціль = найближча HTF-ліквідність
    # симуляція
    R=None;reason=None
    for k in range(fill+1, min(fill+1+MAXHOLD_BARS, N)):
        if int(T[k][11:13])>=FLAT_H:
            c=B[k][3]; pnl=(c-entry)/PIP if bias=='long' else (entry-c)/PIP
            R=(pnl-COST)/(sl_d+COST); reason='FLAT'; break
        o,h,l,c=B[k]
        hit_sl=(l<=sl) if bias=='long' else (h>=sl)
        hit_tp=(h>=liq) if bias=='long' else (l<=liq)
        if hit_sl: R=(-sl_d-COST)/(sl_d+COST); reason='SL'; break     # песимістично
        if hit_tp: R=(tp2_d-COST)/(sl_d+COST); reason='TP'; break
    if R is None:
        c=B[min(fill+MAXHOLD_BARS,N-1)][3]
        pnl=(c-entry)/PIP if bias=='long' else (entry-c)/PIP
        R=(pnl-COST)/(sl_d+COST); reason='TIME'
    perday[day]+=1; busy_until=fill+MAXHOLD_BARS
    stat[reason]+=1
    trades.append(dict(t=T[fill],dir=bias,R=R,reason=reason,sl=sl_d,rr=rr,tp2=tp2_d,entry=entry,fill=fill))

def win(t):
    d=t[:10]
    return 'CTRL24' if d<'2025-01-01' else ('CTRL25' if d<'2026-01-01' else 'DEV26')
def rep(nm,tr):
    if not tr: print(f"  {nm:8} —"); return
    Rs=[x['R'] for x in tr]; w=[x for x in tr if x['R']>0]
    gp=sum(x['R'] for x in w); gl=-sum(x['R'] for x in tr if x['R']<=0)
    print(f"  {nm:8} N={len(tr):3d}  WR {100*len(w)/len(tr):5.1f}%  E {st.mean(Rs):+.3f}R  PF {gp/gl if gl>0 else 99:.2f}  Σ {sum(Rs):+.1f}R")
print("\n=== ТС-3.2 low-RR / high-WR — обидві сторони ===")
rep('ВСЬОГО',trades)
for w_ in ('CTRL24','CTRL25','DEV26'): rep(w_,[x for x in trades if win(x['t'])==w_])
print()
rep('LONG',[x for x in trades if x['dir']=='long'])
rep('SHORT',[x for x in trades if x['dir']=='short'])
print(f"\n  виходи: {dict(collections.Counter(x['reason'] for x in trades))}")
print(f"  відсіяно: {dict(stat)}")
if trades:
    print(f"  медіанний SL {st.median([x['sl'] for x in trades]):.1f}п · RR план {st.median([x['rr'] for x in trades]):.2f}")
json.dump(trades,open('ts32_trades.json','w'))
