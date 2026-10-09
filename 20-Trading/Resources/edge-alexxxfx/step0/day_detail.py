#!/usr/bin/env python3
"""Детальний розбір конкретних днів за первинною логікою v5 (БЕЗ доборів)."""
import sys,io,contextlib,importlib.util,datetime as dt
spec=importlib.util.spec_from_file_location("v5","sweep_mss_m5_v5.py")
m=importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()):
    sys.argv=["v5"]; spec.loader.exec_module(m)
bars,days,dk,dhi,dlo=m.bars,m.days,m.dk,m.dhi,m.dlo
T=[t for t in m.trades if t["kind"]=="PRIMARY"]

for ds in sys.argv[1:] or ["2026-01-07","2026-01-08"]:
    d=dt.date.fromisoformat(ds); di=dk.index(d); pd_=dk[di-1]
    idxs=days[d]; o=bars[idxs[0]][1]; c=bars[idxs[-1]][4]
    asia=[i for i in idxs if bars[i][0].hour<6]
    print(f"\n{'='*64}\n{d} {d.strftime('%A')}")
    print(f"  Daily open {o:.5f}  H {dhi[d]:.5f}  L {dlo[d]:.5f}  C {c:.5f}  діапазон {(dhi[d]-dlo[d])*10000:.1f}п")
    print(f"  PDH {dhi[pd_]:.5f}  PDL {dlo[pd_]:.5f}")
    if asia: print(f"  Asia H {max(bars[i][2] for i in asia):.5f}  Asia L {min(bars[i][3] for i in asia):.5f}")
    tr=[t for t in T if t["date"]==d]
    if not tr: print("  ⛔ сетапу немає"); continue
    for t in tr:
        print(f"\n  {'SHORT' if t['dir']<0 else 'LONG'}  пул {t['pool']}")
        print(f"    вхід  {t['entry']:.5f}  о {t['t']:%H:%M} UTC")
        print(f"    SL    {t['sl']:.5f}   ризик {t['risk']*10000:.1f}п")
        print(f"    TP    {t['tp']:.5f}   RR {t['rr']:.2f}")
        print(f"    →     {t['exit']}  {t['R']:+.2f}R")
