"""AB — механічний прогін. Специфікація: ab-mechanical-spec-2026-09-16.md (зафіксована до результатів)."""
import csv,statistics as st,collections,datetime as dt,random,json,sys
D='/Users/serhiin/AI/research/strategies/data/'
FILES=['eurusd_blind2024_M15.csv','eurusd_blind2025_M15.csv','eurusd_gate2025_M15.csv',
       'eurusd_janfeb_M15.csv','eurusd_mam_M15.csv','eurusd_june_M15.csv','eurusd_july_M15.csv']
PIP=0.0001; COST=2.0; SWAP=1.0; BUF=2.0; MIN_RR=1.8; MAXHOLD=30; MAXPOS=2
FILL_BARS_H4=12; CONF_BARS_H4=12; SEED=20260916; NREP=200

bars={}
for f in FILES:
    for r in csv.DictReader(open(D+f)):
        bars[r['time_utc']]=(float(r['open']),float(r['high']),float(r['low']),float(r['close']))
T=sorted(bars); IDX={t:i for i,t in enumerate(T)}
print(f"M15 барів {len(T)}  {T[0][:10]} → {T[-1][:10]}", file=sys.stderr)

def agg(key):
    out=[];cur=None;ck=None;ct=None
    for t in T:
        o,h,l,c=bars[t];k=key(t)
        if k!=ck:
            if cur: out.append((ct,cur[0],cur[1],cur[2],cur[3]))
            cur=[o,h,l,c];ck=k;ct=t
        else:
            cur[1]=max(cur[1],h);cur[2]=min(cur[2],l);cur[3]=c
    if cur: out.append((ct,cur[0],cur[1],cur[2],cur[3]))
    return out
H4=agg(lambda t:(t[:10],int(t[11:13])//4))
W1=agg(lambda t:dt.date.fromisoformat(t[:10]).isocalendar()[:2])
def fr(x,n=2):
    H=[];L=[]
    for i in range(n,len(x)-n):
        if x[i][2]>max(x[j][2] for j in range(i-n,i+n+1) if j!=i): H.append(i)
        if x[i][3]<min(x[j][3] for j in range(i-n,i+n+1) if j!=i): L.append(i)
    return H,L
h4H,h4L=fr(H4); w1H,w1L=fr(W1)

# ---- сигнали
sig=[]
for d in ('long','short'):
    pts = h4L if d=='long' else h4H
    for n,i in enumerate(pts):
        if n==0: continue
        prev=pts[n-1]
        if d=='long':
            if H4[i][3]>=H4[prev][3]: continue
            opp=[j for j in h4H if prev<j<i]
            if not opp: continue
            lvl=max(H4[j][2] for j in opp)
        else:
            if H4[i][2]<=H4[prev][2]: continue
            opp=[j for j in h4L if prev<j<i]
            if not opp: continue
            lvl=min(H4[j][3] for j in opp)
        conf=None
        for k in range(i+1,min(i+1+CONF_BARS_H4,len(H4))):
            if d=='long' and H4[k][4]>lvl: conf=k;break
            if d=='short' and H4[k][4]<lvl: conf=k;break
        if conf is None: continue
        strong = H4[i][3] if d=='long' else H4[i][2]
        ext = H4[conf][2] if d=='long' else H4[conf][3]
        limit = strong + 0.5*(ext-strong)
        sig.append(dict(dir=d, conf_t=H4[conf][0], conf_i=conf, strong=strong, limit=limit))
sig.sort(key=lambda s:s['conf_t'])
print(f"сигналів {len(sig)}", file=sys.stderr)

def near_w1(ts,price,d):
    if d=='long':
        c=[W1[j][2] for j in w1H if W1[j][0]<ts and W1[j][2]>price]
        return min(c) if c else None
    c=[W1[j][3] for j in w1L if W1[j][0]<ts and W1[j][3]<price]
    return max(c) if c else None

def simulate(entry_i, d, entry, sl, tp, sl_dist):
    """повертає (R, reason, hold_days)"""
    t0=dt.datetime.fromisoformat(T[entry_i].replace('Z','+00:00'))
    prev_t=T[entry_i]
    for k in range(entry_i+1,len(T)):
        t=T[k]; o,h,l,c=bars[t]
        tt=dt.datetime.fromisoformat(t.replace('Z','+00:00'))
        hold=(tt-t0).total_seconds()/86400
        # 1) геп через SL на відкритті
        if (d=='long' and o<=sl) or (d=='short' and o>=sl):
            pnl=(o-entry)/PIP if d=='long' else (entry-o)/PIP
            return (pnl-COST-SWAP*hold)/(sl_dist+COST),'GAP_SL',hold
        hit_sl = (l<=sl) if d=='long' else (h>=sl)
        hit_tp = (h>=tp) if d=='long' else (l<=tp)
        if hit_sl:                      # 2) песимістично: SL має пріоритет
            pnl=-sl_dist
            return (pnl-COST-SWAP*hold)/(sl_dist+COST),'SL',hold
        if hit_tp:
            pnl=abs(tp-entry)/PIP
            return (pnl-COST-SWAP*hold)/(sl_dist+COST),'TP',hold
        if hold>=MAXHOLD:
            pnl=(c-entry)/PIP if d=='long' else (entry-c)/PIP
            return (pnl-COST-SWAP*hold)/(sl_dist+COST),'TIME_STOP',hold
    return None,'EOD_DATA',None

trades=[]; stat=collections.Counter()
open_until=[]
for s in sig:
    ci=IDX.get(s['conf_t'])
    if ci is None: continue
    # вікно наповнення ліміту: FILL_BARS_H4 H4-барів = 16*FILL_BARS_H4 M15
    fill_i=None
    for k in range(ci+1, min(ci+1+16*FILL_BARS_H4, len(T))):
        o,h,l,c=bars[T[k]]
        if (s['dir']=='long' and l<=s['limit']) or (s['dir']=='short' and h>=s['limit']):
            fill_i=k; break
    if fill_i is None: stat['NO_FILL']+=1; continue
    ts=T[fill_i]
    entry=s['limit']; strong=s['strong']
    sl = strong-BUF*PIP if s['dir']=='long' else strong+BUF*PIP
    sl_dist=abs(entry-sl)/PIP
    if sl_dist<=0: stat['BAD_SL']+=1; continue
    tp=near_w1(ts,entry,s['dir'])
    if tp is None: stat['NO_TP']+=1; continue
    tp_dist=abs(tp-entry)/PIP
    rr=(tp_dist-COST)/(sl_dist+COST)
    if rr<MIN_RR: stat['RR_LOW']+=1; continue
    open_until=[x for x in open_until if x>ts]
    if len(open_until)>=MAXPOS: stat['SLOTS']+=1; continue
    R,reason,hold=simulate(fill_i,s['dir'],entry,sl,tp,sl_dist)
    if R is None: stat['EOD_DATA']+=1; continue
    end=(dt.datetime.fromisoformat(ts.replace('Z','+00:00'))+dt.timedelta(days=hold)).isoformat().replace('+00:00','Z')
    open_until.append(end)
    stat[reason]+=1
    trades.append(dict(t=ts,dir=s['dir'],R=R,reason=reason,hold=hold,sl=sl_dist,tp=tp_dist,rr=rr,entry=entry))

def window(t):
    d=t[:10]
    if d<'2025-01-01': return 'CTRL24'
    if d<'2026-01-01': return 'CTRL25'
    return 'DEV26'
print(json.dumps(dict(stat=dict(stat),n=len(trades)),ensure_ascii=False), file=sys.stderr)

def rep(name,tr):
    if not tr: print(f"{name}: немає трейдів"); return
    Rs=[x['R'] for x in tr]; w=[x for x in tr if x['R']>0]
    gp=sum(x['R'] for x in w); gl=-sum(x['R'] for x in tr if x['R']<=0)
    print(f"  {name:8} N={len(tr):3d}  WR {100*len(w)/len(tr):5.1f}%  E {st.mean(Rs):+.3f}R  "
          f"медіана {st.median(Rs):+.3f}  PF {gp/gl if gl>0 else float('inf'):.2f}  Σ {sum(Rs):+.1f}R")
print("\n=== AB механічний ===")
rep('ВСЬОГО',trades)
for wn in ('CTRL24','CTRL25','DEV26'):
    rep(wn,[x for x in trades if window(x['t'])==wn])
print("\n  виходи:", dict(collections.Counter(x['reason'] for x in trades)))
print("  відсіяно:", dict(stat))
if trades:
    print(f"  медіанний SL {st.median([x['sl'] for x in trades]):.1f}п · TP {st.median([x['tp'] for x in trades]):.1f}п · "
          f"RR план {st.median([x['rr'] for x in trades]):.2f} · утримання {st.median([x['hold'] for x in trades]):.1f} дн")


# ---- нульова модель: ті самі входи і геометрія, напрямок монетою
import random
def sim_dir(entry_i,d,entry,sl_dist,tp_dist):
    sl = entry - sl_dist*PIP if d=='long' else entry + sl_dist*PIP
    tp = entry + tp_dist*PIP if d=='long' else entry - tp_dist*PIP
    return simulate(entry_i,d,entry,sl,tp,sl_dist)

def null_means(subset, nrep=NREP):
    out=[]
    for k in range(nrep):
        r=random.Random(SEED+k); Rs=[]
        for x in subset:
            R,_,_=sim_dir(IDX[x['t']], r.choice(('long','short')), x['entry'], x['sl'], x['tp'])
            if R is not None: Rs.append(R)
        if Rs: out.append(st.mean(Rs))
    return out

print("\n=== Надлишок над нульовою моделлю ===")
print(f"  (той самий вхід, той самий SL/TP, напрямок монетою; {NREP} реплікацій, seed {SEED})\n")
def q(v,p):
    z=sorted(v); return z[int(p*(len(z)-1))]
for name,subset in (('ВСЬОГО',trades),
                    ('CTRL24',[x for x in trades if window(x['t'])=='CTRL24']),
                    ('CTRL25',[x for x in trades if window(x['t'])=='CTRL25']),
                    ('DEV26', [x for x in trades if window(x['t'])=='DEV26'])):
    if not subset: continue
    e_ab=st.mean([x['R'] for x in subset])
    nm=null_means(subset)
    e0=st.mean(nm); lo,hi=q(nm,.025),q(nm,.975)
    exc=e_ab-e0
    # CI надлишку = e_ab - [hi, lo] нуля
    print(f"  {name:8} E_AB {e_ab:+.3f}R | E_null {e0:+.3f}R [{lo:+.3f}; {hi:+.3f}] | "
          f"надлишок {exc:+.3f}R  CI [{e_ab-hi:+.3f}; {e_ab-lo:+.3f}]  "
          f"{'✅' if e_ab-hi>0 else '❌'}")
