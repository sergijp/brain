---
title: "Стратегія: SMC + Price Action Combo (Multi-TF)"
date: 2026-04-21
tags: [trading, strategy, smc, price-action, multi-timeframe]
category: trading
status: active
pinecone_indexed: false
---

# 📊 SMC + Price Action Combo (Multi-TF)

## 🎯 Загальний опис

Top-down аналіз з використанням SMC структури на H4/H1, підтвердженням price action та входом на 15m/5m. Торгівля виключно в зонах інтересу (OB, FVG) після підтвердження через BOS/ChoCH та ліквідаційних свупів.

---

## ⏱️ Таймфрейми

| Рівень | ТФ | Призначення |
|--------|-----|-------------|
| HTF Bias | W / D / H4 | Визначення загального напрямку, ключові зони |
| Entry Context | H1 | Структура, OB та FVG зони, BOS/ChoCH |
| Entry Trigger | 15m / 5m | Liquidity sweep → BOS/ChoCH → вхід |

---

## 🧠 Ключові концепції

### Order Blocks (OB)
Зона де ціна зробила сильний рух. Вхід при ретесті з підтвердженням BOS/ChoCH на LTF.
- **Bullish OB**: Остання ведмежа свічка перед сильним рухом вгору
- **Bearish OB**: Остання бичача свічка перед сильним рухом вниз

### Fair Value Gap (FVG / Imbalance)
Незаповнений гэп між трьома свічками. Магніт для ціни, зона для входу або TP.
- Між High[2] та Low[0] (bullish FVG) або High[0] та Low[2] (bearish FVG)

### BOS / ChoCH
- **BOS** (Break of Structure): Підтвердження продовження тренду
- **ChoCH** (Change of Character): Перший сигнал розвороту → вхід обережно

### Liquidity Sweeps
- **SSL** (Sell-Side Liquidity): Стопи під мінімумами. Sweep = сигнал для LONG
- **BSL** (Buy-Side Liquidity): Стопи над максимумами. Sweep = сигнал для SHORT
- Рівні: PDH, PDL, PWH, PWL, Asian Range High/Low

---

## 📈 Bias Definition

### ✅ Bullish Bias
- H4/H1: структура HH/HL (Higher Highs, Higher Lows)
- Ціна вище ключового H4 OB або FVG
- BOS вгору на H1 підтверджений
- SSL sweep виконано (стопи під PDL/Asian Low зняті)
- NY/London відкриття вище PDH або Asian Range High

### 🔴 Bearish Bias
- H4/H1: структура LH/LL (Lower Highs, Lower Lows)
- Ціна нижче ключового H4 OB або FVG
- BOS вниз на H1 підтверджений
- BSL sweep виконано (стопи над PDH/Asian High зняті)
- NY/London відкриття нижче PDL або Asian Range Low

### ⚪ Neutral (не торгувати)
- Ціна всередині consolidation зони без чіткого BOS
- Немає чіткого HH/HL або LH/LL на H4
- Поза активними торговими сесіями (азіатська без тригера)
- Ціна між рівнями ліквідності без підтвердження напрямку

---

## 📋 Алгоритм аналізу (покрокова інструкція)

```
Крок 1: H4/D — Визначити BIAS
  → Структура HH/HL = Bullish | LH/LL = Bearish | Інше = Neutral (стоп)
  → Де знаходиться ціна відносно ключових OB/FVG?

Крок 2: H1 — Entry Context
  → Знайти ключові OB та FVG зони
  → Підтвердити BOS або ChoCH
  → Де розміщена ліквідність (SSL/BSL)?

Крок 3: 15m/5m — Entry Trigger
  → Чекати Liquidity Sweep (SSL для LONG / BSL для SHORT)
  → Після sweep — BOS/ChoCH у напрямку bias
  → Pullback до OB або FVG на 5m → вхід

Крок 4: Trade Plan
  → Entry: midpoint OB або top/bottom FVG
  → SL: нижче/вище OB/FVG + буфер 2-5 pips
  → TP1: наступний liquidity level (1:1 → breakeven)
  → TP2: PDH/PDL або H1 OB/FVG
  → TP3: HTF ціль або RR 1:3+
```

---

## ⚡ Умови входу LONG

1. Bias на H4/H1 — **bullish**
2. Ціна ретестує bullish OB або заповнює bullish FVG на 15m/5m
3. BOS вгору на 15m або 5m після ретесту
4. **Бажано**: SSL sweep (зніс нижніх стопів / PDL / Asian Low) перед входом
5. Вхід: limit order на midpoint OB або top of FVG, або market при підтвердженому BOS
6. SL: нижче OB / FVG з буфером 2-5 pips

## 📉 Умови входу SHORT

1. Bias на H4/H1 — **bearish**
2. Ціна ретестує bearish OB або заповнює bearish FVG на 15m/5m
3. BOS вниз на 15m або 5m після ретесту
4. **Бажано**: BSL sweep (зніс верхніх стопів / PDH / Asian High) перед входом
5. Вхід: limit order на midpoint OB або bottom of FVG, або market при підтвердженому BOS
6. SL: вище OB / FVG з буфером 2-5 pips

## ❌ Умови інвалідації (не входити)

- Ціна пробила OB більш ніж на 50% без відновлення
- Вхід проти H4 bias
- Вихід важливих новин (NFP, CPI, FOMC, ECB) ±30 хв
- Азіатська сесія без ICT Asian Range сетапу

---

## 🏦 Активи (Watchlist)

| Клас | Інструменти |
|------|-------------|
| Forex Majors | EURUSD, GBPUSD, USDJPY, USDCAD, USDCHF |
| Metals | XAUUSD (Gold), XAGUSD (Silver) |
| Indices | GER40 (DAX), US100 (Nasdaq), US500 (S&P500) |

---

## 🕐 Торгові сесії

| Сесія | UTC | Фокус | Кращі пари |
|-------|-----|-------|-----------|
| London KZ | 07:00–09:00 | Маніпуляція Asian Range, sweep | EURUSD, GBPUSD, XAUUSD |
| London | 08:00–12:00 | Основний тренд дня | EURUSD, GBPUSD, GER40 |
| NY KZ | 12:00–14:00 | Другий рух, реверсал або продовження | EURUSD, XAUUSD, US100 |
| New York | 13:00–17:00 | Тренд NY, US індекси | US100, US500, XAUUSD, USDCAD |

---

## 🔗 Пов'язані нотатки
- [[20-Trading/Resources/trading-rules]]
- [[20-Trading/Resources/tradingview-mcp-workflow]]
