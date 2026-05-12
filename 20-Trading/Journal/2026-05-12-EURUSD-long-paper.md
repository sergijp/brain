---
title: "EURUSD LONG — 2026-05-12 Paper Trade (Sweep + CHoCH + Retest)"
date: 2026-05-12
time_kyiv: "09:16"
time_utc: "06:16"
tags: [trading, journal, eurusd, smc-price-action-combo, paper-trade]
category: trading
pair: EURUSD
direction: long
strategy: smc-price-action-combo
status: open
agent: journal-writer
type: paper-trade
paper: true
risk_override: paper_trade_no_real_risk
pinecone_indexed: false
---

# EURUSD LONG — 2026-05-12 (PAPER TRADE)

> ⚠️ Paper trade — симуляція. Не реальна позиція. Ризик-гейт пройдено умовно. Реальний ризик-стан не змінено.
> Причина виключення з реального торгу: Kassandra BLOCK (SMT дивергенція у попередньому аналізі 05:10 UTC).

## Plan

| Field | Value |
|-------|-------|
| Entry zone | 1.17520 (market, double sweep у H4 OB) |
| Trigger | Double sweep 1.17523 + 1.17516 в H4 OB 1.17523–1.17572. M15 CHoCH 06:05 UTC (1.17682). Deeper sweep = кращий entry. |
| SL | 1.17455 (нижче H1 low 1.17488, −6.5 pips) |
| TP1 | 1.17700 (RR ~2.8) |
| TP2 | 1.17878 (RR ~5.5) — основна ціль, BSL target |
| TP3 | 1.17967 (RR ~6.9) |
| Paper Lot | 1.54 (симуляція $100 ризику / 6.5 pips × $10) |
| Risk (paper) | $100 (1.0%) — умовно |
| Kill-switch | 11:25 UTC (до US CPI 12:30 UTC) |
| Strategy | [[Strategies/smc-price-action-combo]] |

## Why

- HTF bias W/D Bullish-Corrective — вища таймфреймова структура підтримує лонг
- H4 Demand OB 1.17523–1.17572 — ціна увійшла в зону і відреагувала
- H1 SSL sweep відбувся: low 1.17488 — ліквідність зібрано нижче
- M15 CHoCH підтверджено о 06:05 UTC на London open — зміна структури в напрямку HTF bias
- GBPUSD синхронна корекція — міжвалютна кореляція підтверджує напрям
- Setup score: 7/10

## Risk check (paper — умовний)

- Day risk used: 0.0% / 3% (paper trade не враховується)
- Correlation: PASS (paper — не впливає на реальний ризик-стан)
- News: US CPI 12:30 UTC — kill-switch о 11:25 UTC обов'язковий
- Session: PASS — London open (06:00-08:00 UTC, літній час)

## Kassandra challenge (resolved)

Kassandra заблокувала реальний трейд через SMT дивергенцію (EURUSD vs GBPUSD розходження на M15 о 05:10 UTC). Рішення: зберегти як paper trade для перевірки сетапу без реального ризику. Якщо ціна відпрацює TP2 — переглянути вагу SMT дивергенції як блокера при наявності H4 OB confluence.

## Links

- Analysis: [[Analysis/2026-05-12/EURUSD-analysis]]
- Strategy: [[Strategies/smc-price-action-combo]]

## Execution log (paper)

(заповнюється при симуляції)

- [x] Opened at 1.17520 @ 06:50 UTC (double sweep H4 OB, market entry)
- [ ] Moved SL to BE at <price>
- [ ] TP1 hit at <time>
- [ ] TP2 hit at <time> — основна ціль
- [ ] Closed at <price> @ <time> — result <pips>/<USD paper>
- [ ] Kill-switch виконано до 11:25 UTC (якщо TP не досягнуто)

## Lessons (post-trade)

(заповнюється після закриття)
