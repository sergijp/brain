---
title: "GER40 — Ретроспектива 2026-04-23"
date: 2026-04-23
tags: [trading, retro, GER40, indices]
category: trading
symbol: GER40
outcome: open
---

# GER40 Retro — 2026-04-23

## План (з Analysis)
- **Side:** Short
- **Entry:** 24212.5 (OTE High)
- **SL:** 24262.5 (50 pts)
- **TP:** 23667.2 (545 pts)
- **Planned RR:** 1:10.9

## Реальні дані (M15, FOREXCOM:GER40)
| Метрика | Значення |
|---|---|
| Day Open | 24027 |
| Day High | **24258.5** |
| Day Low | 23839 |
| Day Close | 24120.5 |
| Entry touched | ✅ 14:45 UTC (17:45 Kyiv) |
| SL hit | ❌ (day_high 24258.5 — **лише 4 pts від SL**!) |
| TP hit | ❌ (day_low 23839 — 171.8 pts над TP) |
| MFE | 373.5 pts (1:7.47R) |
| MAE | 46 pts (з 50 — дуже близько до SL) |
| Outcome | **OPEN** — великий рух в потрібну сторону, TP не взятий |

## Що пішло добре
- Entry спрацював, напрямок правильний (373.5 pts руху вниз).
- TP нереалізований, але MFE 1:7.47 = потенційно виграшний день.

## Що пішло погано 🔴
- **MAE 46 pts з SL 50 pts** — трейд пройшов на 92% до SL! Дуже небезпечно.
- **TP занадто амбіційний** (−545 pts при day range 419 pts). ATR-adjusted TP мав би бути ~−400.
- Не було стратегії "move SL to BE" після MFE > 2R.

## Урок
> **Правило (критичне)**: після MFE ≥ 2R **обов'язково** рухати SL на breakeven. У цьому трейді MFE досяг 7.47R — BE давно мав би бути поставлений.
>
> **Правило для indices**: SL повинен бути в межах 0.3 × daily range. 50 pts для GER40 (range 400+) — on the edge.

[[_DAILY-RETRO|← До Daily Retro]] · [[../../Analysis/2026-04-23/GER40-analysis|План оригіналу]]
