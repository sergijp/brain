#!/usr/bin/env python3
"""
v3 = v2 + ПОВНИЙ протокол читання з Trading CT (reading-protocol.md).
Заявлено ДО перегляду результатів. Два прогони: MIN_RR=3.0 (протокол) і MIN_RR=1.0 (довідково).

Додано поверх v2:
  п.5.1  напрямок угоди має збігатись із D1 BIAS
  п.5.2  свіп ключового пулу (вже було)
  п.5.3  вхід тільки London KZ 07:00-10:00 UTC або NY KZ 12:00-15:00 UTC
  п.5.3  маніпуляція відносно TDO (07:00 UTC): шорт — свіп вище TDO, лонг — нижче
  п.5.5  RR >= MIN_RR
  п.6.2  Premium/Discount: шорт тільки в Premium D1-рейнджу, лонг тільки в Discount
  п.6.4  модель, сформована ДО 07:00 UTC, пропускається
"""
import csv, sys, datetime as dt
from collections import defaultdict, Counter
from statistics import median

PIP=0.0001; COST=2.0*PIP; BUF=0.0; MIN_PEN=0.5*PIP; EQ_TOL=1.0*PIP
SWING_N=2; LOOKBACK_SWINGS=60; MSS_WINDOW=48
FLAT_H=19; MAX_LOSERS=3
DR_DAYS=5                      # дилінг-рейндж для Premium/Discount
MIN_RR=float(sys.argv[1]) if len(sys.argv)>1 else 3.0
KZ=lambda h: (7<=h<10) or (12<=h<15)
MAJOR=("PDH","PDL","PWH","PWL","ASH","ASL","EQH","EQL")

PATH="/Users/serhiin/AI/research/strategies/data_dukascopy/duka_eurusd_m5cache_mid_M5.csv"
bars=[]
with open(PATH) as f:
    for r in csv.DictReader(f):
        bars.append((dt.datetime.strptime(r["time_utc"],"%Y-%m-%dT%H:%M:%SZ"),
                     float(r["open"]),float(r["high"]),float(r["low"]),float(r["close"])))
bars.sort(key=lambda x:x[0])
days=defaultdict(list)
for i,b in enumerate(bars): days[b[0].date()].append(i)
dk=sorted(days)
dhi={d:max(bars[i][2] for i in days[d]) for d in dk}
dlo={d:min(bars[i][3] for i in days[d]) for d in dk}
dcl={d:bars[days[d][-1]][4] for d in dk}
weeks=defaultdict(list)
for d in dk: weeks[d.isocalendar()[:2]].append(d)
wk=sorted(weeks)
whi={w:max(dhi[d] for d in weeks[w]) for w in wk}
wlo={w:min(dlo[d] for d in weeks[w]) for w in wk}
prev_week={wk[k]:wk[k-1] for k in range(1,len(wk))}

def d1_bias(di):
    """п.2 протоколу: аналіз закриття денної свічки."""
    if di<2: return 0
    y,yy=dk[di-1],dk[di-2]
    ph,pl=dhi[yy],dlo[yy]
    took_h = dhi[y] > ph + MIN_PEN
    took_l = dlo[y] < pl - MIN_PEN
    if took_h and not took_l:
        return 1 if dcl[y] > ph else -1        # закріпилась вище -> продовження; повернулась -> розворот
    if took_l and not took_h:
        return -1 if dcl[y] < pl else 1
    if took_h and took_l:
        return 1 if dcl[y] > (dhi[y]+dlo[y])/2 else -1
    # нічого не зняла -> структура D1 за 3 дні
    if di>=4:
        a,b,c=dk[di-3],dk[di-2],dk[di-1]
        if dhi[c]>dhi[b]>dhi[a] and dlo[c]>dlo[b]: return 1
        if dlo[c]<dlo[b]<dlo[a] and dhi[c]<dhi[b]: return -1
    return 0

trades=[]; rej=Counter()
for di in range(max(DR_DAYS,2), len(dk)):
    d=dk[di]; pd_=dk[di-1]; idxs=days[d]
    bias=d1_bias(di)
    if bias==0: rej["no_bias"]+=1; continue
    # дилінг-рейндж для Premium/Discount
    dr_hi=max(dhi[x] for x in dk[di-DR_DAYS:di]); dr_lo=min(dlo[x] for x in dk[di-DR_DAYS:di])
    dr_mid=(dr_hi+dr_lo)/2
    pw=prev_week.get(d.isocalendar()[:2])
    pools_hi=[("PDH",dhi[pd_])]+([("PWH",whi[pw])] if pw else [])
    pools_lo=[("PDL",dlo[pd_])]+([("PWL",wlo[pw])] if pw else [])
    hist=days[dk[di-2]]+days[pd_]
    sh,sl=[],[]
    for k in range(SWING_N,len(hist)-SWING_N):
        j=hist[k]; w=[bars[hist[k+o]] for o in range(-SWING_N,SWING_N+1)]
        if all(bars[j][2]>=x[2] for x in w): sh.append(bars[j][2])
        if all(bars[j][3]<=x[3] for x in w): sl.append(bars[j][3])
    sh,sl=sh[-LOOKBACK_SWINGS:],sl[-LOOKBACK_SWINGS:]
    pools_hi+=[("SWH",p) for p in sh]; pools_lo+=[("SWL",p) for p in sl]
    for nm,src,dst in (("EQH",sh,pools_hi),("EQL",sl,pools_lo)):
        s=sorted(src)
        for a,b in zip(s,s[1:]):
            if abs(a-b)<=EQ_TOL: dst.append((nm,(a+b)/2))
    asia=[i for i in idxs if bars[i][0].hour<6]
    if asia:
        pools_hi.append(("ASH",max(bars[i][2] for i in asia)))
        pools_lo.append(("ASL",min(bars[i][3] for i in asia)))
    tdo=None
    for i in idxs:
        if bars[i][0].hour==7: tdo=bars[i][1]; break
    if tdo is None: rej["no_tdo"]+=1; continue

    taken=set(); losers=0; open_trade=None
    for pos,i in enumerate(idxs):
        t,o,h,l,c=bars[i]
        if open_trade:
            tr=open_trade
            hit_sl=(l<=tr["sl"]) if tr["dir"]==1 else (h>=tr["sl"])
            hit_tp=(h>=tr["tp"]) if tr["dir"]==1 else (l<=tr["tp"])
            px=None
            if hit_sl: px,tr["exit"]=tr["sl"],"SL"
            elif hit_tp: px,tr["exit"]=tr["tp"],"TP"
            elif t.hour>=FLAT_H: px,tr["exit"]=c,"FLAT"
            if px is not None:
                tr["R"]=(tr["dir"]*(px-tr["entry"])-COST)/(tr["risk"]+COST)
                trades.append(tr); open_trade=None
                if tr["R"]<0: losers+=1
            continue
        if losers>=MAX_LOSERS or pos<SWING_N*2: continue
        if t.hour<7: continue                                   # п.6.4 — до 07:00 UTC не працюємо
        sweep=None
        for nm,lv in pools_hi:
            if lv in taken: continue
            if h>=lv+MIN_PEN and c<lv: sweep=(-1,nm,lv,h); break
        if not sweep:
            for nm,lv in pools_lo:
                if lv in taken: continue
                if l<=lv-MIN_PEN and c>lv: sweep=(1,nm,lv,l); break
        if not sweep: continue
        dirn,pname,plevel,sw_ext=sweep
        taken.add(plevel)
        if dirn!=bias: rej["bias"]+=1; continue                 # п.5.1
        if dirn==-1 and sw_ext<dr_mid: rej["pd"]+=1; continue   # п.6.2 шорт лише в Premium
        if dirn==1 and sw_ext>dr_mid: rej["pd"]+=1; continue
        if dirn==-1 and sw_ext<tdo: rej["tdo"]+=1; continue     # п.5.3 маніпуляція відносно TDO
        if dirn==1 and sw_ext>tdo: rej["tdo"]+=1; continue
        ref_rng=range(max(idxs[0],i-12),i)
        if not ref_rng: continue
        ref=min(bars[k][3] for k in ref_rng) if dirn==-1 else max(bars[k][2] for k in ref_rng)
        mss_i=None
        for k in range(i+1,min(i+1+MSS_WINDOW,idxs[-1]+1)):
            if bars[k][0].date()!=d: break
            if dirn==-1 and bars[k][4]<ref: mss_i=k; break
            if dirn==1 and bars[k][4]>ref: mss_i=k; break
            if dirn==-1 and bars[k][2]>sw_ext: break
            if dirn==1 and bars[k][3]<sw_ext: break
        if mss_i is None: rej["no_mss"]+=1; continue
        gap=int((bars[mss_i][0]-t).total_seconds()//60)
        entry=bars[mss_i][4]
        for k in range(max(i,mss_i-6),mss_i-1):
            a,b3=bars[k],bars[k+2]
            if dirn==-1 and a[3]>b3[2]: entry=(a[3]+b3[2])/2
            elif dirn==1 and a[2]<b3[3]: entry=(a[2]+b3[3])/2
        entry=max(entry,bars[mss_i][4]) if dirn==-1 else min(entry,bars[mss_i][4])
        sl=sw_ext+BUF*(1 if dirn==-1 else -1)
        risk=abs(entry-sl)
        if risk<2*PIP or risk>40*PIP: rej["risk"]+=1; continue
        cands=[lv for nm,lv in (pools_lo if dirn==-1 else pools_hi)
               if nm in MAJOR and lv not in taken
               and (lv<entry-2*PIP if dirn==-1 else lv>entry+2*PIP)]
        if not cands: rej["no_tp"]+=1; continue
        tp=max(cands) if dirn==-1 else min(cands)
        rr=(abs(tp-entry)-COST)/(risk+COST)
        if rr<MIN_RR: rej["rr"]+=1; continue
        fill=None
        for k in range(mss_i,min(mss_i+12,idxs[-1]+1)):
            if bars[k][0].date()!=d or bars[k][0].hour>=FLAT_H: break
            if not KZ(bars[k][0].hour): continue                # п.5.3 — вхід лише в KZ
            if dirn==-1 and bars[k][2]>=entry: fill=k; break
            if dirn==1 and bars[k][3]<=entry: fill=k; break
            if dirn==-1 and bars[k][3]<=tp: break
            if dirn==1 and bars[k][2]>=tp: break
        if fill is None: rej["no_fill"]+=1; continue
        open_trade=dict(date=d,t=bars[fill][0],dir=dirn,pool=pname,entry=entry,sl=sl,tp=tp,
                        risk=risk,rr=rr,gap=gap,exit=None,R=0.0)
    if open_trade:
        open_trade["exit"]="EOD"; px=bars[idxs[-1]][4]
        open_trade["R"]=(open_trade["dir"]*(px-open_trade["entry"])-COST)/(open_trade["risk"]+COST)
        trades.append(open_trade)

if __name__=="__main__":
    print(f"MIN_RR={MIN_RR}   днів {len(dk)}   трейдів {len(trades)}")
    if trades:
        rs=[t["R"] for t in trades]
        print(f"E[R]={sum(rs)/len(rs):+.3f}  WR={sum(1 for r in rs if r>0)/len(rs):.1%}  "
              f"med_RR={median(t['rr'] for t in trades):.2f}  med_SL={median(t['risk'] for t in trades)*10000:.1f}п")
        print("Виходи:",dict(Counter(t["exit"] for t in trades)))
        W=[("W1 вер-гру25",dt.date(2025,9,1),dt.date(2025,12,31)),
           ("W2 січ-бер26",dt.date(2026,1,1),dt.date(2026,3,31)),
           ("W3 кві-лип26",dt.date(2026,4,1),dt.date(2026,7,31))]
        for nm,a,b in W:
            ts=[t for t in trades if a<=t["date"]<=b]
            if ts: print(f"  {nm}: n={len(ts):<3} E[R]={sum(x['R'] for x in ts)/len(ts):+.3f}")
    print("Відсіяно:",dict(rej))
