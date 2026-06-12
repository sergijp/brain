---
title: EURUSD Top-Down Analysis
date: 2026-05-12
tags: [EURUSD, TDA, bullish-corrective, forex, paper-trade]
category: Analysis
project: Trading
pair: EURUSD
strategy: smc-price-action-combo
agent: analyst
status: analysis-complete
pinecone_indexed: false
---

# EURUSD: Top-Down Analysis — 12.05.2026

> Оновлений аналіз: 06:16 UTC / 09:16 EEST. London KZ активна (~1:16 від відкриття).  
> **PAPER TRADE** — реальний ордер виключено через Kassandra BLOCK (SMT дивергенція). Симуляція для перевірки setup-у.

## 🏛 Weekly (Тижневий графік)

15W діапазон: 1.1411 – 1.19288. Останні 5W closes: `1.17638 → 1.17186 → 1.17212 → 1.17852 → 1.17566 (поточний)` — після SSL sweep на W-3 (1.16551) відбувся bullish reclaim. W-2 закрилась 1.17852 (бичачий бар). Поточний тижневий бар: open 1.17524, high 1.17878, low 1.17483, close 1.17566 — корекція від weekly high. **HTF bias: Bullish-Corrective.**

## 📅 Daily (Денний графік)

20D діапазон: 1.16551 – 1.18492. Останні 5D closes: `1.17484 → 1.17237 → 1.17852 → 1.17824 → 1.17567 (сьогодні)`. D-1 (вчора): bullish close 1.17824, new D high 1.17878. Сьогодні відкрилось 1.17814, low 1.17523, поточна ціна 1.17567 — bearish intraday pullback. Daily структура HL збережена. **D bias: Bullish, корекція до H4 demand OB.**

## ⏱ 4-Hour (4-годинний графік)

H4 30-барний діапазон: 1.16812 – 1.17967. Останні 5×4H closes: `1.17733 → 1.17824 → 1.17672 → 1.17571 → 1.17565 (поточний)` — корекція від H4 high 1.17878. **H4 Demand OB: 1.17523–1.17572** (остання бичача основа перед імпульсом до 1.17878). Ціна зараз у цій зоні. **H4 bias: Bearish retracement до H4 demand у bullish HTF context.**

## 🕐 1-Hour (1-годинний графік)

H1 30-барний діапазон: 1.17488 – 1.17878. Останні 5H closes: `1.17626 → 1.17564 → 1.17571 → 1.17624 → 1.17564 (поточний)`. **SSL sweep відбувся:** H1 low 1.17488 (нижче H4 OB bottom). London open (06:00 UTC) дав бичачу H1 свічку: low 1.17523 → high 1.17682. Поточна H1 свічка (07:00 UTC): 1.17626 open, 1.17663 high, 1.17553 low, 1.17564 close — retracement. **SMT:** GBPUSD паралельно в аналогічній зоні demand. Кореляція підтверджена, дивергенції немає.

## 🎯 15-Minute (15-хвилинний графік)

M15 30-барний діапазон: 1.17523 – 1.17855. **CHoCH СФОРМОВАНО:**
- Sweep SSL: M15 low 1.17523 (06:05 UTC)
- Bullish impulse candle: 1.17555 → 1.17682 (12.7 pip рух) ← CHoCH
- Retest: поточна ціна 1.17553–1.17576 = retest рівня CHoCH

Останні 5 M15 closes: `1.17551 → 1.17560 → 1.17624 → 1.17576 → 1.17564` — retest після CHoCH.

Сценарії:
1. **Консервативно (LONG — paper):** retest 1.17553–1.17576 тримає + наступна M15 бичача свічка закривається вище 1.17590 → ВХІД. Поточна ціна В ЗОНІ ВХОДУ.
2. **Агресивно:** M15 BOS вище 1.17682 → retest → entry.

## ⚡ 5-Minute (5-хвилинний графік) — Торговий план (PAPER TRADE)

> ⚠️ PAPER TRADE — не реальна позиція. Виключено через Kassandra (SMT дивергенція у попередньому аналізі). Симуляція для оцінки setup-у.

- **Bias:** Bullish-Corrective (pullback завершено, CHoCH M15 підтверджено) 📈
- **Entry Zone:** `1.17553 – 1.17580` (retest CHoCH рівня, поточна ціна)
- **Stop Loss:** `1.17480` (нижче sweep low 1.17523 — 4.3 pip buffer) — **~8-9 pips**
- **TP1:** `1.17700` — RR ~1.5 (H1 resistance / recent high)
- **TP2:** `1.17878` — RR ~3.6 (H4/D high = BSL target) ← **managing TP**
- **TP3:** `1.17967` — RR ~4.6 (D/H4 extension high)
- **Paper Lot Size:** `$100 / (8.7 × $10) ≈ 1.15 lot` (EURUSD: 1 pip ≈ $10/lot — перевірити брокер)

---
**Setup score: 7/10** (paper trade)

**Коментар:** З моменту попереднього аналізу (05:10 UTC) ринок відпрацював очікуваний сценарій: SSL sweep 1.17488-1.17523 відбувся, London open дав CHoCH на M15 (imbalance candle 1.17555 → 1.17682). Поточна ціна 1.17564 — retest зони CHoCH. Це класичний PRIMARY PATTERN вхід (Sweep + OB Rejection + Retest). GBPUSD корелює синхронно (підтвердження). News: US CPI 12:30 UTC — kill-switch 11:25 UTC (збігається з реальними планами). **RR TP2 ~3.6 — торгувальний. Для paper trade — якісний benchmark.**
