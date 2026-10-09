"""Крок 0-B: RR до структурних цілей D1/W1 + тривалість утримання (для swap і gap-ризику)."""
import csv,statistics as st,collections,datetime as dt,json
D='/Users/serhiin/AI/research/strategies/data/'
FILES=['eurusd_blind2024_H1.csv','eurusd_blind2025_H1.csv','eurusd_gate2025_H1.csv',
       'eurusd_janfeb_H1.csv','eurusd_mam_H1.csv','eurusd_june_H1.csv','eurusd_july_H1.csv','eurusd_recent_H1.csv']
PIP=0.0001; COST=2.0
bars={}
for f in FILES:
    for r in csv.DictReader(open(D+f)):
        bars[r['time_utc']]=(float(r['open']),float(r['high']),float(r['low']),float(r['close']))
T=sorted(bars)
def agg(key):
    out=[];cur=None;ck=None;ct=None
    for t in T:
        o,h,l,c=bars[t]; k=key(t)
        if k!=ck:
            if cur: out.append((ct,cur[0],cur[1],cur[2],cur[3]))
            cur=[o,h,l,c];ck=k;ct=t
        else:
            cur[1]=max(cur[1],h);cur[2]=min(cur[2],l);cur[3]=c
    if cur: out.append((ct,cur[0],cur[1],cur[2],cur[3]))
    return out
D1=agg(lambda t:t[:10]); W1=agg(lambda t:dt.date.fromisoformat(t[:10]).isocalendar()[:2])
def fr(x,n=2):
    H=[];L=[]
    for i in range(n,len(x)-n):
        if x[i][2]>max(x[j][2] for j in range(i-n,i+n+1) if j!=i): H.append(i)
        if x[i][3]<min(x[j][3] for j in range(i-n,i+n+1) if j!=i): L.append(i)
    return H,L
d1H,d1L=fr(D1); w1H,w1L=fr(W1)
# ATR тижневий
atrw=[]
for i in range(14,len(W1)):
    trs=[]
    for j in range(i-14,i):
        _,o,h,l,c=W1[j]; pc=W1[j-1][4]
        trs.append(max(h-l,abs(h-pc),abs(l-pc)))
    atrw.append(sum(trs)/14)
ATRW=st.median(atrw)/PIP
print(f"медіанний ATR_W(14) = {ATRW:.1f} п\n")
EV=json.load(open('step0b_events.json'))['H4']   # H4-якір: 104 події, ~4.3/міс
def near(series,Hs,Ls,ts,price,direction):
    if direction=='long':
        c=[series[j][2] for j in Hs if series[j][0]<ts and series[j][2]>price]
        return min(c) if c else None
    c=[series[j][3] for j in Ls if series[j][0]<ts and series[j][3]<price]
    return max(c) if c else None
def q(v,p):
    s=sorted(v); return s[int(p*(len(s)-1))]
IDX={t:i for i,t in enumerate(T)}
for MODEL,skey,ekey in (('M1','sl1','e1'),('M2','sl2','e2')):
    print(f"{'='*74}\n{MODEL}  (SL за H4 Strong H/L + буфер 2п)\n{'='*74}")
    for TFN,S,Hs,Ls in (('D1',D1,d1H,d1L),('W1',W1,w1H,w1L)):
        rr=[];dist=[];hold=[];reach=0;n=0;wgate=collections.Counter()
        for e in EV:
            entry=e[ekey]; sl=e[skey]+2.0; ts=e['t']
            tp=near(S,Hs,Ls,ts,entry,e['dir'])
            if tp is None: continue
            td=abs(tp-entry)/PIP
            if td<=COST: continue
            n+=1; dist.append(td); rr.append((td-COST)/(sl+COST))
            # скільки годин до дотику цілі (без урахування SL) — оцінка утримання
            i0=IDX.get(ts)
            if i0 is not None:
                hit=None
                for k in range(i0+1,min(i0+24*30,len(T))):
                    _,h,l,_=bars[T[k]]
                    if (e['dir']=='long' and h>=tp) or (e['dir']=='short' and l<=tp): hit=k-i0; break
                if hit: reach+=1; hold.append(hit/24)
            # свінг-аналог гейта: ціль у межах 1 тижневого ATR
            wgate['PASS' if td<=0.6*ATRW else ('WARN' if td<=ATRW else 'BLOCK')]+=1
        print(f"  B = найближчий {TFN} фрактал   N={n}")
        print(f"     TP_dist  медіана {st.median(dist):6.1f} п | p75 {q(dist,.75):6.1f}")
        print(f"     RR_net   медіана {st.median(rr):6.2f}   | p25 {q(rr,.25):5.2f} | p75 {q(rr,.75):5.2f} | max {max(rr):5.2f}")
        print(f"     частка RR ≥ 1.8: {100*sum(1 for x in rr if x>=1.8)/n:.1f}%   ≥ 1.0: {100*sum(1 for x in rr if x>=1.0)/n:.1f}%")
        print(f"     свінг-гейт (1×ATR_W={ATRW:.0f}п): PASS {wgate['PASS']} / WARN {wgate['WARN']} / BLOCK {wgate['BLOCK']}")
        if hold:
            print(f"     дійшло до цілі {reach}/{n} ({100*reach/n:.0f}%) · утримання медіана {st.median(hold):.1f} дн | p75 {q(hold,.75):.1f} | p90 {q(hold,.90):.1f}")
        print()
