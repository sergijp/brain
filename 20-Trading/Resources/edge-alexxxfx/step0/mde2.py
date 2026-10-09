import math
ADJ=0.78
def sd(p,w): return (w+1)*math.sqrt(p*(1-p))*ADJ    # виграш +w, програш -1
def E(p,w):  return p*w-(1-p)
def n_exp(e,s,z=2.80): return (z*s/e)**2
def n_prop(p0,p1,a=1.645,b=0.842):
    return ((a*math.sqrt(p0*(1-p0))+b*math.sqrt(p1*(1-p1)))/(p1-p0))**2

# (назва, WR ціль, геометричний RR на вході, avg R per win заявлений, ціль expectancy, поточна ціль вибірки)
TS=[('ТС-1',0.45,3.0,2.0,0.40,30),
    ('ТС-2',0.45,3.0,2.0,0.40,30),
    ('ТС-3',0.40,3.0,3.0,0.50,40),
    ('NS'  ,0.40,3.0,2.5,0.60,50)]

print("1) ВНУТРІШНЯ УЗГОДЖЕНІСТЬ КРИТЕРІЇВ")
print("   Якщо виконати рівно WR ціль і avg-win ціль — чи проходить поріг expectancy?\n")
print(f"{'ТС':6} {'WR':>5} {'avg win':>8} {'→ E фактично':>14} {'поріг E':>9}  вердикт")
for n,p,g,w,et,cur in TS:
    e=E(p,w)
    ok = e>=et
    need_wr=(et+1)/(w+1)
    print(f"{n:6} {p*100:4.0f}% {w:8.1f}R {e:+13.2f}R {et:+8.2f}R  "
          f"{'✅' if ok else '❌ недосяжно — треба WR ≥ %.1f%%'%(need_wr*100)}")

print("\n\n2) СКІЛЬКИ ТРЕБА ТРЕЙДІВ — два різні питання дають різні відповіді\n")
print(f"{'ТС':6} {'WR нуля':>8} {'N: WR > нуля':>13} {'E ціль':>8} {'sd':>6} {'N: expectancy':>14} {'зараз':>6} {'→ ставити':>10}")
for n,p,g,w,et,cur in TS:
    p0=1/(1+g)
    n1=n_prop(p0,p)
    e=E(p,w); s=sd(p,w); n2=n_exp(e,s)
    rec=int(round(max(n1,n2)/5)*5)
    print(f"{n:6} {p0*100:7.1f}% {n1:13.0f} {e:+7.2f}R {s:6.2f} {n2:14.0f} {cur:6} {rec:10}")

print("""
Різниця між колонками — бо заявлений avg R per win НИЖЧИЙ за геометричний RR входу
(часткові фіксації, BE). Тест на winrate це ігнорує, тест на expectancy — ні.
Гроші робить expectancy, тому ставити треба за нею.""")
