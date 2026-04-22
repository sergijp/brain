---
title: "Проект: Trading — Rollout Фаза B (MVP для бектесту)"
date: 2026-04-22
tags: [work, session, trading, strategy, smc, rollout, v2, backtest]
category: work
project: trading
status: completed
pinecone_indexed: false
---

## 🎯 Мета сесії

Продовжити rollout Strategy v2 з точки зупинки 21.04. Замість сліпого виконання оригінального плану — переглянути стан (частина оригінального плану стосувалась застарілих шляхів) і запустити **скорочену Фазу B**: створити MVP-комплект файлів, достатній для старту Етапу 1 бектесту (Manual Bar Replay).

---

## ✅ Виконано

### 1. Аудит стану rollout (21.04 → 22.04)
- Перечитано auto-memory (`trading_eurusd_session_apr21.md`) + vault session notes
- Переглянуто persistent rollout plan у `rollout-plan-strategy-v2.md` (ephemeral `~/.claude/plans/joyful-twirling-yeti.md` вже очищений)
- Зафіксовано розбіжність: **Фаза A (project CLAUDE.md)** оригінального плану — неактуальна, бо `/Users/serhiinadolskyi/AI/Projects/Trading/` на цій машині не існує. Уся робота через vault + TradingView MCP.

### 2. Створено 4 MVP-артефакти

| Файл | Призначення |
|------|-------------|
| `20-Trading/Backtest/README.md` | 4-етапний процес (Manual → Pine → Paper → Go-Live) + go-live критерії |
| `20-Trading/Backtest/template-backtest-trade.md` | YAML schema журналу трейдів (identity, bias, entry, confluence, management, result, psychology, review) |
| `20-Trading/Checklists/pre-trade-checklist.md` | 6-point gate (BIAS/POI/SWEEP/BOS/RR/CALM) + 6 hard blockers + швидка форма |
| `20-Trading/Strategies/correlation-table.md` | 15 пар-кореляцій + алгоритм розподілу ризику + hard caps + quarterly review |

### 3. Оновлено persistent rollout plan
`rollout-plan-strategy-v2.md` → статус 🟡 → 🟢, зафіксовано неактуальність Фази A, намічено наступний крок (Етап 1 бектесту).

---

## 🔑 Важливі рішення (ADR)

| Рішення | Причина | Альтернатива (відхилено) |
|---------|---------|--------------------------|
| **Скорочена Фаза B** (4 файли), а не повна (7 файлів) | Weekly-review + Dashboards + Journal templates непотрібні, поки немає ≥1 тижня трейдів. Створимо lazy, коли виникне потреба | Повна Фаза B одразу (overhead без value) |
| **Фаза A — skip** | Project CLAUDE.md шлях не існує на цій машині — інший user у path. Auto-memory workflow оновимо ad-hoc при наступному MCP draw-сеансі | Створити project CLAUDE.md "про запас" (marginal value, надмірна робота) |
| **Correlation table: hard cap 2% сумарного ризику** | Захист від концентрації у режимах коли корі-ляції ростуть (risk-off) — класичний 2008-style blow-up | Без cap (агресивніше, але без safety net) |
| **Hard blocker: model retirement <40% WR на 30+ трейдах** | Уникнути sunk-cost fallacy — якщо модель не працює статистично, не можна торгувати "на віру" | Soft rule (рекомендація) — легше ігнорувати |
| **YAML template з полями `gate_*` мапиться 1-to-1 на pre-trade checklist** | Одна точка істини — checklist заповнюється ЗВ'ЯЗКОМ, не дублюється у template | Два незалежні документи (risk: divergence над часом) |

---

## 🐛 Проблеми й як вирішили

### Проблема: шляхи в оригінальному плані не відповідають поточній машині
- **Причина:** оригінальний rollout-plan писався з посиланням на `/Users/serhiinadolskyi/AI/Projects/Trading/` (ймовірно інша установка). Поточний user = `serhiin`, auto-memory у `~/.claude/projects/-Users-serhiin/`
- **Вирішення:** Фаза A skipped, плану присвоєно статус "неактуальна в поточній конфігурації", зафіксовано у rollout-plan для майбутньої сесії

### Проблема: ephemeral `joyful-twirling-yeti.md` уже очищений
- **Причина:** plan files у `~/.claude/plans/` — тимчасові, persistent копія у vault — по задуму
- **Вирішення:** persistent version у `rollout-plan-strategy-v2.md` був повний → жодного loss'у, робота продовжилась без даунтайму

---

## 📎 Артефакти

### Створено
- `~/MyVault/20-Trading/Backtest/README.md`
- `~/MyVault/20-Trading/Backtest/template-backtest-trade.md`
- `~/MyVault/20-Trading/Checklists/pre-trade-checklist.md`
- `~/MyVault/20-Trading/Strategies/correlation-table.md`

### Оновлено
- `~/MyVault/10-Work/Projects/trading/rollout-plan-strategy-v2.md` (секція Status + новий "Наступний крок")

### Залишилось до повного rollout (lazy, при потребі)
- `Checklists/weekly-review-template.md` — коли закінчиться перший тиждень paper/replay
- `Dashboards/live-stats.md` — коли буде ≥10 трейдів у journal
- `Journal/daily-bias-template.md`, `Journal/morning-brief-template.md` — опційно

---

## 🎯 Наступні кроки

1. **Етап 1 бектесту — Manual Bar Replay** (1-2 тижні)
   - TradingView Ctrl+Alt+R або MCP (`mcp__tradingview__replay_*`)
   - 6 міс історії, 50+ трейдів
   - Журнал: `20-Trading/Backtest/trades/YYYY-MM-DD-NN-[pair]-[model].md`
   - Ціль часу: ≤10 хв/трейд
2. **Коли назбирається ~10 трейдів** → створити `Dashboards/live-stats.md` з Dataview
3. **Після Етапу 1** → Етап 2 (Pine `strategy()`)
4. **Активний EURUSD setup 1.17880** — продовжує трекатись окремо (див. auto-memory `trading_eurusd_session_apr21.md`)

---

## 🔗 Пов'язані нотатки

- [[10-Work/Projects/trading/sessions/2026-04-21-strategy-v2-planning]] — попередня сесія (origin)
- [[10-Work/Projects/trading/rollout-plan-strategy-v2]] — persistent rollout plan
- [[20-Trading/Strategies/smc-playbook-v2]] — стратегія яку валідуємо
- [[20-Trading/Backtest/README]] — 4-етапний бектест-процес
- [[20-Trading/Checklists/pre-trade-checklist]] — 6-point gate
