---
title: "Проект: trading — створення NS (власна SMC стратегія)"
date: 2026-04-22
tags: [work, session, trading, ns-strategy]
category: work
project: trading
status: completed
pinecone_indexed: false
---

# Проект: trading — створення NS (власна SMC стратегія)

## 🎯 Мета сесії

Побудувати **власну** торгову стратегію під назвою **NS** на базі:
1. 7 фундаментальних принципів користувача (top-down W→H1, bias, POI, ліквідність, opens DO/WO/MO, AMD, sweep)
2. Знань з NotebookLM **Trading CT** (36 PDF, повний SMC курс)

Ціль: зафіксувати стратегію у Obsidian vault як **незалежну від smc-playbook-v2** одиницю з власними risk/scoring/gates/journal, ТФ-каркасом, backtest-планом.

---

## ✅ Виконано

| Задача | Результат |
|--------|-----------|
| Розвідка джерел у NotebookLM Trading CT | Знайдено 36 PDF, виокремлено 13 найрелевантніших |
| 3 паралельні запити до NotebookLM | Витягнуто правила по top-down/BIAS/MMSM, POI/ліквідність/sweep, AMD/opens/setup |
| Синтез 7 принципів + CT знань у стратегію | 5-крокова confluence-воронка входу |
| Створення файлу `ns-strategy.md` | Повний документ 200+ рядків у `~/MyVault/20-Trading/Strategies/` |
| Оновлення `ts-tracker.md` | Додано рядок NS, live-stats block, NS-колонка в Success criteria, запис в історію |
| Запис session note | Поточний файл |

---

## 🔑 Важливі рішення (ADR)

| # | Рішення | Обґрунтування |
|---|---------|---------------|
| 1 | NS — **незалежна стратегія**, не успадковує `smc-playbook-v2` | Користувач хоче повну гнучкість: власні risk/scoring/gates без прив'язки до master |
| 2 | Style: **intraday only** | Співпадає з ТС-1/2/3; EOD 21:00 UTC; no overnight |
| 3 | Ринки: **Forex + Indices/Commodities** (DXY/SPX/Gold) | Crypto поза scope v1; indices потрібні для SMT divergence |
| 4 | Min RR **1:3** hard gate, scoring bonus за 1:5+ | Узгоджено з усіма іншими ТС — єдиний risk-standard |
| 5 | Бектест: **30 Forex + 15 Indices/Commodities** | Ширший семпл через мульти-ринок; перед go-live |
| 6 | Scoring 6-факторний (HTF POI, sweep of open, SMT, trending profile, RR≥1:5, single-session) | Оцифровано confluence — не суб'єктивне "вподобання" |
| 7 | 5-крокова воронка: Bias → POI → Sweep → LTF Shift → Entry | Кожен крок hard-gate; менше одного — skip |

---

## 🧠 Ключові правила NS (короткий reference)

- **Top-down:** D1 → H4/H1 → m15/m5/m1
- **Continuation/Reversal правило:** закриття тіла **за** рівнем = continuation; sweep wick + тіло всередині = reversal
- **NYM 00:00 NY (07:00 Kyiv)** — true daily open для Forex; лонги нижче, шорти вище
- **AMD:** Asia accum → London manip (LOKZ) → NY distr (NYKZ). Fallback: Q2 consol → Q3 manip
- **Sweep підтверджений:** Rejection Block (wick knocks BSL/SSL, body closes back) + LTF Shift
- **SMT divergence** між кореляціями посилює sweep
- **Skip:** consolidation-day ("Seek & Destroy"), high-impact news ±15min, RR < 1:3

---

## 🐛 Проблеми й як вирішили

| Проблема | Рішення |
|----------|---------|
| NotebookLM повертав `RPC rLM1Ne null result` при `use` | Причина — неправильний notebook ID (6b2bbdc5-d0eb-4715-8665-2**b7e82389a5e** замість `...2b74058fde29`). Витягнув правильний через `list --json` |
| 3 notebookLM запити тривалі | Запустив паралельно в background, синтезував по мірі готовності |
| Hook вимагав Read перед кожним Edit | Читав цільовий фрагмент перед кожною модифікацією файлу |

---

## 📦 Артефакти

**Створені файли:**
- `~/MyVault/20-Trading/Strategies/ns-strategy.md` — основний документ стратегії
- `~/MyVault/10-Work/Projects/trading/sessions/2026-04-22-ns-strategy-v1.md` — цей session note

**Оновлені файли:**
- `~/MyVault/20-Trading/Strategies/ts-tracker.md` — додано NS

**Не створені / не торкнуті (свідомо):**
- `smc-playbook-v2.md` — залишено як read-only master для ТС-1/2/3
- ТС-1/2/3 файли — без змін

**NotebookLM lineage (Trading CT, notebook id `6b2bbdc5-d0eb-4715-8665-2b74058fde29`):**
- 1-14 Top-Down Analysis, 1-5 Ринкова структура, 1-6 Ліквідність, 1-9 FVG, 1-10 OB/BB, 1-13 Бічний рух
- 2-2 MMSM/MMBM, 2-5 PO3/AMD/DO-WO-MO, 2-11 Сетапи Forex
- 3-1 BIAS, 3-4 Денні профілі, 3-5 Квартальна теорія

---

## 🔗 Пов'язані нотатки

- [[20-Trading/Strategies/ns-strategy]] — сама стратегія
- [[20-Trading/Strategies/ts-tracker]] — live-статус
- [[20-Trading/Strategies/smc-playbook-v2]] — master (reference)
- [[20-Trading/Strategies/ts-1-reversal-at-poi]] — сусідня ТС (шаблон структури)
- [[20-Trading/Strategies/correlation-table]] — для cross-market секції NS
- [[10-Work/Projects/trading/sessions/2026-04-22-strategy-split-3-ts]] — попередня сесія (спліт на 3 ТС)
- [[10-Work/Projects/trading/sessions/2026-04-21-strategy-v2-planning]] — планування v2

---

## 📍 Наступні кроки

1. Ревізія `ns-strategy.md` користувачем — перевірити чи всі 7 принципів коректно перекладені в operational rules
2. Можливо додати cross-посилання з `smc-price-action-combo.md` на NS models секцію
3. Після завершення backtest ТС-1 — розглянути чи ставити NS на 🔵 Backtesting (паралельно з ТС-2/3 чи послідовно)
4. При першому live-сетапі за NS — пройти 5-крокову воронку end-to-end як dry-run (напр. на активному EURUSD 1.17880 short з пам'яті)
