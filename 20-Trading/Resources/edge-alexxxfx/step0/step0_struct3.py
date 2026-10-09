"""Крок 0.1e — три рамки точки B + розподіли дистанцій."""
import csv,json,statistics as st,collections,datetime as dt
D='/Users/serhiin/AI/research/strategies/data/'
FILES=['eurusd_janfeb_H1.csv','eurusd_mam_H1.csv','eurusd_june_H1.csv','eurusd_july_H1.csv','eurusd_recent_H1.csv']
PIP=0.0001; COST=2.0; FLAT=19; K=1.5
bars={}
for f in FILES:
    for r in csv.DictReader(open(D+f)):
        bars[r['time_utc']]=(float(r['open']),float(r['high']),float(r['low']),float(r['close']))
T=sorted(bars); B=[bars[t] for t in T]
def agg(step):
    out=[];cur=None;ct=None
    for t in T:
        hr=int(t[11:13]); o,h,l,c=bars[t]
        new = (hr%step==0) if step<24 else (ct is None or t[:10]!=ct[:10])
        if new or cur is None:
            if cur: out.append((ct,cur[0],cur[1],cur[2],cur[3]))
            cur=[o,h,l,c];ct=t
        else:
            cur[1]=max(cur[1],h);cur[2]=min(cur[2],l);cur[3]=c
    if cur: out.append((ct,cur[0],cur[1],cur[2],cur[3]))
    return out
def fract(x):
    H=[];L=[]
    for i in range(2,len(x)-2):
        if x[i][2]>max(x[i-1][2],x[i-2][2],x[i+1][2],x[i+2][2]): H.append(i)
        if x[i][3]<min(x[i-1][3],x[i-2][3],x[i+1][3],x[i+2][3]): L.append(i)
    return H,L
H4=agg(4); D1=agg(24)
h4H,h4L=fract(H4); d1H,d1L=fract(D1)
print(f"H4 {len(H4)} барів, фракталів {len(h4H)}/{len(h4L)}   D1 {len(D1)} барів, фракталів {len(d1H)}/{len(d1L)}")
days=collections.OrderedDict()
for t in T:
    d=t[:10]; o,h,l,c=bars[t]
    if d not in days: days[d]=[o,h,l,c]
    else:
        days[d][1]=max(days[d][1],h);days[d][2]=min(days[d][2],l);days[d][3]=c
dl=list(days); atr={}
for i,d in enumerate(dl):
    if i<14: continue
    trs=[]
    for j in range(i-14,i):
        o,h,l,c=days[dl[j]]; pc=days[dl[j-1]][3]
        trs.append(max(h-l,abs(h-pc),abs(l-pc)))
    atr[d]=sum(trs)/14
ev=json.load(open('step0_events.json'))
def near(series,Hs,Ls,tstamp,price,direction):
    if direction=='long':
        c=[series[j][2] for j in Hs if series[j][0]<tstamp and series[j][2]>price]
        return min(c) if c else None
    c=[series[j][3] for j in Ls if series[j][0]<tstamp and series[j][3]<price]
    return max(c) if c else None
def q(v,p):
    s=sorted(v); return s[int(p*(len(s)-1))]
print(f"\nмедіанний ATR_D = {st.median(list(atr.values()))/PIP:.1f} п\n")
for MODEL,skey,ekey in (('M1','sl1','e1'),('M2','sl2','e2')):
    sls=[]; 
    print(f"{'='*78}\n{MODEL}\n{'='*78}")
    for TF,series,Hs,Ls in (('H4',H4,h4H,h4L),('D1',D1,d1H,d1L)):
        rr=[];dist=[];res=collections.Counter();ok=0;n=0
        for e in ev:
            t=e['t'];day=t[:10];hr=int(t[11:13])
            wd=dt.date.fromisoformat(day).weekday()
            if wd==6 or (wd==4 and hr>=15) or hr>=FLAT or day not in atr: continue
            entry=e[ekey]; sl=e[skey]+2.0
            tp=near(series,Hs,Ls,t,entry,e['dir'])
            if tp is None: continue
            td=abs(tp-entry)/PIP
            if td<=COST: continue
            n+=1; dist.append(td); r=(td-COST)/(sl+COST); rr.append(r)
            if MODEL and TF=='H4': sls.append(sl)
            a=atr[day]/PIP
            hi=lo=None
            for tt in T:
                if tt[:10]!=day: continue
                if tt>t: break
                _,h,l,_=bars[tt]
                hi=h if hi is None else max(hi,h); lo=l if lo is None else min(lo,l)
            consumed=(hi-lo)/PIP; tb=a*((FLAT-hr)/24)*K
            r1='PASS' if td<=0.6*tb else ('WARN' if td<=tb else 'BLOCK')
            outside=max(0.0,(tp-hi)/PIP) if e['dir']=='long' else max(0.0,(lo-tp)/PIP)
            eb=max(0.0,a-consumed)
            if outside<=0: r2='n/a'
            elif eb<=0: r2='BLOCK'
            else: r2='PASS' if outside<=0.6*eb else ('WARN' if outside<=eb else 'BLOCK')
            o={'PASS':0,'WARN':1,'BLOCK':2}
            w=max([x for x in (r1,r2) if x!='n/a'],key=lambda z:o[z])
            res[w]+=1
            if w=='PASS' and r>=1.8: ok+=1
        print(f"  B = найближчий {TF} фрактал   N={n}")
        print(f"     TP_dist  медіана {st.median(dist):5.1f} п | p75 {q(dist,.75):5.1f} | p90 {q(dist,.90):5.1f}")
        print(f"     RR_net   медіана {st.median(rr):5.2f}   | p75 {q(rr,.75):5.2f} | max {max(rr):5.2f} | ≥1.8: {100*sum(1 for x in rr if x>=1.8)/n:.1f}%")
        print(f"     гейт     PASS {res['PASS']} / WARN {res['WARN']} / BLOCK {res['BLOCK']}")
        print(f"     ✅ PASS І RR≥1.8:  {ok} з {n}  = {100*ok/n:.1f}%\n")
    print(f"  SL (буфер 2п): медіана {st.median(sls):.1f} п\n")
