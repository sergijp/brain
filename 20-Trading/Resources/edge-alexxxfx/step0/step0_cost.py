# 0.2 — реальний round-trip cost EURUSD з Dukascopy BID vs MID
import csv,statistics as st,collections
D='/Users/serhiin/AI/research/strategies/data_dukascopy/'
def load(p):
    rows=[]
    for r in csv.DictReader(open(D+p)):
        rows.append((r['time_utc'],float(r['open']),float(r['high']),float(r['low']),float(r['close'])))
    return rows
mid=load('duka_eurusd_partial_mid_H1.csv'); bid=load('duka_eurusd_partial_bid_H1.csv')
assert len(mid)==len(bid)
PIP=0.0001
by_hour=collections.defaultdict(list); allsp=[]
for m,b in zip(mid,bid):
    assert m[0]==b[0]
    sp=2*(m[4]-b[4])/PIP        # mid = bid + spread/2  =>  spread = 2*(mid-bid)
    if sp<0: continue
    h=int(m[0][11:13])
    by_hour[h].append(sp); allsp.append(sp)
def q(v,p): 
    s=sorted(v); i=int(p*(len(s)-1)); return s[i]
print(f"EURUSD H1 spread, Dukascopy, {mid[0][0][:10]} → {mid[-1][0][:10]}, N={len(allsp)}")
print(f"  медіана      {st.median(allsp):.2f} pip")
print(f"  середнє      {st.mean(allsp):.2f} pip")
print(f"  p75 / p90    {q(allsp,.75):.2f} / {q(allsp,.90):.2f} pip")
print(f"  p95 / max    {q(allsp,.95):.2f} / {max(allsp):.2f} pip")
print()
print("  година UTC | медіана | p90 | N")
for h in sorted(by_hour):
    v=by_hour[h]
    mark='  ← торгові години' if 6<=h<=15 else ''
    print(f"      {h:02d}     |  {st.median(v):5.2f}  | {q(v,.90):5.2f} | {len(v):4d}{mark}")
trade_h=[s for m,b in zip(mid,bid) for s in [2*(m[4]-b[4])/PIP] if 6<=int(m[0][11:13])<=15 and s>=0]
print()
print(f"Тільки 06:00–15:00 UTC: N={len(trade_h)}  медіана {st.median(trade_h):.2f}  p90 {q(trade_h,.90):.2f}")
print()
print("ROUND-TRIP (спред платиться один раз на вхід+вихід = 1×спред):")
print(f"  медіанний round-trip cost = {st.median(trade_h):.2f} pip")
print(f"  у репозиторії зашито cost_pips = 2.0 (lib/feature_lab.py)")
