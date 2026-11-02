"""Стандартний звіт для нічного циклу: report(label, family, **kw) -> рядок у LOG.md + друк."""
import sys, json, random, datetime as D
sys.path.insert(0, '..')
from bt import *
import os
STATE = os.path.join(os.path.dirname(__file__), 'state.json')
LOGF = os.path.join(os.path.dirname(__file__), 'LOG.md')
EDGES = [D.datetime(2026,8,16,tzinfo=UTC), D.datetime(2026,8,30,tzinfo=UTC), D.datetime(2026,9,13,tzinfo=UTC), D.datetime(2026,9,27,tzinfo=UTC), D.datetime(2026,10,11,tzinfo=UTC)]
_data = {nm: load(nm) for nm in INST}
def fold_of(t):
    dt = D.datetime.fromtimestamp(t, UTC)
    for k in range(4):
        if EDGES[k] <= dt < EDGES[k+1]: return k
    return 3
def boot(rs, n=4000, seed=7):
    random.seed(seed); m = len(rs)
    if m < 5: return (float('nan'), float('nan'))
    b = sorted(sum(random.choices(rs, k=m))/m for _ in range(n))
    return (b[int(0.025*n)], b[int(0.975*n)])
def run_all(**kw):
    out = {}
    for nm in INST: out[nm] = run(_data[nm], nm, **kw)
    return out
def metrics(trs):
    allr = [t['r'] for nm in trs for t in trs[nm]]
    n = len(allr)
    if n == 0: return None
    folds = [[t['r'] for nm in trs for t in trs[nm] if fold_of(t['t']) == k] for k in range(4)]
    lo, hi = boot(allr)
    return dict(n=n, avg=sum(allr)/n, tot=sum(allr), wr=sum(1 for r in allr if r>0)/n, lo=lo, hi=hi,
                folds=[(len(f), (sum(f)/len(f) if f else 0.0)) for f in folds],
                inst={nm: (len(trs[nm]), (sum(t['r'] for t in trs[nm])/len(trs[nm]) if trs[nm] else 0.0)) for nm in trs})
def report(label, family='', bonf=1, log=True, **kw):
    trs = run_all(**kw); m = metrics(trs)
    st = json.load(open(STATE)); st['tested'] = st.get('tested', 0) + 1; json.dump(st, open(STATE, 'w'))
    if not m: line = f'- [{family}] {label}: 0 угод'
    else:
        pos = sum(1 for n_, a in m['folds'] if n_ >= 5 and a > 0); eff = sum(1 for n_, a in m['folds'] if n_ >= 5)
        z = 1.96 if bonf <= 1 else {2:2.24,3:2.39,5:2.58,10:2.81,20:3.02,50:3.29}.get(min([k for k in (2,3,5,10,20,50) if k >= bonf] or [50]), 3.29)
        # CI з поправкою: розширюємо відносно 95% CI
        mid = (m['lo']+m['hi'])/2; half = (m['hi']-m['lo'])/2 * (z/1.96); lo_b = mid - half
        verdict = 'ПЕРЕВАГА?' if (m['avg']>0 and pos>=3 and eff>=3 and lo_b>0) else ('не доведено' if m['avg']>0 else 'мінус')
        fo = ' '.join(f'{n_}:{a:+.2f}' for n_, a in m['folds'])
        ins = ' '.join(f'{k[:3]}:{v[0]}/{v[1]:+.2f}' for k, v in m['inst'].items())
        line = f"- [{family}] {label}: N={m['n']} avgR={m['avg']:+.2f} Σ={m['tot']:+.1f} wr={m['wr']:.0%} CI95=[{m['lo']:+.2f};{m['hi']:+.2f}] (Bonf×{bonf}: нижня {lo_b:+.2f}) фолди(n:avgR) {fo} | {ins} → **{verdict}**"
    print(line)
    if log: open(LOGF, 'a').write(line + '\n')
    return trs, m
