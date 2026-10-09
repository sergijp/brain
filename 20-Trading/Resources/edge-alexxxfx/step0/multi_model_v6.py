#!/usr/bin/env python3
"""
v6 — шість моделей входу з Trading CT на M5, EURUSD.
Заявлено ДО перегляду результатів. Дві конфігурації: BIAS=on / BIAS=off.
Моделі: №3 STB/BTS · №5 OB Entry · №6 I-FVG · №14 Three Tap · №4 SMR · №9 Session Raid
Спільні правила: SL за структурний екстремум (без буфера), TP — найближчий великий пул,
RR>=1.0, вхід до 17:00 UTC, flat 19:00, МАКС 2 УГОДИ НА ДЕНЬ, витрати 2.0п симетрично.
"""
import csv,sys,datetime as dt
from collections import defaultdict,Counter
from statistics import median
PIP=0.0001; COST=2.0*PIP; MIN_PEN=0.5*PIP
FLAT_H=19; LAST_H=17; MAX_TRADES=2; MIN_RR=1.0
BIAS_ON = (len(sys.argv)>1 and sys.argv[1]=="bias")
INV_THR = 2.0*PIP

PATH="/Users/serhiin/AI/research/strategies/data_dukascopy/duka_eurusd_m5cache_mid_M5.csv"
bars=[]
for r in csv.DictReader(open(PATH)):
    bars.append((dt.datetime.strptime(r["time_utc"],"%Y-%m-%dT%H:%M:%SZ"),
                 float(r["open"]),float(r["high"]),float(r["low"]),float(r["close"])))
bars.sort(key=lambda x:x[0])
days=defaultdict(list)
for i,x in enumerate(bars): days[x[0].date()].append(i)
dk=sorted(days)
ATR14=[0.0]*len(bars)
_tr=[]
for i in range(1,len(bars)):
    tr=max(bars[i][2]-bars[i][3], abs(bars[i][2]-bars[i-1][4]), abs(bars[i][3]-bars[i-1][4]))
    _tr.append(tr)
    if len(_tr)>14: _tr.pop(0)
    ATR14[i]=sum(_tr)/len(_tr)
dhi={d:max(bars[i][2] for i in days[d]) for d in dk}
dlo={d:min(bars[i][3] for i in days[d]) for d in dk}
dcl={d:bars[days[d][-1]][4] for d in dk}
wks=defaultdict(list)
for d in dk: wks[d.isocalendar()[:2]].append(d)
wk=sorted(wks); whi={w:max(dhi[x] for x in wks[w]) for w in wk}; wlo={w:min(dlo[x] for x in wks[w]) for w in wk}
pw={wk[k]:wk[k-1] for k in range(1,len(wk))}

def daily_bias(di):
    if di<2: return 0
    y,yy=dk[di-1],dk[di-2]; ph,pl=dhi[yy],dlo[yy]
    th=dhi[y]>ph+MIN_PEN; tl=dlo[y]<pl-MIN_PEN
    if tl and not th: base=+1 if dcl[y]>pl else -1
    elif th and not tl: base=-1 if dcl[y]<ph else +1
    elif th and tl: base=+1 if dcl[y]>(dhi[y]+dlo[y])/2 else -1
    else:
        if di<4: return 0
        a,b,c=dk[di-3],dk[di-2],dk[di-1]
        if dhi[c]>dhi[b]>dhi[a] and dlo[c]>dlo[b]: base=+1
        elif dlo[c]<dlo[b]<dlo[a] and dhi[c]<dhi[b]: base=-1
        else: return 0
    pB=dhi[y] if base==1 else dlo[y]
    d=dk[di]; a=[i for i in days[d] if bars[i][0].hour<6]
    if a:
        ah=max(bars[i][2] for i in a); al=min(bars[i][3] for i in a)
        if (base==1 and ah>=pB+INV_THR) or (base==-1 and al<=pB-INV_THR): return -base
    return base

trades=[]
for di in range(2,len(dk)):
    d=dk[di]; y=dk[di-1]; idxs=days[d]
    bias=daily_bias(di)
    if BIAS_ON and bias==0: continue
    w=pw.get(d.isocalendar()[:2])
    POOL_HI=[("PDH",dhi[y])]+([("PWH",whi[w])] if w else [])
    POOL_LO=[("PDL",dlo[y])]+([("PWL",wlo[w])] if w else [])
    a=[i for i in idxs if bars[i][0].hour<6]
    if not a: continue
    AH=max(bars[i][2] for i in a); AL=min(bars[i][3] for i in a)
    POOL_HI.append(("AsiaH",AH)); POOL_LO.append(("AsiaL",AL))
    ALL=[(n,p,1) for n,p in POOL_HI]+[(n,p,-1) for n,p in POOL_LO]

    cands=[]                      # (bar_idx, dirn, entry, sl, model)
    work=[i for i in idxs if 6<=bars[i][0].hour<LAST_H]
    taps=defaultdict(list)

    for pos,i in enumerate(work):
        t,o,h,l,c=bars[i]
        # --- №3 STB/BTS + №9 Session Raid: свіп пулу + повернення ---
        for n,p,side in ALL:
            if side==1 and h>=p+MIN_PEN and c<p:
                cands.append((i,-1,None,h,"STB/BTS" if not (7<=t.hour<8) else "SessionRaid"))
            elif side==-1 and l<=p-MIN_PEN and c>p:
                cands.append((i,+1,None,l,"STB/BTS" if not (7<=t.hour<8) else "SessionRaid"))
            # --- №14 Three Tap: облік торкань ---
            if abs(h-p)<=1.0*PIP: taps[(n,round(p,5),1)].append(i)
            if abs(l-p)<=1.0*PIP: taps[(n,round(p,5),-1)].append(i)
        # --- №5 OB Entry: імпульсне поглинання ---
        if pos>=3:
            prev=bars[work[pos-1]]
            body=abs(c-o); pbody=abs(prev[4]-prev[1])
            if body>=2.0*PIP and body>1.5*pbody:
                if c<o and c<prev[3]: cands.append((i,-1,max(o,prev[2]),max(h,prev[2]),"OB"))
                elif c>o and c>prev[2]: cands.append((i,+1,min(o,prev[3]),min(l,prev[3]),"OB"))
        # --- №6 I-FVG: FVG інвалідований тілом ---
        if pos>=8:
            for k in range(max(0,pos-20),pos-3):
                A,B3=bars[work[k]],bars[work[k+2]]
                if A[3]-B3[2]>=1.5*PIP:          # ведмежий FVG
                    if c>A[3]+MIN_PEN: cands.append((i,+1,(A[3]+B3[2])/2,B3[2],"I-FVG"))
                elif B3[3]-A[2]>=1.5*PIP:        # бичачий FVG
                    if c<A[2]-MIN_PEN: cands.append((i,-1,(A[2]+B3[3])/2,B3[3],"I-FVG"))
        # --- №4 SMR: FVG у русі після Shift ---
        if pos>=14:
            wnd=[bars[j] for j in work[pos-12:pos]]
            bhi=max(max(z[1],z[4]) for z in wnd); blo=min(min(z[1],z[4]) for z in wnd)
            sh = -1 if c<blo-MIN_PEN else (+1 if c>bhi+MIN_PEN else 0)
            if sh:
                for k in range(max(0,pos-6),pos-1):
                    A,B3=bars[work[k]],bars[work[k+2]]
                    if sh==-1 and A[3]-B3[2]>=1.0*PIP:
                        cands.append((i,-1,(A[3]+B3[2])/2,max(z[2] for z in wnd[-6:]),"SMR"))
                    elif sh==+1 and B3[3]-A[2]>=1.0*PIP:
                        cands.append((i,+1,(A[2]+B3[3])/2,min(z[3] for z in wnd[-6:]),"SMR"))
    # --- №14 Three Tap: третє торкання ---
    for (n,p,side),lst in taps.items():
        if len(lst)>=3:
            i=lst[2]
            cands.append((i,-side,p-side*1.0*PIP,p+side*2.0*PIP,"ThreeTap"))

    # --- виконання ---
    cands.sort(key=lambda z:z[0])
    used_model=set(); done=0; last_exit=-1
    for i,dirn,entry,sl_anchor,model in cands:
        if done>=MAX_TRADES: break
        if model in used_model: continue
        if i<=last_exit: continue
        if BIAS_ON and dirn!=bias: continue
        t=bars[i][0]
        if t.hour>=LAST_H: continue
        # вхід: заданий або 0.5 FVG у нозі, або close
        e=entry
        if e is None:
            e=bars[i][4]
            for k in range(max(idxs[0],i-6),i-1):
                A,B3=bars[k],bars[k+2]
                if dirn==-1 and A[3]>B3[2]: e=(A[3]+B3[2])/2
                elif dirn==1 and A[2]<B3[3]: e=(A[2]+B3[3])/2
            e=max(e,bars[i][4]) if dirn==-1 else min(e,bars[i][4])
        buf=1.5*ATR14[i]
        sl=sl_anchor + (buf if dirn==-1 else -buf)
        risk=abs(e-sl)
        if not (2*PIP<risk<40*PIP): continue
        if (dirn==-1 and sl<=e) or (dirn==1 and sl>=e): continue
        tp_c=[p for n,p,side in ALL if (p<e-2*PIP if dirn==-1 else p>e+2*PIP)]
        if not tp_c: continue
        tp=max(tp_c) if dirn==-1 else min(tp_c)
        rr=(abs(tp-e)-COST)/(risk+COST)
        if rr<MIN_RR: continue
        fill=None
        for k in range(i+1,min(i+13,idxs[-1]+1)):
            if bars[k][0].hour>=FLAT_H: break
            if dirn==-1 and bars[k][2]>=e: fill=k; break
            if dirn==1 and bars[k][3]<=e: fill=k; break
            if dirn==-1 and bars[k][3]<=tp: break
            if dirn==1 and bars[k][2]>=tp: break
        if fill is None: continue
        out=None
        for k in range(fill+1,idxs[-1]+1):
            if bars[k][0].hour>=FLAT_H: out=("FLAT",bars[k][4]); break
            if (bars[k][2]>=sl if dirn==-1 else bars[k][3]<=sl): out=("SL",sl); break
            if (bars[k][3]<=tp if dirn==-1 else bars[k][2]>=tp): out=("TP",tp); break
            last_k=k
        if out is None: out=("EOD",bars[idxs[-1]][4]); k=idxs[-1]
        R=(dirn*(out[1]-e)-COST)/(risk+COST)
        trades.append(dict(date=d,t=bars[fill][0],dir=dirn,model=model,entry=e,sl=sl,tp=tp,
                           risk=risk,rr=rr,exit=out[0],R=R))
        used_model.add(model); done+=1; last_exit=k

if __name__=="__main__":
    print(f"BIAS-фільтр: {'ON' if BIAS_ON else 'OFF'}   днів {len(dk)}   трейдів {len(trades)}")
    if not trades: sys.exit()
    def rep(ts,lab):
        if len(ts)<5: print(f"  {lab:<14} n={len(ts)}"); return
        rs=[t["R"] for t in ts]
        print(f"  {lab:<14} n={len(rs):<4} E[R]={sum(rs)/len(rs):+.3f} WR={sum(1 for r in rs if r>0)/len(rs):5.1%} "
              f"medRR={median(t['rr'] for t in ts):4.2f} medSL={median(t['risk'] for t in ts)*10000:4.1f}п")
    rep(trades,"ВСІ")
    print()
    for mdl in sorted({t["model"] for t in trades}): rep([t for t in trades if t["model"]==mdl],mdl)
    print("\n  Виходи:",dict(Counter(t["exit"] for t in trades)))
    W=[("W1 вер-гру25",dt.date(2025,9,1),dt.date(2025,12,31)),
       ("W2 січ-бер26",dt.date(2026,1,1),dt.date(2026,3,31)),
       ("W3 кві-лип26",dt.date(2026,4,1),dt.date(2026,7,31))]
    print()
    for nm,x,z in W: rep([t for t in trades if x<=t["date"]<=z],nm)
