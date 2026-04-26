---
title: "Daily Retro — 2026-04-24"
date: 2026-04-24
tags: [trading, retro, daily, summary]
category: trading
type: daily_retro
instruments: [EURUSD, GBPUSD, USDJPY, USDCAD, USDCHF, XAUUSD, XAGUSD, GER40, US100, US500]
---

# Daily Retro — 2026-04-24

> **Мета**: оцінити виконання 10 top-down планів за реальними M15 OHLC (OANDA/FOREXCOM) через TradingView MCP. Порівняти прогноз vs ринкову поведінку. День стався **протилежним** до 04-23 — USD послабився, ризик-активи виросли, метали зробили reversal.

---

## 1. Підсумкова таблиця

| # | Ticker | Side | Plan | Entry | Outcome | MFE | Net |
|---|--------|------|-----|-------|---------|------|-----|
| 1 | EURUSD | Short | ✅ valid | ✅ 02:45 | **SL_HIT** 14:00 | 0.63R | **−1.0R** |
| 2 | GBPUSD | Short | ✅ valid | ✅ 10:00 | **SL_HIT** 14:00 | 0.55R | **−1.0R** |
| 3 | USDJPY | Long  | ✅ valid | ✅ 14:00 | OPEN −0.6R | 0.62R | ~−0.6R unr. |
| 4 | USDCAD | Long  | ✅ valid | ✅ 14:00 | OPEN −0.2R | 0.39R | ~−0.2R unr. |
| 5 | USDCHF | Long  | ❌ INVALID (scale) | — | — | — | — |
| 6 | XAUUSD | Short | ✅ valid | ✅ 14:00 | OPEN +2.5R | **2.95R** | ~+2.5R unr. |
| 7 | XAGUSD | Short | ❌ INVALID (scale) | — | — | — | — |
| 8 | GER40  | Short | ✅ valid | ✅ 02:00 | **SL_HIT** 14:00 (after 5.78R MFE!) | **5.78R** | **−1.0R** (BE: 0) |
| 9 | US100  | Long  | ✅ valid (zone too deep) | ❌ MISSED | — | — | 0 |
| 10 | US500 | Long  | ❌ INVALID (scale) | — | — | — | — |

### Realized P/L
- **SL_HIT (3)**: EURUSD −1R · GBPUSD −1R · GER40 −1R = **−3.0R**
- **MISSED (1)**: US100 — bias правильний, entry задалеко = 0R
- **OPEN (3)**: USDJPY −0.6R · USDCAD −0.2R · XAUUSD +2.5R unrealized = **~+1.7R unrealized**
- **INVALID (3)**: USDCHF, XAGUSD, US500 — план не міг бути виконаний
- **Day net realized: −3.0R · Day net incl. unrealized: ~−1.3R**

> Порівняння з 2026-04-23: **+11.1R realized**. День 04-24 — повне дзеркало: dollar weakness, indices rallied, метали reversed.

---

## 2. Три повторювані крос-паттерни

### Паттерн А — **Reversal Day після Trend Day**
04-23 був дзеркальним днем USD strength. 04-24 розгорнувся на 180°:
- EURUSD/GBPUSD plan Short → ринок UP (closed +35 / +65 pips)
- USDJPY/USDCAD plan Long → ринок DOWN
- US100/US500 plan Long bias → правильно (+1.3% / +0.8%)
- Метали reversal: XAUUSD план Short — день low 4658 (за TP), потім bounce
- **Вивід**: після сильного trend day слідкувати за можливим reversal day. Не екстраполювати вчорашній bias автоматично.

### Паттерн B — **NY Open (14:00 UTC) — точка розвороту**
- EURUSD SL hit 14:00
- GBPUSD SL hit 14:00
- GER40 SL hit 14:00 (після MFE 5.78R)
- USDJPY entry 14:00 (drop)
- USDCAD entry 14:00 (drop)
- XAUUSD entry 14:00 (rally до зони)
- **Вивід**: **14:00 UTC = критична точка**. Усі позиції які мають MFE > 1R **перед 14:00 UTC обов'язково на BE**. Це третій раз поспіль (04-22, 04-23, 04-24) NY open перевертає ринок.

### Паттерн C — **Plan Quality Crisis (3 INVALID з 10)**
USDCHF, XAGUSD, US500 — всі мали **entry zone на хибному масштабі ціни**:
- USDCHF: 0.8845 vs реальна 0.7860 (1000+ pips off)
- XAGUSD: 28.40 vs реальна 75.79 (47.4 unit off)
- US500: 5485 vs реальна 7163 (1670 pts off)
- **Вивід**: workflow генерування планів **не верифікує current price**. Це системна помилка, не випадковість.

---

## 3. Три actionable правила (CRITICAL)

### Правило 1 — **Pre-Flight Price Verification (НОВЕ)**
> Перед створенням Top-Down Analysis для кожного інструмента:
> ```
> current = quote_get(symbol)
> if abs(planned_entry − current) / current > 0.05  # 5% threshold
>     ABORT plan, logical error in scale
> ```
> Це блокує 30% помилок сьогоднішнього дня.

### Правило 2 — **BE@2R MANDATORY (повторне з 04-23)**
> Це другий день поспіль коли GER40 показав MFE > 5R і потім SL. На 04-23 — 7.47R, на 04-24 — 5.78R. Без BE правила втрачено мінімум 5R за 2 дні.
>
> **Дія**: створити TradingView alert на 1:2 від entry для кожної відкритої позиції. При спрацюванні — обов'язковий перевід SL на BE.

### Правило 3 — **Bias Re-validation на NY Open**
> При вході в NY (14:00 UTC) **ПЕРЕВІРИТИ** чи актуальна структура з ранкового аналізу:
> - Якщо H1 показує LH/LL після Asian high/low → bias може бути перевернутий
> - Якщо USD сила/слабкість на DXY ≠ ранковому припущенню → анулювати непідтверджені плани
>
> 4 плани (EURUSD, GBPUSD, USDJPY, USDCAD) сьогодні провалились бо bias не був підтверджений на NY open.

---

## 4. Чеклист для нового плану (оновлений)

- [ ] **NEW**: Current price verified (entry within 5% of market)?
- [ ] SL ≥ 1.5× M5 ATR?
- [ ] TP ≤ 0.7× Daily ATR (або staircase)?
- [ ] Asia entry → SL +5–10 pts buffer?
- [ ] Після 17:00 UTC → TP скорочено до 1:2?
- [ ] Entry має safe layer (не тільки aggressive OTE 70%)?
- [ ] **NEW**: Set TradingView alert at 1:2R for BE move?
- [ ] **NEW**: Bias re-validated at NY open (14:00 UTC)?

---

## 5. Уроки специфічно з 04-24

| # | Інструмент | Урок |
|---|---|---|
| 1 | EURUSD | Sweep до TP-3 pips, потім reverse → потрібен partial TP1 1:1 |
| 2 | GBPUSD | Day low 06:30 < entry → sweep вже стався, Short анульовано |
| 3 | USDJPY | LH після Asian high = bias broken, не входити Long |
| 4 | USDCAD | High дня в Лондоні + потім падіння = reversal, не accumulation |
| 5 | USDCHF | INVALID PLAN — масштаб |
| 6 | XAUUSD | Двошаровий entry: aggressive (4720) + safe (4738) для catching trend pre-OTE |
| 7 | XAGUSD | INVALID PLAN — масштаб |
| 8 | GER40 | **BE@2R КРИТИЧНО** — MFE 5.78R втрачено втретє за 3 дні |
| 9 | US100 | Continuation/breakout entry коли ціна вже вище зони — не чекати OTE |
| 10 | US500 | INVALID PLAN — масштаб |

---

## 6. Порівняння днів

| Метрика | 04-23 | 04-24 |
|---|---|---|
| Direction USD | Strong | Weak |
| TP_HIT | 3 | 0 |
| SL_HIT | 1 | 3 |
| OPEN | 5 | 3 |
| MISSED | 1 | 1 |
| INVALID | 0 | **3** |
| Day Net | **+11.1R** | **−3.0R** |
| Plan quality issues | 0 | **3 (30%)** |

---

## 7. Артефакти
- `~/MyVault/20-Trading/Retro/2026-04-24/{10 per-instrument retro files}`
- `/tmp/retro-2026-04-24/bars/EURUSD.json` (raw M15 OHLC)
- `/tmp/retro-2026-04-24/plans.json` (захоплені рівні плану)

## 8. Пов'язані нотатки
- [[../2026-04-23/_DAILY-RETRO|Daily Retro 2026-04-23]] (TP_HIT 3× → +11.1R)
- [[../../Journal/2026-04-24-trading-session|Journal 2026-04-24]]
- [[../../Journal/2026-04-24-retro-session|Retro Session Notes (04-23 review)]]
