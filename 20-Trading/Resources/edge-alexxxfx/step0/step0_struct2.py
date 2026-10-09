"""Крок 0.1d — TP = найближчий H4 KL (точка B на X TF), як у специфікації AB."""
import csv,json,statistics as st,collections,datetime as dt
D='/Users/serhiin/AI/research/strategies/data/'
FILES=['eurusd_janfeb_H1.csv','eurusd_mam_H1.csv','eurusd_june_H1.csv','eurusd_july_H1.csv','eurusd_recent_H1.csv']
PIP=0.0001; COST=2.0; FLAT=19; K=1.5
bars={}
for f in FILES:
    for r in csv.DictReader(open(D+f)):
        bars[r['time_utc']]=(float(r['open']),float(r['high']),float(r['low']),float(r['close']))
T=sorted(bars); B=[bars[t] for t in T]; IDX={t:i for i,t in enumerate(T)}
# --- H4 агрегація (00,04,08,12,16,20 UTC)
h4=[]
cur=None;ct=None
for t in T:
    hr=int(t[11:13]); o,h,l,c=bars[t]
    if hr%4==0 or cur is None:
        if cur: h4.append((ct,cur[0],cur[1],cur[2],cur[3]))
        cur=[o,h,l,c]; ct=t
    else:
        cur[1]=max(cur[1],h); cur[2]=min(cur[2],l); cur[3]=c
if cur: h4.append((ct,cur[0],cur[1],cur[2],cur[3]))
# H4 фрактали
h4h=[];h4l=[]
for i in range(2,len(h4)-2):
    if h4[i][2]>max(h4[i-1][2],h4[i-2][2],h4[i+1][2],h4[i+2][2]): h4h.append(i)
    if h4[i][3]<min(h4[i-1][3],h4[i-2][3],h4[i+1][3],h4[i+2][3]): h4l.append(i)
print(f"H4 барів {len(h4)}  фракталів: highs {len(h4h)} / lows {len(h4l)}")
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
ev=json.load(open('step0_events.json'))
def nearest_h4(tstamp, price, direction):
    if direction=='long':
        c=[h4[j][2] for j in h4h if h4[j][0]<tstamp and h4[j][2]>price]
        return min(c) if c else None
    c=[h4[j][3] for j in h4l if h4[j][0]<tstamp and h4[j][3]<price]
    return max(c) if c else None
def day_state(day,upto):
    hi=lo=None
    for t in T:
        if t[:10]!=day: continue
        if t>upto: break
        o,h,l,c=bars[t]
        hi=h if hi is None else max(hi,h); lo=l if lo is None else min(lo,l)
    return hi,lo
def q(v,p):
    s=sorted(v); return s[int(p*(len(s)-1))]
for MODEL,skey,ekey,label in (('M1','sl1','e1','вхід по закриттю BOS-бара'),
                              ('M2','sl2','e2','лімітний вхід 50% ноги (IDM)')):
    rr=[];res=collections.Counter();rr_pass=[];n=0;noTP=0
    for e in ev:
        t=e['t']; day=t[:10]; hr=int(t[11:13])
        wd=dt.date.fromisoformat(day).weekday()
        if wd==6 or (wd==4 and hr>=15) or hr>=FLAT or day not in atr: continue
        entry=e[ekey]; sl=e[skey]+2.0
        tp=nearest_h4(t,entry,e['dir'])
        if tp is None: noTP+=1; continue
        tp_dist=abs(tp-entry)/PIP
        if tp_dist<=COST: noTP+=1; continue
        n+=1
        r=(tp_dist-COST)/(sl+COST); rr.append(r)
        a=atr[day]/PIP; hi,lo=day_state(day,t); consumed=(hi-lo)/PIP; h_left=FLAT-hr
        tb=a*(h_left/24)*K
        r1='PASS' if tp_dist<=0.6*tb else ('WARN' if tp_dist<=tb else 'BLOCK')
        outside=max(0.0,(tp-hi)/PIP) if e['dir']=='long' else max(0.0,(lo-tp)/PIP)
        eb=max(0.0,a-consumed)
        if outside<=0: r2='n/a'
        elif eb<=0: r2='BLOCK'
        else: r2='PASS' if outside<=0.6*eb else ('WARN' if outside<=eb else 'BLOCK')
        o={'PASS':0,'WARN':1,'BLOCK':2}
        worst=max([x for x in (r1,r2) if x!='n/a'],key=lambda z:o[z])
        res[worst]+=1
        if worst=='PASS': rr_pass.append(r)
    print(f"\n{'='*78}\n{MODEL} — {label}  ·  TP = найближчий H4 фрактал (точка B)\n{'='*78}")
    print(f"подій: {n}  (без валідної H4-цілі: {noTP})")
    print(f"RR_net до гейта: медіана {st.median(rr):.2f} | p25 {q(rr,.25):.2f} | p75 {q(rr,.75):.2f} | max {max(rr):.2f}")
    print(f"   частка RR ≥ 1.8: {100*sum(1 for x in rr if x>=1.8)/len(rr):.1f}%")
    for k in ('PASS','WARN','BLOCK'): print(f"   {k:6} {res[k]:4d}  {100*res[k]/n:5.1f}%")
    both=[ (r,w) for r,w in zip(rr,[None]*len(rr)) ]
    # перетин: RR>=1.8 І PASS
    cnt=0; cnt_w=0
    rr2=[];i2=0
    for e in ev:
        pass
    print(f"RR серед PASS: медіана {st.median(rr_pass):.2f} | max {max(rr_pass):.2f} | N={len(rr_pass)}" if rr_pass else "PASS немає")
    if rr_pass:
        print(f"   ПЕРЕТИН (PASS І RR≥1.8): {sum(1 for x in rr_pass if x>=1.8)} з {n} подій = {100*sum(1 for x in rr_pass if x>=1.8)/n:.1f}%")
