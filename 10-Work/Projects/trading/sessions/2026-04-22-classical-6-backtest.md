---
title: "Проект: Trading — Бек-тест 6 класичних стратегій + HTF filter + ансамбль"
date: 2026-04-22
tags: [work, session, trading, backtest, python, classical-strategies, ensemble]
category: work
project: trading
status: completed
pinecone_indexed: false
---

## 🎯 Мета сесії
Продовжити роботу з NotebookLM-блокнота "Торгова стратегія": витягти 6 класичних стратегій з конкретними алгоритмами (VWAP, RSI, MA Cross, Pivots, Breakout, Bollinger MR), формалізувати і бектестувати у тому самому фреймворку що IBR. Додати HTF regime filter і ансамбль для знаходження edge.

## ✅ Виконано

1. **Аналіз джерел** через NotebookLM — витягнуто параметри для 6 стратегій
2. **[`strategies.py`](strategies.py)** (~500 рядків) — 6 стратегій з єдиним інтерфейсом:
   - VWAP (anchored 6-bar + 1.9×ATR breakout)
   - RSI (14, thresholds 30/70)
   - MA_Cross (SMA 50/200 golden/death)
   - Pivots (classic: P = (H+L+C)/3, S1/R1 daily)
   - Breakout (Donchian 20-bar high + volume > 1.5×SMA)
   - BB_MR (Bollinger 20/2σ mean reversion)
3. **[`run_classical.py`](run_classical.py)** — оркестратор H4 + D1, 2024-2026
4. **[`htf_filter.py`](htf_filter.py)** — BTC D1 SMA200 regime (bull/bear) з post-filter для trades і setups
5. **[`run_filtered.py`](run_filtered.py)** — повторний прогон всіх стратегій + IBR з HTF filter
6. **[`ensemble.py`](ensemble.py)** — confluence detector (≥K стратегій у вікні ±N барів, TP 10% / SL 5%)
7. **Obsidian:** [[20-Trading/Strategies/classical-6-comparison]]

## 🔑 Важливі рішення (ADR)

| Рішення | Причина | Альтернатива |
|---------|---------|-------------|
| Post-filter замість inline regime param | Простіше — не треба торкатись 6 функцій | Inline param (cleaner API, але більше коду) |
| BTC SMA200 на D1 для regime | Класичний bull/bear маркер | SMA100, EMA200, BTC EMA cross |
| Confluence window ±2 H4 бари (8 год) | Природній захоплення "same day" сигналів | ±1 бар (занадто вузько), ±4 (занадто широко) |
| Ensemble TP 10% / SL 5% (RR 1:2) | Середні з прибуткових стратегій | Dynamic ATR-based |
| All-in per-trade модель | Для порівняння стратегій | 1% risk per trade (realistic) |

## 📊 Головні результати

**Baseline (без filter):**
- 🥇 IBR D1 k=1.5 fixed: +369% sum, WR 30.8% (351 угода)
- 🥈 H4 MA_Cross: +357%, WR 26.2% (397 угод)
- 🥉 H4 RSI: +164%, WR 49.2% (1111 угод)
- Pivots і BB_MR — розгромні на обох TF попри високий WR (до 56%)

**HTF filter (BTC > SMA200 D1):**
- ✅ Breakout D1: -16% → **+291%** (Δ +307%) — ГОЛОВНИЙ виграш
- ✅ MA_Cross H4: +357% → **+453%** (Δ +96%)
- ✅ Pivots H4: -1615% → -1130% (Δ +484, але все ще мінус)
- ❌ RSI H4: +164% → -225% — filter вирізає sweep-reclaims
- ❌ IBR k=1.5: +369% → +155% — filter режет валідні bull-ретест сигнали

**Ансамбль (3+ стратегій у window ±2 H4 бари):**
- n = 469 угод / 2 роки
- WR 41.2%, Sum +141%
- Стабільно, але **програє MA_Cross alone (+357%)** → confluence зайво обмежує
- Per-symbol edge: **ETH +155, LINK +140, XLM +90** vs IOTA -176, ADA -160

## 💡 Ключові інсайти

1. **Мean reversion у крипто — пастка.** BB_MR дає 56% WR на H4 але -1235% sum. Класична asymmetric losses proble у трендовому ринку.
2. **HTF filter не універсальний.** Допомагає "нейтральним" стратегіям (Breakout, Pivots, VWAP). Шкодить трендовим (RSI, MA_Cross, IBR) — бо ті вже incorporate trend.
3. **Ансамбль confluence гірший за single-strategy best.** Пересіктя сигналів не означає "більший edge" — скоріше "узгоджена впевненість у середньому сигналі".
4. **Per-symbol selectivity** — ETH/LINK/XLM стабільно прибуткові у всіх тестах. IOTA/ADA/XRP — хронічно збиткові. Якщо фокусуватися тільки на top-3 символах — edge сильно посилюється.
5. **Pivot Points НЕ ПРАЦЮЄ в крипто.** TP (до P) близький, SL (3%) далекий → негативна expectancy попри 53% WR.

## 📈 Фінальний рейтинг best configs

| # | Конфігурація | Sum | WR | n | Коментар |
|---|--------------|-----|-----|---|----------|
| 1 | H4 MA_Cross + HTF filter | +453% | 26% | 199 | Найкращий overall |
| 2 | D1 IBR k=1.5 fixed (no filter) | +369% | 31% | 351 | High volatility |
| 3 | H4 MA_Cross (no filter) | +357% | 26% | 397 | Baseline |
| 4 | D1 Breakout + HTF filter | +291% | 32% | 267 | Filter transformed |
| 5 | D1 IBR k=2.0 fixed + HTF filter | +237% | 35% | 91 | Safer IBR |
| 6 | H4 RSI (no filter) | +164% | 49% | 1111 | Stable |
| 7 | Ensemble 3+ window=2 | +141% | 41% | 469 | Diversified |

## 🐛 Проблеми й вирішення

### Проблема: `pd.infer_freq` повертає None для нерегулярних інтервалів (крипто 24/7 немає gap)
- **Причина:** у Pivots зробив залежність від `infer_freq` для bars_per_day
- **Вирішення:** переключив на resample("1D") → автоматично обробляє будь-який інтервал

### Проблема: плаваюча точність у Trade.return_pct
- **Причина:** pandas float64 операції
- **Вирішення:** `round(net, 3)` у `_mk_trade`

### Проблема: Ensemble greedy dedup пропускав сигнали
- **Причина:** індекси не скидались після фільтрації по символу
- **Вирішення:** `.reset_index(drop=True)` перед greedy loop

## 📎 Артефакти

- Код: `~/AI/Projects/Trading/backtest_denysenko/`
- Нові файли: `strategies.py`, `htf_filter.py`, `run_classical.py`, `run_filtered.py`, `ensemble.py`
- Звіти: `CLASSICAL_REPORT.md`
- Угоди: `results/classical_trades_*.csv`, `filtered_trades_*.csv`, `ensemble_trades.csv`
- Summary: `results/classical_summary.csv`, `filtered_summary.csv`, `ensemble_confluences.csv`

## 🔗 Пов'язані

- [[20-Trading/Strategies/classical-6-comparison]] — повний аналіз результатів
- [[20-Trading/Strategies/impulse-breakdown-reclaim]] — IBR reference
- [[10-Work/Projects/trading/sessions/2026-04-22-denysenko-backtest]] — IBR session

## 🎯 План далі

- [ ] **Per-symbol strategy assignment:** тестувати чи різні стратегії працюють на різних символах (BTC → trend, ETH → MR, etc.)
- [ ] **Pine Script для MA_Cross + HTF filter + RSI confluence** на TradingView
- [ ] **Live тест:** запустити H4 MA_Cross на paper account 1 місяць — валідація OOS
- [ ] **Integration з SMC workflow:** використати класичні як screener для моїх SMC-сетапів
- [ ] **Position sizing:** переписати бек-тест у 1% risk/trade модель → realistic account curves
