---
title: "Trading session — 2026-07-22 — дослідження та переписування 4 MetaTrader EA"
date: 2026-07-22
tags: [trading, metatrader, expert-advisor, mql5, session]
category: session
project: trading
status: completed
agent: session-recorder
pinecone_indexed: false
---

# Trading session — 2026-07-22 — MetaTrader EAs analysis

## Мета сесії

Користувач приніс 4 файли MetaTrader-роботів із папки Downloads + відео "Ключ АРІ UA.mp4". Просив: дослідити що це і як працює, потім виправити для MT5.

## Джерело всіх 4 файлів

Усі підписані однаково: **robot4trade.com / "GPT4trade" / Copyright 2016-2025**. Це шаблонні GPT-згенеровані "AI-роботи" з гучними назвами. Класичний патерн низькоякісних/скам-adjacent "AI EA": гучні назви, демо-код, фейкові фільтри ризику/новин, реального edge немає.

## Аналіз оригіналів (що знайдено)

### 1. PulseTrade AI.mq4 (MT4) — "Smart EMA Trend Rider"
- **Задум:** EMA50 vs EMA200 на H1, фільтр ADX>20, ATR-стоп, RR 2.5, ризик 1%, макс 2/напрямок.
- **Проблеми:**
  - (а) новинний фільтр фейк — `IsNewsTime()` завжди false, інпут `NewsFilter` не працює;
  - (б) зламаний sizing — формула `lot=(Balance×Risk%)/(ATR×mult)` розмірнісно неправильна, не враховує tick value;
  - (в) лічильники `buyTrades`/`lastBuyPrice` ніколи не скидаються при закритті → після 2 угод перестає торгувати назавжди;
  - (г) `iATR` виклик з пропущеним таймфреймом.

### 2. GridScalp Pro.mq4 (MT4) — назва бреше
- **Насправді** RSI+MA mean-reversion, **НЕ сітка.** Buy: RSI<30 і Close>MA50; Sell: RSI>70 і Close<MA50. RR 1:1, фікс лот 0.1, макс 5.
- **Проблеми:**
  - (а) `Grid_Gap=10` оголошений але НІДЕ не використовується — "grid" обман;
  - (б) суперечливі умови входу (RSI<30 разом з ціною вище MA — майже не буває) → сигнали практично не спрацьовують.

### 3. TrendMaster EA.mq5 (MT5) — не компілюється
- **Задум:** SuperTrend + EMA50 + трейлінг.
- **Проблеми:**
  - (а) `CalculateSuperTrend()` і `CalculateEMA()` — ПОРОЖНІ функції, ядра стратегії немає, масиви ніколи не заповнюються;
  - (б) змішаний MT4/MT5 API (`OrderSend`/`OP_BUY`/`OrderSelect`/`MODE_TRADES` у .mq5) → не скомпілюється в MT5.

### 4. METSWI SCALPER.mq5 (MT5) — "Quantum Pulse" = рандом
- **Проблеми:**
  - (а) сигнал буквально випадковий: `CalculateQuantumPulse()=MathRand()%100/100.0`;
  - (б) торгує лише Buy (pulse завжди 0..1, ніколи не <0);
  - (в) невалідний MQL5 API: `TRADE_ACTION_BUY`, `ORDER_BUY`, `request.slippage` — таких констант/полів немає → не компілюється.

## Виконано — переписав усі 4 на робочий MQL5

Збережено новими файлами в `~/Downloads/` з суфіксом `_MT5` (оригінали не чіпав):

| Файл | Що зроблено |
|------|-------------|
| PulseTrade_AI_MT5.mq5 | EMA Trend Rider: EMA50/200 + ADX>20, SL=ATR×1.5, TP=RR×SL (2.5), реальний ризик-сайзинг 1% через tick value, макс 2/напрямок, сесійний фільтр. Новинний фейк-фільтр прибрано. |
| GridScalp_Pro_MT5.mq5 | RSI-відкат у тренді MA50 + **реальна сітка** через Grid_Gap (нова позиція в напрямку лише якщо ≥Grid_Gap пунктів від найближчого входу, до MaxConcurrentTrades). Виправлено суперечливі умови. |
| TrendMaster_EA_MT5.mq5 | SuperTrend реально порахований з ATR (стандартна рекурсія final upper/lower bands + напрямок), вхід на перевороті + фільтр EMA50, трейлінг-стоп до лінії SuperTrend. Прибрано MT4-код. |
| METSWI_SCALPER_MT5.mq5 | Момент-скальпер: EMA8/21 кросовер + RSI-фільтр (>50 buy / <50 sell) на M5, одна позиція, фікс SL/TP у пунктах. Рандом-сигнал замінено реальною логікою. |

**Спільне для всіх переписаних:** `#include <Trade/Trade.mqh>` + `CTrade`, хендли індикаторів + `CopyBuffer`, позиції через `PositionsTotal`/`PositionGetTicket` з фільтром Magic, нормалізація лота (min/max/step) і цін (`_Digits`), вхід раз на закриту свічку.

## Важливі рішення (ADR)

| Рішення | Чому |
|---------|------|
| Не затирати оригінали — нові файли з суфіксом `_MT5` | зберегти вихідні для порівняння/аудиту |
| Для TrendMaster і METSWI "виправлення" = дописування реальної логіки | у оригіналах стратегії не існувало: порожній SuperTrend / MathRand |
| Прибрати фейковий новинний фільтр замість імітації | краще явна відсутність, ніж інпут, який брехливо створює відчуття захисту |

## Проблеми й застереження

| Проблема | Статус / застереження |
|----------|-----------------------|
| Компіляцію фінально треба зробити в MetaEditor | у Claude Code компілятора MQL5 немає |
| Навіть виправлені — прості шаблонні стратегії (EMA-cross, RSI-відкат, SuperTrend, EMA-scalp) | НЕ протестовані на edge. На реал тільки після Strategy Tester + демо |
| ⚠️ SECURITY: відео "Ключ АРІ UA.mp4" (назва "API-ключ") | насторожує в контексті таких пакетів. **Не вводити жодних API-ключів/реквізитів** за інструкціями з такого пакета. Відео поки не досліджено (користувач прибрав зі списку) |

## Артефакти

- **Оригінали:** `~/Downloads/{PulseTrade AI.mq4, GridScalp Pro.mq4, TrendMaster EA.mq5, METSWI SCALPER.mq5}`
- **Переписані:** `~/Downloads/{PulseTrade_AI_MT5, GridScalp_Pro_MT5, TrendMaster_EA_MT5, METSWI_SCALPER_MT5}.mq5`

## Наступні кроки

- Скомпілювати 4 файли в MetaEditor.
- Прогнати через `performance-analyst` у Strategy Tester.

## Linked notes

- [[Strategies/asr-orb-intraday-system]]
- [[Strategies/smc-price-action-combo]]
