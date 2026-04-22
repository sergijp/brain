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
| **ТС-1** | [[ts-1-reversal-at-poi\|Reversal at POI]] | ⏸ Pine FAIL (PF 0.79 post-cost) | EURUSD 15m Pine, 5.5m period | 24/30 | Потребує rework — див. гіпотези |
| **ТС-2** | [[ts-2-session-manipulation\|Session Manipulation]] | ⏸ Pine FAIL (0% WR, gross=$0) | EURUSD 15m Pine, 5.5m period | 11/30 | Потребує manual Bar Replay — не подаєтся Pine-proxy |
| **ТС-3** | [[ts-3-inner-fvg-sniper\|Inner FVG Sniper]] | ⏸ Pine FAIL cross-pair (EURUSD PF 1.43, GBPUSD PF 0.39) | EURUSD+GBPUSD 15m Pine, 5.5m | 10/40 | v5 edge був cherry-pick — manual Bar Replay required |
| **NS** | [[ns-strategy\|NS — Top-Down SMC]] | 🟢 Pine Validation (стартувало 2026-04-22) | EURUSD 15m Pine, 2024-05 → 2026-04 | 0/50 | Pine v1 код готовий — запуск ітерацій v1-v10 див. [[pine-ns-2026-04-22]] |

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

### ТС-1 — Reversal at POI (Pine v3 full rules, 15m EURUSD, 5.5 міс)
- Trades: **24** / 30 (sample insufficient)
- WR: **37.5%** (comm=0) → **33.3%** (comm=0.03%)
- PF: **1.135** (comm=0) → **0.789** (post-cost) ❌
- Avg win: +0.46% | Avg loss: −0.24%
- Max DD: 0.17% (comm=0) / 0.25% (post-cost)
- Sharpe: −3.27 | Long PF: 1.03 | Short PF: 1.30
- **Verdict:** edge РЕАЛЬНИЙ але ТОНКИЙ, не витримує FX costs. Потрібен rework (див. [[20-Trading/Backtest/pine-ts1-2026-04-22#Next steps]]).
- Full results: [[pine-ts1-2026-04-22]]

### ТС-2 — Session Manipulation (Pine v1-v3, 15m EURUSD, 5.5m)
- Trades: **11** / 30 (sample insufficient, KZ setups занадто рідкісні)
- WR: **0-9%** (v1: 1/11, v2-v3: 0/11)
- PF: **0-0.04** ❌
- Gross Profit (v2-v3): **$0** — жоден сетап не дійшов до 1:2 TP
- **Verdict:** Pine-proxy НЕ годиться для TS-2 (discretionary edge неповторний алгоритмом). Треба manual Bar Replay.
- Full results: [[pine-ts2-2026-04-22]]

### ТС-3 — Inner FVG Sniper (Pine v5 shorts-only, EURUSD+GBPUSD 15m, 5.5m)
- EURUSD: 10 trades, WR 50%, PF **1.427** post-cost ✅ (+$4.63)
- GBPUSD: 21 trades, WR **19%**, PF **0.388** ❌ (−$18.94)
- GBPUSD + H1 bias: 13 trades, WR 23%, PF 0.483 ❌
- **Verdict:** v5 edge на EURUSD був **period cherry-pick** (EURUSD bearish −1.9% vs GBPUSD +3.4%). Shorts-only FVG = trend-follower reversed, не працює на bullish pair. НЕ robust edge.
- Pine НЕ годиться для TS-3 (аналогічно TS-2 discretionary).
- Full results: [[pine-ts3-2026-04-22]]

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
| 2026-04-22 | ТС-1 Pine bench (5 iter, v1→v5): edge РЕАЛЬНИЙ (PF 1.135 comm=0, WR 37.5%) але НЕ витримує realistic FX costs (PF 0.79). H1 не рятує. Переходимо в ⏸ — rework required |
| 2026-04-22 | ТС-2 Pine bench (3 iter, v1→v3): 11 trades, WR 0-9%, gross=$0. Pine НЕ годиться як proxy для TS-2 (discretionary edge). Переходимо в ⏸ — manual Bar Replay required |
| 2026-04-22 | ТС-3 Pine bench (6 iter + cross-pair): EURUSD v5 PF 1.43 виявився cherry-pick (GBPUSD PF 0.39, WR 19%). Shorts-only FVG = прихований trend-follower, fails на bullish pair. Pine НЕ годиться для TS-3 |
| 2026-04-22 | Retrospective analysis: [[retrospective-analysis-2026-04-22]] — 6-gate filter прогноз дає ~+25-50% WR improvement, але не вистачає cost hurdle. Next: manual Bar Replay 30 trades у TV app |
| 2026-04-22 | **NS** створена як незалежна стратегія (Forex + Indices/Commodities, intraday, self-contained rules) — ⚪ Draft |
| 2026-04-22 | NS → 🟢 Pine Validation. Створено [[pine-ns-2026-04-22]]: повний Pine v6 з 5-крок воронкою + 6-point scoring + AMD Kyiv TZ + opens + SMT (GBPUSD proxy). Запуск v1 (comm=0) → v10 (cross-pair) попереду |

---

## 🔗
- [[20-Trading/Strategies/smc-playbook-v2]] — master (shared rules)
- [[20-Trading/Backtest/README]] — 4-етапний процес
- [[20-Trading/Backtest/template-backtest-trade]] — YAML schema
- [[20-Trading/Checklists/pre-trade-checklist]]
- [[10-Work/Projects/trading/rollout-plan-strategy-v2]]
