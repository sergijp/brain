---
title: "EURUSD LONG — 07.05.2026 (planned)"
date: 2026-05-07
time_kyiv: "09:13"
time_utc: "06:13"
tags: [trading, journal, eurusd, long, planned]
category: trading
pair: EURUSD
direction: long
strategy: smc-price-action-combo
status: planned
agent: journal-writer
scenario_preferred: B
entry_a: 1.17420
entry_b: 1.17280
sl: 1.17160
tp1_b: 1.17832
tp2: 1.17965
lot_a: 0.04
lot_b: 0.08
risk_usd_a: 104
risk_usd_b: 96
rr_tp2_a: 2.10
rr_tp2_b: 5.70
entry_deadline: "11:45 UTC"
fomc_management: "SL→BE або -50% до 17:30 UTC"
risk_override: false
pinecone_indexed: false
---

# EURUSD LONG — 2026-05-07

## Plan

### Сценарій A — без sweep SSL

| Field | Value |
|-------|-------|
| Entry | 1.17420 (M5 demand, після M15 CHoCH) |
| SL | 1.17160 (-260 pips) |
| TP1 | 1.17665 (H1 Premium boundary — BE-тригер, не фіксація) |
| TP2 | 1.17965 (H4 HH/BSL) |
| RR | 1:2.10 (TP2) |
| Lot | 0.04 |
| Risk | $104 (1.04%) |
| Strategy | [[Strategies/smc-price-action-combo]] |

### Сценарій B — після SSL sweep ~1.17190 (PREFERRED)

| Field | Value |
|-------|-------|
| Entry | 1.17280 (post-sweep, M5 BOS вгору підтверджений) |
| SL | 1.17160 (-120 pips) |
| TP1 | 1.17832 (H1 Supply OB — BE-тригер) |
| TP2 | 1.17965 (H4 HH/BSL) |
| RR | 1:4.6 (TP1), 1:5.7 (TP2) |
| Lot | 0.08 |
| Risk | $96 (0.96%) |
| Strategy | [[Strategies/smc-price-action-combo]] |

**Дедлайн тригера:** 11:45 UTC — якщо до цього часу немає CHoCH/BOS вгору — пропуск.

## Why

- W Demand OB на рівні 1.17–1.18: ціна торгується в зоні щотижневого попиту, що формує bullish bias HTF.
- D Midpoint 0.5 Fib @ 1.1750: денний рівень рівноваги виступає магнітом/підтримкою для лонгів.
- H4 HL @ 1.17415 підтверджено: bullish Higher Low структура на H4 збережена — ознака продовження тренду.
- H1 BOS LONG @ 1.17549: H1 вже дав Break of Structure вгору, підтверджуючи короткострокову бичачу імпульсну хвилю.
- SSL @ 1.17190 — Judas Swing ризик: London може сміттяризнути ліквідність нижче перед рухом вгору, тому Сценарій B (post-sweep entry) є preferred з кращим RR і чіткішим тригером.

## Risk check

- Day risk used: 0.0% / 3% (новий день)
- Correlation: PASS (немає відкритих USD-major позицій)
- News: WARN — Claims 12:30 UTC (HIGH), FOMC Minutes 18:00 UTC (HIGH)
- Session: PASS — London open (09:13 Kyiv / 06:13 UTC), KZ активна

## Kassandra challenge (resolved)

Kassandra висувала concern щодо подвійного новинного ризику (Claims + FOMC) та ширини SL в Сценарії A. Після дебату досягнуто конвергенцію: Сценарій B усуває обидва заперечення завдяки tight SL (-120 pips) та підтвердженому BOS-тригеру. Управління позицією (SL→BE до 12:00, закрити 50% або повністю до 17:30 UTC) прийнято як обов'язкова умова трейду.

## Links

- Analysis: [[Analysis/2026-05-07/EURUSD-analysis]]
- Strategy: [[Strategies/smc-price-action-combo]]

## Execution log

(заповнюється при відкритті/закритті)

- [ ] Opened at <price> @ <time>
- [ ] SSL sweep підтверджено @ <price> (якщо Сценарій B)
- [ ] Moved SL to BE at <price>
- [ ] TP1 hit at <time>
- [ ] Оцінка позиції перед Claims @ 12:00 UTC
- [ ] Закрито 50% або SL→BE до 17:30 UTC (FOMC prep)
- [ ] Closed at <price> @ <time> — result <pips>/<USD>

## Lessons (post-trade)

(заповнюється на ретро)
