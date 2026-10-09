#!/usr/bin/env python3
"""
v5 = v2 (свіп→MSS→FVG, SL за екстремум свіпу, TP з великих пулів)
   + Continuation Model (модель №7 Trading CT / M4 EDGE) — добори "в догонку".
Ліміт «одна відкрита позиція» знято; діє лише правило «3 збиткові за день → стоп».
Заявлено ДО перегляду результатів. Головна метрика — надлишок над нульовою моделлю.
"""
import csv, sys, datetime as dt
from collections import defaultdict, Counter
from statistics import median

PIP=0.0001; COST=2.0*PIP; BUF=0.0; MIN_PEN=0.5*PIP; EQ_TOL=1.0*PIP
SWING_N=2; LOOKBACK=60; MSS_WINDOW=48
FLAT_H=19; LAST_ENTRY_H=17; MAX_LOSERS=3
MIN_RR=1.0
MAJOR=("PDH","PDL","PWH","PWL","ASH","ASL","EQH","EQL")
CONT_LEG=10          # скільки барів назад дивимось для SL добору
CONT_FVG=6           # де шукаємо FVG у нозі добору
CONT_COOL=6          # пауза в барах після заповнення добору

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
weeks=defaultdict(list)
for d in dk: weeks[d.isocalendar()[:2]].append(d)
wkk=sorted(weeks)
whi={w:max(dhi[x] for x in weeks[w]) for w in wkk}
wlo={w:min(dlo[x] for x in weeks[w]) for w in wkk}
pw_of={wkk[k]:wkk[k-1] for k in range(1,len(wkk))}

trades=[]
for di in range(2,len(dk)):
    d=dk[di]; pd_=dk[di-1]; idxs=days[d]
    pw=pw_of.get(d.isocalendar()[:2])
    pools_hi=[("PDH",dhi[pd_])]+([("PWH",whi[pw])] if pw else [])
    pools_lo=[("PDL",dlo[pd_])]+([("PWL",wlo[pw])] if pw else [])
    hist=days[dk[di-2]]+days[pd_]
    sh,sl_=[],[]
    for k in range(SWING_N,len(hist)-SWING_N):
        j=hist[k]; w=[bars[hist[k+o]] for o in range(-SWING_N,SWING_N+1)]
        if all(bars[j][2]>=x[2] for x in w): sh.append(bars[j][2])
        if all(bars[j][3]<=x[3] for x in w): sl_.append(bars[j][3])
    sh,sl_=sh[-LOOKBACK:],sl_[-LOOKBACK:]
    pools_hi+=[("SWH",p) for p in sh]; pools_lo+=[("SWL",p) for p in sl_]
    for nm,src,dst in (("EQH",sh,pools_hi),("EQL",sl_,pools_lo)):
        s=sorted(src)
        for a,b2 in zip(s,s[1:]):
            if abs(a-b2)<=EQ_TOL: dst.append((nm,(a+b2)/2))
    asia=[i for i in idxs if bars[i][0].hour<6]
    if asia:
        pools_hi.append(("ASH",max(bars[i][2] for i in asia)))
        pools_lo.append(("ASL",min(bars[i][3] for i in asia)))

    taken=set(); losers=0; live=[]; of_dir=0; of_from=None; cool=-1

    def close_out(tr,px,why):
        tr["exit"]=why
        tr["R"]=(tr["dir"]*(px-tr["entry"])-COST)/(tr["risk"]+COST)
        trades.append(tr)

    for pos,i in enumerate(idxs):
        t,o,h,l,c=bars[i]
        # ---- супровід відкритих ----
        still=[]
        for tr in live:
            hit_sl=(l<=tr["sl"]) if tr["dir"]==1 else (h>=tr["sl"])
            hit_tp=(h>=tr["tp"]) if tr["dir"]==1 else (l<=tr["tp"])
            if hit_sl: close_out(tr,tr["sl"],"SL"); losers+=1
            elif hit_tp: close_out(tr,tr["tp"],"TP")
            elif t.hour>=FLAT_H:
                close_out(tr,c,"FLAT")
                if trades[-1]["R"]<0: losers+=1
            else: still.append(tr)
        live=still
        if losers>=MAX_LOSERS or t.hour>=LAST_ENTRY_H or pos<SWING_N*2: continue

        # ---- 1. ПЕРВИННИЙ вхід: свіп ключового пулу ----
        if of_dir==0:
            sweep=None
            for nm,lv in pools_hi:
                if lv in taken: continue
                if h>=lv+MIN_PEN and c<lv: sweep=(-1,nm,lv,h); break
            if not sweep:
                for nm,lv in pools_lo:
                    if lv in taken: continue
                    if l<=lv-MIN_PEN and c>lv: sweep=(1,nm,lv,l); break
            if sweep:
                dirn,pname,plevel,sw_ext=sweep; taken.add(plevel)
                ref_rng=range(max(idxs[0],i-12),i)
                ref=(min(bars[k][3] for k in ref_rng) if dirn==-1 else max(bars[k][2] for k in ref_rng)) if ref_rng else None
                mss_i=None
                if ref is not None:
                    for k in range(i+1,min(i+1+MSS_WINDOW,idxs[-1]+1)):
                        if bars[k][0].date()!=d: break
                        if dirn==-1 and bars[k][4]<ref: mss_i=k; break
                        if dirn==1 and bars[k][4]>ref: mss_i=k; break
                        if dirn==-1 and bars[k][2]>sw_ext: break
                        if dirn==1 and bars[k][3]<sw_ext: break
                if mss_i is not None:
                    entry=bars[mss_i][4]
                    for k in range(max(i,mss_i-6),mss_i-1):
                        a,b3=bars[k],bars[k+2]
                        if dirn==-1 and a[3]>b3[2]: entry=(a[3]+b3[2])/2
                        elif dirn==1 and a[2]<b3[3]: entry=(a[2]+b3[3])/2
                    entry=max(entry,bars[mss_i][4]) if dirn==-1 else min(entry,bars[mss_i][4])
                    slp=sw_ext+BUF*(1 if dirn==-1 else -1); risk=abs(entry-slp)
                    if 2*PIP<risk<40*PIP:
                        cands=[lv for nm,lv in (pools_lo if dirn==-1 else pools_hi)
                               if nm in MAJOR and lv not in taken
                               and (lv<entry-2*PIP if dirn==-1 else lv>entry+2*PIP)]
                        if cands:
                            tp=max(cands) if dirn==-1 else min(cands)
                            rr=(abs(tp-entry)-COST)/(risk+COST)
                            if rr>=MIN_RR:
                                fill=None
                                for k in range(mss_i,min(mss_i+12,idxs[-1]+1)):
                                    if bars[k][0].date()!=d or bars[k][0].hour>=FLAT_H: break
                                    if dirn==-1 and bars[k][2]>=entry: fill=k; break
                                    if dirn==1 and bars[k][3]<=entry: fill=k; break
                                    if dirn==-1 and bars[k][3]<=tp: break
                                    if dirn==1 and bars[k][2]>=tp: break
                                if fill is not None:
                                    live.append(dict(date=d,t=bars[fill][0],dir=dirn,pool=pname,kind="PRIMARY",
                                                     entry=entry,sl=slp,tp=tp,risk=risk,rr=rr,exit=None,R=0.0))
                                    of_dir=dirn; of_from=fill; cool=fill
            continue

        # ---- 2. CONTINUATION після первинної ----
        if of_dir!=0 and i>cool+CONT_COOL:
            w=[bars[k] for k in range(max(of_from,i-12),i)]
            if len(w)<5: continue
            ref=min(x[3] for x in w) if of_dir<0 else max(x[2] for x in w)
            if not ((of_dir<0 and c<ref) or (of_dir>0 and c>ref)): continue
            fvg=None
            for k in range(max(of_from,i-CONT_FVG), i-1):
                a,b3=bars[k],bars[k+2]
                if of_dir<0 and a[3]>b3[2]: fvg=(b3[2],a[3])
                elif of_dir>0 and a[2]<b3[3]: fvg=(a[2],b3[3])
            if not fvg: continue
            entry=(fvg[0]+fvg[1])/2
            leg=[bars[k] for k in range(max(of_from,i-CONT_LEG),i+1)]
            slp=max(x[2] for x in leg) if of_dir<0 else min(x[3] for x in leg)
            risk=abs(entry-slp)
            if not (2*PIP<risk<30*PIP): continue
            cands=[lv for nm,lv in (pools_lo if of_dir==-1 else pools_hi)
                   if nm in MAJOR and (lv<entry-2*PIP if of_dir==-1 else lv>entry+2*PIP)]
            if not cands: continue
            tp=max(cands) if of_dir==-1 else min(cands)
            rr=(abs(tp-entry)-COST)/(risk+COST)
            if rr<MIN_RR: continue
            fill=None
            for k in range(i,min(i+12,idxs[-1]+1)):
                if bars[k][0].date()!=d or bars[k][0].hour>=FLAT_H: break
                if of_dir<0 and bars[k][2]>=entry: fill=k; break
                if of_dir>0 and bars[k][3]<=entry: fill=k; break
            if fill is None: continue
            live.append(dict(date=d,t=bars[fill][0],dir=of_dir,pool="CONT",kind="CONT",
                             entry=entry,sl=slp,tp=tp,risk=risk,rr=rr,exit=None,R=0.0))
            cool=fill

    for tr in live:
        close_out(tr,bars[idxs[-1]][4],"EOD")

if __name__=="__main__":
    def rep(ts,label):
        if not ts: print(f"{label:<22} n=0"); return
        rs=[t["R"] for t in ts]
        print(f"{label:<22} n={len(rs):<4} E[R]={sum(rs)/len(rs):+.3f}  WR={sum(1 for r in rs if r>0)/len(rs):5.1%}  "
              f"med_RR={median(t['rr'] for t in ts):.2f}  med_SL={median(t['risk'] for t in ts)*10000:4.1f}п")
    print(f"днів {len(dk)}  трейдів {len(trades)}")
    rep(trades,"ВСІ")
    rep([t for t in trades if t["kind"]=="PRIMARY"],"первинні")
    rep([t for t in trades if t["kind"]=="CONT"],"добори")
    print("\nВиходи:",dict(Counter(t["exit"] for t in trades)))
    perday=Counter(t["date"] for t in trades)
    print(f"Днів з трейдами: {len(perday)}  ·  середньо {sum(perday.values())/len(perday):.2f} трейда/день  ·  макс {max(perday.values())}")
    W=[("W1 вер-гру25",dt.date(2025,9,1),dt.date(2025,12,31)),
       ("W2 січ-бер26",dt.date(2026,1,1),dt.date(2026,3,31)),
       ("W3 кві-лип26",dt.date(2026,4,1),dt.date(2026,7,31))]
    print()
    for nm,a,b in W:
        ts=[t for t in trades if a<=t["date"]<=b]
        if ts: rep(ts,nm)
