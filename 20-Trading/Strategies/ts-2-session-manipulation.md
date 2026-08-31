---
title: "ТС-2 — Session Manipulation"
date: 2026-04-22
tags: [trading, strategy, smc, ts-2, ict, killzone, session]
category: trading
status: rework
parent: "[[20-Trading/Strategies/smc-playbook-v2]]"
journal_tag: ts-2-session
pinecone_indexed: false
---

# 📊 ТС-2 — Session Manipulation

> 🔧 **ДООПРАЦЮВАННЯ (рішення власника 2026-08-24).** Стратегія залишається в роботі.
>
> **Важливо: попередній тест провалив НЕ стратегію, а метод тестування.** Pine-бенч дав 11 угод, WR 0-9%, gross $0 — і висновок у [[ts-tracker]] був однозначний: *«Pine НЕ годиться як proxy для ТС-2 (discretionary edge)»*. Тобто едж не спростовано — його **жодного разу не виміряли**.
>
> ## 🎯 План доопрацювання
>
> **Ключова можливість:** з дослідження 962 стратегій (серпень 2026) з'явився **чесний симулятор без lookahead** — `~/AI/research/strategies/s88/sim.py` і `s534/simlib.py`. Саме він виявив, що більшість «прибуткових» стратегій були артефактом підглядання. Цей інструмент і треба застосувати замість Pine.
>
> | # | Крок | Деталі |
> |---|------|--------|
> | 1 | **Механізувати правила** | Головна причина провалу — R3 `manipulation → distribution` описано дискреційно. Потрібне формальне визначення: що саме рахується manipulation-leg (sweep рівня? глибина? за скільки барів?) і що — distribution |
> | 2 | **Порт на чесний симулятор** | Не Pine. Взяти движок з `s88/` або `s534/`, EURUSD M15 |
> | 3 | **Розбити на DEV / CHECKPOINT / ГЕЙТ** | Той самий протокол, що дав валідні №88 і №534: налаштування тільки на DEV, сліпе вікно недоторкане |
> | 4 | **Порівняти з ASR і №88** | Обидві вже ловлять killzone-маніпуляцію на London open. Треба знати, чи ТС-2 дає **щось нове**, чи це третя обгортка тієї самої ідеї |
>
> ⚠️ **Ризик, який треба перевірити першим:** ASR (основна) і №88 обидві побудовані на sweep у killzone. Якщо ТС-2 після механізації дає ті самі сигнали — це не третя стратегія, а дублікат, і чесніше злити її в одну з них.
>
> **Success criteria лишаються з нотатки:** WR ≥ 45%, min RR 1:3.

**Філософія:** time-of-day driven intraday-entries. Killzone-вікна відомі заздалегідь, у них чекаємо **manipulation → distribution** patterns. Сесія відкриває і закриває позицію.

**Inherits from:** [[20-Trading/Strategies/smc-playbook-v2]] (risk, scoring, gates, journal, EOD-close rule)

**Style:** intraday | **Min RR:** 1:3

---

## 🎲 Включені моделі

| # | Модель | Killzone |
|---|--------|----------|
| 4 | **AMD / Power of Three (ICT)** | London KZ 07:00-09:00 UTC + NY KZ 12:00-14:00 UTC |
| 6 | **Silver Bullet** | NY 15:00-16:00 UTC (10:00-11:00 NY) |
| 7 | **London Reversal** | ~10:00 UTC (після London open) |

**Чому разом:** усі три — **session-bound**, спрацьовують у фіксованому годинному вікні. Тригер: Judas sweep (manipulation) → reversal/distribution. Без killzone — setup не існує.

---

## ⏱️ Робочі таймфрейми
- HTF Bias: **D / H4**
- Range mark-up: **H1** (Asian range / попередня сесія)
- Trigger: **15m / 5m**

---

## 🎯 Унікальні правила ТС-2

### R1. Killzone-only входи
Поза killzone — **не торгуємо** (навіть якщо setup ідеальний). Це ціна систематичності для цієї ТС.

### R2. Pre-session ритуал (15 хв до KZ)
- HTF bias підтверджено?
- Asian / попередня сесія: range high/low розмічено
- News calendar чистий ±30 хв?
- Daily profile (Expansion/Consolidation/Retracement) визначено

### R3. Manipulation first, distribution second
Послідовність обов'язкова:
1. Sweep протилежної сторони у KZ (Judas)
2. LTF ChoCH у напрямку HTF bias
3. Вхід на OB/FVG що створив ChoCH

Без sweep — **skip**. «Тихе» пробиття без захвату стопів = слабкий сигнал для ТС-2.

### R4. Hard time exit (intraday)
- Якщо setup не сформувався до **кінця KZ** — skip, чекаємо наступну сесію
- Якщо у позиції без TP1 за **30 хв до EOD (20:30 UTC)** — manual close на market
- **EOD hard exit:** усі позиції закриваються до 21:00 UTC (NY close) — no overnight, без винятків

### R6. Min RR 1:3 (hard gate)
TP1 до найближчої ліквідності має давати RR ≥ 1:3 від sweep extreme SL. Якщо ні — skip (часта ситуація на range-днях, де distribution leg короткий).

### R5. Session overlap rule
NY KZ і Silver Bullet перетинаються по часу — **не подвоюємо** експозицію. Один трейд на сесію максимум.

---

## 📊 Scoring (наслідує master, тюн)
Стартуємо на **Standard профілі** (≥8 / 5-7 / <5).
**Корекція для ТС-2:**
- +1 бал якщо sweep захопив **equal highs/lows** (не просто wick)
- -1 бал якщо великий range в Asian (low-quality manipulation сетапи)

---

## 🛡️ Risk
Базовий 1% з master.
**Унікальний guard:** макс **2 трейди на день** (по одному на KZ). 3-й = заборонено навіть якщо валідний — overtrading guard.

---

## 🎯 Backtest план

| Параметр | Значення |
|----------|----------|
| Sample size | **30 трейдів** мінімум |
| Період | 6 міс історії |
| Watchlist | EURUSD, GBPUSD (London-sensitive), US100/GER40 (NY-sensitive) |
| Журнал | `20-Trading/Backtest/trades/YYYY-MM-DD-NN-[pair]-ts2-[model].md` |
| Ціль часу | ≤10 хв/трейд |

### Success criteria (для go-live)
- WR ≥ 45%
- Expectancy ≥ +0.4R після costs
- Max DD ≤ 8% (intraday — менший толеранс)
- Adherence ≥ 90% full

### Retirement criteria
- WR < 40% на 30+ трейдах → пауза
- Якщо одна модель з 3-х валить статистику — викидаємо її, ТС працює на 2-х

---

## 🏷️ Journal tag
```yaml
ts: ts-2-session
model: amd | silver_bullet | london_reversal
session: london_kz | ny_kz
```

---

## 📌 Status
🟡 **Queued** — створено 2026-04-22, очікує запуску бектесту.

---

## 🔗
- [[20-Trading/Strategies/smc-playbook-v2]] — master playbook
- [[20-Trading/Strategies/ts-1-reversal-at-poi]]
- [[20-Trading/Strategies/ts-3-inner-fvg-sniper]]
- [[20-Trading/Strategies/ts-tracker]]
- [[20-Trading/Backtest/README]]
