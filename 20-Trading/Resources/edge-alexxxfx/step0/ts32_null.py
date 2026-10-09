exec(open('ts32_backtest.py').read().split("def win(t):")[0])
import random,statistics as st
SEED=20260916; NREP=300
def sim_dir(fi,d,entry,sl_d,tp_d):
    sl = entry-sl_d*PIP if d=='long' else entry+sl_d*PIP
    tp = entry+tp_d*PIP if d=='long' else entry-tp_d*PIP
    for k in range(fi+1, min(fi+1+MAXHOLD_BARS,N)):
        if int(T[k][11:13])>=FLAT_H:
            c=B[k][3]; pnl=(c-entry)/PIP if d=='long' else (entry-c)/PIP
            return (pnl-COST)/(sl_d+COST), 0
        o,h,l,c=B[k]
        if (l<=sl) if d=='long' else (h>=sl): return (-sl_d-COST)/(sl_d+COST), 0
        if (h>=tp) if d=='long' else (l<=tp): return (tp_d-COST)/(sl_d+COST), 1
    c=B[min(fi+MAXHOLD_BARS,N-1)][3]
    pnl=(c-entry)/PIP if d=='long' else (entry-c)/PIP
    return (pnl-COST)/(sl_d+COST), 0
Es=[];WRs=[]
for r_ in range(NREP):
    rg=random.Random(SEED+r_); Rs=[];w=0
    for x in trades:
        R,win_=sim_dir(x['fill'], rg.choice(('long','short')), x['entry'], x['sl'], x['tp2'])
        Rs.append(R); w+=1 if R>0 else 0
    Es.append(st.mean(Rs)); WRs.append(100*w/len(Rs))
def q(v,p):
    z=sorted(v); return z[int(p*(len(z)-1))]
eab=st.mean([x['R'] for x in trades]); wab=100*sum(1 for x in trades if x['R']>0)/len(trades)
print(f"\nТС-3.2, N={len(trades)}, RR-гейт знято (медіанний план {st.median([x['rr'] for x in trades]):.2f})")
print(f"\n{'':10} {'WR':>8} {'E':>9}")
print(f"{'ТС-3.2':10} {wab:7.1f}% {eab:+8.3f}R")
print(f"{'нуль':10} {st.mean(WRs):7.1f}% {st.mean(Es):+8.3f}R   95% CI WR [{q(WRs,.025):.1f}; {q(WRs,.975):.1f}]  E [{q(Es,.025):+.3f}; {q(Es,.975):+.3f}]")
print(f"\nнадлишок WR: {wab-st.mean(WRs):+.1f} пп   CI [{wab-q(WRs,.975):+.1f}; {wab-q(WRs,.025):+.1f}]")
print(f"надлишок E:  {eab-st.mean(Es):+.3f}R  CI [{eab-q(Es,.975):+.3f}; {eab-q(Es,.025):+.3f}]")
print(f"\n{'❌ ГІРШЕ за випадковий вхід' if wab < q(WRs,.025) else ('✅ краще' if wab > q(WRs,.975) else '⚪ нерозрізнимо від випадкового')}")
