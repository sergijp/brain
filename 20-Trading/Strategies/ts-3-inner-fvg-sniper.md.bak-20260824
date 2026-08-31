---
title: "ТС-3 — Inner FVG Sniper"
date: 2026-04-22
tags: [trading, strategy, smc, ts-3, fvg, sniper, scalp]
category: trading
status: queued
parent: "[[20-Trading/Strategies/smc-playbook-v2]]"
journal_tag: ts-3-fvg-sniper
pinecone_indexed: false
---

# 📊 ТС-3 — Inner FVG Sniper

**Філософія:** opportunistic semi-scalp precision-entries на свіжих FVG усередині impulse leg після LTF BOS. Дуже tight SL → асиметричний RR 1:4-1:6. Висока частота setups, max 2 години у позиції.

**Inherits from:** [[20-Trading/Strategies/smc-playbook-v2]] (risk, scoring, gates, journal, EOD-close rule)

**Style:** semi-scalp | **Min RR:** 1:3 (типово 1:4-1:6)

---

## 🎲 Включена модель

| # | Модель | Розширення |
|---|--------|------------|
| 3 | **Inner FVG after LTF BOS** | + 5m execution + ICT Optimal Trade Entry (OTE) zone |

**Чому окремо:** тригер відрізняється кардинально — не reversal на готовому POI (ТС-1) і не sweep у KZ (ТС-2), а **continuation entry усередині свіжого impulse**. SL метрично tight (10-15 pips для FX), що дає інший risk-profile і потребує іншого management.

---

## ⏱️ Робочі таймфрейми
- HTF Bias: **H1** (легше — головне напрямок поточного імпульсу)
- BOS detection: **15m**
- Entry: **5m** на limit-ордер у proximal edge FVG

---

## 🎯 Унікальні правила ТС-3

### R1. Тільки після свіжого 15m BOS
- BOS має бути у напрямку H1 bias
- BOS має статись у поточних **30 хвилинах** (sniper = тільки fresh impulse, не stale)
- FVG усередині impulse leg, який створив BOS

### R2. FVG quality filter
Валідні FVG:
- **Не violated** (proximal edge не пробитий від моменту створення)
- Розмір ≥ 5 pips для FX major / ≥ 0.3% для XAU / ≥ 5 pts для індексів
- Розташований у **discount/premium zone** залежно від напрямку (long → discount, short → premium)

Інакше — skip.

### R3. SL placement
- За **50% equilibrium FVG** АБО за swing що створив BOS — **що далі**
- Буфер 2-3 pips
- Якщо SL виходить ширшим за **20 pips для FX** — setup не для ТС-3 (це ТС-1 territory), skip

### R4. TP framework (специфіка ТС-3)
- **Min RR 1:3 hard gate** — якщо до найближчої ліквідності < 1:3, skip
- TP1: 1:3 → BE (швидко закриваємо ризик через tight SL)
- TP2: наступна ліквідність (часто session H/L) → ціль 1:5+
- TP3: HTF target → 1:6+
- Trail після TP2: **5m swing** (агресивніше за master, бо tight SL)
- **Max hold 2 години** — після цього close незалежно від BE/TP статусу
- **EOD hard exit:** 21:00 UTC — без винятків

### R5. No trade у low-vol періоди
- Asian session (00:00-07:00 UTC) — skip
- Останні 30 хв перед close сесії — skip
- ATR(14) на 15m < median 30d → skip (low-vol → FVG fill безсилий)

---

## 📊 Scoring (наслідує master, тюн)
Стартуємо на **Aggressive профілі** (≥6 / 4-5 / <4) — ТС-3 за дизайном частотна.
**Корекція:**
- +1 бал якщо FVG у golden zone (62-79% retracement OTE)
- -1 бал якщо BOS старший за 1 годину

---

## 🛡️ Risk
Базовий 1% з master.
**Унікальний guard:** **3 трейди на день** ліміт (вища частота = вища дисципліна потрібна).
**Tilt protection** жорсткіша: **2 losses підряд** → cut до 0.5% (не 3 як у master).

---

## 🎯 Backtest план

| Параметр | Значення |
|----------|----------|
| Sample size | **40 трейдів** мінімум (вища частота → можна швидше набрати) |
| Період | 3 міс історії (короткий період бо setups часті) |
| Watchlist | EURUSD, XAUUSD (один FX major + один metals для diversity) |
| Журнал | `20-Trading/Backtest/trades/YYYY-MM-DD-NN-[pair]-ts3.md` |
| Ціль часу | ≤8 хв/трейд (швидше, бо setup більш формальний) |

### Success criteria (для go-live)
- WR ≥ 40% (ТС-3 має нижчий WR, але високий R-multiple)
- Avg R per win ≥ **+3.0R** (нагнано через min RR 1:3)
- Expectancy ≥ +0.5R після costs
- Max DD ≤ 12%
- Adherence ≥ 92% (tight SL → дисципліна критична)

### Retirement criteria
- WR < 35% на 40+ трейдах
- Avg R per win < +2.0R (значить SL надто tight або TP занадто далеко)

---

## 🏷️ Journal tag
```yaml
ts: ts-3-fvg-sniper
model: inner_fvg
fvg_quality: A | B | C
ote_zone: true | false
```

---

## 📌 Status
🟡 **Queued** — створено 2026-04-22, очікує запуску бектесту.

---

## 🔗
- [[20-Trading/Strategies/smc-playbook-v2]] — master playbook
- [[20-Trading/Strategies/ts-1-reversal-at-poi]]
- [[20-Trading/Strategies/ts-2-session-manipulation]]
- [[20-Trading/Strategies/ts-tracker]]
- [[20-Trading/Backtest/README]]
