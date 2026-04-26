---
title: "Supply/Demand — Sam Seiden (RBR/DBD)"
date: 2026-04-22
tags: [trading, strategy, supply-demand, seiden, positional, swing, non-smc]
category: trading
status: draft
journal_tag: sd-seiden
pinecone_indexed: false
---

# 📊 Supply/Demand — Sam Seiden (RBR/DBD)

**Філософія:** фундамент institutional-pricing — зони, де **banks/institutions залишили незавершені ордери**. Base (тісна консолідація) + сильний leg-out = fresh zone. Ціна повертається до зони → новий leg у напрямку оригінального імпульсу. Не-SMC підхід: працює **без вимоги HTF BOS**, без OB термінології. Джерело: Sam Seiden (OnlineTradingAcademy).

**Незалежна стратегія.** Self-contained (власні risk/scoring/gates).

**Style:** positional / swing | **Min RR:** 1:3 (hard gate) | **Hold:** до TP або invalidation (multi-day)

---

## 🎯 Ідея
- Зона, де ціна провела **2-6 тісних свічок** (base) і потім **різко пішла** (leg) = доказ великого institutional ордера, який не повністю заповнено
- Коли ціна повертається до такої зони — лишилися "непридбані" (для demand) або "непродані" (для supply) ордери → висока імовірність реакції
- **Fresh zone** (не ретестована) = high probability; **stale zone** (вже торкалася) = low probability → skip

---

## 🧩 4 Патерни зон

| Патерн | Повна назва | Тип | Напрямок |
|--------|-------------|-----|----------|
| **RBR** | Rally–Base–Rally | Demand | Continuation up |
| **DBD** | Drop–Base–Drop | Supply | Continuation down |
| **DBR** | Drop–Base–Rally | Demand | Reversal up |
| **RBD** | Rally–Base–Drop | Supply | Reversal down |

---

## ⏱️ Робочі таймфрейми
- **Zone identification:** **D1** (primary) + **H4** (refinement)
- **Entry TF:** **H1** (limit order placement)
- **Context:** W1 bias (для positional trades)

---

## 📐 Алгоритм LONG (demand RBR/DBR, дзеркально для SHORT)

### Крок 1 — знайти valid base
1. На D1/H4 знайти **base** (консолідація):
   - **2-6 свічок** з малим body range
   - Body кожної свічки ≤ 50% її total range (wicks дозволені)
   - Max base width: 6 свічок (якщо більше = accumulation, інша парадигма)

### Крок 2 — valid leg-out
2. Leg-out свічка (одразу після base):
   - Body ≥ 1.5× ATR(14) на цьому TF
   - Close у дальній third свічки (strong close)
   - Gap up вітається але не обов'язковий

### Крок 3 — визначити zone edges
3. **Proximal edge** (ближня до ціни):
   - Для RBR/DBR (demand): **highest body** base-свічок
   - Для DBD/RBD (supply): **lowest body** base-свічок
4. **Distal edge** (дальня):
   - Для demand: **lowest wick** base-свічок
   - Для supply: **highest wick** base-свічок

### Крок 4 — score zone (Freshness + Strength)
5. **Freshness:** ×2 якщо ціна не повертається у зону з моменту leg-out (fresh = неторкана)
6. **Strength:** leg-out ≥ 2.0×ATR → strong | 1.5-2.0×ATR → medium
7. **Alignment:** zone відповідає HTF bias (W1 trend) → +1

### Крок 5 — limit entry
8. Поставити **buy limit** на **proximal edge** зони
9. **SL:** **distal edge − 0.1×ATR(14, D1)** buffer
10. **TP1 (50%):** proximal + 1×base-height → BE
11. **TP2 (30%):** **opposite fresh zone** (найближча supply для лонгу)
12. **TP3 (20%):** HTF swing high / monthly pivot

---

## 🚦 Entry Gates

| # | Умова | Причина skip |
|---|-------|--------------|
| G1 | Zone ретестована ≥ 1 раз | Stale — edge втрачено |
| G2 | Leg-out < 1.5×ATR(14) | Слабкий імпульс, institutional intent під сумнівом |
| G3 | Base > 6 свічок | Accumulation/distribution — інший патерн |
| G4 | Zone у напрямку проти W1 structure | Counter-trend, low RR |
| G5 | RR до nearest opposite zone < 1:3 | Hard gate RR |
| G6 | Zone overlap з major news resistance (recent CPI/FOMC spike) | Artificial zone |

---

## 📊 Scoring (0-10)

| Фактор | Бали |
|--------|------|
| Freshness (zone не ретестована) | +3 |
| Leg-out ≥ 2.0×ATR (strong impulse) | +2 |
| HTF bias (W1) aligned | +2 |
| Base: 2-3 свічки (tight) vs 4-6 (wider) | +1 tight / 0 wider |
| Confluence з round number / HTF S-R | +1 |
| Gap у leg-out | +1 |

**Гейти:** ≥7 full / 5-6 half / <5 skip.

---

## 🛡️ Risk

- **Ризик/угоду:** 1% = $100 на $10k
- **Max open positions:** 3 (різні пари, uncorrelated)
- **Correlation cap:** max 1 лонг на USD-quote pair (EURUSD + GBPUSD = 1 position бюджет)
- **Portfolio heat:** total open risk ≤ 3% ($300)

### Формула лоту (FX):
```
Lot = $100 / (SL_pips × $10)  ← для 1.0 standard lot
```

---

## 🎯 Приклад (EURUSD, D1 RBR demand zone)

D1 chart EURUSD:
- 2026-02-10 — base: 3 свічки consol 1.0820-1.0845
- 2026-02-13 — leg-out D1 candle: body 1.0850 → 1.0950 (+100 pips, ATR(14) = 65 pips → 1.54×ATR)
- Zone: proximal 1.0845, distal 1.0820
- Freshness: ✅ не ретестована до 2026-04-15
- 2026-04-18 — ціна повертається до 1.0848 area
- **Entry (limit):** 1.0845 | **SL:** 1.0818 (distal − buffer) = 27 pips | **TP1:** 1.0870 (BE) | **TP2:** 1.0950 (prev high) | **TP3:** 1.1030 (H4 supply)
- Lot: 0.37 ($100 / (27 × $10))
- RR TP2: 105/27 ≈ 1:3.9 ✅

---

## 🚫 Коли НЕ торгувати

- **News-driven spike candles** як leg-out (artificial strength, немає real institutional demand)
- **Earnings season** для indices (stock-specific flow спотворює)
- **Holiday thin weeks** (Christmas, mid-August) — false base pattern
- **Recent zone** (leg-out менше ніж 3 торгові дні тому) — занадто "raw"
- Пари у backwardation від твоєї core watchlist

---

## 🏷️ Journal tag
```yaml
ts: sd-seiden
zone_type: rbr | dbd | dbr | rbd
tf: d1 | h4
freshness: fresh | once_tested
```

---

## 📌 Status
⚪ **Draft** — створено 2026-04-22. Потребує manual Bar Replay (zones hard to automate у Pine). Тест: 30 трейдів через EURUSD/GBPUSD/XAUUSD/USDJPY D1.

---

## 🔗
- [[20-Trading/Strategies/ts-tracker]]
- [[20-Trading/Strategies/smc-playbook-v2]] — overlap у OB, але different rules
- [[20-Trading/Backtest/README]]
