---
title: "Daily Retro — 2026-04-23"
date: 2026-04-23
tags: [trading, retro, daily, summary]
category: trading
type: daily_retro
instruments: [EURUSD, GBPUSD, USDJPY, USDCAD, USDCHF, XAUUSD, XAGUSD, GER40, US100, US500]
---

# Daily Retro — 2026-04-23

> **Мета**: дистилювати 10 торгових сетапів за день у структуровані уроки, повторювані паттерни, і actionable правила на майбутнє. Всі метрики отримані з реальних M15 OHLC (OANDA/FOREXCOM) через TradingView MCP.

---

## 1. Підсумкова таблиця

| # | Ticker | Side | Entry Touched | Outcome | Planned RR | MFE (R) | MAE (R) | Net Result |
|---|--------|------|---------------|---------|-----------|---------|---------|------------|
| 1 | EURUSD | Short | ✅ 14:45 | **OPEN** (−0.5 pip від TP) | 1:3.75 | 3.71R | 0.24R | Near-win |
| 2 | GBPUSD | Short | ✅ 11:45 | **TP_HIT** 17:15 | 1:4.08 | 4.61R | 0.78R | **+4.08R** |
| 3 | USDJPY | Long | ✅ 02:00 | **OPEN** | 1:5.0 | 2.13R | 0.53R | Partial |
| 4 | USDCAD | Short | ✅ 17:45 | **OPEN** | 1:5.0 | 1.22R | 0.04R | Small win |
| 5 | USDCHF | Long | ✅ 14:45 | **OPEN** | 1:5.33 | 2.49R | 0.29R | Good partial |
| 6 | XAUUSD | Short | ❌ (5 pt miss) | **MISSED ENTRY** | 1:11.4 | N/A | N/A | **Whiff** |
| 7 | XAGUSD | Short | ✅ 01:45 | **TP_HIT** 07:00 | 1:4.0 | 6.73R | 0.2R | **+4.0R** |
| 8 | GER40 | Short | ✅ 14:45 | **OPEN** | 1:10.9 | 7.47R | 0.92R | Huge unrealized |
| 9 | US100 | Long | ✅ 03:30 | **TP_HIT** 09:00 | 1:4.02 | 6.48R | 0.17R | **+4.02R** |
| 10 | US500 | Long | ✅ 02:15 | **SL_HIT** 03:30 | 1:5.0 | 1.01R | 1.36R | **−1.0R** |

### Realized P/L
- **TP_HIT (3)**: GBPUSD +4.08R · XAGUSD +4.00R · US100 +4.02R = **+12.1R**
- **SL_HIT (1)**: US500 −1.00R = **−1.0R**
- **OPEN (5)**: EURUSD, USDJPY, USDCAD, USDCHF, GER40 — partial profit, не закриті на TP
- **MISSED (1)**: XAUUSD — entry не торкнувся
- **Day net realized (only closed trades): +11.1R**

---

## 2. Три повторювані крос-паттерни

### Паттерн А — **Dollar Divergence Day**
Сьогодні: USD short проти EUR/GBP/CAD + USD long проти JPY/CHF + US100 long.
- **FX шорти USD** (EURUSD/GBPUSD/USDCAD) — всі попали в напрямок.
- **USD проти JPY/CHF** (long) — всі попали.
- **US indices long** (US100 win, US500 SL swept) — mixed.
- **Вивід**: коли detecting USD-розворот мати "basket confidence" — якщо EUR/GBP short плани однакові, впевненість вища.

### Паттерн B — **Entry Depth Is Destiny**
Три кейси чітко це показали:
- **XAUUSD (miss)** — entry на 5 pt вище day_high → цілий рух на 85 pt повз нас.
- **US500 (SL)** — entry on-the-dot, але SL на 10 pt → swept noise → **TP взяв би з SL 15 pt**.
- **US100 (win)** — entry у deep discount з SL 43.8 pt = buffer проти noise → TP.
- **Вивід**: **depth entry + adequate SL buffer** — два найважливіших параметри після напрямку.

### Паттерн C — **Asia Stop-Hunt Before London**
Три Asia entries: USDJPY 02:00 · US500 02:15 · XAGUSD 01:45.
- USDJPY → OK (повільний рух).
- US500 → **swept** (Judas Swing).
- XAGUSD → TP за 5h (швидкий momentum).
- **Вивід**: Asia entries з tight SL — ризик Judas Swing. Додавати buffer **5-10 pts** beyond Asia session range.

---

## 3. Три actionable правила на завтра

### Правило 1 — **POI Depth > Aggressive Entry**
> При plan RR > 1:8 ставити **два entries**: aggressive (точний OTE 70%) + safe (OTE 61-62% або попередній HTF FVG). XAUUSD сьогодні — ідеальна ілюстрація.

### Правило 2 — **SL Buffer Based on ATR, not "tight risk"**
> SL для intraday: **мінімум 1.5 × M5 ATR** (для indices — ~15-20 pts, для FX — ~10-15 pips).
> Якщо entry в Asia — додавати **+5-10 pts buffer**.
> US500 з SL 10 pt — приклад того, чого не робити.

### Правило 3 — **TP Calibration vs Daily Range**
> TP **не повинен** перевищувати **0.7 × Daily ATR**. Якщо план 1:5 вимагає TP > ATR*0.7 — робити TP-staircase:
> - TP1 = 1:2 → fix 50%
> - TP2 = 1:4 → fix 30%, SL to BE
> - TP3 (runner) = 1:5+ → trail SL
>
> Сьогодні 5 трейдів з 10 (всі OPEN) постраждали від цього: EURUSD, USDJPY, USDCAD, USDCHF, GER40 — усі мали хороший MFE, але TP задалеко.

---

## 4. Ключові моменти що потрібно не забути

1. **News + POI**: XAUUSD і US500 — обидва були в time window US cash open (13:30-14:45 UTC). Два stop-runs в indices, але при правильних entries вони могли б бути wins. **При high-impact news → entry ставити тільки після того, як ціна зробить cleanup** (sweep + return).
2. **GER40 MFE 7.47R** — ніби "не закрили", але насправді потенціал був. Правило: після MFE > 2R **обов'язково** SL → BE. Потім при MFE > 5R — trail у підтримках.
3. **Metals кластер-паттерн**: XAUUSD (miss) + XAGUSD (win) однаковий напрямок = кореляційна підтримка. Якщо один триггер — другий ймовірніший.

---

## 5. Links

- [[EURUSD-retro]] · [[GBPUSD-retro]] · [[USDJPY-retro]] · [[USDCAD-retro]] · [[USDCHF-retro]]
- [[XAUUSD-retro]] · [[XAGUSD-retro]] · [[GER40-retro]] · [[US100-retro]] · [[US500-retro]]
- [[../../Analysis/2026-04-23/|← Плани на 2026-04-23]]
- [[../../Journal/2026-04-23-trading-session|Journal 2026-04-23]]

---

## 6. Score

- **Decision quality**: 9/10 — напрямки у 9 з 10 були правильні.
- **Execution quality**: 6/10 — entries ок, але TP/SL calibration страждає.
- **Overall day**: 7/10 — прибутковий день, але багато "залишкового золота" на столі.
