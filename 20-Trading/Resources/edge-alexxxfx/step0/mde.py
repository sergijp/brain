import math
def sd_R(p,rr):            # R=+rr з ймовірністю p, -1 інакше
    return (rr+1)*math.sqrt(p*(1-p))
def E(p,rr): return p*rr-(1-p)
def n_for(eff,sd,z=2.80): return (z*sd/eff)**2
def mde(N,sd,z=2.80): return z*sd/math.sqrt(N)
ADJ=0.78   # емпірична поправка: AB аналітично 1.97R, фактично 1.53R (BE/time-stop стискають хвіст)

TS=[('ТС-1 (архів)',0.45,3.0,24),('ТС-2',0.45,3.0,11),('ТС-3',0.40,3.0,10),
    ('ТС-3 (типовий RR 1:4)',0.40,4.0,10),('NS',0.40,2.5,0),('AB (факт)',0.31,3.27,42)]
print("Нульовий winrate = 1/(1+RR): для фіксованої геометрії випадковий вхід влучає в TP саме так часто.\n")
print(f"{'ТС':24} {'WR ціль':>8} {'RR':>5} {'WR нуля':>8} {'перевага':>9} {'E ціль':>8} {'sd/трейд':>9}")
for name,p,rr,N in TS:
    p0=1/(1+rr)
    print(f"{name:24} {p*100:7.0f}% {rr:5.1f} {p0*100:7.1f}% {(p-p0)*100:+8.1f}пп {E(p,rr):+7.2f}R {sd_R(p,rr)*ADJ:8.2f}R")

print(f"\n{'='*84}\nСкільки трейдів треба, щоб відрізнити цільову перевагу від нуля (потужність 80%)\n{'='*84}")
print(f"{'ТС':24} {'N зараз':>8} {'MDE зараз':>11} {'N треба':>9} {'дефіцит':>9}")
for name,p,rr,N in TS:
    sd=sd_R(p,rr)*ADJ; e=E(p,rr)
    need=n_for(e,sd)
    cur=f"{mde(N,sd):+.2f}R" if N>0 else "—"
    print(f"{name:24} {N if N else '—':>8} {cur:>11} {need:9.0f} {(need-N) if N else need:9.0f}")

print(f"\n{'='*84}\nТе саме у відсоткових пунктах winrate (простіше перевіряти)\n{'='*84}")
for name,p,rr,N in TS:
    p0=1/(1+rr); d=p-p0
    # n для різниці пропорцій vs відомого p0, односторонній 5%, потужність 80%
    n=((1.645*math.sqrt(p0*(1-p0))+0.842*math.sqrt(p*(1-p)))/d)**2
    print(f"  {name:24} нуль {p0*100:.0f}% → ціль {p*100:.0f}%  (Δ {d*100:+.0f} пп)   N ≈ {n:.0f}")

print(f"\n{'='*84}\nЩо насправді показували наявні вибірки\n{'='*84}")
from math import comb
def pbinom_ge(k,n,p): return sum(comb(n,i)*p**i*(1-p)**(n-i) for i in range(k,n+1))
cases=[('ТС-3 EURUSD Pine v5',10,5,0.25),('ТС-3 GBPUSD',21,4,0.25),
       ('ТС-2 Pine v1',11,1,0.25),('ТС-1 Pine v3',24,9,0.25),('AB механічний',42,13,0.25)]
for name,n,k,p0 in cases:
    pv=pbinom_ge(k,n,p0)
    print(f"  {name:22} {k}/{n} = WR {100*k/n:4.1f}%  vs нуль {p0*100:.0f}%  →  p = {pv:.3f}  "
          f"{'(значуще, але одиничний тест з багатьох)' if pv<0.05 else '(нерозрізнимо від нуля)'}")
