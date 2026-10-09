import sys
from grid import *
def show(label,**kw):
    o=ev(**kw);r=row(label,o)
    print(f'{label:46s} N={r[1]:3d} avgR={r[3]:+.2f} tot={r[2]:+.1f} | IS n={r[4]} {r[5]:+.2f} | OOS n={r[6]} {r[7]:+.2f} | per inst {r[8]} n={r[9]}')
    return o
base=dict(setup='reclaim',bias='htf_with',entry='limitopen',buf=1.0,risk_max=3.0,kz=[(420,600),(750,960)])
show('кандидат v2',**base)
show('  ринком замість ліміту',**{**base,'entry':'market'})
show('  без killzone',**{**base,'kz':None})
show('  біас auto (азія)',**{**base,'bias':'auto'})
show('  біас any',**{**base,'bias':'any'})
show('  буфер 0.75',**{**base,'buf':0.75,'risk_max':2.5})
show('  буфер 1.5',**{**base,'buf':1.5,'risk_max':4.0})
show('  без витрат (спред=0)',**{**base,'cost':False})
show('  окно 07-10/13-16',**{**base,'kz':[(420,600),(780,960)]})
show('  окно 06-11/12-17',**{**base,'kz':[(360,660),(720,1020)]})
show('  пендинг 3 бари',**{**base,'pend_bars':3})
show('  пендинг 12 барів',**{**base,'pend_bars':12})
show('  RR>=3',**{**base,'rr_min':3.0})
show('  RR>=2.0',**{**base,'rr_min':2.0})
