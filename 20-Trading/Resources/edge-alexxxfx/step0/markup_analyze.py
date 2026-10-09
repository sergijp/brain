#!/usr/bin/env python3
"""Аналіз розмітки: чи відбір трейдера додає перевагу над нульовою моделлю.
Запуск:  python3 markup_analyze.py ~/MyVault/20-Trading/Journal/markup-eurusd.csv"""
import csv,sys,math,random,statistics as st,collections,datetime as dt,glob,os
D=os.path.expanduser('~/AI/research/strategies/data/')
PIP=0.0001; COST=2.0; MAXDAYS=10; SEED=20260916; NREP=400

bars={}
for f in sorted(glob.glob(D+'eurusd_*_M15.csv')):
    for r in csv.DictReader(open(f)):
        bars[r['time_utc']]=(float(r['open']),float(r['high']),float(r['low']),float(r['close']))
T=sorted(bars); IDX={t:i for i,t in enumerate(T)}; B=[bars[t] for t in T]; N=len(T)

def bar_index(s):
    t=s.strip().replace(' ','T')
    if len(t)==16: t+=':00Z'
    elif not t.endswith('Z'): t+='Z'
    if t in IDX: return IDX[t]
    for i,x in enumerate(T):          # найближчий бар уперед
        if x>=t: return i
    return None

def sim(fi,d,entry,sl,tp):
    sl_d=abs(entry-sl)/PIP; tp_d=abs(tp-entry)/PIP
    if sl_d<=0: return None,None,None
    lim=min(fi+1+MAXDAYS*96,N)
    for k in range(fi+1,lim):
        o,h,l,c=B[k]
        if (l<=sl) if d=='long' else (h>=sl): return (-sl_d-COST)/(sl_d+COST),'SL',sl_d
        if (h>=tp) if d=='long' else (l<=tp): return (tp_d-COST)/(sl_d+COST),'TP',sl_d
    c=B[lim-1][3]; pnl=(c-entry)/PIP if d=='long' else (entry-c)/PIP
    return (pnl-COST)/(sl_d+COST),'TIME',sl_d

rows=[]
src=sys.argv[1] if len(sys.argv)>1 else os.path.expanduser('~/MyVault/20-Trading/Journal/markup-eurusd.csv')
for r in csv.DictReader(open(src)):
    if not r.get('datetime_utc') or 'приклад' in (r.get('notes') or ''): continue
    i=bar_index(r['datetime_utc'])
    if i is None: print(f"  ⚠️ поза даними: id={r['id']} {r['datetime_utc']}"); continue
    # вхід: limit — чекаємо дотик до 24 барів; market — по close бара рішення
    e=float(r['entry']); d=r['direction'].strip()
    fi=i
    if r.get('entry_type','limit').strip()=='limit':
        fi=None
        for k in range(i,min(i+25,N)):
            if (d=='long' and B[k][2]<=e) or (d=='short' and B[k][1]>=e): fi=k;break
        if fi is None: print(f"  ⚠️ ліміт не наповнився: id={r['id']}"); continue
    R,why,sl_d=sim(fi,d,e,float(r['sl']),float(r['tp']))
    if R is None: continue
    rows.append(dict(r, R=R, why_exit=why, sl_d=sl_d, fill=fi,
                     entryf=e, slf=float(r['sl']), tpf=float(r['tp']),
                     conv=int(r['conviction']) if r.get('conviction','').strip().isdigit() else 0))
if not rows: print("немає придатних рядків"); sys.exit()

def q(v,p):
    z=sorted(v); return z[int(p*(len(z)-1))]
def nullrun(sub):
    """та сама геометрія (ті самі відстані SL/TP), напрямок монетою.
       SL/TP розставляються ВІДНОСНО випадкового напрямку — інакше кожен short б'є в стоп одразу."""
    Es=[];WRs=[]
    for k in range(NREP):
        rg=random.Random(SEED+k); Rs=[]
        for x in sub:
            d=rg.choice(('long','short'))
            e=x['entryf']; sld=x['sl_d']*PIP; tpd=abs(x['tpf']-e)
            sl = e-sld if d=='long' else e+sld
            tp = e+tpd if d=='long' else e-tpd
            R,_,_=sim(x['fill'], d, e, sl, tp)
            if R is not None: Rs.append(R)
        if Rs: Es.append(st.mean(Rs)); WRs.append(100*sum(1 for r in Rs if r>0)/len(Rs))
    return Es,WRs
def block(name,sub):
    if not sub: print(f"  {name}: —"); return
    Rs=[x['R'] for x in sub]; w=100*sum(1 for x in sub if x['R']>0)/len(sub)
    print(f"  {name:16} N={len(sub):3d}  WR {w:5.1f}%  E {st.mean(Rs):+.3f}R  Σ {sum(Rs):+6.1f}R")

taken=[x for x in rows if x['taken'].strip()=='yes']
skipped=[x for x in rows if x['taken'].strip()=='no']
print(f"\n{'='*66}\nРОЗМІТКА — {len(rows)} рядків ({len(taken)} взято / {len(skipped)} пропущено)\n{'='*66}")
block('ВЗЯТІ',taken); block('ПРОПУЩЕНІ',skipped)

if taken:
    Es,WRs=nullrun(taken)
    w=100*sum(1 for x in taken if x['R']>0)/len(taken); e=st.mean([x['R'] for x in taken])
    n=len(taken); se=math.sqrt(0.5*0.5/n)*100
    print(f"\n--- ВЗЯТІ проти нуля ({NREP} реплікацій) ---")
    print(f"  ви:   WR {w:5.1f}%  E {e:+.3f}R")
    print(f"  нуль: WR {st.mean(WRs):5.1f}%  E {st.mean(Es):+.3f}R  CI WR [{q(WRs,.025):.1f}; {q(WRs,.975):.1f}]")
    print(f"  надлишок WR {w-st.mean(WRs):+.1f} пп  CI [{w-q(WRs,.975):+.1f}; {w-q(WRs,.025):+.1f}]")
    print(f"  надлишок E  {e-st.mean(Es):+.3f}R CI [{e-q(Es,.975):+.3f}; {e-q(Es,.025):+.3f}]")
    print(f"  MDE при N={n}: ±{2.8*se:.0f} пп")
    print(f"  → {'✅ ВІДБІР ПРАЦЮЄ' if w>q(WRs,.975) else ('❌ гірше за випадковий' if w<q(WRs,.025) else '⚪ нерозрізнимо (або замала вибірка)')}")

print(f"\n--- Conviction-градієнт (найчутливіший тест відбору) ---")
for lo,hi,nm in ((1,2,'низька 1-2'),(3,3,'середня 3'),(4,5,'висока 4-5')):
    block(nm,[x for x in rows if lo<=x['conv']<=hi])
cv=[(x['conv'],x['R']) for x in rows if x['conv']>0]
if len(cv)>=8:
    mx=st.mean([c for c,_ in cv]); my=st.mean([r for _,r in cv])
    num=sum((c-mx)*(r-my) for c,r in cv); den=math.sqrt(sum((c-mx)**2 for c,_ in cv)*sum((r-my)**2 for _,r in cv))
    if den>0:
        rho=num/den
        print(f"  кореляція conviction↔R: {rho:+.3f}  (N={len(cv)})  "
              f"{'✅ позитивна' if rho>2/math.sqrt(len(cv)) else '⚪ не відрізняється від нуля'}")

for field,label in (('why','Why-теза'),('market_state','Market State'),('model','Модель')):
    g=collections.defaultdict(list)
    for x in rows:
        v=(x.get(field) or '').strip() or 'null'
        g['є' if (field=='why' and v not in ('null','')) else v].append(x)
    if len(g)>1:
        print(f"\n--- {label} (описово, з поправкою на множинність) ---")
        for k,v in sorted(g.items(), key=lambda z:-len(z[1])): block(k,v)

print(f"\nвиходи: {dict(collections.Counter(x['why_exit'] for x in rows))}")
print(f"медіанний SL {st.median([x['sl_d'] for x in rows]):.1f} п")
