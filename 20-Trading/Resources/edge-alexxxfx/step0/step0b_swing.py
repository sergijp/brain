"""Крок 0 (варіант B — SWING). X=D1, X-1=H4, X-2=H1, X+1=W1.
   Вікна: 2024-09..12, 2025-01..12, 2026-01..08. Сліпий резерв 2010-2019 НЕ чіпається."""
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
print(f"H1 барів {len(T)}   {T[0][:10]} → {T[-1][:10]}")
def agg(key):
    out=[];cur=None;ck=None
    for t in T:
        o,h,l,c=bars[t]; k=key(t)
        if k!=ck:
            if cur: out.append((ct,cur[0],cur[1],cur[2],cur[3]))
            cur=[o,h,l,c]; ck=k; ct=t
        else:
            cur[1]=max(cur[1],h); cur[2]=min(cur[2],l); cur[3]=c
    if cur: out.append((ct,cur[0],cur[1],cur[2],cur[3]))
    return out
H4=agg(lambda t:(t[:10],int(t[11:13])//4))
D1=agg(lambda t:t[:10])
W1=agg(lambda t:dt.date.fromisoformat(t[:10]).isocalendar()[:2])
print(f"H4 {len(H4)}  D1 {len(D1)}  W1 {len(W1)}")
def fract(x,n=2):
    H=[];L=[]
    for i in range(n,len(x)-n):
        if x[i][2]>max(x[i-k][2] for k in list(range(-n,0))+list(range(1,n+1))): H.append(i)
        if x[i][3]<min(x[i-k][3] for k in list(range(-n,0))+list(range(1,n+1))): L.append(i)
    return H,L
def fr(x,n=2):
    H=[];L=[]
    for i in range(n,len(x)-n):
        nb=[x[j][2] for j in range(i-n,i+n+1) if j!=i]
        nl=[x[j][3] for j in range(i-n,i+n+1) if j!=i]
        if x[i][2]>max(nb): H.append(i)
        if x[i][3]<min(nl): L.append(i)
    return H,L
h4H,h4L=fr(H4); d1H,d1L=fr(D1); w1H,w1L=fr(W1)
print(f"фракталів  H4 {len(h4H)}/{len(h4L)}   D1 {len(d1H)}/{len(d1L)}   W1 {len(w1H)}/{len(w1L)}")
# ATR_D для довідки
atrs=[]
for i in range(14,len(D1)):
    trs=[]
    for j in range(i-14,i):
        _,o,h,l,c=D1[j]; pc=D1[j-1][4]
        trs.append(max(h-l,abs(h-pc),abs(l-pc)))
    atrs.append(sum(trs)/14)
print(f"медіанний ATR_D {st.median(atrs)/PIP:.1f} п\n")

def scan(series,Hs,Ls,name,KCONF):
    ev=[]
    for direction in ('long','short'):
        pts = Ls if direction=='long' else Hs
        for n,i in enumerate(pts):
            if n==0: continue
            prev=pts[n-1]
            if direction=='long':
                if series[i][3]>=series[prev][3]: continue
                opp=[j for j in Hs if prev<j<i]
                if not opp: continue
                lvl=max(series[j][2] for j in opp)
            else:
                if series[i][2]<=series[prev][2]: continue
                opp=[j for j in Ls if prev<j<i]
                if not opp: continue
                lvl=min(series[j][3] for j in opp)
            conf=None
            for k in range(i+1,min(i+1+KCONF,len(series))):
                if direction=='long' and series[k][4]>lvl: conf=k;break
                if direction=='short' and series[k][4]<lvl: conf=k;break
            if conf is None: continue
            strong = series[i][3] if direction=='long' else series[i][2]
            e1=series[conf][4]
            legext = series[conf][2] if direction=='long' else series[conf][3]
            e2=strong+0.5*(legext-strong)
            ev.append(dict(dir=direction,t=series[conf][0],strong=strong,e1=e1,e2=e2,
                           sl1=abs(e1-strong)/PIP, sl2=abs(e2-strong)/PIP, anchor=name))
    return ev

EV={}
EV['H4'] = scan(H4,h4H,h4L,'H4',12)   # SL за H4 Strong H/L (X-1)
EV['D1'] = scan(D1,d1H,d1L,'D1',10)   # SL за D1 Strong H/L (X)
def q(v,p):
    s=sorted(v); return s[int(p*(len(s)-1))]
for a in ('H4','D1'):
    ev=EV[a]
    print(f"{'='*72}\nSL-якір: {a} Strong High/Low  —  подій {len(ev)}\n{'='*72}")
    for lbl,k in (('M1 закриття BOS-бара','sl1'),('M2 лімітний 50% ноги','sl2')):
        v=[e[k]+2 for e in ev]
        print(f"  {lbl:24} SL медіана {st.median(v):6.1f} п | p25 {q(v,.25):5.1f} | p75 {q(v,.75):6.1f} | p90 {q(v,.90):6.1f}")
    print()
json.dump(EV,open('step0b_events.json','w'))
