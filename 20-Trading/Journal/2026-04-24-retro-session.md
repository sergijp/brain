---
title: "Retro Session — 2026-04-23 (висновки і правила)"
date: 2026-04-24
tags: [trading, retro, session, rules, SMC]
category: trading
type: retro_session
status: completed
pinecone_indexed: false
---

# Retro Session — 2026-04-23
> Дата проведення ретро: 2026-04-24
> Метод: реальні M15 OHLC з TradingView MCP (OANDA/FOREXCOM), analyzer.py, 10 інструментів

---

## Мета сесії
Провести ретроспективу торгового дня 2026-04-23 з нуля — без опори на попередні ретро-файли, на основі об'єктивних даних (entry touch, SL/TP hit, MFE, MAE).

## Виконано

| # | Завдання | Результат |
|---|---|---|
| 1 | Отримано M15 OHLC для 10 інструментів | ✅ OANDA + FOREXCOM через TV MCP |
| 2 | Розраховано метрики (entry, MFE, MAE, outcome) | ✅ analyze.py per ticker |
| 3 | Написано 10 per-instrument retro файлів | ✅ `~/MyVault/20-Trading/Retro/2026-04-23/` |
| 4 | Написано `_DAILY-RETRO.md` з таблицею + паттерни | ✅ |
| 5 | Оновлено auto-memory з 3 новими правилами | ✅ `trading_retro_2026_04_23_rules.md` |
| 6 | Сформульовано висновки для майбутніх планів | ✅ (ця нотатка) |

---

## Підсумки дня 2026-04-23

| Outcome | Тикери | Net R |
|---|---|---|
| TP_HIT (3) | GBPUSD, XAGUSD, US100 | **+12.10R** |
| SL_HIT (1) | US500 | **−1.00R** |
| OPEN (5) | EURUSD, USDJPY, USDCAD, USDCHF, GER40 | partial, TP задалеко |
| MISSED (1) | XAUUSD | miss на 5 pts |
| **Day realized** | | **+11.1R** |

---

## Важливі рішення (ADR)

| # | Рішення | Обґрунтування | Вплив |
|---|---|---|---|
| 1 | SL мінімум = 1.5× M5 ATR | US500: SL=10 pts → swept, TP −0.62 pt | Критичний |
| 2 | TP ≤ 0.7× Daily ATR (staircase якщо більше) | 5 трейдів OPEN з завищеним TP | Великий |
| 3 | При RR > 1:8 → двошаровий entry | XAUUSD miss на 5 pts → −85 pt рух повз | Критичний |
| 4 | Asia entries → SL buffer +5–10 pts | US500 Judas Swing, US100 OK (bigger SL) | Середній |
| 5 | Late NY (17+ UTC) → TP max 1:2 | USDCAD 17:45 UTC з TP 1:5 = structural error | Середній |
| 6 | Після MFE ≥ 2R → SL на BE | GER40: MFE 7.47R, SL ніколи не рухався | Великий |

---

## Висновки для майбутніх планів

### 1. Entry — глибина важливіша за точність
- При RR > 1:8 → **два ордери**: aggressive (OTE 70%) + safe (OTE 61-62% або HTF FVG)
- Entry ніколи **на** liquidity level — завжди 2–5 pips/pts **за** ним
- Asia entries → SL +5–10 pts buffer

### 2. SL — прив'язати до ATR
| Інструмент | Мінімальний SL |
|---|---|
| Forex (EUR/GBP/CAD) | 10–15 pips |
| JPY/CHF | 15–20 pips |
| US100/US500 | 20–25 pts |
| GER40 | 40–60 pts |
| XAUUSD | 10–15 pts |
| XAGUSD | 0.40–0.60 |

### 3. TP — staircase замість single target
- **TP1** (1:2) → fix 50%, SL → BE
- **TP2** (1:4) → fix 30%
- **TP3 runner** → trail SL по M15 структурі

### 4. Тайминг
| Session | Правило |
|---|---|
| Asia (00–07 UTC) | Тільки momentum + широкий SL |
| London (07–12 UTC) | Найкращі entries |
| NY open (12–15 UTC) | Чекати cleanup після news |
| Late NY (17+ UTC) | TP max 1:2 або skip |

### 5. Кластерна впевненість
- 3+ пари однаковий USD direction → **basket confidence**, +20–30% size
- Metals кластер (XAUUSD + XAGUSD) → підвищена впевненість

---

## Чеклист для нового плану (copy-paste)

- [ ] SL ≥ 1.5× M5 ATR?
- [ ] TP ≤ 0.7× Daily ATR (або staircase)?
- [ ] Asia entry → SL +5–10 pts buffer?
- [ ] Після 17:00 UTC → TP скорочено до 1:2?
- [ ] Entry має safe layer (не тільки aggressive OTE 70%)?
- [ ] Після MFE ≥ 2R → є план BE?

---

## Паттерни-вінери (playbook)
1. **GBPUSD Short OTE High** → London → US hours. Tier-1.
2. **XAGUSD Short OTE High** → Asia → London. Кластер з XAUUSD.
3. **US100 Long deep Discount** → Asia → London catch-up.

---

## Артефакти
- `~/MyVault/20-Trading/Retro/2026-04-23/_DAILY-RETRO.md`
- `~/MyVault/20-Trading/Retro/2026-04-23/{10 per-instrument retro files}`
- `~/.claude/projects/-Users-serhiin/memory/trading_retro_2026_04_23_rules.md`
- `/tmp/retro-2026-04-23/analyze.py` (аналізатор OHLC)

## Пов'язані нотатки
- [[../Retro/2026-04-23/_DAILY-RETRO|Daily Retro 2026-04-23]]
- [[2026-04-23-trading-session|Journal 2026-04-23]]
- [[../Strategies/|Strategies]]
