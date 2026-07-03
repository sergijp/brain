---
title: "EURUSD LONG (PAPER) — buy-limit pullback у discount, форвард-тест"
date: 2026-07-03
time_kyiv: "10:22"
time_utc: "07:22"
tags: [trading, journal, eurusd, smc-price-action-combo, paper, forward-test, repeated-focus]
category: trading
pair: EURUSD
direction: long
order_type: buy-limit
strategy: smc-price-action-combo
status: planned   # planned → open → closed
agent: journal-writer
paper: true
real_account_touched: false
risk_state_touched: false
risk_override: false
repeated_focus:
  scope: EURUSD-long
  level: ACTIVE-BLOCK-WATCH
  attempts: 5
  wins: 0
  note: "5-та спроба EURUSD-long. Real BLOCK через repeated-focus #5. Дозволено лише як paper до проходження бектесту (performance-analyst)."
tv_shape_id: "2WnCCq"
pinecone_indexed: false
---

# EURUSD LONG (PAPER) — 2026-07-03

> 🧪 **PAPER / FORWARD-TEST.** Real risk $0. `real_account_touched: false`. `_risk-state.json` НЕ змінюється.
> ⛔ Real-гілка заблокована: repeated-focus #5 (EURUSD-long, 4 спроби / 0 wins). Live дозволено лише після бектесту.

## Plan

| Field | Value |
|-------|-------|
| Order type | **BUY LIMIT** (pending) |
| Entry | 1.14450 (нижній край discount / Asian High) |
| SL | 1.14170 (−28 pips, під Asian Low 1.14207) |
| TP1 | 1.14583 (RR 1:0.48) |
| TP2 | 1.14730 (RR 1:1.00) — основна, намальована |
| TP3 | 1.15000 (RR 1:1.96) |
| Lot | 0.18 (half-size) |
| Risk | ~$50 (0.5%) — **PAPER, не реальний** |
| Strategy | [[Strategies/smc-price-action-combo]] |
| TV shape | `2WnCCq` (long_position, M15, через tv-position) |

## Why

- HTF bias bull, ціна відкотилась у **discount**-зону — вхід на нижньому краю (1.14450, Asian High) як POI для pullback-in-discount.
- SL захований **під Asian Low** (1.14207) на 1.14170 — тісний, −28 pips, дає природний RR до TP3 ~1:2.
- TP2 (1.14730) — основна, намальована ціль; консервативний реалістичний таргет у межах дня (інтрадей, flat 17:45).
- Half-size lot (0.18) — свідоме зменшення експозиції через тонку п'ятничну ліквідність (US Bank Holiday) та repeated-focus watch.
- Discretionary setup за `smc-price-action-combo` (pullback-in-discount), НЕ ASR/ORB.

## Risk check

- Day risk used: **0% / 3% (real)** — paper не рахується у денний ліміт.
- Correlation: PASS (real open positions немає; paper ізольований).
- News: **WARN** — Lagarde 10:30–11:30 Kyiv (MEDIUM, прямий EUR-драйвер). Ризик заповнення лімітки у вікні виступу.
- Session: London KZ / інтрадей-вікно. Скасувати лімітку, якщо не заповнилась до **17:00 Kyiv**. **Flat 17:45**.
- Context: п'ятниця, **US Bank Holiday** — тонка ліквідність, знижена якість руху.

## Repeated-focus (resolved → paper-only)

- **#5 ACTIVE-BLOCK-WATCH**, scope `EURUSD-long`: 4 попередні спроби, 0 wins.
- Real-вхід ЗАБЛОКОВАНО. Ця спроба — **paper/forward-test** для збору статистики.
- Ескалація: після цього запису — передати `performance-analyst` для бектесту сетапу перед розблокуванням live.

## Kassandra challenge (resolved)

- Головне заперечення: 5-та поспіль спроба EURUSD-long без виграшів + новинний ризик (Lagarde) + свято.
- Резолюція: НЕ ставити real. Взяти лише як paper half-size для форвард-тесту, з жорсткими вимкненнями (cancel 17:00, flat 17:45) і без впливу на реальний ризик-стан.

## Links

- Analysis: [[Analysis/2026-07-03/EURUSD-analysis]]
- Strategy: [[Strategies/smc-price-action-combo]]

## Execution log

(filled when position is opened/closed — PAPER only)

- [ ] Buy-limit виставлено @ 1.14450 (pending) @ <time>
- [ ] Filled @ 1.14450 @ <time>
- [ ] Moved SL to BE @ <time>
- [ ] TP1 hit @ <time>
- [ ] Cancel (не заповнилось до 17:00 Kyiv) / Closed @ <price> @ <time> — result <pips>/<USD paper>

## Lessons (post-trade)

(filled at retro)
