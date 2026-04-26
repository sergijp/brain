---
title: "Проект: Trading — Бек-тест стратегії Денисенка (NotebookLM → код)"
date: 2026-04-22
tags: [work, session, trading, backtest, notebooklm, python, smc-compatible]
category: work
project: trading
status: completed
pinecone_indexed: false
---

## 🎯 Мета сесії
Витягти з NotebookLM-блокнота "Торгова стратегія" єдину стратегію з цифрами бек-тесту (Денисенко, 2022: 32.4%/3 міс, WR 80%), формалізувати її алгоритм і об'єктивно протестувати на Binance-історії.

## ✅ Виконано

1. **NotebookLM analysis** — переглянув 29 джерел блокнота "Торгова стратегія", знайшов 17 стратегій, ТОП-5 за прибутковістю
2. **Витяг стратегії** — через `notebooklm source fulltext` + targeted `ask` отримав повний алгоритм Impulse-Breakdown-Reclaim
3. **Проект бек-тесту** створено в `~/AI/Projects/Trading/backtest_denysenko/`:
   - `data_loader.py` — ccxt Binance OHLCV, CSV cache
   - `pattern.py` — детектор патерну (impulse + breakdown + reclaim, LONG + SHORT)
   - `backtest.py` — симуляція з TP 35/50% partial, 3 режими SL, комісії 0.2%
   - `run.py` — grid search
4. **Дані:** 15 USDT-пар (BTC, ETH, BNB, XRP, ADA, DOGE, DOT, MATIC, LTC, LINK, AVAX, ATOM, UNI, IOTA, XLM) × 2 TF (D1, W1)
5. **Grid search:** `{k: 1.5/2.0/2.5} × {SL: struct/fixed/hybrid} × {Q4'21, Q1'22, Q2'22, OOS 2024-2026}`
6. **Записано патерн IBR** у `20-Trading/Strategies/impulse-breakdown-reclaim.md`

## 🔑 Важливі рішення (ADR)

| Рішення | Причина | Альтернатива |
|---------|---------|-------------|
| CSV cache замість parquet | pyarrow не встановлений, CSV достатньо швидкий | встановити pyarrow |
| ccxt з Binance | безкоштовний, 1000 барів/запит, підтримує spot | Binance Vision dumps |
| TP 35%/50% як % gain від entry | природня інтерпретація для D1/W1 крипто | retrace ratio (не підтвердилось) |
| SL 3 режими (struct, fixed, hybrid) | автор не дав формулу — тестую всі розумні | тільки один |
| Комісії 0.2% roundtrip | реальний Binance spot fee | ігнорувати (завищило б цифри) |
| 15 USDT-пар | широка вибірка, уникає cherry-picking | тільки DOGE+IOTA з прикладів |

## 📊 Результати бек-тесту

**Головне:** заявлене Денисенком не відтворюється на портфелі.

| Метрика | Заявлено | Фактично |
|---------|----------|----------|
| Win rate | 80% | 30-45% (up to 67% на DOGE W1) |
| Return / 3 міс | +32.4% | від -315% (Q1'22) до +151% (Q4'21) |
| Best single trade | +26% | +42% ✅ |

**Найкращі конфігурації:**
- D1, k=1.5, SL=fixed → 351 угода / 2 роки, WR 30.8%, sum +369%
- D1, k=2.5, SL=struct (Q4 2021 bull) → WR 63.6%, sum +87%/3міс
- DOGE W1, k=2.0, SL=struct → WR 66.7%, sum +102%/5років

## 🐛 Проблеми й як вирішили

### Проблема: W1 генерує майже 0 сигналів у 3-міс. вікнах
- **Причина:** 12-13 W1-барів замало для сформованого impulse+breakdown+reclaim патерну
- **Вирішення:** переключитись на D1 як первинний TF (збігається з Miota-прикладом автора)

### Проблема: parquet cache не пишеться
- **Причина:** pandas 3.0 потребує pyarrow/fastparquet
- **Вирішення:** CSV cache (простіше, розмір файлів прийнятний)

### Проблема: structural SL дає великі збитки у bear
- **Причина:** breakdown low часто 15-25% від entry → один стоп вбиває 3-5 виграшів
- **Вирішення:** fixed -10% SL показав кращі результати майже в усіх фазах

## 💡 Інсайти

1. **Стратегія має позитивну експектацію тільки в bull-фазі** — без HTF regime-фільтру (BTC > SMA200) використовувати не можна
2. **Патерн сам по собі валідний** — найкращі угоди +42%, що підтверджує механіку sweep+reclaim. Проблема — hit rate
3. **SMC конвергенція:** IBR ~= ChoCH → BOS-retest. Можна інтегрувати в мій існуючий workflow як додатковий сигнал
4. **Short-сторона симетрично програє** у bull — не компенсує лонги

## 📎 Артефакти

- Проект: `~/AI/Projects/Trading/backtest_denysenko/`
- Звіт: `~/AI/Projects/Trading/backtest_denysenko/REPORT.md`
- Дані: 30 CSV файлів у `data/`
- Результати: `results/trades_*.csv` (25+ файлів), `summary_1d.csv`, `summary_1w.csv`
- Патерн як стратегія: `~/MyVault/20-Trading/Strategies/impulse-breakdown-reclaim.md`

## 🔗 Пов'язані нотатки

- [[20-Trading/Strategies/impulse-breakdown-reclaim]] — формалізований патерн IBR
- [[20-Trading/Strategies/smc-price-action-combo]] — інтеграція з основною стратегією
- [[10-Work/Projects/trading/project-overview]]

## 🎯 План далі

- [ ] Додати HTF regime-фільтр (BTC SMA200) і перевірити WR boost
- [ ] Перевірити IBR на H4/H1 для інтрадей-сетапів
- [ ] Порівняти IBR-входи з моїми живими SMC-сетапами (чи збігаються?)
- [ ] Написати Pine Script індикатор для автоматичного розпізнавання IBR на TradingView
