---
title: "USDCAD SHORT — 07.05.2026 (conditional planned)"
date: 2026-05-07
tags: [trading, journal, usdcad, short, planned, conditional]
category: trading
pair: USDCAD
direction: short
strategy: smc-price-action-combo
agent: journal-writer
status: planned
risk_conditional: true
entry_zone: "1.3700-1.3720"
entry_point: 1.3705
sl: 1.3745
tp1: 1.3595
tp2: 1.3500
lot: 0.34
risk_usd: 100
risk_pct: 1.0
rr_tp1: 2.75
rr_tp2: 5.13
activation_window: "14:30-17:15 UTC"
condition_a: "BSL sweep відбувся → вхід після 14:30 UTC"
condition_b: "WTI H4 не в breakdown"
condition_c: "M15 CHoCH + BOS 1.3680 на закритій свічці"
risk_override: false
pinecone_indexed: false
---

# USDCAD SHORT — 2026-05-07

> **Conditional planned.** Трейд активується ТІЛЬКИ при одночасному виконанні умов A + B + C у вікні 14:30–17:15 UTC. Поза вікном — скасування.

## Plan

| Field | Value |
|-------|-------|
| Entry zone | 1.3700–1.3720 (H4 bearish OB) |
| Entry point | 1.3705 |
| Trigger | M15 bearish CHoCH після sweep BSL + BOS нижче 1.3680 (закрита свічка) |
| Activation window | 14:30–17:15 UTC |
| SL | 1.3745 (+40 pips від entry, 25 pips вище BSL cluster @ 1.3720) |
| TP1 | 1.3595 (D Low, RR 1:2.75) |
| TP2 | 1.3500 (swing SSL, RR 1:5.13) |
| Lot | 0.34 |
| Risk | $100 (1.0%) |
| Strategy | [[Strategies/smc-price-action-combo]] |

## Why

- W/D структура підтверджує bearish bias: серія LH/LL, H4 CHoCH @ 1.37, BOS @ 1.36.
- H4 bearish OB зона 1.3700–1.3720 — ключова точка реакції продавців.
- London KZ sweep вже пропущений; сейф-вікно NY KZ (після Claims blackout) відкривається о 14:30 UTC.
- Необхідний sweep BSL вище 1.3700 → підтвердження маніпуляції перед продовженням тренду.
- M15 BOS нижче 1.3680 (закрита свічка) як фінальний тригер входу знижує ризик хибного сигналу.

## Risk check

- Day risk used: 0.0% / 3%
- Correlation: PASS (немає відкритих позицій у групі USD-major)
- News: BLOCK до 14:30 UTC (USD Claims 12:30 UTC MEDIUM, blackout 12:00–13:00; safe від 14:30) / BLOCK від 17:30 UTC (FOMC Minutes 18:00 UTC HIGH, blackout 17:30–18:30)
- Session: NY KZ 12:00–14:00 UTC (safe window починається 14:30)
- Verdict: OK (УМОВНИЙ) — активується тільки при A + B + C

## Kassandra challenge (resolved)

Kassandra висунула три жорсткі умови-блокери. Після дебатів Dixie прийняла всі три як обов'язкові. Конвергенція досягнута: трейд умовний, без виконання всіх трьох умов вхід заборонений.

### Три жорсткі умови (всі три одночасно):

| | Умова | Опис |
|-|-------|------|
| **A** | BSL sweep | Ціна дійшла до 1.3700+ → вхід тільки після 14:30 UTC |
| **B** | WTI H4 check | Немає breakdown нафти нижче ключової підтримки (зростання CAD = проти трейду) |
| **C** | M15 CHoCH + BOS | BOS нижче 1.3680 підтверджений на ЗАКРИТІЙ свічці |

Якщо хоча б одна умова не виконана — трейд скасовується.

## Links

- Analysis: [[Analysis/2026-05-07/USDCAD-analysis]]
- Strategy: [[Strategies/smc-price-action-combo]]

## Execution log

(заповнюється при відкритті / закритті позиції)

- [ ] Перевірено умову A: BSL sweep @ 1.3700+ (після 14:30 UTC)
- [ ] Перевірено умову B: WTI H4 — немає breakdown
- [ ] Перевірено умову C: M15 CHoCH + BOS нижче 1.3680 (закрита свічка)
- [ ] Opened at <price> @ <time>
- [ ] Moved SL to BE at <price>
- [ ] TP1 hit at <time>
- [ ] Closed at <price> @ <time> — result <pips>/<USD>

## Lessons (post-trade)

(заповнюється на ретро)
