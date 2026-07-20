---
title: "EURUSD LONG (PAPER) — Asia SSL sweep+reclaim, risk-override forward → CLOSED LOSS"
date: 2026-07-16
time_kyiv: "10:05"
time_utc: "07:05"
tags: [trading, journal, eurusd, smc-price-action-combo, paper, forward-test, risk-override, repeated-focus]
category: trading
pair: EURUSD
direction: long
order_type: buy-limit
strategy: smc-price-action-combo
status: closed   # planned → open → closed
agent: journal-writer
paper: true
real_account_touched: false
risk_state_touched: false
risk_override: true
override_reason: "Risk-gate BLOCK (real). Override дозволено ЛИШЕ як paper/demo для форвард-спостереження. Real рахунок недоторканий (real_risk_usd 0)."
override_scope: paper/demo-only
risk_usd_real: 0
rr_planned: 1.98
result: loss
result_pips: -11.2
result_R: -1.0
result_usd_real: 0
result_usd_paper: -50
closed_at_kyiv: "16:00"
closed_at_utc: "13:00"
price_at_update: 1.14481
repeated_focus:
  scope: EURUSD-long
  level: ACTIVE-BLOCK-WATCH
  attempt: 5
  clean_wins: 0
  window_days: 30
  note: "5-та спроба EURUSD-long (discretionary-SMC), 0 clean wins / 30д. Real BLOCK. Закрито LOSS (paper) — теза підтверджена, block-watch посилено."
tv_position_id: "teaOOk"
tv_symbol: "OANDA:EURUSD"
pinecone_indexed: false
---

# EURUSD LONG (PAPER) — 2026-07-16

> 🧪 **PAPER / FORWARD-TEST.** Real risk $0. `real_account_touched: false`. Реальний `_risk-state.json` day/week-risk НЕ змінюється.
> ⚠️ **Risk override applied:** Risk-gate повернув 🔴 BLOCK (real). Override дозволено ЛИШЕ як paper/demo. Real рахунок недоторканий (real_risk_usd 0, real_account_touched false).
> ⛔ Real-гілка заблокована: repeated-focus #5 (EURUSD-long, ACTIVE-BLOCK-WATCH, 0 clean wins / 30д) + pair-heat 7/0. Live лише після бектесту.
> 🔴 **CLOSED — STOP LOSS.** result −11.2 pips / −1.0R (paper −$50). Kassandra була права: sweep Asia low забрав лонг, стеля 1.14870 навіть не тестувалась.

## Plan

| Field | Value |
|-------|-------|
| Order type | **BUY LIMIT** (pending) |
| Entry | 1.14602 (Asia low / SSL, тригер M15 sweep + reclaim-close) |
| SL | 1.14490 (−11.2 pips, **неструктурний**) |
| TP1 | 1.14746 (Asia high / BSL, RR 1:1.29, часткова 50%) |
| TP2 | 1.14824 (20D high, RR 1:1.98, головна ціль) |
| Lot | 0.45 (paper, half-size) |
| Risk (real) | **$0 (0%) — PAPER, реальний депозит недоторканий** |
| RR planned | 1:1.98 |
| Strategy | [[Strategies/smc-price-action-combo]] |
| TV position | `teaOOk` (OANDA:EURUSD, через tv-position) |

Валідність ордера: **09:00–14:30 Kyiv**. Hard flat **17:45**. Закрити руками до USD MED-кластера **15:30 Kyiv**.

## Result (CLOSED — STOP LOSS)

| Field | Value |
|-------|-------|
| Outcome | 🔴 **STOP LOSS** |
| result_pips | **−11.2** |
| result_R | **−1.0** |
| result_usd (real) | $0 (paper) |
| result_usd (paper) | ~**−$50** (0.45 lot) |
| Closed | ~16:00 Kyiv (≈13:00 UTC) |
| Price @ update | 1.14481 |

**Як відпрацювало:** London торкнувся Asia low (sweep 1.14602 → 1.14567), короткий reclaim до 1.14706 (entry 1.14602 виконано б), далі злам вниз, SL 1.14490 пробитий. Ціна пішла до H4 demand **1.14425** замість вгору — стеля 1.14870 навіть не тестувалась.

## Why (Dixie — NO-TRADE як пріоритет)

- **Dixie: NO-TRADE / C-grade.** Лонг у стелю під незнятим **Weak High 1.14870** — низька якість, обмежений простір.
- Discretionary retest-of-support long (`smc-price-action-combo`): вхід на Asia SSL 1.14602 після M15 sweep + reclaim-close.
- SL 1.14490 неструктурний (−11.2p): над H4 OB 1.14425, під круглим 1.14500 — ліквідний магніт.
- TP2 1.14824 упирається під Weak High 1.14870 — головна ціль у зоні потенційної пастки.
- Записується як **signal-mode форвард-спостереження** для збору статистики (discretionary N=0).

## Risk check (🔴 BLOCK real → override PAPER)

- **VERDICT: 🔴 BLOCK (real).** Override → **paper only**, real рахунок недоторканий.
- **2 hard-підстави BLOCK:**
  1. `repeated_focus_watch` **ACTIVE-BLOCK-WATCH** — attempt **#5**, clean_wins **0 / 30д**.
  2. **Pair-heat 7 / 0** цього тижня (real-вхід потребує чистого win або бектесту).
- **WARN-фактори** (не самостійний BLOCK, посилюють):
  - TP1 RR **1.29 < 1.8** — перша ціль не покриває мінімум.
  - SL **неструктурний** (над H4 OB, під круглим 1.14500).
- **PASS-гейти:** correlation PASS (real open_positions=[]); news PASS (EURUSD CLEAR по HIGH, USD MED 15:30 поза вікном входу до 14:30); session PASS (10:05 Kyiv у London-вікні, вхід після 09:00, flat 17:45); day/week 0%/0% << 3%/6%; четвер (не Пт>18:00) PASS.
- **override_scope:** paper/demo only — real_risk_usd 0, real_account_touched false.

## Kassandra challenge (resolved → SKIP, конвергенція)

- **Kassandra: SKIP** (конвергенція з Dixie).
- TP2 = **пастка** під незнятим Weak High 1.14870.
- **Рецидив** — 3-й захід у стелю 1.148 за день; attempt #5 у ширшому watch.
- Форвард discretionary **N=0** — недостатньо статистики для будь-якого live-рішення.
- Резолюція: НЕ ставити real. Взяти лише як **paper half-size** для форвард-спостереження, без впливу на реальний ризик-стан.

## Links

- Analysis: [[Analysis/2026-07-16/EURUSD-analysis]]
- Strategy: [[Strategies/smc-price-action-combo]]
- Risk state: [[Journal/_risk-state]]

## Execution log (PAPER)

- [x] Buy-limit виставлено @ 1.14602 (pending) @ 10:05 Kyiv
- [x] Filled @ 1.14602 (London торкнув Asia low, sweep 1.14602→1.14567, reclaim до 1.14706)
- [ ] Moved SL to BE — НЕ досягнуто
- [ ] TP1 hit @ 1.14746 — НЕ досягнуто (стеля не тестувалась)
- [x] **STOP LOSS @ 1.14490 @ ~16:00 Kyiv (≈13:00 UTC)** — result **−11.2 pips / −1.0R** (paper ≈ −$50). Ціна пішла далі до H4 demand 1.14425; на момент апдейту 1.14481.

## Lessons (post-trade)

- **Kassandra була права.** Sweep Asia low забрав лонг, стеля 1.14870 навіть не тестувалась. Ціна пішла до H4 demand 1.14425 замість вгору.
- **Класичний buy-stop-hunt** під незнятою стелею — саме те, що передбачали Dixie (C-grade NO-TRADE) і Kassandra (SKIP). Конвергенція команди на SKIP підтвердилась результатом.
- **Форвард-урок:** підтверджено тезу — **лонг у верхню чверть range під незнятим Weak High = негативний EV**. Неструктурний SL під круглим 1.14500 спрацював як магніт.
- **repeated-focus EURUSD-long** тепер має ще один задокументований LOSS (paper), attempt #5 → **block-watch посилено**. clean_wins лишається 0. Live discretionary EURUSD-long — тільки після performance-analyst бектесту.
