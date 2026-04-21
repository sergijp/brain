---
title: "Торгові Правила — Ризик, Входи, Виходи"
date: 2026-04-21
tags: [trading, rules, risk-management, exit-rules]
category: trading
status: active
pinecone_indexed: false
---

# 📏 Торгові Правила

## 💰 Рахунок та Ризик

| Параметр | Значення |
|----------|---------|
| Розмір рахунку | **$10,000** |
| Ризик на угоду | **1% = $100** |
| Daily Drawdown limit | **3% = $300** → зупинити торгівлю на день |
| Weekly Drawdown limit | **5% = $500** → переглянути стратегію |
| Мінімальний RR | **1:2** |
| Ідеальний RR | **1:3+** |
| Макс. угод одночасно | **2–3** (не на корельованих парах) |

---

## 📐 Розрахунок Лоту

### EURUSD / GBPUSD / USDCHF / USDCAD
```
Lot = Ризик $ / (Risk pips × $10)
Lot = $100 / (risk_pips × 10)

Приклад: SL = 16 pips → Lot = 100 / (16 × 10) = 0.625 ≈ 0.63
```

### XAUUSD (Gold)
```
Lot = Ризик $ / (Risk pips × $1)
(1 pip Gold = $1 на 0.01 lot = $10 на 0.1 lot)
```

### US100 / US500 (Indices)
```
Lot = Ризик $ / (Risk points × contract_size)
```

---

## ⚡ Правила Входу

### LONG (Buy)
- [ ] Bias на H4/H1 — **bullish** (BOS вгору підтверджений)
- [ ] Ціна ретестує bullish OB або FVG на 15m/5m
- [ ] SSL sweep виконано (стопи під PDL/Asian Low зняті)
- [ ] BOS/ChoCH вгору на 5m або 15m після sweep
- [ ] Вхід: midpoint OB або top of FVG
- [ ] SL: нижче OB/FVG + буфер 2-5 pips

### SHORT (Sell)
- [ ] Bias на H4/H1 — **bearish** (BOS вниз підтверджений)
- [ ] Ціна ретестує bearish OB або FVG на 15m/5m
- [ ] BSL sweep виконано (стопи над PDH/Asian High зняті)
- [ ] BOS/ChoCH вниз на 5m або 15m після sweep
- [ ] Вхід: midpoint OB або bottom of FVG
- [ ] SL: вище OB/FVG + буфер 2-5 pips

### ❌ НЕ входити якщо
- Ціна пробила OB більш ніж на 50% без відновлення
- Вхід проти H4 bias
- За 15 хв до і 30 хв після: NFP, CPI, FOMC, ECB
- Азіатська сесія без ICT Asian Range сетапу

---

## 🎯 Правила Виходу

### Take Profit
| TP | Розмір позиції | Умова |
|----|---------------|-------|
| TP1 | 30–50% закрити | При RR 1:1 → SL у беззбиток |
| TP2 | 50% закрити | Наступний ключовий рівень ліквідності (PDH/PDL, OB, FVG) |
| TP3 | Залишок | HTF ціль або RR 1:3+ |

Якщо немає чіткого рівня → TP3 = RR 1:3

### Stop Loss
- SL: нижче/вище зони входу (OB або FVG) + буфер
- При RR 1:1 → перемістити в **беззбиток** (breakeven)
- Trailing stop після breakeven: слідкувати за структурними min/max на 5m-15m
- **Максимум SL**: не більше 1% від депозиту ($100)

---

## 🔗 Корельовані активи

Не тримати одночасно в **одному напрямку** більш ніж на 1% кожну:

| Корельована пара | Правило |
|-----------------|---------|
| EURUSD + GBPUSD | Не обидві LONG або обидві SHORT |
| EURUSD + USDCHF | Зворотня кореляція — не обидві одночасно |
| US100 + US500 | Обидві разом = подвійний ризик на US market |

---

## 🕐 Торгові сесії (UTC)

| Сесія | Час UTC | Торгувати? |
|-------|---------|-----------|
| Asian | 00:00–07:00 | ❌ Тільки якщо ICT Asian Range сетап |
| London KZ | 07:00–09:00 | ✅ Пріоритет |
| London | 08:00–12:00 | ✅ Основна сесія |
| NY KZ | 12:00–14:00 | ✅ Пріоритет |
| New York | 13:00–17:00 | ✅ |
| After NY | 17:00+ | ❌ |

---

## 📊 Ключові Рівні для моніторингу

| Тип | Рівні |
|-----|-------|
| Daily | PDH, PDL, Previous Day Mid |
| Weekly | PWH, PWL |
| Session | Asian Range High/Low, London Open |
| Structure | HH, HL, LH, LL |

---

## 🔗 Пов'язані нотатки
- [[20-Trading/Strategies/smc-price-action-combo]]
- [[20-Trading/Resources/tradingview-mcp-workflow]]
