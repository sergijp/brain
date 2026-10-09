"""Крок 0.1 — медіанна ширина SL за H1 Strong High/Low, EURUSD, DEV 2026-01..08
   + прогін через чинний двоногий гейт досяжності TP (traversal + extension).
   Сліпий резерв 2010-2019 НЕ використовується."""
import csv,statistics as st,collections,datetime as dt
D='/Users/serhiin/AI/research/strategies/data/'
FILES=['eurusd_janfeb_H1.csv','eurusd_mam_H1.csv','eurusd_june_H1.csv','eurusd_july_H1.csv','eurusd_recent_H1.csv']
PIP=0.0001; COST=2.0; FLAT_H=19; MIN_RR=1.8; K_TRAV=1.5

bars={}
for f in FILES:
    for r in csv.DictReader(open(D+f)):
        t=r['time_utc']
        bars[t]=(float(r['open']),float(r['high']),float(r['low']),float(r['close']))
T=sorted(bars); B=[bars[t] for t in T]
print(f"H1 барів: {len(T)}   {T[0]} → {T[-1]}")

# --- денні бари + ATR_D(14) по календарних UTC-днях
days=collections.OrderedDict()
for t in T:
    d=t[:10]; o,h,l,c=bars[t]
    if d not in days: days[d]=[o,h,l,c]
    else:
        days[d][1]=max(days[d][1],h); days[d][2]=min(days[d][2],l); days[d][3]=c
dl=list(days)
atr={}
for i,d in enumerate(dl):
    if i<14: continue
    trs=[]
    for j in range(i-14,i):
        o,h,l,c=days[dl[j]]; pc=days[dl[j-1]][3]
        trs.append(max(h-l,abs(h-pc),abs(l-pc)))
    atr[d]=sum(trs)/14
print(f"днів: {len(dl)}   медіанний ATR_D: {st.median(list(atr.values()))/PIP:.1f} п")

# --- H1 фрактали (2 бари з кожного боку)
sw_h=[];sw_l=[]
for i in range(2,len(B)-2):
    h=B[i][1]; l=B[i][2]
    if h>max(B[i-1][1],B[i-2][1],B[i+1][1],B[i+2][1]): sw_h.append(i)
    if l<min(B[i-1][2],B[i-2][2],B[i+1][2],B[i+2][2]): sw_l.append(i)
print(f"H1 swing highs: {len(sw_h)}   swing lows: {len(sw_l)}")

KCONF=12   # вікно підтвердження BOS, H1 барів
events=[]
def scan(direction):
    pts = sw_l if direction=='long' else sw_h
    for n,i in enumerate(pts):
        if n==0: continue
        prev=pts[n-1]
        # 1) свіп ліквідності попереднього фракталу
        if direction=='long':
            if B[i][2] >= B[prev][2]: continue
            opp=[j for j in sw_h if prev< j < i]
            if not opp: continue
            bos_lvl=max(B[j][1] for j in opp)
        else:
            if B[i][1] <= B[prev][1]: continue
            opp=[j for j in sw_l if prev< j < i]
            if not opp: continue
            bos_lvl=min(B[j][2] for j in opp)
        # 2) імпульсне підтвердження (BOS закриттям) протягом KCONF барів
        conf=None
        for k in range(i+1, min(i+1+KCONF, len(B))):
            if direction=='long' and B[k][3] > bos_lvl: conf=k; break
            if direction=='short' and B[k][3] < bos_lvl: conf=k; break
        if conf is None: continue
        strong = B[i][2] if direction=='long' else B[i][1]
        e1 = B[conf][3]                                    # M1: вхід по закриттю BOS-бара
        leg_ext = B[conf][1] if direction=='long' else B[conf][2]
        e2 = strong + 0.5*(leg_ext-strong)                 # M2: лімітний вхід 50% ноги (проксі IDM)
        sl1=abs(e1-strong)/PIP; sl2=abs(e2-strong)/PIP
        events.append(dict(dir=direction, t=T[conf], strong=strong,
                           e1=e1, e2=e2, sl1=sl1, sl2=sl2))
scan('long'); scan('short')
events.sort(key=lambda x:x['t'])
print(f"\nStrong H/L подій з підтвердженим BOS: {len(events)}  (long {sum(1 for e in events if e['dir']=='long')} / short {sum(1 for e in events if e['dir']=='short')})")

def q(v,p):
    s=sorted(v); return s[int(p*(len(s)-1))]
for lbl,key in (('M1  вхід по закриттю BOS-бара','sl1'),('M2  лімітний вхід 50% ноги (IDM-проксі)','sl2')):
    v=[e[key] for e in events]
    print(f"\n{lbl}  (без буфера)")
    print(f"   медіана {st.median(v):6.1f} п | середнє {st.mean(v):6.1f} | p25 {q(v,.25):5.1f} | p75 {q(v,.75):5.1f} | p90 {q(v,.90):5.1f} | max {max(v):.1f}")
    vb=[x+2 for x in v]
    print(f"   +буфер 2п: медіана {st.median(vb):6.1f} п")
import json
json.dump(events, open('step0_events.json','w'))
