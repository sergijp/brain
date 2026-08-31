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
| **ТС-1** | [[_archive/ts-1-reversal-at-poi\|Reversal at POI]] | 🗄 **АРХІВ** (24.08) — PF 0.79 post-cost, едж < спреду | EURUSD 15m Pine, 5.5m period | 24/30 | Потребує rework — див. гіпотези |
| **ТС-2** | [[ts-2-session-manipulation\|Session Manipulation]] | 🔧 **REWORK** (24.08) — Pine провалив метод, не стратегію | EURUSD 15m Pine, 5.5m period | 11/30 | Потребує manual Bar Replay — не подаєтся Pine-proxy |
| **ТС-3** | [[ts-3-inner-fvg-sniper\|Inner FVG Sniper]] | 🔧 **REWORK** (24.08) — cross-pair FAIL, але EURUSD-only не перевіряли | EURUSD+GBPUSD 15m Pine, 5.5m | 10/40 | v5 edge був cherry-pick — manual Bar Replay required |
| **NS** | [[_archive/ns-strategy\|NS — Top-Down SMC]] | 🟢 Pine Validation (стартувало 2026-04-22) | EURUSD 15m Pine, 2024-05 → 2026-04 | 0/50 | Pine v1 код готовий — запуск ітерацій v1-v10 див. [[pine-ns-2026-04-22]] |
| **ORB** | [[_archive/orb-opening-range-breakout\|Opening Range Breakout]] | ⚪ Draft | — | 0/30 | Non-SMC breakout intraday (US100/US500/GER40, Gold). 5m entry після 15m/30m OR window, London/NY open |
| **VWAP** | [[_archive/vwap-pullback\|VWAP Pullback]] | ⚪ Draft | — | 0/30 | Non-SMC institutional intraday (indices+Gold). Pullback до session VWAP у trending day, ADX filter ≥ 20 |
| **SD** | [[_archive/supply-demand-seiden\|Supply/Demand (Seiden)]] | ⚪ Draft | — | 0/30 | Non-SMC positional swing (FX+Gold/Silver). D1/H4 fresh zones RBR/DBD, limit entry на proximal edge, Min RR 1:3 |
| **MR** | [[_archive/mr-bb-rsi-divergence\|MR BB+RSI]] | ⚪ Draft | — | 0/30 | Non-SMC counter-trend ranging (EURUSD/USDCHF/USDCAD). H1 BB(20,2) touch + RSI divergence, ADX < 20 filter |

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
| 2026-04-22 | Додано 4 non-SMC стратегії (⚪ Draft): [[_archive/orb-opening-range-breakout\|ORB]], [[_archive/vwap-pullback\|VWAP Pullback]], [[_archive/supply-demand-seiden\|Supply/Demand Seiden]], [[_archive/mr-bb-rsi-divergence\|MR BB+RSI]]. Закривають gaps: breakout, institutional-benchmark, positional zones, ranging counter-trend |

---

## 🔗
- [[20-Trading/Strategies/smc-playbook-v2]] — master (shared rules)
- [[20-Trading/Backtest/README]] — 4-етапний процес
- [[20-Trading/Backtest/template-backtest-trade]] — YAML schema
- [[20-Trading/Checklists/pre-trade-checklist]]
- [[10-Work/Projects/trading/rollout-plan-strategy-v2]]

---

## 📅 2026-08-24 — ревізія бібліотеки

| Дія | Що |
|---|---|
| 🗄 **Архів** | ТС-1 → `_archive/`. Pine PF 1.135 (comm=0) → **0.79** post-cost. Едж реальний, але менший за спред. Критерій виходу (WR<40% на 30+) виконано на 24/30 |
| 🔧 **Rework** | ТС-2 — попередній тест провалив **метод**, а не стратегію. Pine не підходить для discretionary edge; едж жодного разу не виміряли |
| 🔧 **Rework** | ТС-3 — відбраковку робили за **cross-pair** критерієм, а торгівля ведеться **тільки по EURUSD**. «Не універсальний» ≠ «не працює на EURUSD» |
| ✅ **Активовано** | [[liquidity-sweep-88]] і [[quasimodo-534]] — перші стратегії зі сліпим гейтом |

### 🔑 Що змінилось методологічно

З дослідження 962 стратегій з'явився **чесний симулятор без lookahead**:
- `~/AI/research/strategies/s88/sim.py`
- `~/AI/research/strategies/s534/simlib.py`

Саме він показав, що більшість «прибуткових» стратегій були артефактом підглядання. **Pine як бектест-proxy більше не використовується** — ТС-2 і ТС-3 переганяються на цей движок за протоколом DEV / CHECKPOINT / сліпий ГЕЙТ.

### ⚠️ Наскрізний ризик обох rework

ТС-2 ловить killzone-маніпуляцію — те саме роблять [[asr-orb-intraday-system]] (ASR) і [[liquidity-sweep-88]]. Перед повним бектестом перевірити, чи ТС-2 дає **нові** сигнали, а не третю обгортку тієї самої ідеї.

ТС-3 має тісний SL і RR 1:4-1:6 → **максимальна чутливість до моделі витрат**. У ТС-1 едж помер саме на цьому. Рахувати за симетричною конвенцією `(target − cost)/(SL + cost)`.

---

## 📅 2026-08-24 (вечір) — ASR архівована

Перший бектест основної системи за 74 дні. Дані: 11 244 бари M15 (січ–сер 2026), 0 дірок.

| Вікно | N | winrate | expectancy |
|---|---|---|---|
| DEV | **6** | 33% | **−0.373** |
| CHECKPOINT | **2** | **0%** | −0.635 |

Стійко негативна через 6 конфігурацій. **Архівована** → [[_archive/asr-orb-intraday-system]] · звіт [[Backtest/asr-2026-08-24]]

**Нова основна система: [[liquidity-sweep-88]]** — та сама ідея (Asia sweep & reclaim), але на ідентичних даних дає **33 угоди / 75.8% / +104.1п** проти 6 / 33% / −2.24R.

**Відтворюваність перевірено:** №88 і №534 збіглися з опублікованими цифрами до десятої. Код і дані цілі.
