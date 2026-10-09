"""Крок 0.1b — прогін Strong H/L подій через чинний гейт досяжності TP
   (risk-rules.md, гібрид traversal + extension, 2026-09-11)."""
import csv,json,statistics as st,collections,datetime as dt
D='/Users/serhiin/AI/research/strategies/data/'
FILES=['eurusd_janfeb_H1.csv','eurusd_mam_H1.csv','eurusd_june_H1.csv','eurusd_july_H1.csv','eurusd_recent_H1.csv']
PIP=0.0001; COST=2.0; FLAT=19; K=1.5; MIN_RR=1.8
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
dl=list(days); atr={}
for i,d in enumerate(dl):
    if i<14: continue
    trs=[]
    for j in range(i-14,i):
        o,h,l,c=days[dl[j]]; pc=days[dl[j-1]][3]
        trs.append(max(h-l,abs(h-pc),abs(l-pc)))
    atr[d]=sum(trs)/14
ev=json.load(open('step0_events.json'))

def day_state(day,upto):
    hi=None;lo=None
    for t in T:
        if t[:10]!=day: continue
        if t>upto: break
        o,h,l,c=bars[t]
        hi=h if hi is None else max(hi,h); lo=l if lo is None else min(lo,l)
    return hi,lo

def gate(atr_d, h_left, consumed, tp_dist, outside):
    trav_budget = atr_d*(h_left/24)*K
    r1 = 'PASS' if tp_dist<=0.6*trav_budget else ('WARN' if tp_dist<=1.0*trav_budget else 'BLOCK')
    ext_budget = max(0.0, atr_d-consumed)
    if outside<=0: r2='n/a'
    elif ext_budget<=0: r2='BLOCK'
    else: r2='PASS' if outside<=0.6*ext_budget else ('WARN' if outside<=1.0*ext_budget else 'BLOCK')
    order={'PASS':0,'WARN':1,'BLOCK':2,'n/a':-1}
    worst=max([r for r in (r1,r2) if r!='n/a'], key=lambda x:order[x])
    return r1,r2,worst,trav_budget,ext_budget

for MODEL,skey,ekey,label in (('M1','sl1','e1','вхід по закриттю BOS-бара'),
                              ('M2','sl2','e2','лімітний вхід 50% ноги (IDM-проксі)')):
    res=collections.Counter(); skipped=collections.Counter(); rows=[]
    for e in ev:
        t=e['t']; day=t[:10]; hr=int(t[11:13])
        wd=dt.date.fromisoformat(day).weekday()
        if wd==6: skipped['неділя']+=1; continue
        if wd==4 and hr>=15: skipped['пт після 15:00 UTC']+=1; continue
        if hr>=FLAT: skipped['вхід після flat 19:00']+=1; continue
        if day not in atr: skipped['нема ATR_D']+=1; continue
        a=atr[day]/PIP
        hi,lo=day_state(day,t)
        if hi is None: continue
        consumed=(hi-lo)/PIP
        sl=e[skey]+2.0                       # буфер 2 п
        tp_dist=MIN_RR*(sl+COST)+COST        # симетрична конвенція
        entry=e[ekey]
        if e['dir']=='long':
            tp_price=entry+tp_dist*PIP; outside=max(0.0,(tp_price-hi)/PIP)
        else:
            tp_price=entry-tp_dist*PIP; outside=max(0.0,(lo-tp_price)/PIP)
        h_left=FLAT-hr
        r1,r2,worst,tb,eb=gate(a,h_left,consumed,tp_dist,outside)
        res[worst]+=1
        rows.append((t,e['dir'],sl,tp_dist,a,consumed,h_left,r1,r2,worst))
    n=sum(res.values())
    print(f"\n{'='*78}\n{MODEL} — {label}   |  RR_net {MIN_RR}, cost {COST}п, буфер 2п")
    print(f"{'='*78}")
    print(f"подій у вибірці: {n}   (відсіяно: {dict(skipped)})")
    for k in ('PASS','WARN','BLOCK'):
        print(f"   {k:6} {res[k]:4d}   {100*res[k]/n:5.1f}%")
    sls=[r[2] for r in rows]; tps=[r[3] for r in rows]
    print(f"   медіанний SL {st.median(sls):.1f} п → TP_dist {st.median(tps):.1f} п "
          f"= {100*st.median(tps)/st.median([r[4] for r in rows]):.0f}% медіанного ATR_D")
    l1=collections.Counter(r[7] for r in rows); l2=collections.Counter(r[8] for r in rows)
    print(f"   нога traversal: {dict(l1)}")
    print(f"   нога extension: {dict(l2)}")

# максимальний RR, що проходить PASS на медіанній геометрії
print(f"\n{'='*78}\nЯкий RR взагалі проходить (медіанна геометрія, вхід 08:00 UTC)\n{'='*78}")
med_atr=st.median(list(atr.values()))/PIP
for MODEL,skey in (('M1','sl1'),('M2','sl2')):
    sl=st.median([e[skey] for e in ev])+2.0
    for hr in (6,8,11,14):
        h_left=FLAT-hr
        tb=med_atr*(h_left/24)*K
        best=None
        for rr in [x/10 for x in range(10,51)]:
            tp=rr*(sl+COST)+COST
            if tp<=0.6*tb: best=rr
        print(f"  {MODEL} SL {sl:4.1f}п · вхід {hr:02d}:00 UTC · traversal-бюджет {tb:5.1f}п → max RR з PASS: {best if best else '<1.0'}")
