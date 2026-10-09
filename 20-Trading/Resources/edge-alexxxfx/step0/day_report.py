import csv,sys,datetime as dt
from collections import defaultdict
D=sys.argv[1]
PATH="/Users/serhiin/AI/research/strategies/data_dukascopy/duka_eurusd_m5cache_mid_M5.csv"
bars=[]
with open(PATH) as f:
    for r in csv.DictReader(f):
        bars.append((dt.datetime.strptime(r["time_utc"],"%Y-%m-%dT%H:%M:%SZ"),
                     float(r["open"]),float(r["high"]),float(r["low"]),float(r["close"])))
days=defaultdict(list)
for i,b in enumerate(bars): days[b[0].date()].append(i)
dk=sorted(days); d=dt.date.fromisoformat(D); pi=dk.index(d)
pd_=dk[pi-1]
hi=lambda x:max(bars[i][2] for i in days[x]); lo=lambda x:min(bars[i][3] for i in days[x])
print(f"=== {d} (пн-нд: {d.strftime('%A')}) ===")
print(f"PDH {hi(pd_):.5f}   PDL {lo(pd_):.5f}   (за {pd_})")
wk=[x for x in dk[:pi] if x.isocalendar()[:2]==dk[pi-1].isocalendar()[:2]]
asia=[i for i in days[d] if bars[i][0].hour<6]
print(f"Asia H {max(bars[i][2] for i in asia):.5f}  Asia L {min(bars[i][3] for i in asia):.5f}")
print(f"Daily open {bars[days[d][0]][1]:.5f}   день: H {hi(d):.5f}  L {lo(d):.5f}  C {bars[days[d][-1]][4]:.5f}")
print(f"Діапазон дня: {(hi(d)-lo(d))*10000:.1f} п")
# M5 swings of prev 2 days
hist=days[dk[pi-2]]+days[pd_]
sh,sl=[],[]
for k in range(2,len(hist)-2):
    j=hist[k]; w=[bars[hist[k+o]] for o in range(-2,3)]
    if all(bars[j][2]>=x[2] for x in w): sh.append((bars[j][0],bars[j][2]))
    if all(bars[j][3]<=x[3] for x in w): sl.append((bars[j][0],bars[j][3]))
print("\nОстанні M5 swing highs:", ", ".join(f"{p:.5f}" for _,p in sh[-6:]))
print("Останні M5 swing lows: ", ", ".join(f"{p:.5f}" for _,p in sl[-6:]))
print("\nГодинний хід дня (UTC):")
for h in range(24):
    b=[i for i in days[d] if bars[i][0].hour==h]
    if b: print(f"  {h:02d}:00  O {bars[b[0]][1]:.5f}  H {max(bars[i][2] for i in b):.5f}  L {min(bars[i][3] for i in b):.5f}  C {bars[b[-1]][4]:.5f}")
