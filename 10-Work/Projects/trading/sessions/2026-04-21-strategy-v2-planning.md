---
title: "Проект: Trading — Сесія планування Strategy v2 (SMC + PA Combo розширена)"
date: 2026-04-21
tags: [work, session, trading, strategy, smc, planning, v2]
category: work
project: trading
status: completed
pinecone_indexed: false
---

## 🎯 Мета сесії

Розширити базову SMC стратегію (v1 — `20-Trading/Strategies/smc-price-action-combo.md`) гнучкішими моделями входу, формалізувати дисципліну/ризик-менеджмент, і побудувати бектест-процес для валідації edge до переходу на реальні гроші.

Поточні обмеження v1:
- Вхід прив'язаний до моменту аналізу (жорстка послідовність bias→POI→sweep→BOS→вхід за один сеанс)
- Немає inner FVG на LTF як точки входу
- Немає AMD / ICT Power of Three як окремої моделі
- Немає формалізованого бектест-процесу

---

## ✅ Виконано

### 1. Опрацьовано 3 користувацькі пропозиції

| # | Назва | Суть |
|---|-------|------|
| 1 | **Delayed Entry** | Вхід не обов'язково в момент аналізу. Після POI-визначення — alert на рівень, повернення тільки при торканні + LTF-confirm |
| 2 | **Inner FVG after LTF BOS** | Після BOS (5m/15m) вхід з FVG всередині impulse leg. Tighter SL → кращий RR vs broad OB retest |
| 3 | **AMD / Power of Three** | Сесійна модель: Asian accumulation → London/NY Judas sweep manipulation → distribution у напрямку HTF bias |

### 2. Додано 5 пропозицій Claude

- **Breaker Block entry** (пробитий OB як entry у напрямку пробиття)
- **Liquidity-to-Liquidity TP framework** (TP тільки до наступного pool ліквідності, не довільні рівні)
- **Explicit invalidation rules** (час-стоп для alerts, close-back інвалідація, протилежний LTF BOS)
- **Confluence scoring (A/B/C grading)** — фіналізовано як 3 профілі (див. ADR нижче)
- **Partial risk on correlated pairs** (другий скорельований = 0.5% risk)

### 3. Додано 17 розширень (A/B/C/D)

**A. Risk & Money Management:**
- A1 Spread+commission у R (поле `cost_R` ~-0.1R)
- A2 Trailing SL (TP1→BE, TP2→TP1, між — 15m swing)
- A3 Dynamic risk sizing (3 losses → 0.5%, 2 wins → повернення 1%, daily DD 3% = стоп)
- A4 Kelly-lite compounding (+5% equity → перерахунок $risk)

**B. Setup & Entry Precision:**
- B1 DXY / inter-market confluence (обов'язковий screenshot для EUR/GBP/AUD/XAU)
- B2 News filter ±30 хв від NFP/CPI/FOMC/ECB/BoE (hard rule через TV economic calendar alert)
- B3 HTF key levels expanded (Weekly Open, Monthly Open, PWH/PWL, Quarterly H/L)
- B4 Daily profile classification (Expansion / Consolidation / Retracement до NY open)
- B5 Sub-models: Silver Bullet (10:00-11:00 NY), London Reversal (10:00 UTC Judas-sweep)

**C. Process & Discipline:**
- C1 Pre-trade checklist (6-point gate: bias? POI? sweep? BOS? RR≥1:2? psychology OK?)
- C2 Daily bias log (NY close → файл на наступний день, no intraday flipping без H4 BOS)
- C3 Psychology gate "AM I CALM?" (Tilted/Angry/Manic/Impatient/Calm — тільки Calm → OK)
- C4 Weekly review ritual (п'ятниця 18:00 Kyiv — equity, adherence %, top 3 помилки, 1 фокус)

**D. Measurement & Feedback:**
- D1 Obsidian Dataview dashboard (WR by pair/model/session/grade/day-of-week)
- D2 Model retirement rule (<40% WR на 30+ трейдів → pause/rework)
- D3 Adherence tracking (`rule_adherence: full|partial|broken`, ціль ≥90% full)
- D4 A/B testing scoring profiles (тиждень Conservative → Standard → Aggressive)

### 4. Визначено 4-етапний бектест-процес

1. **Manual Bar Replay** (TradingView Ctrl+Alt+R через MCP) — 50+ трейдів на 6 міс історії
2. **Pine Script `strategy()`** — автоматизовані фільтри (EMA bias, FVG detection, BOS pivot) на 2-5 років
3. **Paper forward test** — 1 місяць на demo, мінімум 20 трейдів
4. **Go-live критерії:** expectancy >+0.3R, WR >40%, adherence ≥90%, max DD <15%

Timeline: ~6-8 тижнів setup + backtest + paper → real.

---

## 🔑 Важливі рішення (ADR)

| Рішення | Причина | Альтернатива (відхилено) |
|---------|---------|--------------------------|
| **3 scoring profiles** (Conservative A≥9 / Standard A≥8 / Aggressive A≥6) як режими через `scoring_profile` поле | Ринок не моногенний — drawdown recovery потребує жорсткіших порогів, trending market — м'якших | Один жорсткий поріг (втрачаєш flex) або прибрати scoring (втрачаєш filter) |
| **Correlation table з розподілом** (1% → 0.5% для другого скорельованого) | EUR/GBP кор ~0.85 → 2×1% = 2% фактичного ризику замість 1% | "Max 2 USD-напрямки" (простіше, але грубіше) |
| **Manual + Pine strategy() обидва** | SMC має discretionary elements (який OB валідний), але фільтри (тренд/сесія) автоматизуються. Два треки валідують з різних кутів | Тільки manual (повільно) або тільки Pine (втрачається SMC edge) |
| **AMD на обидві KZ** (London 07-09 UTC + NY 12-14 UTC) | Максимум setup'ів, обидві сесії мають Judas-swing edge | Одна сесія — простіше, але half opportunity |
| **News filter як hard rule** ±30 хв | Минулі спайки на CPI/NFP знищували setup'и — краще пропустити | Soft rule (suggest skip) — ризиковано |
| **Trailing SL формалізовано** (TP1→BE, TP2→TP1, between — 15m swing) | Discretionary trailing призводить до inconsistency на бектесті | Fixed TP only (втрачається runner potential) |
| **Dynamic risk sizing** (3L → 0.5%, 2W → 1%) | Tilt/drawdown spiral — класична психологічна проблема. Kelly-lite захист | Static 1% (не захищає від серії lossів) |

---

## 🐛 Проблеми й як вирішили

### Проблема: план написано, але нічого ще не впроваджено
- **Причина**: користувач у plan mode, не execute — свідоме обмеження щоб валідувати обсяг
- **Вирішення**: збережено session notes + повний план → при команді "виконуй" є recoverable state

### Проблема: Obsidian папка `20-Trading/Strategy/` (single) не існувала
- **Причина**: у vault vault-структурі реально `Strategies/` (plural), що збіглося з v1 файлом
- **Вирішення**: план оновлено використовувати `Strategies/` усюди

---

## 📎 Артефакти

### Основні файли
- **Повний план**: `~/.claude/plans/joyful-twirling-yeti.md` (приблизно 230 рядків, включає Context + 6 секцій + статистику)
- **V1 playbook (існуючий)**: `20-Trading/Strategies/smc-price-action-combo.md` — буде помічено як legacy при впровадженні
- **Auto-memory**: `~/.claude/projects/-Users-serhiinadolskyi-AI-Projects-Trading/memory/tradingview_draw_workflow.md` — MCP draw workflow v1

### Плановані до створення (при "виконуй")
- `20-Trading/Strategies/smc-playbook-v2.md` — консолідований playbook (7 моделей + decision tree)
- `20-Trading/Strategies/correlation-table.md` — таблиця корів + розподіл ризику
- `20-Trading/Backtest/README.md` + `template-backtest-trade.md`
- `20-Trading/Checklists/pre-trade-checklist.md` + `weekly-review-template.md`
- `20-Trading/Dashboards/live-stats.md` — Dataview queries
- `20-Trading/Journal/` — daily bias log + weekly review
- Оновлення project `CLAUDE.md` + `tradingview_draw_workflow.md`

---

## 🎯 Наступні кроки

1. **При команді "виконуй"** — повний rollout за планом у `~/.claude/plans/joyful-twirling-yeti.md`:
   - Фаза 1: оновити project `CLAUDE.md` (секція Стратегія)
   - Фаза 2: оновити `tradingview_draw_workflow.md` (Inner FVG + AMD + Alert workflow)
   - Фаза 3: створити Obsidian файли (playbook-v2, correlation-table, backtest, checklists, dashboard)
2. **Після rollout** — verification за секцією 4 плану (3 історичних сетапи + 5 pilot replay трейдів)
3. **Далі** — manual backtest 50+ трейдів → Pine strategy() → paper 1 міс → go-live

---

## 🔗 Пов'язані нотатки

- [[10-Work/Projects/trading/project-overview]]
- [[20-Trading/Strategies/smc-price-action-combo]] (v1, legacy після rollout)
- [[20-Trading/Resources/trading-rules]]
- [[20-Trading/Resources/tradingview-mcp-workflow]]
