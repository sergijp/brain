---
title: "Бектест — 4-етапний процес валідації SMC v2"
date: 2026-04-22
tags: [trading, backtest, process, smc, v2]
category: trading
status: active
pinecone_indexed: false
---

# 🧪 Бектест SMC v2 — 4-етапний процес

**Мета:** Довести статистичний edge стратегії `[[Strategies/smc-playbook-v2]]` **до** переходу на реальні гроші. Без цієї валідації стратегія = спекуляція.

**Правило №1:** Якщо якась цифра з "Go-Live критеріїв" (секція внизу) не виконана — **залишаємось у paper**, не йдемо у live.

---

## 📍 Де ми зараз

| Етап | Status | Результат |
|------|--------|-----------|
| 1. Manual Bar Replay | ⏳ Не розпочато | — |
| 2. Pine Script `strategy()` | ⏳ Не розпочато | — |
| 3. Paper Forward Test | ⏳ Не розпочато | — |
| 4. Go-Live Decision | 🔒 Заблоковано до завершення 1-3 | — |

Статус оновлюється наприкінці кожної сесії бектесту.

---

## 🎯 Етап 1 — Manual Bar Replay (1-2 тижні)

### Інструментарій
- **TradingView Bar Replay** (`Ctrl+Alt+R` або через MCP `mcp__tradingview__replay_*`)
- **Journal:** окремий файл на кожен трейд у `20-Trading/Backtest/trades/YYYY-MM-DD-NN-[pair]-[model].md` за шаблоном `[[Backtest/template-backtest-trade]]`

### Обсяг
- **6 місяців історії** на парах з watchlist (EURUSD, GBPUSD, XAUUSD як pilot)
- **Мінімум 50 трейдів**
- Розподіл по моделях: мінімум 5 трейдів на модель (щоб порівняти WR)

### Правила проведення
1. **Один трейд за раз, повна YAML-картка** — заповнюється перед натисканням "наступна свічка"
2. **Ніякого look-ahead** — замкнути права сторона replay перед аналізом
3. **Scoring профіль** фіксується ДО входу (не змінюється постфактум)
4. **Ціль часу:** ≤10 хв/трейд — якщо довше, значить стратегія надто amіbiguous → додати правило
5. **Skip** — якщо setup не проходить 6-point gate, пишемо у журнал "skipped + why" (це теж data)

### Метрики на виході (мінімум)
- Win Rate % (total + by model + by session + by grade)
- Avg R (wins vs losses)
- Expectancy: `(WR × avgW) - (LR × avgL)`
- Max Drawdown (% від початкового $10k)
- Max consecutive losses
- Adherence % (скільки трейдів виконано за правилами без deviation)

### Red flags → стоп бектесту, повернення до playbook
- Модель <40% WR на 10+ трейдах → кандидат на retirement
- Adherence <80% → правила нечіткі, треба уточнити
- Expectancy <0 після 30 трейдів → стратегія не має edge, rework

---

## 🤖 Етап 2 — Pine Script `strategy()` (2-4 тижні)

### Що кодифікуємо
Тільки **автоматизовувані фільтри** (SMC discretionary elements — OB validity, POI choice — залишаються manual):

| Елемент | Pine-реалізація |
|---------|-----------------|
| HTF bias | EMA(200) slope + H4 pivot structure break |
| FVG detection | 3-бар imbalance: `high[2] < low[0]` або навпаки |
| BOS / ChoCH | Break of pivot high/low з `ta.pivothigh/pivotlow` |
| News window | External session filter (ручне відключення ±30 хв) |
| Session filter | London (07-09 UTC) + NY (12-14 UTC) killzones |
| Risk sizing | Fixed 1% per trade з dynamic: 3L → 0.5% |

### Запуск
- **Діапазон:** 2-5 років історії на EURUSD (основа) + 1 рік cross-validation на GBPUSD/XAUUSD
- **Built-in report:** Net P&L, Profit Factor, Max DD, Win %, Sharpe
- **Property Export:** `List of Trades` → CSV → порівняти з manual bar replay

### Обмеження
Pine **не замінює** manual test — він валідує чи автоматизовувані фільтри самі по собі дають позитивне expectancy. Якщо Pine показує edge → manual додає ще одну "lens" зверху. Якщо Pine у збитку — перевірити чи edge взагалі в фільтрах, чи тільки у discretionary entry.

### Артефакти
- `Backtest/pine-mvp-2026-04-21.md` (існує)
- `Backtest/pine-v4-plan-2026-04-21.md` (існує)
- Додати: `Backtest/pine-results-YYYY-MM-DD.md` — executions report

---

## 📝 Етап 3 — Paper Forward Test (1 місяць мінімум)

### Формат
- **Demo-рахунок** або **paper journal** (той самий YAML template як у Етапі 1)
- Тільки за правилами v2 playbook — **жодного деваціонного трейду**
- **Мінімум 20 трейдів** за період (пріоритет якість > кількість, але <20 недостатня вибірка)

### Що відрізняється від Етапу 1
- Жодного look-ahead ризику (це live ціна)
- Реальний psychology stress (навіть на paper)
- Реальна execution: spread, slippage, missed fills

### Метрики
Ті самі що Етап 1 + додатково:
- **Adherence %** (за полем `rule_adherence` у journal) — ціль ≥90% full
- **Psychology log** — скільки трейдів з `emotion: Tilted/Angry/Manic/Impatient` vs `Calm`
- **Correlation Manual-vs-Paper:** результати мають бути в межах ±20% від Етапу 1

---

## 🟢 Етап 4 — Go-Live Critеrії

**Перехід на реальні гроші ТІЛЬКИ якщо ВСІ чекбокси виконано:**

### Статистика (hard rules)
- [ ] Manual backtest (Етап 1): expectancy **> +0.3R**
- [ ] Manual backtest: WR **> 40%** при середньому RR 1:2+
- [ ] Manual backtest: Max DD **< 15%** капіталу
- [ ] Pine `strategy()` (Етап 2): Profit Factor **> 1.3**
- [ ] Paper (Етап 3): WR у межах ±20% від manual
- [ ] Paper: adherence **≥ 90%** full

### Процесні (hard rules)
- [ ] Weekly review ritual проведено **≥4 тижні** поспіль
- [ ] Жодна модель не у retirement state (<40% WR на 30+ трейдів)
- [ ] Pre-trade checklist заповнюється **<60 сек** на живому графіку
- [ ] Alert-creation workflow (`mcp__tradingview__alert_create`) стабільно працює

### Якщо хоча б один пункт FAIL
→ **Не йдемо live.** Діагностуємо що провалилось:
- Низька WR → модель/фільтри потребують rework
- Низьке expectancy → RR ratio замало → переглянути TP framework
- Низька adherence → правила нечіткі, психологія слабка → checklist + review ritual
- Висока кореляція з Paper відсутня → різниця між replay та live → додатковий місяць paper

---

## 📐 Orієнтовний timeline

| Фаза | Тривалість |
|------|-----------|
| Етап 1 (manual 50 трейдів) | 1-2 тижні |
| Етап 2 (Pine coding + backtest + review) | 2-4 тижні |
| Етап 3 (paper forward 1 міс) | 4 тижні |
| Go-live decision + preparation | 1 тиждень |
| **Разом до реальних грошей** | **~6-8 тижнів** |

Якщо фаза провалюється → timeline розтягується. Немає ring fence по часу — тільки по критеріях.

---

## 🔗 Пов'язані

- [[Strategies/smc-playbook-v2]] — стратегія яку тестуємо
- [[Backtest/template-backtest-trade]] — YAML шаблон журналу
- [[Checklists/pre-trade-checklist]] — 6-point gate (використовується у Етапі 1+3)
- [[10-Work/Projects/trading/rollout-plan-strategy-v2]] — origin rollout plan
