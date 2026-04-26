---
title: "USDCHF — Ретроспектива 2026-04-24"
date: 2026-04-24
tags: [trading, retro, USDCHF, forex, invalid-plan]
category: trading
symbol: USDCHF
outcome: invalid_plan
---

# USDCHF Retro — 2026-04-24

## План
- **Side:** Long
- **Entry Zone:** 0.8845 - 0.8860 ❌
- **SL:** 0.8830
- **TP:** 0.8950

## Реальні дані (M15, OANDA)
| Метрика | Значення |
|---|---|
| Day Open | 0.78626 |
| Day High | 0.78766 (11:00 UTC) |
| Day Low | 0.78458 (15:45 UTC) |
| Day Close | 0.78498 |

## ⚠️ НЕВАЛІДНИЙ ПЛАН
**Entry zone 0.8845-0.8860 знаходиться на ~10000 pips ВИЩЕ за реальну ціну (0.7846-0.7877).**

План базувався на застарілій або помилковій ціновій шкалі. Ціна жодного разу не торгувалась поблизу зазначених рівнів за весь день. Угода фізично неможлива.

## Урок
> **Правило**: ПЕРЕД написанням плану — перевірити поточну ціну через `quote_get` або `chart_get_state`. Якщо аналіз робиться на основі screenshots, переконатися що Y-вісь (price scale) не обрізана/зміщена. Помилка масштабу робить весь top-down аналіз фікцією.

> **Системне зауваження**: Аналогічна помилка масштабу зустрічається у USDCHF, XAGUSD, US500 на 2026-04-24. Це сигнал що template/copy-paste workflow генерує плани без перевірки реальної ціни. **Додати в pre-flight checklist**: `if abs(entry_zone − current_price) > 5% × current_price → ABORT plan`.

[[_DAILY-RETRO|← До Daily Retro]] · [[../../Analysis/2026-04-24/USDCHF-analysis|План оригіналу]]
