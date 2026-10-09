exec(open('ts2_backtest.py').read().replace('MIN_RR=3.0','MIN_RR=0.0').split("def win(t):")[0])
import random,statistics as st
SEED=20260916; NREP=300
def sim_dir(fi,d,entry,sl_d,tp_d,day):
    sl=entry-sl_d*PIP if d=='long' else entry+sl_d*PIP
    tp=entry+tp_d*PIP if d=='long' else entry-tp_d*PIP
    for k in range(fi+1,N):
        if int(T[k][11:13])>=FLAT_H or T[k][:10]!=day:
            c=B[k-1][3]; pnl=(c-entry)/PIP if d=='long' else (entry-c)/PIP
            return (pnl-COST)/(sl_d+COST)
        o,h,l,c=B[k]
        if (l<=sl) if d=='long' else (h>=sl): return (-sl_d-COST)/(sl_d+COST)
        if (h>=tp) if d=='long' else (l<=tp): return (tp_d-COST)/(sl_d+COST)
    return None
Es=[];WRs=[]
for r_ in range(NREP):
    rg=random.Random(SEED+r_); Rs=[]
    for x in trades:
        R=sim_dir(x['fill'], rg.choice(('long','short')), x['entry'], x['sl'], x['tp'], x['t'][:10])
        if R is not None: Rs.append(R)
    if Rs:
        Es.append(st.mean(Rs)); WRs.append(100*sum(1 for r in Rs if r>0)/len(Rs))
def q(v,p):
    z=sorted(v); return z[int(p*(len(z)-1))]
e=st.mean([x['R'] for x in trades]); w=100*sum(1 for x in trades if x['R']>0)/len(trades)
print(f"\nТС-2, N={len(trades)}, RR-гейт знято (медіанний план {st.median([x['rr'] for x in trades]):.2f})")
print(f"\n{'':10} {'WR':>8} {'E':>10}")
print(f"{'ТС-2':10} {w:7.1f}% {e:+9.3f}R")
print(f"{'нуль':10} {st.mean(WRs):7.1f}% {st.mean(Es):+9.3f}R   CI WR [{q(WRs,.025):.1f}; {q(WRs,.975):.1f}]  CI E [{q(Es,.025):+.3f}; {q(Es,.975):+.3f}]")
print(f"\nнадлишок WR: {w-st.mean(WRs):+.1f} пп   CI [{w-q(WRs,.975):+.1f}; {w-q(WRs,.025):+.1f}]")
print(f"надлишок E:  {e-st.mean(Es):+.3f}R  CI [{e-q(Es,.975):+.3f}; {e-q(Es,.025):+.3f}]")
print(f"\n{'❌ гірше за випадковий' if w<q(WRs,.025) else ('✅ КРАЩЕ за випадковий' if w>q(WRs,.975) else '⚪ нерозрізнимо від випадкового')}")
import collections
print(f"\nвиходи: {dict(collections.Counter(x['reason'] for x in trades))}")
for k in ('LON','NY','SB'):
    sub=[x for x in trades if x['kz']==k]
    if sub: print(f"  {k}: N={len(sub)} WR {100*sum(1 for x in sub if x['R']>0)/len(sub):.0f}% E {st.mean([x['R'] for x in sub]):+.3f}R")
