---
title: "Rollout Plan — SMC Strategy v2 (Впровадження)"
date: 2026-04-21
tags: [work, project, trading, planning, rollout, v2]
category: work
project: trading
status: active
pinecone_indexed: false
---

# 🚀 Rollout Plan — SMC Strategy v2

**Strategy:** [[20-Trading/Strategies/smc-playbook-v2]]
**Session origin:** [[10-Work/Projects/trading/sessions/2026-04-21-strategy-v2-planning]]
**Temp plan file:** `~/.claude/plans/joyful-twirling-yeti.md` (ephemeral — ця нотатка = persistent копія)

---

## Context

Базова SMC стратегія v1 ([[20-Trading/Strategies/smc-price-action-combo]]) має обмеження:
- Вхід прив'язаний до моменту аналізу (жорстка послідовність за один сеанс)
- Немає inner FVG на LTF як точки входу
- Немає AMD / ICT Power of Three як окремої моделі
- Немає формалізованого бектест-процесу
- Рішення "на око" без статистики edge

**Мета v2:** розширити гнучкими моделями входу, кодифікувати AMD, додати scoring/risk/process формалізми, побудувати 4-етапний бектест для валідації edge до реальних грошей.

---

## 🎲 Обсяг змін (що впроваджуємо)

### Стратегія (7 моделей замість 1)
1. Classic BOS Retest (v1 carry-over)
2. **Delayed Entry** — alert-driven
3. **Inner FVG after LTF BOS** — tighter SL
4. **AMD / Power of Three** — обидві KZ (London + NY)
5. **Breaker Block Entry**
6. **Silver Bullet** (10:00-11:00 NY)
7. **London Reversal** (10:00 UTC)

### Scoring — 3 профілі
| Профіль | A (1%) | B (0.5%) | C (skip) | Коли |
|---------|--------|----------|-----------|------|
| Conservative | ≥9 | 7-8 | <7 | DD recovery, нова модель |
| Standard | ≥8 | 5-7 | <5 | Default |
| Aggressive | ≥6 | 4-5 | <4 | Trending, high-conviction |

### Risk Management
- **A1** Spread/commission у R (`cost_R` -0.1R)
- **A2** Trailing SL: TP1→BE, TP2→TP1, between — 15m swing
- **A3** Dynamic sizing: 3L → 0.5%, 2W → 1%, daily DD 3% → стоп
- **A4** Kelly-lite compounding (+5% equity → recalc)
- **A5** Correlation: другий скорельований = 0.5%

### Setup Precision
- **B1** DXY/yields confluence (обов'язковий screenshot)
- **B2** News filter ±30 хв (hard rule)
- **B3** HTF key levels: Weekly Open, Monthly Open, PWH/PWL, Quarterly
- **B4** Daily profile classification (Expansion/Consolidation/Retracement)
- **B5** Liquidity-to-Liquidity TP framework

### Process & Discipline
- **C1** Pre-trade 6-point checklist
- **C2** Daily bias log (NY close)
- **C3** Psychology gate "AM I CALM?"
- **C4** Weekly review (п'ятниця 18:00 Kyiv)

### Measurement
- **D1** Obsidian Dataview dashboard
- **D2** Model retirement rule (<40% WR на 30+ → pause)
- **D3** Adherence tracking (ціль ≥90% full)
- **D4** A/B testing scoring profiles

---

## 📁 Файли — повний список

### Оновлення існуючих
| Файл | Зміни |
|------|-------|
| `/Users/serhiinadolskyi/AI/Projects/Trading/CLAUDE.md` | Секція "Стратегія (SMC + PA Combo)" → додати 7 моделей, Scoring (3 профілі), Invalidation, Trailing SL, Dynamic Risk, News Filter, Correlation |
| `~/.claude/projects/-Users-serhiinadolskyi-AI-Projects-Trading/memory/tradingview_draw_workflow.md` | Додати: Inner FVG after BOS step; AMD workflow (Asian range → KZ sweep → ChoCH); DXY confluence screenshot step; Alert-driven Delayed Entry flow |
| [[20-Trading/Strategies/smc-price-action-combo]] | Позначити як legacy-v1 з посиланням на v2 |

### Вже створено ✅
- [[20-Trading/Strategies/smc-playbook-v2]] — консолідований playbook
- [[10-Work/Projects/trading/sessions/2026-04-21-strategy-v2-planning]] — session notes
- `~/MyVault/00-Inbox/2026-04-21-strategy-v2-quick-summary.md` — 1-screen саммарі
- **Цей файл** — rollout plan

### Нові файли (при "виконуй")
| Файл | Зміст |
|------|-------|
| `20-Trading/Strategies/correlation-table.md` | Таблиця корів watchlist (EUR/GBP 0.85, XAU/DXY -0.7, etc) + розподіл ризику |
| `20-Trading/Backtest/README.md` | 4-етапний процес + go-live критерії |
| `20-Trading/Backtest/template-backtest-trade.md` | YAML schema для трейд-журналу |
| `20-Trading/Checklists/pre-trade-checklist.md` | 6-point gate + AM I CALM |
| `20-Trading/Checklists/weekly-review-template.md` | П'ятничний ритуал |
| `20-Trading/Dashboards/live-stats.md` | Dataview queries (WR by pair/model/session/grade) |
| `20-Trading/Journal/` (folder) | Daily bias + weekly review templates |

---

## 📊 Бектест — 4 етапи

### Етап 1: Manual Bar Replay (1-2 тижні)
- TradingView Ctrl+Alt+R через MCP (`mcp__tradingview__replay_*`)
- 6 міс історії, 50+ трейдів
- Заповнення journal schema повне
- Ціль: ≤10 хв/трейд

### Етап 2: Pine Script `strategy()` (2-4 тижні)
Кодифікувати автоматизовувані фільтри:
- HTF bias (EMA slope + pivot structure break)
- FVG detection (3-bar imbalance)
- BOS/ChoCH (break of pivot high/low)
- Entry/SL/TP rules

Запуск на 2-5 років → built-in report (Net P&L, Profit Factor, Max DD, Win %).

**Обмеження:** discretionary elements SMC не автоматизуються повністю. Pine — для фільтрів/тренду, не остаточного edge.

### Етап 3: Paper Forward Test (1 місяць)
- Demo-рахунок або paper journal
- Тільки за оновленими правилами
- Мінімум 20 трейдів
- Метрики: WR, avg R, max consecutive losses, adherence %

### Етап 4: Go-Live Критерії
Перехід на реальні гроші **тільки якщо всі виконано**:
- ✅ Manual backtest: expectancy > +0.3R
- ✅ WR > 40% (при RR 1:2+)
- ✅ Max DD на бектесті < 15% капіталу
- ✅ Paper adherence ≥ 90%
- ✅ Paper результати corroborate backtest (±20%)

**Timeline:** ~6-8 тижнів setup + backtest + paper → real.

---

## ✅ Verification (Definition of Done)

### Після rollout
- [ ] Прогнати 3 історичних сетапи через оновлені правила (EURUSD з `CLAUDE.md` приклад + 2 нові з різних моделей) — кожна модель дає чіткий алгоритм без ambiguity
- [ ] 5 pilot-трейдів через Bar Replay за новим шаблоном — час ≤10 хв/трейд
- [ ] Alert creation через `mcp__tradingview__alert_create` працює — критично для Delayed Entry та News Filter
- [ ] Dataview dashboard повертає метрики на 5 pilot-трейдах
- [ ] Pre-trade checklist заповнюється <60 сек на живому chart

### Перед go-live
- [ ] Всі критерії Етапу 4 виконано
- [ ] Weekly review ritual проведено ≥4 тижні
- [ ] Adherence tracking показує ≥90% full
- [ ] Жодна модель не у retirement state (<40% WR)

---

## 🔑 ADR — Зафіксовані рішення

| # | Рішення | Причина |
|---|---------|---------|
| 1 | 3 scoring профілі (Conservative/Standard/Aggressive) як режими через `scoring_profile` поле | Ринок не моногенний — DD recovery потребує жорсткіших порогів, trending — м'якших |
| 2 | Correlation table з розподілом ризику (1% → 0.5%) | EUR/GBP кор ~0.85 → 2×1% = 2% фактичного ризику замість 1% |
| 3 | Manual + Pine `strategy()` обидва | SMC discretionary elements + автоматизовувані фільтри → два треки з різних кутів |
| 4 | AMD на обидві KZ (London + NY) | Максимум setup'ів, обидві сесії мають Judas-swing edge |
| 5 | News filter як hard rule ±30 хв | Минулі спайки на CPI/NFP знищували setup'и |
| 6 | Trailing SL формалізовано (TP1→BE, TP2→TP1, between — 15m swing) | Discretionary trailing → inconsistency на бектесті |
| 7 | Dynamic risk sizing (3L → 0.5%, 2W → 1%) | Tilt/DD spiral — класична психологічна проблема |

---

## 🗺️ Roadmap впровадження (при "виконуй")

### Фаза A: Auto-memory & project CLAUDE.md (1 сесія, ~30 хв)
1. Оновити `/Users/serhiinadolskyi/AI/Projects/Trading/CLAUDE.md` (секція Стратегія)
2. Оновити `tradingview_draw_workflow.md` (Inner FVG + AMD + Alert workflow)

### Фаза B: Obsidian доповнення (1 сесія, ~30 хв)
1. Створити correlation-table.md
2. Створити Backtest/ (README + template)
3. Створити Checklists/ (pre-trade + weekly-review)
4. Створити Dashboards/live-stats.md
5. Створити Journal/ templates

### Фаза C: Verification (1-2 сесії)
1. 3 історичних сетапи через нові правила
2. 5 pilot Bar Replay трейдів
3. Alert MCP test

### Фаза D: Backtest execution (6-8 тижнів, самостійно)
1. Manual replay 50+ трейдів
2. Pine `strategy()` на 2-5 років
3. Paper 1 місяць
4. Go-live decision

---

## ⏭️ Status

🟢 **Фаза B (скорочена) виконана 2026-04-22** — MVP-комплект для старту Manual Bar Replay готовий.

### Що зроблено (2026-04-22)
- ✅ `Backtest/README.md` — 4-етапний процес + go-live критерії
- ✅ `Backtest/template-backtest-trade.md` — YAML schema для журналу
- ✅ `Checklists/pre-trade-checklist.md` — 6-point gate + AM I CALM
- ✅ `Strategies/correlation-table.md` — таблиця корів + алгоритм ризику

### Що залишилось (опційно перед Etapom 1, точно перед Paper)
- ⏳ `Checklists/weekly-review-template.md` — п'ятничний ритуал (потрібен коли є ≥1 тиждень трейдів)
- ⏳ `Dashboards/live-stats.md` — Dataview queries (потрібен коли є ≥10 трейдів у journal)
- ⏳ `Journal/` templates — daily bias + morning brief (опційно)

### Фаза A — статус
⚠️ **Неактуальна в поточній конфігурації** — project Trading repo (`/Users/serhiinadolskyi/AI/...`) не існує на цій машині. Уся робота через vault + TradingView MCP. Auto-memory workflow — перероблено ad-hoc при наступному MCP draw-сеансі.

### Наступний крок
→ **Стартуємо Етап 1 — Manual Bar Replay.** 50+ трейдів за новим template'ом через TV Ctrl+Alt+R / MCP.

## 🔗 Пов'язані нотатки

- [[20-Trading/Strategies/smc-playbook-v2]] — **стратегія v2** (основний документ)
- [[20-Trading/Strategies/smc-price-action-combo]] — v1 legacy
- [[10-Work/Projects/trading/project-overview]]
- [[10-Work/Projects/trading/sessions/2026-04-21-strategy-v2-planning]] — origin session
