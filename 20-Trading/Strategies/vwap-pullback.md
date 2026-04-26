---
title: "VWAP Pullback — Institutional Intraday"
date: 2026-04-22
tags: [trading, strategy, vwap, intraday, institutional, indices, gold]
category: trading
status: draft
journal_tag: vwap
pinecone_indexed: false
---

# 📊 VWAP Pullback — Institutional Intraday

**Філософія:** VWAP (Volume-Weighted Average Price) — benchmark, за яким працюють інституціональні desks. Великі ордери виконуються "at VWAP" або краще. Pullback до session-VWAP у trending day = high-probability re-entry у напрямку інституційного флоу. Не-SMC лінза, ортогональна до твоїх playbook'ів.

**Незалежна стратегія.** Self-contained risk/gates/journal.

**Style:** intraday trend-pullback | **Min RR:** 1:2 (hard gate) | **EOD:** close 21:00 UTC

---

## 🎯 Ідея
- **Session VWAP** ресетиться на початку London / NY
- Якщо ціна торгується **над VWAP** всю сесію = bullish institutional pressure
- Кожен pullback до VWAP (або 1σ band) = entry opportunity у напрямку тренду
- Ранjging days (ціна cross VWAP > 4 разів) — skip

---

## ⏱️ Робочі таймфрейми
- **Context TF:** 15m (ADX/trend filter)
- **Entry TF:** 5m
- **Trigger TF:** 1m (reaction candle на VWAP touch)
- **VWAP anchor:** session open (London 08:00 UTC / NY 13:30 UTC)
- **Bands:** ±1σ, ±2σ (deviation bands на основі intraday volume-weighted stddev)

---

## 📐 Алгоритм LONG (дзеркально для SHORT)

### Крок 1 — визначити trend-day (filter)
1. Відкрити 5m chart з VWAP + σ bands
2. На 15m:
   - **ADX(14) ≥ 20** (trend present)
   - **Ціна над VWAP > 70% часу** у перші 60-90 хв сесії
   - Менше **3 cross** VWAP за першу годину
3. Якщо все TRUE → bullish trend-day → дозволено лонги при pullback

### Крок 2 — pullback-zone
4. Чекаємо pullback до одного з рівнів:
   - **Primary:** session VWAP line
   - **Secondary:** −1σ band (якщо VWAP далеко)
5. Skip якщо ціна пробиває −2σ (можливий trend reversal)

### Крок 3 — reaction trigger
6. На 1m: bullish rejection candle на VWAP (pin / hammer / engulfing)
7. **Volume confirmation:** reaction-candle volume > попередньої спадаючої свічки
8. **Entry:** buy market на close reaction candle

### Крок 4 — SL / TP
- **SL:** −2σ band OR low reaction candle − 0.2×ATR(14, 5m) (беремо більший)
- **TP1 (40%):** HOD (High of Day) поточної сесії → move SL to BE
- **TP2 (40%):** +2σ band (extension до opposite volatility edge)
- **TP3 (20%):** HTF рівень (H4 swing high / PDH)

---

## 🚦 Entry Gates

| # | Умова | Причина skip |
|---|-------|--------------|
| G1 | ADX(14) 15m < 18 | Ranging day — VWAP pullback не валідний |
| G2 | Ціна crossed VWAP > 3 рази у першу годину | Chop, не trend |
| G3 | High-impact news ±15 хв | Volatility spike долбає VWAP |
| G4 | Pullback пробиває −2σ (для longs) | Можливий trend reversal |
| G5 | Reaction candle без volume bump | Слабка відповідь, фейк |
| G6 | EOD ≤ 60 хв (після 20:00 UTC) | Недостатньо часу на TP2 |

---

## 📊 Scoring (0-10)

| Фактор | Бали |
|--------|------|
| ADX(14) 15m ≥ 25 (strong trend) | +2 |
| Pullback до VWAP (не до −1σ) | +2 |
| Reaction candle = engulfing на 1m | +2 |
| HTF bias (H1) aligned | +2 |
| Volume reaction > 1.5× prev | +1 |
| Pullback не пробиває prev swing low | +1 |
| Confluence з institutional level (PDH/L, H1 OB, round number) | +1 |

**Гейти:** ≥7 full / 5-6 half / <5 skip.

---

## 🛡️ Risk

- **Ризик/угоду:** 1% = $100 на $10k
- **Daily DD cap:** 2%
- **Max open positions:** 1 одночасно
- **Correlation cap:** не торгувати VWAP на US100 + US500 одночасно

### Формула лоту:
```
Lot = $100 / (SL_points × $value_per_point)
XAUUSD: $10/pip (1 lot), US100: $2/point (1 mini), US500: $5/point (1 mini)
```

---

## 🎯 Приклад (XAUUSD, NY session)

Припустимо NY open 13:30 UTC, XAUUSD торгується над VWAP 75% часу:
- 14:20 — VWAP 2385.20, ціна 2389.50, ADX 15m = 27 (strong trend)
- 14:35 — pullback до 2385.40 (VWAP touch)
- 14:37 — 1m bullish engulfing, volume 1.8× prev
- **Entry:** 2386.20 | **SL:** 2383.50 (−2σ + buffer) | **TP1:** 2391.00 (HOD) | **TP2:** 2394.30 (+2σ) | **TP3:** 2398.80 (H4 level)
- Lot: 0.37 ($100 / (27 × $10))

---

## 🚫 Коли НЕ торгувати

- **FOMC / NFP / ECB** — VWAP розривається news-driven spike'ом
- **Перші 15 хв** після сесії (VWAP ще не сформована)
- **Thin Fridays** після 18:00 UTC (liquidity drop)
- Дні з gap open > 0.5% (VWAP calculation distorted)
- Crypto-style sessions (24/7 pairs без clear session anchor) — пропустити

---

## 🏷️ Journal tag
```yaml
ts: vwap
session: london | ny
pullback_level: vwap | minus_1_sigma
direction: long | short
```

---

## 📌 Status
⚪ **Draft** — створено 2026-04-22. Потребує Pine-бектесту (session VWAP + bands, 2 роки, indices + gold).

---

## 🔗
- [[20-Trading/Strategies/orb-opening-range-breakout]] — комплементарна breakout
- [[20-Trading/Strategies/ts-tracker]]
- [[20-Trading/Backtest/README]]
