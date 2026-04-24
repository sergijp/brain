---
title: "US500 — Ретроспектива 2026-04-23"
date: 2026-04-23
tags: [trading, retro, US500, indices, loss]
category: trading
symbol: US500
outcome: sl_hit
---

# US500 Retro — 2026-04-23

## План (з Analysis)
- **Side:** Long
- **Entry:** 7097.9 (OTE Low)
- **SL:** 7087.9 (**10 pts — tight**)
- **TP:** 7147.9 (50 pts)
- **Planned RR:** 1:5.0

## Реальні дані (M15, FOREXCOM:SPX500)
| Метрика | Значення |
|---|---|
| Day Open | 7110.98 |
| Day High | **7147.28** (всього 0.62 pt нижче TP!) |
| Day Low | 7046.58 |
| Day Close | 7116.03 |
| Entry touched | ✅ 02:15 UTC (05:15 Kyiv, Asia) |
| SL hit | ✅ **03:30 UTC** (той же бар, 01:15 после entry) |
| TP hit | ❌ (**day_high 7147.28 — всього 0.62 pt нижче TP!**) |
| MFE before SL | 10.08 pts (1:1.01R) |
| MAE (after SL) | 13.55 pts (1:1.36R beyond stop) |
| Outcome | **SL_HIT → −1.0R** (classic stop-hunt перед TP-move) |

## Що пішло добре
- Напрямок 100% правильний — ціна через 5 годин дійшла до 7147.28 (−0.62 pt до TP).
- OTE Low логіка спрацювала б без tight SL.

## Що пішло погано 🔴🔴🔴
- **SL занадто тугий (10 pts)** — swept normal M15 noise. За ~5 годин ціна збілотилась stop-hunt'ом і потім пішла до 7147.
- **Класичний Judas Swing pattern** не був врахований: після entry Asia session часто робить stop hunt перед London move.
- Якби SL був **15 pts (до 7082.9)** — trade би вижив і взяв TP.

## Урок (головний day lesson)
> **Правило (критичне)**: SL для indices на M15 entry мінімум **1.5 × M5 ATR** (зазвичай ~15-20 pts для US500). 10 pts — це noise range.
>
> **Правило Judas Swing**: якщо entry в Asia session — додавати buffer **5-10 pts** до SL (beyond Asia range low/high).
>
> **Крос-зв'язок з US100**: той самий day, US100 взяв TP бо SL був 43.8 pts (аж 4× більше відносно volatility). US500 з 10 pts **не мав шансів**.

## Найболючіший втрачений профіт
~50 pts × 1R = **4R потенціальний gain**, отримали −1R. Net impact: **−5R**.

[[_DAILY-RETRO|← До Daily Retro]] · [[../../Analysis/2026-04-23/US500-analysis|План оригіналу]]
