---
title: USDJPY Top-Down Analysis
date: 2026-05-25
tags: [USDJPY, TDA, bullish-corrective, forex]
category: Analysis
project: Trading
status: analysis-complete
pair: USDJPY
agent: analyst
pinecone_indexed: false
---

# USDJPY: Top-Down Analysis — 25.05.2026

> Час аналізу: 06:15 UTC / 09:15 Kyiv. London KZ активна (літо 06:00-08:00 UTC).
> Поточна ціна: **159.034**.

## 🏛 Weekly (Тижневий графік)

W: **-1.10%** від 160.786. Останні 5W closes: `157.088 → 156.686 → 158.776 → 159.206 → 159.010` — серія HL після pullback з ATH 161.95 до W low 155.03. Тиждень тримається над key support 155-156. **HTF Bias: Bullish-Corrective** — структура bull з повільним recovery, але price ще під ключовим W swing high 161.95.

15W range: `139.579 – 161.950`. Bias-confirming context: довгий W bullish leg з Q3 2025.

## 📅 Daily (Денний графік)

20D **+1.69%**, range `152.09 – 160.726`. Останні 5D closes: `159.080 → 158.934 → 158.990 → 159.206 → 159.012` — tight consolidation під D resistance 159.35. Серія HH/HL від кінця квітня тримається.

**Daily POI:**
- Resistance: **159.347** (D swing high), далі **160.726** (D ATH останніх 20 барів).
- Support: **158.59** (D demand), далі **157.09** (PWL/W swing).

**Daily bias: Bullish-Corrective** — ціна в top консолідації, готується до breakout або відштовху від 159.35.

## ⏱ 4-Hour (4-годинний графік)

H4 range `155.032 – 159.347`, **+1.56%** за тиждень. Останні 5×4H closes: `159.176 → 159.206 → 158.900 → 158.863 → 159.016` — BOS UP з 156.5 (W low recovery), зараз pullback на нижню межу bullish leg + recovery.

**H4 структура: BOS UP confirmed.** H4 OB ~158.5-158.8 — поточна demand зона активно тестується.

## 🕐 1-Hour (1-годинний графік)

H1 діапазон останніх 12H: `158.588 – 159.347`, поточно 159.034 (recovery з 158.836). Останні 5H closes: `158.886 → 158.863 → 158.926 → 158.907 → 159.034`.

**H1 структура:** sweep equal-lows @ 158.83-158.85 → bullish reaction → recovery на +20 pts. Формується HL над H4 demand → потенціал bull continuation.

**SMT vs DXY:** не перевірено через паралельний tab-конфлікт зі сканером — припущення нейтрально-бичача DXY. ⚠️ Перед входом перевірити DXY: якщо DXY теж робить HL/BOS — confluence підтверджено.

## 🎯 15-Minute (15-хвилинний графік)

M15 діапазон сесії: `158.759 – 159.234`. Останні 5×M15: `158.916 → 158.927 → 158.907 → 158.990 → 159.023` — recovery з sweep low 158.759 (Asian/London transition liquidity).

**Сценарії:**
1. **Консервативно (LONG):** дочекатися M15 close > 159.040 (BOS UP) + retest 158.90-158.95 → entry @ retest до **TP 159.20 / 159.35**.
2. **Агресивно:** breakout 159.05 → market entry, SL < 158.76, target 159.35.

## ⚡ 5-Minute (5-хвилинний графік) — Торговий план

M5 range `158.759 – 159.038`, recovery 26 pts з sweep low. М5 short-term BOS UP.

- **Bias:** Bullish (long, continuation після sweep) 📈
- **Entry Zone:** `158.85 – 158.95` (M15 OB retest після M15 BOS UP)
- **Stop Loss:** `158.70` (нижче sweep low 158.759) — **~20 pts** від entry midpoint
- **TP1:** `159.20` — RR ~1.5
- **TP2:** `159.347` (D/H4 swing high) — RR ~2.5
- **TP3:** `159.55` (round number + extension) — RR ~4.0
- **Lot Size:** `$100 / (20 pts × ~$0.94/pt на 0.1 lot) ≈ 0.5 lot` (USDJPY: 1 pip ≈ $9.43 на 1 lot @ 159.0 — **перевірити OANDA**)

---

## Setup Summary

| Параметр | Значення |
|----------|----------|
| Setup type | Sweep + M15 BOS retest (PRIMARY pattern, smc-price-action-combo) |
| Setup score | **7/10** |
| Trigger watch | M15 close > 159.040, потім retest 158.90 зони |
| Best window | London KZ (зараз активна) + NY KZ (12:00-14:00 UTC) |
| Risk | $100 (1% від $10 000) |
| Min RR (TP2) | 2.5 ✅ |

## Pros / Cons

**+** W/D/H4 узгоджений bullish-corrective, BOS UP на H4 свіжий
**+** Sweep low + recovery + М5 BOS видно
**+** Сесія активна (London KZ)
**+** RR 2.5 на TP2 проходить мін поріг

**−** Trigger ще не спрацював (потрібен M15 close > 159.040)
**−** TP3 159.55 близько до D resistance 159.35 — stretched
**−** SMT vs DXY не верифіковано через tab-конфлікт зі сканером

## News / Risks

- ⚠️ Перевірити ForexFactory на JPY/USD high-impact події в межах ±60 хв до планованого entry (через `news-watcher`).
- ⚠️ BOJ rhetoric завжди може створити gap risk на USDJPY — особливо в Tokyo сесії.
- ⚠️ Інтрадей-правило: позиція має бути закрита до кінця дня. TP3 досяжний у London-NY вікні.

## Wiki-links

- [[Strategies/smc-price-action-combo]]
- [[Strategies/ts-1-reversal-at-poi]] (альтернатива при reversal-сценарії)
