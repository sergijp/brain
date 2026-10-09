import csv,statistics as st,collections,datetime as dt,json
D='/Users/serhiin/AI/research/strategies/data/'
FILES=['eurusd_blind2024_H1.csv','eurusd_blind2025_H1.csv','eurusd_gate2025_H1.csv',
       'eurusd_janfeb_H1.csv','eurusd_mam_H1.csv','eurusd_june_H1.csv','eurusd_july_H1.csv','eurusd_recent_H1.csv']
PIP=0.0001; COST=2.0
bars={}
for f in FILES:
    for r in csv.DictReader(open(D+f)):
        bars[r['time_utc']]=(float(r['open']),float(r['high']),float(r['low']),float(r['close']))
T=sorted(bars); IDX={t:i for i,t in enumerate(T)}
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
W1=agg(lambda t:dt.date.fromisoformat(t[:10]).isocalendar()[:2])
def fr(x,n=2):
    H=[];L=[]
    for i in range(n,len(x)-n):
        if x[i][2]>max(x[j][2] for j in range(i-n,i+n+1) if j!=i): H.append(i)
        if x[i][3]<min(x[j][3] for j in range(i-n,i+n+1) if j!=i): L.append(i)
    return H,L
w1H,w1L=fr(W1)
EV=json.load(open('step0b_events.json'))['H4']
def near(ts,price,d):
    if d=='long':
        c=[W1[j][2] for j in w1H if W1[j][0]<ts and W1[j][2]>price]
        return min(c) if c else None
    c=[W1[j][3] for j in w1L if W1[j][0]<ts and W1[j][3]<price]
    return max(c) if c else None
HOR=[3,5,10,15,20,30]
print("M2 + B=W1 фрактал.  Скільки цілей досягнуто в межах горизонту (SL ігнорується):")
print("   horizon |  дійшло  | частка | серед RR≥1.8")
rows=[]
for e in EV:
    entry=e['e2']; sl=e['sl2']+2.0; ts=e['t']
    tp=near(ts,entry,e['dir'])
    if tp is None: continue
    td=abs(tp-entry)/PIP
    if td<=COST: continue
    rr=(td-COST)/(sl+COST)
    i0=IDX.get(ts); hit=None
    if i0 is not None:
        for k in range(i0+1,min(i0+24*40,len(T))):
            _,h,l,_=bars[T[k]]
            if (e['dir']=='long' and h>=tp) or (e['dir']=='short' and l<=tp): hit=(k-i0)/24; break
    rows.append((rr,hit,sl,td))
n=len(rows); hi=[r for r in rows if r[0]>=1.8]
for H in HOR:
    a=sum(1 for r in rows if r[1] is not None and r[1]<=H)
    b=sum(1 for r in hi  if r[1] is not None and r[1]<=H)
    print(f"     {H:2d} дн  |  {a:3d}/{n}  | {100*a/n:5.1f}% | {b:3d}/{len(hi)} = {100*b/len(hi):5.1f}%")
print()
sl=st.median([r[2] for r in hi]); td=st.median([r[3] for r in hi])
print(f"Підмножина RR≥1.8 (N={len(hi)}, {100*len(hi)/n:.0f}% усіх сетапів):")
print(f"   медіанний SL {sl:.1f} п · TP {td:.1f} п · RR {st.median([r[0] for r in hi]):.2f}")
print(f"   частота: {len(hi)} сетапів за 24 міс = {len(hi)/24:.1f}/міс")
print()
print("Чутливість до swap (EURUSD, негативний carry на long):")
for sw in (0.3,0.5,0.7,1.0):
    for H in (5,10,20):
        cost=sw*H
        print(f"   swap {sw}п/дн × {H:2d} дн = {cost:5.1f} п = {cost/sl:.2f}R  (RR {(td-COST-cost)/(sl+COST):.2f} замість {(td-COST)/(sl+COST):.2f})")
    print()
