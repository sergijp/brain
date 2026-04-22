---
title: "Retrospective Analysis — TC-1/2/3 Pine findings + 6-gate filter hypothesis"
date: 2026-04-22
tags: [trading, backtest, analysis, retrospective, smc, ts-1, ts-2, ts-3]
category: trading
status: analysis
pinecone_indexed: false
---

# 🔎 Retrospective Analysis — що дав Pine і що дасть discretionary filter

**Контекст:** 17 Pine-ітерацій за сесію 2026-04-22 (TC-1: 5, TC-2: 3, TC-3: 6 + cross-pair). Результати зафіксовано у трьох backtest-файлах. Нижче — **висновки + прогноз** що дасть manual 6-gate filter поверх цього.

---

## 📊 Що Pine вже показав

| ТС | Best Pine config | Sample | WR | PF post-cost | Gross edge? |
|----|------------------|--------|----|----|----|
| **TC-1** v3 (full rules) | full rules, qty 10% | 24 | 37.5% | 0.79 | Yes (1.135 comm=0) |
| **TC-2** v3 (Asian sweep) | best of 3 | 11 | 0% | 0 | No |
| **TC-3** v5 EURUSD | shorts-only no bias | 10 | 50% | 1.43 | Yes, але cross-pair FAIL |

**3 різні failure-modes:**
1. TC-1: mechanical edge є, але тонкий — commission з'їдає
2. TC-2: Pine — wrong tool (edge discretionary)
3. TC-3: cross-pair інваліднув period cherry-pick

---

## 🎯 Гіпотеза: чи 6-gate filter urятує TC-1?

### Gate-by-gate breakdown для Pine TC-1 v3

| Gate | Pine логіка v3 | Manual філтер додає |
|------|---------------|---------------------|
| 1. **Bias** | H1 EMA50>EMA200 + close > EMA200 | D/H4 BOS структура, Weekly Open, монтечлі confluence |
| 2. **POI** | `last_ph` (pivot high) | Valid OB/FVG, не violated, in premium/discount |
| 3. **Sweep** | pierce ≥ 5 pips + closeback ≥ 50% | Equal highs (BSL) vs random wick, Asian/prev session H/L grade |
| 4. **BOS** | `close > last_ph` | Impulse quality (swing size, volume), not stale |
| 5. **RR** | ≥ 1:3 hard gate | Same, але відштовхуєшся від realistic TP (не nearest opposite pivot чисто) |
| 6. **Psychology** | — (Pine не емулює) | "Am I calm?" — retrospective proxy: чи розташування у розкладі, чи не overtrade |

### Прогноз applied filter на Pine v3 trades

**Очікуваний розподіл 24 трейдів під filter:**

| Результат filter | ~% очікуваних | Trade count | Logic |
|------------------|---------------|-------------|-------|
| ✅ Pass (A-grade, 1% risk) | ~25% | **6** | Clean bias + liquidity + BOS impulse + RR |
| 🟡 Pass (B-grade, 0.5% risk) | ~30% | **7** | Mixed signals, но сетап valid |
| ❌ Skip (C-grade) | ~45% | **11** | Bias conflict, weak sweep, stale BOS |

### Expected metrics post-filter

Аналогічні стратегіям які **фільтрують по якості**, очікуваний improvement:
- WR: 37.5% → **~50-55%** (B-grade skips прибирають marginal losers)
- PF comm=0: 1.135 → **~1.4-1.7** (А-grade concentrates edge)
- Sample: 24 → **13** (A+B) → все ще замало для 30+ requirement
- **Post-cost PF:** 0.79 → **~1.0-1.15** (edge існує, ледь вище breakeven)

### Чи це достатньо для go-live?

Порівняння з critериями README Етап 4:
- Manual: expectancy > +0.3R — **поточно ~+0.1R, недостатньо**
- Manual: WR > 40% при RR 1:2+ — **55% * RR 3:1 = ПРОХОДИТЬ**
- Pine PF > 1.3 — **post-filter ~1.4-1.7 ПРОХОДИТЬ comm=0, post-cost ~1.1 ПРОВАЛ**

**Прогноз: навіть під discretionary filter TC-1 Pine-proxy не проходить cost hurdle.** Треба змінювати:
- RR 1:3 → **1:5** (менше trades, більший win, commission менш impactful relatively)
- Бажано spread ≤0.3 pip broker (ECN) — 50% of our commission calc
- Cross-pair — GBPUSD з різним regime

---

## 📋 TC-1 recommended next spec changes (v2.0 playbook edit)

Базуючись на 17 ітераціях:

1. **RR 1:3 → 1:5 hard gate** (TC-1 spec rule R6 edit)
2. **Skip setups з SL > 15 pips** (risk-per-trade ceiling → наш max_sl_pips input)
3. **Tight SL за sweep candle low, НЕ pivot low** — підтверджено TC-3 v2/v3 результатами
4. **Enter via market at BOS close + FVG retest, не limit-at-pivot** — limit often не fills
5. **Session concentration:** London KZ only, NY cuts volatility

Якщо ці 5 змін + manual 6-gate → оцінка:
- Sample може зменшитись до 10-15 trades / 5.5m → замало для statistics
- **→ Extend to 2-year window на H1 для sample 30-40**
- Або **cross-pair mix**: EURUSD + GBPUSD + XAUUSD рівнопаралельно

---

## ⚠️ Ключові уроки для всіх 3 ТС

### 1. Short edge на EURUSD = trend-following reversed
TC-3 v5 (shorts only) гарно спрацював тому що **EURUSD був bearish за period**. На GBPUSD (bullish period) той самий код дав PF 0.39. Це не edge — це disguised trend-follower.

**Implication:** Cross-pair validation обов'язкова перед claim edge. Single-pair single-period результат = лотерея.

### 2. TradingView commission inputs важить
Pine `commission_value=0` у коді НЕ перемагає `Strategy Properties → Commission: $5/order` у UI. TV UI overrides Pine. Для reproducible benchmark — обов'язково відкрити Strategy Properties і встановити commission=0 перед кожним добавленням strategy to chart.

### 3. Discretionary елементи критичні для SMC
TC-2 (session manipulation) — 11 trades, 0% WR у Pine. Причина: **sweep grade** (equal highs vs random wick), **OB quality**, **daily profile** НЕ кодифікуються механічно. TC-2 едge тільки у manual.

### 4. Commission dominates в FX при малому qty
При qty=10% ($1000 position) у EURUSD: 1 pip = $0.1. Commission $5/order = 100 pips рівнозначно. Тобто при SL 15 pips + TP 30 pips, commission коштує 3× the SL. Це mathematically impossible to profit.

**Fix:** або більший qty (100% = normal leverage), або fraction commission (0.01-0.05%), або нормальний FX broker 0.5 pip spread/round-trip = 5 ticks.

### 5. H1 занадто sparse для FVG signals
TC-3 на H1: 13 trades / 2.3 роки. На 15m: 10 trades / 5.5m. **H1 не підходить для intraday scalping**. TC-1 spec правильний: trigger TF 15m або 5m.

---

## 🎯 Concrete next steps (prioritized)

### A. Manual Bar Replay — це єдиний шлях (як README Етап 1 і каже)
**Process у TradingView app (швидше ніж через MCP):**
1. Open EURUSD 15m, Ctrl+Alt+R для Bar Replay
2. Pick date 6m ago (e.g. 2025-10-15)
3. Crop right side, hit play/step
4. Each trade:
   - Fill YAML template [[template-backtest-trade]]
   - 6-gate checklist
   - Outcome після step-through
5. Sample: 30 trades мін (TC-1 requires 30+)
6. After 30 — compute WR/PF/expectancy/adherence

**Ціль: 30 trades за 3-4 сесії x 1-2 год.**

### B. Якщо manual passes expectancy > +0.3R → крок Pine v4 rebuild
- RR 1:5
- Tight SL per TC-3 findings
- Market entry post-FVG retest
- Cross-pair XAUUSD mandatory

### C. Якщо manual fails TC-1 → moving на TC-3 manual
Але TC-3 теж не passed cross-pair Pine. Priority:
1. TC-1 manual first (most structured)
2. Якщо TC-1 WR < 40% manual → rework spec
3. TC-2 пауза до TC-1 resolve

---

## 🔗 Related

- [[pine-ts1-2026-04-22]] — TC-1 Pine 5 iterations
- [[pine-ts2-2026-04-22]] — TC-2 Pine 3 iterations
- [[pine-ts3-2026-04-22]] — TC-3 Pine 6 iter + cross-pair
- [[ts-tracker]] — dashboard
- [[Backtest/README]] — 4-stage validation process
- [[Backtest/template-backtest-trade]] — journal YAML template
