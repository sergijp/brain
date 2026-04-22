---
title: "Pre-Trade Checklist — 6-Point Gate + AM I CALM"
date: 2026-04-22
tags: [trading, checklist, pre-trade, discipline, smc, v2]
category: trading
status: active
pinecone_indexed: false
---

# ✅ Pre-Trade Checklist

**Правило:** Якщо **будь-який** пункт = FAIL → **SKIP трейд**. Жодних виключень.
**Ціль часу:** заповнити <60 сек на живому графіку. Якщо довше — setup неясний → skip.

---

## 🎯 6-Point Setup Gate

### 1. BIAS — HTF напрямок чіткий?
- [ ] H4 / D показує один напрямок (не sideways / conflict)
- [ ] Weekly Open + Monthly Open **не проти** мого напрямку
- [ ] Немає close за ключовим HTF рівнем проти bias

**FAIL якщо:** HTF bias ambiguous, Weekly/Monthly open проти, або щойно був H4 ChoCH → bias змінюється.

---

### 2. POI — маю валідну точку входу?
- [ ] H1 / H4 OB, FVG, або Breaker identified **до** того як ціна дійшла
- [ ] POI не використаний раніше (фреш, не "вживана" зона)
- [ ] POI у confluence з ключовим рівнем (WO / PWL / PWH / Q-level)

**FAIL якщо:** POI ретроспективний ("drawn after price already tagged"), або зона вже двічі мітована.

---

### 3. SWEEP — liquidity забрана?
- [ ] Ціна swept SSL / BSL / Asian H/L / equal highs-lows
- [ ] Sweep + швидке повернення (ніж інший close за рівнем)
- [ ] DXY / inter-market підтверджує (bullish DXY + short USD-пари = confluence)

**FAIL якщо:** sweep відсутній (entry на трендовому русі без liquidity grab) або ціна закрилась за рівнем (значить pushed через, не swept).

---

### 4. BOS / ChoCH на LTF — structure зламана?
- [ ] M15 або M5 показує BOS у напрямку trade
- [ ] Якщо ChoCH — є подальше підтвердження (retest + impulse)
- [ ] Inner FVG / mini-OB доступні для entry refinement

**FAIL якщо:** немає BOS на LTF (тільки HTF bias + POI = недостатньо), або BOS "кривий" (wick-only break).

---

### 5. RR — математика достатня?
- [ ] SL за структурою (не arbitrary pips) — інвалідація setup'у
- [ ] TP1 до найближчого liquidity pool / POI → **RR мінімум 1:3 (hard gate)**
- [ ] TP2 до наступного major level → цільовий RR 1:5+
- [ ] Враховано `cost_R` (~-0.1R за spread/commission)

**FAIL якщо:** RR <1:3 навіть до TP1, або SL не має structural basis.

---

### 6. PSYCHOLOGY — я у стані торгувати?
**AM I CALM?** → обведи одне:

| State | Опис | Дія |
|-------|------|-----|
| 🟢 **Calm** | Нормальний ментальний стан, фокус на процес | ✅ OK to trade |
| 🟡 **Impatient** | "Треба взяти трейд сьогодні" — FOMO | ❌ SKIP |
| 🟡 **Tilted** | Попередній loss ще сидить у голові | ❌ SKIP |
| 🔴 **Angry** | Reaction-trading, revenge | ❌ SKIP + step away 1h |
| 🔴 **Manic** | Попередній win → overconfidence, size ↑ | ❌ SKIP + stick to 1% |

**FAIL якщо:** будь-що окрім Calm.

---

## 🚫 Hard Blockers (auto-skip, не потребують 6-point перевірки)

- [ ] **News window** — red-folder event (NFP/CPI/FOMC/ECB/BoE) ±30 хв від entry → SKIP
- [ ] **Daily DD limit** — вже втрачено ≥3% за день → STOP до завтра
- [ ] **Dynamic risk gate** — 3 losses поспіль → risk 0.5% (не 1%), поки не буде 2 wins
- [ ] **Correlation cap** — якщо вже маю відкритий скорельований трейд (EUR/GBP, USD/XAU), новий = 0.5% max
- [ ] **Model retirement** — модель <40% WR на 30+ трейдах → не використовую до rework
- [ ] **Weekend / low-liquidity** — пт після 16:00 UTC, нд open перші 2 години

---

## 📝 Швидке заповнення (перед натисканням BUY/SELL)

```
Pair: ______  Direction: ___  Model: _______
[ ] 1. BIAS       [ ] 2. POI       [ ] 3. SWEEP
[ ] 4. BOS LTF    [ ] 5. RR ≥ 1:3  [ ] 6. CALM

Blockers all clear? [ ]
Scoring profile: Conservative | Standard | Aggressive
Grade: A (1%) | B (0.5%) | C (SKIP)

Entry: ____  SL: ____  TP1: ____  TP2: ____
Risk $: ____  Lot: ____
```

→ Якщо всі 6 + blockers clear → **ENTER**. Інакше → **SKIP + логувати чому**.

---

## 🔗 Пов'язані

- [[Strategies/smc-playbook-v2]] — models + scoring профілі (джерело grade logic)
- [[Backtest/template-backtest-trade]] — поля `gate_*` заповнюються сюди
- [[Checklists/weekly-review-template]] — п'ятничний ритуал (adherence review) — **TBD**
