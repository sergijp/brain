---
title: "Проект: Trading — Спліт Strategy v2 на 3 ТС + intraday/RR refinement"
date: 2026-04-22
tags: [work, session, trading, strategy, smc, ts, refactor, intraday, rr]
category: work
project: trading
status: completed
pinecone_indexed: false
---

## 🎯 Мета сесії

Покращити Strategy v2: розбити monolithic-плейбук на окремі торгові системи з чистою attribution для бектесту, узгодити правила зі стилем користувача (semi-scalp + intraday) та підняти мінімальний RR.

---

## ✅ Виконано

### 1. Спліт smc-playbook-v2 на 3 ТС
Замість одного 7-модельного плейбука створено 3 окремі ТС, кожна — самостійний файл з власними правилами, scoring-тюнами, backtest-планом і success/retirement criteria.

| ТС | Назва | Моделі | Файл |
|----|-------|--------|------|
| ТС-1 | Reversal at POI | Classic BOS, Delayed Entry, Breaker | `Strategies/ts-1-reversal-at-poi.md` |
| ТС-2 | Session Manipulation | AMD, Silver Bullet, London Reversal | `Strategies/ts-2-session-manipulation.md` |
| ТС-3 | Inner FVG Sniper | Inner FVG after LTF BOS | `Strategies/ts-3-inner-fvg-sniper.md` |

### 2. Створено TS Tracker
`Strategies/ts-tracker.md` — live-статус борд: статуси (queued/backtesting/paper/live/paused/retired), live-статистика per ТС, success criteria, історія перемикань.

### 3. Універсальне правило intraday + RR 1:3
Користувач уточнив стиль: **semi-scalp + intraday only, no overnight**. Узгоджено всі 6 файлів:
- Усі позиції закриваються до **21:00 UTC** (NY close)
- Session-bound (одна сесія = одна позиція)
- **Min RR 1:3** (hard gate) — було 1:2
- Scoring bonus змінено на **RR ≥ 1:5 = +2 балів** (бо 1:3 тепер не бонус)
- ТС-1 переписано з swing-tone (H4/D bias) на intraday (H1/H4 bias, 5m/15m trigger)
- ТС-3 fresh-BOS зменшено з 2h до 30 хв; max hold 2h; Avg R per win bump +2.5R → +3.0R

### 4. Узгоджено pre-trade-checklist
`Checklists/pre-trade-checklist.md` — gate p.5 та швидке заповнення оновлено на RR 1:3.

---

## 🔑 Важливі рішення (ADR)

| Рішення | Причина | Альтернатива (відхилено) |
|---------|---------|--------------------------|
| **Спліт на 3 ТС, не 2 і не 7** | 7 моделей ÷ 3 кластери дає чисту attribution + reasonable sample size (≥30/ТС). 2 ТС об'єднало б різні тригер-логіки; 7 — дробить дані надто дрібно | 1 monolith / 2 ТС / 7 окремих ТС |
| **Один master + 3 satellite-файли** (а не 3 standalone) | Risk/scoring/gates/journal-schema спільні — дублювання → divergence over time | 3 повністю самостійні плейбуки (overhead) |
| **Universal intraday rule** у master, не дублювати у кожній ТС | Single source of truth для EOD-close + no-overnight | Per-ТС intraday rules (drift) |
| **Min RR 1:3 hard gate** замість поступового підвищення | Користувач явно попросив; різке підвищення planки відсіє слабкі сетапи одразу, не розтягуючи період | Soft рекомендація 1:3 (легше ігнорувати) |
| **Scoring: RR ≥ 1:5 = +2 балів** (заміна старого RR ≥ 1:3 = +2) | Бонус має бути за виняткове, не за мінімум. Інакше confluence-score завжди +2 безкоштовно | Прибрати RR з scoring зовсім (втрачаємо нагороду за асиметрію) |
| **ТС-1 переписано з swing на intraday** (H1/H4 замість H4/D) | Чорновик мав swing-DNA — конфліктувало зі стилем користувача | Зберегти ТС-1 swing як «B-варіант» (overhead, користувач не торгує swing) |
| **Тестувати по одній ТС** (не паралельно) | Паралельний бектест плутає attribution + псує дисципліну (стрибання між playbook-ами) | Паралельний (швидше, гірше) |

---

## 🐛 Проблеми й як вирішили

### Проблема: ТС-1 у початковому чорновику була swing-style
- **Причина:** на момент написання я взяв класичну Model 1 (H4 bias → H1 POI → 15m trigger) як slow/plan-driven, без явної EOD-disciplіне
- **Симптом:** користувач указав що торгує semi-scalp + intraday, і чорновик ТС-1 цьому суперечив
- **Вирішення:** TF понижено (H1/H4 + 15m/H1 POI + 5m/15m trigger), додано session-bound exit, time-stops перераховано в годинах

### Проблема: scoring matrix мав RR ≥ 1:3 = +2 балів, що ставало нонсенсом після підняття мінімуму до 1:3
- **Причина:** scoring пункт нагороджував за те, що тепер є гейтом
- **Вирішення:** замінено на RR ≥ 1:5 (новий бонус за виняткову асиметрію)

### Проблема: hook кожен раз нагадував Read-before-Edit
- **Причина:** PreToolUse Edit hook конфігурація — нормальна поведінка
- **Вирішення:** edits проходили успішно, hook лише попереджав; продовжив без додаткових Read-ів файлів які вже у контексті

---

## 📎 Артефакти

### Створено
- `~/MyVault/20-Trading/Strategies/ts-1-reversal-at-poi.md`
- `~/MyVault/20-Trading/Strategies/ts-2-session-manipulation.md`
- `~/MyVault/20-Trading/Strategies/ts-3-inner-fvg-sniper.md`
- `~/MyVault/20-Trading/Strategies/ts-tracker.md`

### Оновлено
- `~/MyVault/20-Trading/Strategies/smc-playbook-v2.md` (banner про спліт + universal intraday rule + RR 1:3 + scoring корекція + gate p.5)
- `~/MyVault/20-Trading/Checklists/pre-trade-checklist.md` (gate p.5 → RR 1:3)

### Поточні параметри (universal)
- **Style scope:** semi-scalp + intraday only
- **EOD close:** 21:00 UTC (no overnight)
- **Min RR:** 1:3 (hard gate)
- **Scoring bonus:** RR ≥ 1:5 = +2 балів
- **Базовий ризик:** 1% per trade, daily DD 3%

---

## 🎯 Наступні кроки

1. **Запустити Етап 1 бектесту першої ТС** (рекомендація: ТС-1 → ТС-2 → ТС-3)
   - Оновити статус у `ts-tracker.md`: 🟡 Queued → 🔵 Backtesting
   - Manual Bar Replay у TradingView (Ctrl+Alt+R або MCP `replay_*`)
   - Журнал у `20-Trading/Backtest/trades/YYYY-MM-DD-NN-[pair]-ts1-[model].md`
   - Sample target: 30 трейдів для ТС-1
2. **Після ≥10 трейдів** → створити `Dashboards/live-stats.md` з Dataview queries (per-ТС attribution)
3. **Після першої ТС (30+ трейдів)** → вердикт pass/pause/retire → перехід до ТС-2
4. **Активний live setup EURUSD Short 1.17880 / SL 1.18100 / TP 1.17220** — окремий трек, не входить у бектест-pipeline

---

## 🔗 Пов'язані нотатки

- [[10-Work/Projects/trading/sessions/2026-04-22-strategy-v2-rollout-phase-b]] — попередня сесія
- [[10-Work/Projects/trading/rollout-plan-strategy-v2]] — persistent rollout plan
- [[20-Trading/Strategies/smc-playbook-v2]] — master (shared rules)
- [[20-Trading/Strategies/ts-tracker]] — статус-борд
- [[20-Trading/Strategies/ts-1-reversal-at-poi]]
- [[20-Trading/Strategies/ts-2-session-manipulation]]
- [[20-Trading/Strategies/ts-3-inner-fvg-sniper]]
- [[20-Trading/Backtest/README]] — 4-етапний процес
- [[20-Trading/Checklists/pre-trade-checklist]]
