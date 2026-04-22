---
title: "TS Tracker — статус 3 торгових систем"
date: 2026-04-22
tags: [trading, tracker, ts, dashboard]
category: trading
status: active
pinecone_indexed: false
---

# 📊 TS Tracker

Live-статус 3 торгових систем, які походять з [[20-Trading/Strategies/smc-playbook-v2]].

> **Style scope:** semi-scalp + intraday only (no overnight holds, EOD close 21:00 UTC)
> **Min RR:** 1:3 (hard gate для всіх ТС)

---

## 🚦 Статус систем

| ТС | Назва | Status | Тестується | Sample | Decision |
|----|-------|--------|------------|--------|----------|
| **ТС-1** | [[ts-1-reversal-at-poi\|Reversal at POI]] | 🔵 Backtesting | EURUSD 15m, Pine, since 2026-01-01 | 0/30 | — |
| **ТС-2** | [[ts-2-session-manipulation\|Session Manipulation]] | 🟡 Queued | — | 0/30 | — |
| **ТС-3** | [[ts-3-inner-fvg-sniper\|Inner FVG Sniper]] | 🟡 Queued | — | 0/40 | — |

### Легенда статусів
- 🟡 **Queued** — створена, очікує бектесту
- 🔵 **Backtesting** — Етап 1 у процесі (Manual Bar Replay)
- 🟢 **Pine Validation** — Етап 2 (автоматизований бектест)
- 🟣 **Paper Trading** — Етап 3 (forward demo)
- ✅ **Live** — Етап 4, торгується реально
- ⏸ **Paused** — заблокована (низький WR, невідповідність criteria)
- ❌ **Retired** — вилучена остаточно

---

## 📋 Поточний план тестування

**Порядок:** одна ТС за раз (паралельний бектест → плутає atrribution).

1. **🥇 Перша:** **ТС-1 Reversal at POI** (старт 2026-04-22 — Pine на EURUSD 15m, період з 2026-01-01)
2. **🥈 Друга:** ТС-2 Session Manipulation
3. **🥉 Третя:** ТС-3 Inner FVG Sniper

**Правило переходу:** наступна ТС стартує тільки після того, як попередня досягла **30+ трейдів** і отримала вердикт (pass/pause/retire).

---

## 📊 Live-статистика (заповнюється під час бектесту)

### ТС-1 — Reversal at POI
- Trades: 0 / 30
- WR: —
- Avg R: —
- Expectancy: —
- Max DD: —
- Adherence: —
- Avg hold time: —

### ТС-2 — Session Manipulation
- Trades: 0 / 30
- WR: —
- Avg R: —
- Expectancy: —
- Max DD: —
- Adherence: —
- Avg hold time: —

### ТС-3 — Inner FVG Sniper
- Trades: 0 / 40
- WR: —
- Avg R: —
- Expectancy: —
- Max DD: —
- Adherence: —
- Avg hold time: —

---

## 🎯 Success criteria (нагадування)

| Метрика | ТС-1 / ТС-2 | ТС-3 |
|---------|-------------|------|
| WR | ≥ 45% | ≥ 40% |
| Min RR per trade | 1:3 (hard gate) | 1:3 (hard gate) |
| Expectancy | ≥ +0.4R | ≥ +0.5R |
| Avg R per win | ≥ +2.0R | ≥ +3.0R |
| Max DD | ≤ 10% (8% для ТС-2) | ≤ 12% |
| Adherence | ≥ 90% | ≥ 92% |
| Avg hold time | < сесія | ≤ 2h |

---

## 🗓 Історія перемикань

| Дата | Подія |
|------|-------|
| 2026-04-22 | Спліт smc-playbook-v2 на 3 ТС, всі queued |
| 2026-04-22 | Style scope = semi-scalp + intraday (no overnight); min RR 1:3 hard gate усюди; scoring bonus змінено на RR ≥ 1:5 |
| 2026-04-22 | ТС-1 → 🔵 Backtesting (Pine, EURUSD 15m, з 2026-01-01) |

---

## 🔗
- [[20-Trading/Strategies/smc-playbook-v2]] — master (shared rules)
- [[20-Trading/Backtest/README]] — 4-етапний процес
- [[20-Trading/Backtest/template-backtest-trade]] — YAML schema
- [[20-Trading/Checklists/pre-trade-checklist]]
- [[10-Work/Projects/trading/rollout-plan-strategy-v2]]
