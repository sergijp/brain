---
title: "TS Tracker — статус торгових систем"
date: 2026-04-22
tags: [trading, tracker, ts, dashboard]
category: trading
status: active
pinecone_indexed: false
---

# 📊 TS Tracker

Live-статус торгових систем. ТС-1/2/3 походять з [[20-Trading/Strategies/smc-playbook-v2]]; **NS** — незалежна стратегія (власні risk/scoring/gates).

> **Style scope:** semi-scalp + intraday only (no overnight holds, EOD close 21:00 UTC)
> **Min RR:** 1:3 (hard gate для всіх ТС)

---

## 🚦 Статус систем

| ТС | Назва | Status | Тестується | Sample | Decision |
|----|-------|--------|------------|--------|----------|
| **ТС-1** | [[ts-1-reversal-at-poi\|Reversal at POI]] | 🔵 Backtesting | EURUSD 15m, Pine, since 2026-01-01 | 0/30 | — |
| **ТС-2** | [[ts-2-session-manipulation\|Session Manipulation]] | 🟡 Queued | — | 0/30 | — |
| **ТС-3** | [[ts-3-inner-fvg-sniper\|Inner FVG Sniper]] | 🟡 Queued | — | 0/40 | — |
| **NS** | [[ns-strategy\|NS — Власна SMC]] | ⚪ Draft | — | 0/45 (30 FX + 15 Idx) | — |

### Легенда статусів
- ⚪ **Draft** — створена, структура зафіксована, ще не запланована до тестування
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

### NS — Власна SMC стратегія
- Trades: 0 / 45 (30 Forex + 15 Indices/Commodities)
- WR: —
- Avg R: —
- Expectancy: —
- Max DD: —
- Adherence: —
- Avg hold time: —

---

## 🎯 Success criteria (нагадування)

| Метрика | ТС-1 / ТС-2 | ТС-3 | NS |
|---------|-------------|------|----|
| WR | ≥ 45% | ≥ 40% | ≥ 40% |
| Min RR per trade | 1:3 (hard gate) | 1:3 (hard gate) | 1:3 (hard gate) |
| Expectancy | ≥ +0.4R | ≥ +0.5R | ≥ +0.6R |
| Avg R per win | ≥ +2.0R | ≥ +3.0R | ≥ +2.5R |
| Max DD | ≤ 10% (8% для ТС-2) | ≤ 12% | ≤ 10% |
| Adherence | ≥ 90% | ≥ 92% | ≥ 92% |
| Avg hold time | < сесія | ≤ 2h | ≤ 2h |

---

## 🗓 Історія перемикань

| Дата | Подія |
|------|-------|
| 2026-04-22 | Спліт smc-playbook-v2 на 3 ТС, всі queued |
| 2026-04-22 | Style scope = semi-scalp + intraday (no overnight); min RR 1:3 hard gate усюди; scoring bonus змінено на RR ≥ 1:5 |
| 2026-04-22 | ТС-1 → 🔵 Backtesting (Pine, EURUSD 15m, з 2026-01-01) |
| 2026-04-22 | **NS** створена як незалежна стратегія (Forex + Indices/Commodities, intraday, self-contained rules) — ⚪ Draft |

---

## 🔗
- [[20-Trading/Strategies/smc-playbook-v2]] — master (shared rules)
- [[20-Trading/Backtest/README]] — 4-етапний процес
- [[20-Trading/Backtest/template-backtest-trade]] — YAML schema
- [[20-Trading/Checklists/pre-trade-checklist]]
- [[10-Work/Projects/trading/rollout-plan-strategy-v2]]
