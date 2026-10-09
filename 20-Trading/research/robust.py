import random, collections
from grid import *
base=dict(setup='reclaim',bias='htf_with',entry='limitopen',buf=1.0,risk_max=3.0,kz=[(420,600),(750,960)])
def agg(o):
    return [t for n in INST for t in o[n][3]]
print('--- HTF lookback')
for hn in (1,2,3,5,8):
    o=ev(**{**base,'htf_n':hn});r=row(f'htf_n={hn}',o);print(f'  htf_n={hn}: N={r[1]} avgR={r[3]:+.2f} IS {r[5]:+.2f} OOS {r[7]:+.2f} per inst {r[8]}')
print('--- continuation (послаблений)')
for ma in (3,6,12):
    o=ev(**{**base,'setup':'continuation','entry':'market','max_age':ma});r=row('c',o);print(f'  max_age={ma}: N={r[1]} avgR={r[3]:+.2f} per inst {r[8]} n={r[9]}')
o=ev(**base);tr=agg(o)
print('--- кандидат: розбивка (N=%d)'%len(tr))
for key,f in (('рівень',lambda t:t['tag']),('година UTC',lambda t:t['hour']),('сторона',lambda t:'лонг' if t['side']==1 else 'шорт'),('вихід',lambda t:t['why'])):
    g=collections.defaultdict(list)
    for t in tr:g[f(t)].append(t['r'])
    print(' ',key,{k:(len(v),round(sum(v)/len(v),2)) for k,v in sorted(g.items())})
rs=[t['r'] for t in tr];m=sum(rs)/len(rs)
random.seed(1);bs=sorted(sum(random.choices(rs,k=len(rs)))/len(rs) for _ in range(5000))
print('  avgR=%.2f, 95%% bootstrap CI [%.2f; %.2f], частка угод з тейком %.0f%%, вінрейт %.0f%%'%(m,bs[125],bs[4875],100*sum(1 for t in tr if t['why']=='ЦІЛЬ')/len(tr),100*sum(1 for r in rs if r>0)/len(rs)))
wk=collections.defaultdict(float)
for t in tr:wk[ts(t['t']).strftime('%m-%d')[:5]]+=0
w=collections.defaultdict(lambda:[0,0.0])
for t in tr:
    k=(ts(t['t'])-D.timedelta(days=ts(t['t']).weekday())).strftime('%m-%d');w[k][0]+=1;w[k][1]+=t['r']
print('  по тижнях (початок тижня: N, R):',{k:(v[0],round(v[1],1)) for k,v in sorted(w.items())})
print('--- база з індикатора v0.2 (auto/market/0.75/без kz):')
o=ev();r=row('b',o);print(f'  N={r[1]} avgR={r[3]:+.2f} per inst {r[8]}')
print('--- перестановочний тест: випадкові напрямки на тих же сигналах не рахується; перевірка «без витрат x2»')
o=ev(**{**base});
import bt
for k in INST: bt.INST[k]['spread']*=2
o=ev(**base);r=row('c',o);print(f'  спред x2: N={r[1]} avgR={r[3]:+.2f}')
