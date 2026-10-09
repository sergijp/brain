import csv,collections,re
rows=list(csv.DictReader(open('edge_trade_log.csv',encoding='utf-8')))
def esc(s,n=None):
    s=(s or '').replace('|','/').replace('\n',' ').strip()
    return s[:n] if n else s
def g(*c): return [r for r in rows if r['cat'] in c]
out=[];W=out.append

W("# THE EDGE by AlexxxFX — лог угод, планів і аналізів\n")
W(f"Джерело: Telegram-експорт каналу, **{rows[0]['date']} → {rows[-1]['date']}**. "
  f"З 2216 повідомлень (1540 з текстом) відібрано й структуровано **{len(rows)}** торгових записів.\n")
W("> Важливо: канал не є торговим журналом. Явний результат у R вказаний лише в **25** записах — "
  "решта угод живе у 1423 скрінах TradingView і 301 відео. Тому статистика «яка модель працює» "
  "з цього експорту не рахується; рахується — що саме він торгував, як формулював вхід і які "
  "результати публікував по періодах.\n")

W("## Розподіл\n")
W("| Категорія | К-сть | Що це |\n|---|---|---|")
d={'PLAN':'Pre-Session / Trading Plan — план ДО сесії','REVIEW':'Post-Session / Weekly Review / Daily Report',
'NOTE':'Market Note — заметка про поведінку ціни','TRADE_ANALYSIS':'Детальний розбір угоди',
'CHART':'Графік позиції','ANALYSIS':'TDA інструмента','TRADE_IDEA':'Ідея до входу',
'PERFORMANCE':'Опубліковані результати періоду','TRADE_RESULT':'Результат угоди з R'}
for c,n in collections.Counter(r['cat'] for r in rows).most_common(): W(f"| {c} | {n} | {d.get(c,'')} |")
W("\n| Рік | Записів |\n|---|---|")
for y,n in sorted(collections.Counter(r['date'][:4] for r in rows).items()): W(f"| {y} | {n} |")
pc=collections.Counter(); mc=collections.Counter()
for r in rows:
    for p in filter(None,r['pairs'].split('|')): pc[p]+=1
    for p in filter(None,r['models'].split('|')): mc[p]+=1
W("\n**Інструменти:** "+", ".join(f"{k} ({v})" for k,v in pc.most_common()))
W("\n**Елементи PA / моделі за частотою згадок:** "+", ".join(f"{k} ({v})" for k,v in mc.most_common())+"\n")

W("---\n## 1. Опублікована результативність (його цифри)\n")
W("| Дата | Що заявлено |\n|---|---|")
CUR=['2023-10-27','2024-09-05','2024-12-06','2024-12-18','2024-12-23','2025-01-10','2025-01-24',
     '2025-03-31','2025-06-03','2025-07-31','2025-12-11','2026-07-28','2026-08-19']
seen=set()
for r in rows:
    if r['date'] in CUR and r['date'] not in seen and re.search(r'(?i)\d+\s*[R%]',r['text']):
        seen.add(r['date']); W(f"| {r['date']} | {esc(r['text'],330)} |")
W("")

W("---\n## 2. Угоди з зафіксованим R\n")
W("| Дата | Пара | Напрям | R | Елементи | ТФ | Опис |\n|---|---|---|---|---|---|---|")
for r in rows:
    if r['R'] and r['cat'] in ('TRADE_RESULT','TRADE_ANALYSIS','CHART','TRADE_IDEA'):
        W(f"| {r['date']} | {r['pairs'].replace('|','/') or '—'} | {r['dir'] or '—'} | {r['R'].replace('|','/')} | "
          f"{r['models'].replace('|','/') or '—'} | {r['tfs'].replace('|','/') or '—'} | {esc(r['text'],140)} |")
W("")

W("---\n## 3. Явні формули входу з розборів\n")
W("Найцінніше в експорті: 19 записів, де він розписав ланцюг TDA дослівно.\n")
for r in rows:
    if r['chain']:
        head=f"**{r['date']}**"
        if r['pairs']: head+=f" · {r['pairs'].replace('|','/')}"
        if r['R']: head+=f" · **{r['R'].replace('|','/')}R**"
        W(head)
        for c in r['chain'].split(' ;; '): W(f"- `{esc(c,170)}`")
        W(f"\n  {esc(r['text'],300)}\n")

W("---\n## 4. Усі розбори угод та ідеї\n")
W("| Дата | Пара | R | TV-графіків | Відео | Опис |\n|---|---|---|---|---|---|")
for r in sorted(g('TRADE_ANALYSIS','TRADE_RESULT','TRADE_IDEA','CHART'),key=lambda x:x['date']):
    W(f"| {r['date']} | {r['pairs'].replace('|','/') or '—'} | {r['R'].replace('|','/') or '—'} | "
      f"{r['charts'] or '—'} | {(r['yt'].split('|')[0] if r['yt'] else '—')} | {esc(r['text'],150)} |")
W("")

W("---\n## 5. Market Notes — правила, виведені з ринку\n")
for r in g('NOTE'):
    if len(r['text'])>250: W(f"**{r['date']}** — {esc(r['text'],450)}\n")
W("")
open('EDGE-trade-log.md','w',encoding='utf-8').write('\n'.join(out))
print('OK', len('\n'.join(out)),'chars')
