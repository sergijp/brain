---
title: "ORB — Opening Range Breakout"
date: 2026-04-22
tags: [trading, strategy, orb, breakout, intraday, indices, toby-crabel]
category: trading
status: draft
journal_tag: orb
pinecone_indexed: false
---

# 📊 ORB — Opening Range Breakout

**Філософія:** systematic intraday-breakout. Перші 15m або 30m сесії формують **Opening Range (OR)**. Пробій OR за обсягом = тригер continuation руху у напрямку пробою. Популяризована Toby Crabel, Rob Booker, Lancelot Burton. Ядро багатьох institutional intraday-моделей для US indices.

**Незалежна стратегія.** Self-contained (власні risk/gates/journal). НЕ наслідує SMC-playbook.

**Style:** intraday breakout | **Min RR:** 1:2 (hard gate) | **EOD:** close 21:00 UTC

---

## 🎯 Ідея
- Інституціонали відкривають позиції у першу годину сесії
- High/Low першого 15m або 30m = "tested pressure points"
- Коли ціна пробиває OR за обсягом + утримується на retest → розширення руху до 2×OR і далі до HTF level
- Най-чисто працює на **indices** (US100, US500, GER40) через clustered institutional flow на open; gold — secondary

---

## ⏱️ Робочі таймфрейми
- **OR window:** перші **15m** (aggressive) або **30m** (conservative)
- **Entry TF:** 5m
- **Trigger TF:** 1m (для precision retest entry)
- **Sessions:**
  - London open: **08:00–08:15/30 UTC** (GER40, EURUSD)
  - NY open: **13:30–13:45/14:00 UTC** (US100, US500, XAUUSD)

---

## 📐 Алгоритм LONG (дзеркально для SHORT)

### Крок 1 — зафіксувати OR
1. На старті сесії (08:00 UTC London / 13:30 UTC NY) починається OR-вікно
2. Після 15m (або 30m) зафіксувати:
   - **OR High** = найвища ціна вікна
   - **OR Low** = найнижча ціна вікна
   - **OR Range** = OR High − OR Low
3. Намалювати 2 горизонтальні лінії + box

### Крок 2 — breakout-сигнал
4. 5m close **вище OR High** → потенційний LONG
5. Volume поточної breakout-свічки > 1.5× середній volume OR-вікна (для indices; для FX — tick-volume)
6. **Filter:** ATR(14) на 15m ≥ 50% середнього ATR за останні 10 днів (не торгувати у dead market)

### Крок 3 — retest entry
7. Чекаємо pullback до OR High (або до VWAP, якщо вона близько)
8. На 1m: bullish engulfing / pin bar / hammer на retest
9. **Entry:** buy market на close тригер-свічки

### Крок 4 — SL / TP
- **SL:** OR Low − 0.2×ATR(14, 5m) buffer
- **TP1 (50%):** OR High + 1×OR Range (RR ≈ 1:1) → **move SL to BE**
- **TP2 (30%):** OR High + 2×OR Range (RR ≈ 1:2)
- **TP3 (20%):** next HTF level (PDH / H4 swing high / daily pivot R1)

---

## 🚦 Entry Gates (hard-skip умови)

| # | Умова | Причина skip |
|---|-------|--------------|
| G1 | Pre-market gap > 0.5% (indices) | Gap-driven день, ORB менш ефективний |
| G2 | Holiday / half-day session | Low liquidity, false breakouts |
| G3 | High-impact news у ±15 хв від breakout | Volatility spike не respects OR |
| G4 | OR Range < 0.3×ATR(14, H1) | Занадто тісний OR → false signal domain |
| G5 | OR Range > 1.5×ATR(14, H1) | Вже exhausted move, continuation малоімовірне |
| G6 | Breakout без volume confirmation | Слабкий імпульс = fake breakout |

---

## 📊 Scoring (0-10)

| Фактор | Бали |
|--------|------|
| Breakout close ≥ 1.5× OR Range beyond OR | +2 |
| Volume ≥ 2× OR-window average | +2 |
| HTF bias (H1/H4) аligned з напрямком | +2 |
| Retest провалився (miss) — direct chase NO | −3 |
| OR Range у "goldilocks" zone (0.5-1.0×ATR H1) | +1 |
| Breakout у перші 30 хв після OR close | +2 |
| EMA(20) на 5m aligned з breakout direction | +1 |

**Гейти:** ≥7 full size / 5-6 half size / <5 skip.

---

## 🛡️ Risk

- **Ризик/угоду:** 1% = $100 на $10k
- **Daily DD cap:** 2% ($200) → stop trading for the day
- **Max open positions:** 1 одночасно
- **Correlation cap:** не торгувати ORB на US100 + US500 в один день (95%+ correlation)

### Формула лоту (indices, approx):
```
Lot = $100 / (SL_points × $value_per_point)
US500: $5/point (mini), US100: $2/point, GER40: ~€1/point
```

---

## 🎯 Приклад (US500, NY open)

Припустимо NY open 13:30 UTC:
- OR (13:30–13:45): High 4523.50, Low 4519.20 → OR Range 4.3 pts
- 13:52 — 5m close 4526.10 (> OR High), volume 1.8× avg
- 13:58 — pullback до 4523.80 (retest OR High), 1m bullish engulfing
- **Entry:** 4524.00 | **SL:** 4518.80 | **TP1:** 4528.30 (BE) | **TP2:** 4532.60 | **TP3:** 4541.00 (PDH)
- Lot: 3.8 mini ($100 / (5.2 × $5))

---

## 🚫 Коли НЕ торгувати

- **FOMC / NFP / CPI** day (волатильність поглинає OR)
- **FX ORB** під час American session без London participation (quiet period 17-20 UTC)
- **Gold ORB** у п'ятницю після 14:00 UTC (thin liquidity)
- Два підряд breakout failures у одній сесії → зупинка до наступної сесії

---

## 🏷️ Journal tag
```yaml
ts: orb
session: london | ny
or_window: 15m | 30m
direction: long | short
```

---

## 📌 Status
⚪ **Draft** — створено 2026-04-22. Потребує Pine-бектесту на US100/US500/GER40 (2 роки, H4+5m, realistic costs).

---

## 🔗
- [[20-Trading/Strategies/ts-tracker]]
- [[20-Trading/Strategies/vwap-pullback]] — комплементарна intraday
- [[20-Trading/Backtest/README]]
