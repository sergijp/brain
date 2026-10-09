"""Крок 0.1c — ТС як описана: TP = найближчий структурний KL (не фіксований R).
   Питання: який RR реально дає геометрія, і чи проходить він гейт."""
import csv,json,statistics as st,collections,datetime as dt
D='/Users/serhiin/AI/research/strategies/data/'
FILES=['eurusd_janfeb_H1.csv','eurusd_mam_H1.csv','eurusd_june_H1.csv','eurusd_july_H1.csv','eurusd_recent_H1.csv']
PIP=0.0001; COST=2.0; FLAT=19; K=1.5
bars={}
for f in FILES:
    for r in csv.DictReader(open(D+f)):
        bars[r['time_utc']]=(float(r['open']),float(r['high']),float(r['low']),float(r['close']))
T=sorted(bars); B=[bars[t] for t in T]; IDX={t:i for i,t in enumerate(T)}
days=collections.OrderedDict()
for t in T:
    d=t[:10]; o,h,l,c=bars[t]
    if d not in days: days[d]=[o,h,l,c]
    else:
        days[d][1]=max(days[d][1],h); days[d][2]=min(days[d][2],l); days[d][3]=c
dl=list(days); atr={}
for i,d in enumerate(dl):
    if i<14: continue
    trs=[]
    for j in range(i-14,i):
        o,h,l,c=days[dl[j]]; pc=days[dl[j-1]][3]
        trs.append(max(h-l,abs(h-pc),abs(l-pc)))
    atr[d]=sum(trs)/14
sw_h=[];sw_l=[]
for i in range(2,len(B)-2):
    if B[i][1]>max(B[i-1][1],B[i-2][1],B[i+1][1],B[i+2][1]): sw_h.append(i)
    if B[i][2]<min(B[i-1][2],B[i-2][2],B[i+1][2],B[i+2][2]): sw_l.append(i)
ev=json.load(open('step0_events.json'))

def nearest_kl(i, price, direction):
    """найближча H1-ліквідність у бік угоди, сформована ДО входу"""
    if direction=='long':
        c=[B[j][1] for j in sw_h if j<i and B[j][1]>price]
        return min(c) if c else None
    else:
        c=[B[j][2] for j in sw_l if j<i and B[j][2]<price]
        return max(c) if c else None

def day_state(day,upto):
    hi=lo=None
    for t in T:
        if t[:10]!=day: continue
        if t>upto: break
        o,h,l,c=bars[t]
        hi=h if hi is None else max(hi,h); lo=l if lo is None else min(lo,l)
    return hi,lo

for MODEL,skey,ekey,label in (('M1','sl1','e1','вхід по закриттю BOS-бара'),
                              ('M2','sl2','e2','лімітний вхід 50% ноги (IDM)')):
    rr=[];res=collections.Counter();rr_pass=[];n_noTP=0;n=0
    for e in ev:
        t=e['t']; day=t[:10]; hr=int(t[11:13]); i=IDX[t]
        wd=dt.date.fromisoformat(day).weekday()
        if wd==6 or (wd==4 and hr>=15) or hr>=FLAT or day not in atr: continue
        entry=e[ekey]; sl=e[skey]+2.0
        tp_price=nearest_kl(i, entry, e['dir'])
        if tp_price is None: n_noTP+=1; continue
        tp_dist=abs(tp_price-entry)/PIP
        if tp_dist<=0: continue
        n+=1
        r=(tp_dist-COST)/(sl+COST); rr.append(r)
        a=atr[day]/PIP; hi,lo=day_state(day,t)
        consumed=(hi-lo)/PIP; h_left=FLAT-hr
        tb=a*(h_left/24)*K
        r1='PASS' if tp_dist<=0.6*tb else ('WARN' if tp_dist<=tb else 'BLOCK')
        outside=max(0.0,(tp_price-hi)/PIP) if e['dir']=='long' else max(0.0,(lo-tp_price)/PIP)
        eb=max(0.0,a-consumed)
        if outside<=0: r2='n/a'
        elif eb<=0: r2='BLOCK'
        else: r2='PASS' if outside<=0.6*eb else ('WARN' if outside<=eb else 'BLOCK')
        o={'PASS':0,'WARN':1,'BLOCK':2}
        worst=max([x for x in (r1,r2) if x!='n/a'], key=lambda z:o[z])
        res[worst]+=1
        if worst=='PASS': rr_pass.append(r)
    def q(v,p):
        s=sorted(v); return s[int(p*(len(s)-1))]
    print(f"\n{'='*78}\n{MODEL} — {label}  ·  TP = найближчий H1 KL\n{'='*78}")
    print(f"подій: {n}   (без валідної цілі: {n_noTP})")
    print(f"RR_net до гейта:  медіана {st.median(rr):.2f} | p25 {q(rr,.25):.2f} | p75 {q(rr,.75):.2f} | частка ≥1.8: {100*sum(1 for x in rr if x>=1.8)/len(rr):.1f}%")
    for k in ('PASS','WARN','BLOCK'): print(f"   {k:6} {res[k]:4d}  {100*res[k]/n:5.1f}%")
    if rr_pass:
        print(f"RR_net серед PASS: медіана {st.median(rr_pass):.2f} | max {max(rr_pass):.2f} | N={len(rr_pass)}")
        print(f"   частка PASS з RR ≥ 1.8: {100*sum(1 for x in rr_pass if x>=1.8)/len(rr_pass):.1f}%")
