"""AB на рівень НИЖЧЕ: X+1=H4, X=H1, X-1=m15 (SL-якір), X-2=m5.
   Питання: чи стає SL достатньо вузьким, щоб RR 1.8 пройшов інтрадей-гейт."""
import csv,statistics as st,collections,datetime as dt
D='/Users/serhiin/AI/research/strategies/data/'
M15=['eurusd_janfeb_M15.csv','eurusd_mam_M15.csv','eurusd_june_M15.csv','eurusd_july_M15.csv']
PIP=0.0001; COST=2.0; FLAT=19; K=1.5; MIN_RR=1.8
bars={}
for f in M15:
    for r in csv.DictReader(open(D+f)):
        bars[r['time_utc']]=(float(r['open']),float(r['high']),float(r['low']),float(r['close']))
T=sorted(bars); B=[bars[t] for t in T]
print(f"m15 барів {len(T)}  {T[0][:10]} → {T[-1][:10]}")
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
H1=agg(lambda t:t[:13]); H4=agg(lambda t:(t[:10],int(t[11:13])//4)); D1=agg(lambda t:t[:10])
def fr(x,n=2):
    H=[];L=[]
    for i in range(n,len(x)-n):
        if x[i][2]>max(x[j][2] for j in range(i-n,i+n+1) if j!=i): H.append(i)
        if x[i][3]<min(x[j][3] for j in range(i-n,i+n+1) if j!=i): L.append(i)
    return H,L
h1H,h1L=fr(H1); h4H,h4L=fr(H4)
atr=[]
for i in range(14,len(D1)):
    trs=[]
    for j in range(i-14,i):
        _,o,h,l,c=D1[j]; pc=D1[j-1][4]
        trs.append(max(h-l,abs(h-pc),abs(l-pc)))
    atr.append(sum(trs)/14)
ATRD=st.median(atr)/PIP
print(f"медіанний ATR_D {ATRD:.1f} п\n")
# Strong H/L на m15
sh=[];sl_=[]
for i in range(2,len(B)-2):
    if B[i][1]>max(B[j][1] for j in range(i-2,i+3) if j!=i): sh.append(i)
    if B[i][2]<min(B[j][2] for j in range(i-2,i+3) if j!=i): sl_.append(i)
ev=[]
for direction in ('long','short'):
    pts = sl_ if direction=='long' else sh
    for n,i in enumerate(pts):
        if n==0: continue
        prev=pts[n-1]
        if direction=='long':
            if B[i][2]>=B[prev][2]: continue
            opp=[j for j in sh if prev<j<i]
            if not opp: continue
            lvl=max(B[j][1] for j in opp)
        else:
            if B[i][1]<=B[prev][1]: continue
            opp=[j for j in sl_ if prev<j<i]
            if not opp: continue
            lvl=min(B[j][2] for j in opp)
        conf=None
        for k in range(i+1,min(i+13,len(B))):
            if direction=='long' and B[k][3]>lvl: conf=k;break
            if direction=='short' and B[k][3]<lvl: conf=k;break
        if conf is None: continue
        strong=B[i][2] if direction=='long' else B[i][1]
        e1=B[conf][3]; legext=B[conf][1] if direction=='long' else B[conf][2]
        e2=strong+0.5*(legext-strong)
        ev.append(dict(dir=direction,t=T[conf],strong=strong,e1=e1,e2=e2,
                       sl1=abs(e1-strong)/PIP, sl2=abs(e2-strong)/PIP))
print(f"m15 Strong H/L подій: {len(ev)}  ({len(ev)/7:.0f}/міс)")
def q(v,p):
    s=sorted(v); return s[int(p*(len(s)-1))]
for lbl,k in (('M1 закриття BOS-бара','sl1'),('M2 лімітний 50% ноги','sl2')):
    v=[e[k]+2 for e in ev]
    print(f"  {lbl:24} SL медіана {st.median(v):5.1f} п | p25 {q(v,.25):4.1f} | p75 {q(v,.75):5.1f}")
    print(f"  {'':24} cost {COST}п = {100*COST/st.median(v):.0f}% від SL")
print()
def near(S,Hs,Ls,ts,price,d):
    if d=='long':
        c=[S[j][2] for j in Hs if S[j][0]<ts and S[j][2]>price]
        return min(c) if c else None
    c=[S[j][3] for j in Ls if S[j][0]<ts and S[j][3]<price]
    return max(c) if c else None
for MODEL,skey,ekey in (('M1','sl1','e1'),('M2','sl2','e2')):
    print(f"{'='*72}\n{MODEL} — SL за m15 Strong H/L\n{'='*72}")
    for TFN,S,Hs,Ls in (('H1',H1,h1H,h1L),('H4',H4,h4H,h4L)):
        rr=[];res=collections.Counter();ok=0;n=0
        for e in ev:
            ts=e['t']; hr=int(ts[11:13])
            wd=dt.date.fromisoformat(ts[:10]).weekday()
            if wd==6 or (wd==4 and hr>=15) or hr>=FLAT: continue
            entry=e[ekey]; slp=e[skey]+2.0
            tp=near(S,Hs,Ls,ts,entry,e['dir'])
            if tp is None: continue
            td=abs(tp-entry)/PIP
            if td<=COST: continue
            n+=1; r=(td-COST)/(slp+COST); rr.append(r)
            day=ts[:10]; hi=lo=None
            for tt in T:
                if tt[:10]!=day: continue
                if tt>ts: break
                _,h,l,_=bars[tt]
                hi=h if hi is None else max(hi,h); lo=l if lo is None else min(lo,l)
            consumed=(hi-lo)/PIP; tb=ATRD*((FLAT-hr)/24)*K
            r1='PASS' if td<=0.6*tb else ('WARN' if td<=tb else 'BLOCK')
            outside=max(0.0,(tp-hi)/PIP) if e['dir']=='long' else max(0.0,(lo-tp)/PIP)
            eb=max(0.0,ATRD-consumed)
            if outside<=0: r2='n/a'
            elif eb<=0: r2='BLOCK'
            else: r2='PASS' if outside<=0.6*eb else ('WARN' if outside<=eb else 'BLOCK')
            o={'PASS':0,'WARN':1,'BLOCK':2}
            w=max([x for x in (r1,r2) if x!='n/a'],key=lambda z:o[z])
            res[w]+=1
            if w=='PASS' and r>=MIN_RR: ok+=1
        print(f"  B = найближчий {TFN}   N={n}  RR медіана {st.median(rr):.2f} | ≥1.8: {100*sum(1 for x in rr if x>=1.8)/n:.1f}%")
        print(f"     гейт PASS {res['PASS']} / WARN {res['WARN']} / BLOCK {res['BLOCK']}   ✅ PASS І RR≥1.8: {ok} ({100*ok/n:.1f}%)")
    print()
