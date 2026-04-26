---
title: "GER40 — Ретроспектива 2026-04-24"
date: 2026-04-24
tags: [trading, retro, GER40, DAX, indices]
category: trading
symbol: GER40
outcome: sl_hit_after_huge_mfe
---

# GER40 Retro — 2026-04-24

## План
- **Side:** Short
- **Entry Zone:** 24120 - 24135
- **SL:** 24160
- **TP:** 23850
- **Planned RR:** 1:11

## Реальні дані (M15, FOREXCOM)
| Метрика | Значення |
|---|---|
| Day Open | 24200.7 |
| Day High | 24336.5 (14:30 UTC) |
| Day Low | 23990.5 (12:15 UTC) |
| Day Close | 24262.5 |
| Entry touched | ✅ 02:00 UTC (low 24123.5) |
| MFE post-entry | 144.5 pts → **5.78R** (low 23990.5 о 12:15 UTC) |
| TP hit | ❌ (low 23990.5 vs TP 23850 — 140 pts коротко) |
| SL hit | ✅ 14:00 UTC (high 24246) |
| Outcome | **SL_HIT** після MFE 5.78R |
| Net (без BE rule) | **−1.00R** |
| Net (з BE rule після MFE 2R) | **0R** |

## Найдорожчий урок дня — повторення помилки 04-23 GER40
> Це **другий день поспіль** коли GER40 показав MFE 5R+ і потім розворот без BE. На 04-23 MFE був 7.47R, на 04-24 — 5.78R. Без BE rule **обидва дні втрачено величезний нереалізований прибуток**.

## Що пішло погано
- **TP зашироко**: 23850 — це 1:11 RR. Day low 23990.5 було глибокою ціллю, але навіть її не досяг.
- **Без partial TP**: при MFE 5R можна було взяти 50% на 1:3, перевести решту на BE → ~2.5R фіксовано.
- **NY reversal**: 14:00 UTC новини США перевернули ринок — типовий sweep + reversal.

## Що пішло добре
- Entry depth відмінний (low 24123.5 на тригері = ідеальне місце).
- Bias Short був вірним для першої половини дня.

## Урок
> **Правило (КРИТИЧНЕ — повторне)**: При MFE ≥ 2R на indices → SL ОБОВ'ЯЗКОВО на BE. При MFE ≥ 4R → fix 50% позиції. **Це правило було сформульовано в retro 04-23, але знов не застосовано на 04-24**. Потрібен **alert на TradingView** на рівень 1:2 від entry.

> **Правило**: TP ≤ 0.7 × Daily ATR. На 04-24 GER40 daily range = 346 pts; TP 350 pts вниз = 100% range = практично нереалістично. Staircase TP1 = 1:2 (50 pts) обов'язковий.

[[_DAILY-RETRO|← До Daily Retro]] · [[../../Analysis/2026-04-24/GER40-analysis|План оригіналу]]
