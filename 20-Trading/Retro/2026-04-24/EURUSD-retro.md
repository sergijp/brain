---
title: "EURUSD — Ретроспектива 2026-04-24"
date: 2026-04-24
tags: [trading, retro, EURUSD, forex]
category: trading
symbol: EURUSD
outcome: sl_hit
---

# EURUSD Retro — 2026-04-24

## План (з Analysis)
- **Side:** Short (Bearish bias на W/D/H4)
- **Entry Zone:** 1.1688 - 1.1698
- **SL:** 1.1712
- **TP:** 1.1655
- **Planned RR:** 1:2.5 (від entry_lo)

## Реальні дані (M15, OANDA)
| Метрика | Значення |
|---|---|
| Day Open | 1.16836 |
| Day High | 1.17236 (20:45 UTC) |
| Day Low | 1.16729 (07:30 UTC) |
| Day Close | 1.17186 |
| Entry touched | ✅ 02:45 UTC (high 1.16888) |
| MFE post-entry | 15.1 pips → **0.63R** (low 1.16729 о 07:30 UTC) |
| SL hit | ✅ 14:00 UTC (bar high 1.17124) |
| TP hit | ❌ (low 1.16729 vs TP 1.1655 → 7.9 pips коротко) |
| Outcome | **SL_HIT** |
| Net | **−1.00R** |

## Що пішло погано
- **Bias помилковий**: H4/D вказували на ведмежий тренд, але день закрився вище open на +35 pips. Структура зламана була тимчасово.
- **TP майже досяг, потім реверс**: low 1.16729 — лише 8 pips до TP 1.1655. Класичний "near miss" з подальшим розворотом.
- **Без BE rule після MFE**: при MFE 0.63R, BE правило (≥2R) не спрацювало б. Але staircase TP1 1:1 (≈12 pips → 1.16770) — взяв би +1R перед розворотом.

## Що пішло добре
- Entry depth ОК (MAE незначний на момент тригеру).
- Структура SMC дала тригер у потрібну сторону короткостроково.

## Урок
> **Правило**: при виявленні sweep на H1 (як 1.16729 о 07:30) переводити частину позиції (50%) на BE або фіксувати TP1 = 0.5×TP_target. Не чекати TP2/TP3 коли ціна відскочила від TP більше ніж 50% риску.

[[_DAILY-RETRO|← До Daily Retro]] · [[../../Analysis/2026-04-24/EURUSD-analysis|План оригіналу]]
