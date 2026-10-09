import subprocess,re,statistics as st
base=open('ts2_backtest.py').read()
print("Поріг RR |  N  |  WR   |    E     |  PF  | медRR |   Σ R")
res={}
for rr in (0.0,0.5,0.8,1.0,1.5,3.0):
    s=base.replace('MIN_RR=3.0',f'MIN_RR={rr}')
    s=s.replace("json.dump(trades,open('ts2_trades.json','w'))",
f"""import json as _j
_j.dump(trades,open('ts2_tr_{str(rr).replace('.','_')}.json','w'))
if trades:
    import statistics as _s
    Rs=[x['R'] for x in trades]; w=[x for x in trades if x['R']>0]
    gp=sum(x['R'] for x in w); gl=-sum(x['R'] for x in trades if x['R']<=0)
    print('RES',len(trades),100*len(w)/len(trades),_s.mean(Rs),(gp/gl if gl>0 else 99),_s.median([x['rr'] for x in trades]),sum(Rs))
else: print('RES 0 0 0 0 0 0')""")
    open('_t3.py','w').write(s)
    o=subprocess.run(['python3','_t3.py'],capture_output=True,text=True).stdout
    m=re.search(r'RES (\d+) (\S+) (\S+) (\S+) (\S+) (\S+)',o)
    if m:
        n,wr,e,pf,mrr,tot=int(m.group(1)),*[float(m.group(i)) for i in (2,3,4,5,6)]
        print(f"  ≥{rr:.1f}   | {n:3d} | {wr:5.1f}% | {e:+7.3f}R | {pf:4.2f} | {mrr:5.2f} | {tot:+6.1f}")
