---
title: "MR BB+RSI — Mean Reversion Ranging"
date: 2026-04-22
tags: [trading, strategy, mean-reversion, bollinger-bands, rsi, ranging, counter-trend]
category: trading
status: draft
journal_tag: mr-bb-rsi
pinecone_indexed: false
---

# 📊 MR BB+RSI — Mean Reversion у ranging market

**Філософія:** коли ринок **не тренує** (ADX низький, структура horizontal), extreme touches Bollinger Bands + momentum divergence (RSI) дають high-probability reversion до середньої. Класичний counter-trend approach. Закриває діру твоїх SMC-playbook'ів, які потребують clear BOS і страждають у флеті.

**Незалежна стратегія.** Self-contained (власні risk/gates/journal). **Anti-correlated** зі SMC — використовується коли SMC skip'ає через no-trend.

**Style:** counter-trend ranging | **Min RR:** 1:2 (hard gate) | **Hold:** до BB mid (TP1) або opposite band (TP2)

---

## 🎯 Ідея
- **Ranging filter:** ADX(14) < 20 + H4 structure без BOS останні 10 свічок
- Ціна торкається **BB(20, 2σ)** upper або lower band — extreme deviation
- **RSI divergence** підтверджує виснаження momentum (price HH + RSI LH для short; price LL + RSI HL для long)
- Вхід проти руху → TP на BB middle (SMA20) → runner на opposite band

---

## ⏱️ Робочі таймфрейми
- **Context TF:** H4 (ranging confirmation, ADX, structure)
- **Entry TF:** **H1** (BB + RSI signal)
- **Trigger TF:** 15m (reversal candle close)

---

## 📐 Алгоритм LONG (дзеркально для SHORT)

### Крок 1 — ranging filter (H4 + H1)
1. **H4 ADX(14) < 20** — no trend
2. **H4 структура:** без BOS останні 10 свічок (ціна osc у каналі)
3. **H1 ADX(14) < 22** — confirmation ranging locally
4. Якщо BOS на H4 → **SKIP** (тренд почався, MR не валідний)

### Крок 2 — extreme touch
5. H1 ціна торкається **BB(20, 2σ) lower band** (для LONG)
6. **RSI(14) ≤ 30** (oversold)

### Крок 3 — bullish divergence
7. Останні 2 price lows на H1 роблять **LL** (lower low)
8. Останні 2 RSI lows роблять **HL** (higher low) — divergence ✅
9. Якщо no-divergence → skip (може бути trend continuation)

### Крок 4 — reversal trigger (15m)
10. **15m close inside BB** (повертається з extreme)
11. Bullish pin bar / engulfing / hammer на 15m
12. **Entry:** buy market на close 15m trigger candle

### Крок 5 — SL / TP
- **SL:** BB lower band − 0.3×ATR(14, H1) buffer
- **TP1 (50%):** **BB middle (SMA20)** → move SL to BE
- **TP2 (40%):** **BB upper band** (opposite extreme) — most reversions stop here
- **TP3 (10%):** H4 swing high як runner

---

## 🚦 Entry Gates (строгі — MR дорого купується помилками)

| # | Умова | Причина skip |
|---|-------|--------------|
| G1 | H4 ADX(14) ≥ 20 | Trending market — не MR |
| G2 | H4 BOS останні 10 свічок | Тренд почався, skip |
| G3 | High-impact news ±60 хв (FOMC/NFP/ECB/CPI) | News breaks MR logic |
| G4 | No RSI divergence | Трендова oversold → продовження падіння |
| G5 | 15m тригер не закривається inside BB | Break-out, не reversion |
| G6 | Пара у watchlist avoid-list (див. нижче) | Pair-specific low MR success |

---

## 🎯 Пари (critical — MR працює не на всіх)

**✅ High-probability (primary):**
- **EURUSD** — найбільш ranging серед мажорів
- **USDCHF** — low volatility, часто flat
- **USDCAD** — oil-correlated range

**⚠️ Medium (secondary, strict gates only):**
- EURGBP (не у твоєму watchlist але добре пасує MR)

**❌ AVOID (high-vol, trending):**
- **GBPUSD** — випадкові spike moves розривають MR
- **USDJPY** — persistent trending, BOJ interventions
- **XAUUSD, XAGUSD** — sentiment-driven, занадто волатильні
- **US100, US500, GER40** — persistent trends, news-sensitive

---

## 📊 Scoring (0-10)

| Фактор | Бали |
|--------|------|
| H4 ADX < 15 (strong ranging) | +2 |
| RSI divergence: clean 2-leg divergence | +2 |
| Price у BB extreme зі wick (не з body) | +2 |
| H4 range тривалий (≥ 20 свічок sideways) | +2 |
| 15m reversal candle = engulfing/hammer | +1 |
| Confluence з H4 horizontal S/R | +1 |

**Гейти:** ≥7 full / 5-6 half / <5 skip.

---

## 🛡️ Risk

- **Ризик/угоду:** 1% = $100 на $10k (строго — MR дає багато stop-outs при trend початку)
- **Max open positions:** 2 одночасно на різних парах
- **Correlation cap:** EURUSD + USDCHF = counted як 1 (negative correlation, але USD-driven)
- **Daily DD cap:** 2%
- **Weekly retire rule:** 3 stop-outs поспіль на одній парі → **skip the pair for 2 weeks** (trend ймовірно почався)

### Формула лоту (FX):
```
Lot = $100 / (SL_pips × $10)
```

---

## 🎯 Приклад (EURUSD, H1 ranging session)

H4 EURUSD:
- ADX(14) = 14, structure osc 1.0750-1.0830 last 25 свічок
- H1: ціна touch BB(20,2) lower band @ 1.0748
- RSI(14) = 28 (oversold)
- H1 last 2 lows: 1.0760 → 1.0748 (LL)
- RSI last 2 lows: 25 → 28 (HL) → **divergence ✅**
- 15m: bullish engulfing close 1.0762 (inside BB)
- **Entry:** 1.0762 | **SL:** 1.0740 (BB lower − 0.3×ATR buffer) = 22 pips | **TP1:** 1.0790 (BB mid — BE) | **TP2:** 1.0820 (BB upper) | **TP3:** 1.0835 (H4 high)
- Lot: 0.45 ($100 / (22 × $10))
- RR TP2: 58/22 ≈ 1:2.6 ✅

---

## 🚫 Коли НЕ торгувати

- **News week** (FOMC / NFP / ECB / CPI ±24h)
- **Asian session only** (часто thin, fake spikes до bands)
- **Friday 15:00+ UTC** (position squaring, BB extremes неповерхневі)
- **Post-BOS H4** (тренд почався — BB експанде, MR ловить losing knife)
- Pair-specific avoid (див. вище)

---

## 🔄 Інтеграція з рештою стратегій

- Коли SMC/NS skip'ають через no-trend → MR активується
- **НЕ** торгувати MR + SMC одночасно на одній парі (конфлікт напрямків)
- MR як "defensive income" у тижні коли trending стратегії у drawdown

---

## 🏷️ Journal tag
```yaml
ts: mr-bb-rsi
pair_category: primary | secondary
divergence_quality: clean | weak
direction: long | short
```

---

## 📌 Status
⚪ **Draft** — створено 2026-04-22. Потребує Pine-бектесту (BB + RSI + ADX filter, 2 роки, EURUSD/USDCHF/USDCAD H1).

---

## 🔗
- [[20-Trading/Strategies/ts-tracker]]
- [[20-Trading/Strategies/orb-opening-range-breakout]]
- [[20-Trading/Strategies/vwap-pullback]]
- [[20-Trading/Backtest/README]]
