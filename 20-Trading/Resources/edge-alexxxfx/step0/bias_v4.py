"""Daily Bias v4 за daily-bias-algorithm.md: base model + 3 умови інвалідації."""
import csv, datetime as dt
from collections import defaultdict
PIP=0.0001; MIN_PEN=0.5*PIP
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

def bias(di, explain=False):
    """Повертає (bias, point_B, лог). bias: +1 long, -1 short, 0 немає."""
    if di<2: return 0,None,"мало даних"
    y,yy=dk[di-1],dk[di-2]
    ph,pl=dhi[yy],dlo[yy]
    took_h=dhi[y]>ph+MIN_PEN; took_l=dlo[y]<pl-MIN_PEN
    base=0; model=""
    if took_l and not took_h:
        if dcl[y]>pl: base,model=+1,"Reversal (зняло PDL, закрилось вище)"
        else:         base,model=-1,"Continuation (зняло PDL, закрилось нижче)"
    elif took_h and not took_l:
        if dcl[y]<ph: base,model=-1,"Reversal (зняло PDH, закрилось нижче)"
        else:         base,model=+1,"Continuation (зняло PDH, закрилось вище)"
    elif took_h and took_l:
        base,model=(+1,"обидва боки, закрилось вгорі") if dcl[y]>(dhi[y]+dlo[y])/2 else (-1,"обидва боки, закрилось внизу")
    else:
        if di>=4:
            a,b,c=dk[di-3],dk[di-2],dk[di-1]
            if dhi[c]>dhi[b]>dhi[a] and dlo[c]>dlo[b]: base,model=+1,"структура D1 HH/HL"
            elif dlo[c]<dlo[b]<dlo[a] and dhi[c]<dhi[b]: base,model=-1,"структура D1 LL/LH"
    if base==0: return 0,None,"немає моделі"
    # Точка B
    pB = dhi[y] if base==1 else dlo[y]
    d=dk[di]; log=[f"base {base:+d} — {model}; точка B = {pB:.5f}"]
    # умова 2: Азія досягла B
    asia=[i for i in days[d] if bars[i][0].hour<6]
    if asia:
        ah=max(bars[i][2] for i in asia); al=min(bars[i][3] for i in asia)
        if (base==1 and ah>=pB) or (base==-1 and al<=pB):
            log.append(f"ІНВЕРСІЯ: Азія досягла B (AsiaH {ah:.5f} / AsiaL {al:.5f})")
            return -base,pB," | ".join(log)
    # умова 1: закріплення тілом за PDL/PDH проти base до 07:00 UTC
    morn=[i for i in days[d] if bars[i][0].hour<7]
    pdl,pdh=dlo[y],dhi[y]
    for i in morn:
        c=bars[i][4]
        if base==1 and c<pdl-MIN_PEN:
            log.append("ІНВЕРСІЯ: тіло закріпилось нижче PDL до 07:00")
            return -base,pB," | ".join(log)
        if base==-1 and c>pdh+MIN_PEN:
            log.append("ІНВЕРСІЯ: тіло закріпилось вище PDH до 07:00")
            return -base,pB," | ".join(log)
    return base,pB," | ".join(log)

if __name__=="__main__":
    for day in (dt.date(2026,1,2),dt.date(2026,1,5),dt.date(2026,1,6),dt.date(2026,1,7),dt.date(2026,1,8)):
        if day not in days: print(f"{day}: немає даних"); continue
        di=dk.index(day); b,pB,log=bias(di)
        d=day
        o=bars[days[d][0]][1]; c=dcl[d]
        actual = +1 if c>o else -1
        mark = "✅" if b==actual else ("❌" if b!=0 else "—")
        print(f"{day} bias={b:+d}  факт={actual:+d} {mark}  (O {o:.5f} → C {c:.5f}, H {dhi[d]:.5f} L {dlo[d]:.5f})")
        print(f"           {log}")
