---
title: GBPUSD Top-Down Analysis
date: 2026-05-25
tags: [GBPUSD, TDA, bearish-corrective, forex]
category: Analysis
project: Trading
status: analysis-complete
pair: GBPUSD
strategy: smc-price-action-combo
agent: analyst
pinecone_indexed: false
---

# GBPUSD: Top-Down Analysis — 25.05.2026

> Дата UTC: 2026-05-25 06:04 / Київ 09:04 EEST. London KZ активна (summer 06:00-08:00 UTC). Поточна ціна: **1.34837**.

## 🏛 Weekly (Тижневий графік)
W (15W): **+6.52%**, range `1.20997 – 1.387`. Останні 5W closes: `1.3575 → 1.36324 → 1.33242 → 1.34312 → 1.34836` — пік 1.387 у березні, потім distribution під 1.36–1.37, далі масивний ведмежий тиждень (high 1.36536 → close 1.33242, ~-330 pts), pullback 1.34312, поточний тиждень відкрив 1.3459 і дрейфує 1.34514–1.34908. **HTF Bullish-Exhausted / Bearish-Corrective**: довгостроковий аптренд утомлений, попередній цикл показав sweep ATH 1.387 і BOS вниз; поточна динаміка — corrective pullback у зону D/H4 supply.

![[img/gbpusd_w.png]]

## 📅 Daily (Денний графік)
20D range `1.31596 – 1.387`, **-0.43%** за період. Останні 5D closes: `1.33948 → 1.34348 → 1.34296 → 1.34312 → 1.34836` — 4 дні tight consolidation 1.339–1.345, сьогодні відкрив 1.3459 і вже зробив hi 1.34908. **D позиція у W range**: мідл-зона. Структура: **range with bullish drift**, без чіткого BOS. Ключова D supply зона: 1.350–1.365 (попередній distribution). Сьогоднішня D ще тільки розгортається — імовірний тест 1.350 на London open.

![[img/gbpusd_d.png]]

## ⏱ 4-Hour (4-годинний графік)
H4 (30 барів): range `1.33026 – 1.36578`, **-0.7%**. Останні 5×4H closes: `1.34443 → 1.34312 → 1.3479 → 1.34832 → 1.34836` — після bounce від 1.33026 серія слабких higher closes, ціна повзе вгору у зону H4 OB. **H4 OB / Supply**: 1.350–1.355 (попередня підтримка → тепер resistance, перевірена 19–21.05). **H4 структура**: corrective uptrend без BOS, прицільно йде у супплай-зону для майбутньої rejection.

![[img/gbpusd_h4.png]]

## 🕐 1-Hour (1-годинний графік)
H1: range `1.3375 – 1.34908`, **+0.5%** (30 барів). Останні 5H1 closes: `1.34769 → 1.34752 → 1.34832 → 1.34824 → 1.34836` — tight bullish drift, ціна підійшла впритул до **H1/D high 1.34908** = ключова BSL (buy-side liquidity).
**SMT з EURUSD H1:** EURUSD 1.15763–1.1649 / close 1.16428 — також біля локального H1 high. **SMT синхронний** (немає дивергенції): обидві пари у однотипному consolidation біля resistance, USD weakness mild. Це **не дає reversal edge через SMT**, але підтверджує що pair-specific bias має домінувати.

![[img/gbpusd_h1.png]]

## 🎯 15-Minute (15-хвилинний графік)
M15: range `1.3456 – 1.34908`, останні бари 1.3487 → 1.34824 → 1.34838. Ціна стиснулась під BSL 1.34908. Сценарії:
1. **Консервативно (SHORT, primary):** sweep BSL `1.34908` → закриття M15 під 1.3488 + CHoCH вниз → SHORT з ретесту 1.3490–1.3510 (H4 OB зона). Ціль: 1.345 (TP1), 1.340 (TP2), 1.3375 (TP3).
2. **Агресивно (SHORT):** market sell з зони 1.3500–1.3510 при першому ж заході (без чекання CHoCH M15) — вищий ризик, кращий RR.
3. **Counter-trend (LONG, не рекомендовано):** BOS M15 крізь 1.3491 + close H1 above 1.3500 → LONG до 1.355 — суперечить HTF, торгувати тільки якщо є чіткий imbalance reclaim.

![[img/gbpusd_m15.png]]

## ⚡ 5-Minute (5-хвилинний графік) — Торговий план

- **Bias:** Bearish (short, corrective rejection з H4 OB) 📉
- **Entry Zone:** `1.3495 – 1.3510` (H4 OB) — чекати **sweep BSL 1.34908 + M15 rejection candle**
- **Stop Loss:** `1.3540` (вище M15 sweep extreme з буфером, нижче H4 swing high 1.35531) — **~30–40 pts** від entry, точно **40 pts** від mid-entry 1.3500
- **TP1:** `1.3458` (intraday consolidation pivot) — RR **1.05**
- **TP2:** `1.3420` (H1 mid + D opening area) — RR **2.0**
- **TP3:** `1.3375` (H1 swing low, SSL) — RR **3.1**
- **Lot Size:** `$100 / (40 pts × $10/pt) = 0.25 lot` (GBPUSD: 1 pip = $10 на 1 lot — перевірити OANDA)

⚠️ TP1 RR < 1.2 — використовувати лише для часткового виходу (50%), залишок везти на TP2/TP3.

![[img/gbpusd_m5.png]]

---

**Коментар:**
- HTF (W/D) **bearish-corrective** після BOS вниз з ATH 1.387. Поточний pullback у зону H4 OB 1.350–1.355 — класична SMC short-setup точка.
- **Primary playbook**: `smc-price-action-combo` — Sweep BSL 1.34908 + OB rejection + M15 retest entry. Збігається з умовами Trend (continuation bearish) у `strategy-detection.md`.
- **SMT з EURUSD синхронний** — не додає edge, але підтверджує USD-neutral консолідацію перед NY.
- **Сесія**: London KZ активна (06:00–08:00 UTC), очікувати volatility spike. NY KZ 12:00–14:00 UTC — друге вікно для setup, якщо London не дає тригера.
- **News risks (перевірити news-watcher)**: понеділок 25.05 — UK Bank Holiday (Spring Bank Holiday), низька ліквідність GBP-крос; US — Memorial Day, ринки США часткове закриття. **Уважно**: ліквідність може бути аномально низькою, sweep може бути різким і fake.
- **Не входити раніше 09:00 Київ** (виконано — зараз 09:04). Без чіткого M15 CHoCH і rejection candle — пас.
- **Min RR на TP2 = 2.0** — відповідає правилу.

### Перевірка чек-листа

- [x] Папка `2026-05-25/img/` містить 6 PNG (w/d/h4/h1/m15/m5)
- [x] W/D/H4 bias узгоджені (bearish-corrective)
- [x] Entry < SL, TP1 < TP2 < TP3 нижче entry (SHORT — порядок цін правильний)
- [x] RR TP2 ≥ 1:2 (2.0)
- [x] Lot розрахований
- [x] SMT з EURUSD зазначений
- [x] Frontmatter з `pinecone_indexed: false`
- [x] 6 image-посилань вставлені
