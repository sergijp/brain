---
title: "ТС-1 — Reversal at POI"
date: 2026-04-22
tags: [trading, strategy, smc, ts-1, reversal, poi]
category: trading
status: queued
parent: "[[20-Trading/Strategies/smc-playbook-v2]]"
journal_tag: ts-1-reversal-poi
pinecone_indexed: false
---

# 📊 ТС-1 — Reversal at POI

**Філософія:** plan-driven intraday-reversal сетапи на ретесті ключових POI. Bias на H1/H4, виконання у поточній сесії, **no overnight**. Alerts задаються заздалегідь — повертаємось до графіка тільки при тригері.

**Inherits from:** [[20-Trading/Strategies/smc-playbook-v2]] (risk, scoring, gates, journal, EOD-close rule)

**Style:** semi-scalp / intraday | **Min RR:** 1:3

---

## 🎲 Включені моделі

| # | Модель | Призначення |
|---|--------|-------------|
| 1 | **Classic BOS Retest** | Ядро системи — найчистіший SMC-сетап |
| 2 | **Delayed Entry (alert-driven)** | Setup через alerts — але вхід **має лягти у поточну intraday-сесію**, інакше skip |
| 5 | **Breaker Block Entry** | Коли OB не відпрацював, breaker дає кращий RR |

**Чому разом:** усі три — reversal/continuation **на ретесті заздалегідь визначеного POI**. Тригер однотипний: sweep → BOS → pullback. Різниця лише в тому, **який саме POI** обслуговуємо (свіжий OB / старий зрелий POI / пробитий = breaker).

---

## ⏱️ Робочі таймфрейми (intraday-tuned)
- HTF Bias: **H1 / H4** (не D — занадто повільно для intraday)
- POI ID: **15m / H1**
- Trigger: **5m / 15m**
- Hold time: **межа сесії** (London або NY, не cross-session)

---

## 🎯 Унікальні правила ТС-1

### R1. POI має бути pre-marked
POI визначається на H1/H4 **до** entry-сесії. Drawing/alert поставлено заздалегідь. Ad-hoc «бачу OB прямо зараз» — **не валідно** для ТС-1 (це підкрадається до ТС-2/ТС-3).

### R2. Ретест-тригер обов'язковий
Вхід тільки після:
- Sweep ліквідності біля POI
- 15m BOS у напрямку HTF bias
- Pullback до BOS-зони / breaker / OB

«Just touch» без BOS — skip.

### R3. Alert-first workflow
- Поставити TV alert (`mcp__tradingview__alert_create`) на POI
- Прийти до графіка **тільки** при спрацюванні
- Перевірити invalidation: HTF bias не зламано? POI не violated?

### R4. Time stop (intraday)
- Якщо POI не досягнуто за **3 години** від моменту виставлення alert у поточній сесії — alert знято, setup expired
- Якщо позиція відкрита і не дотягнула до TP1 за **2 години** — manual close (no overnight)
- **EOD hard exit:** усі позиції закриваються до 21:00 UTC незалежно від статусу

### R5. Min RR 1:3 (hard gate)
Якщо TP1 до найближчої ліквідності дає RR < 1:3 → **skip**. Wide SL за structure лишається — пересуваємо TP далі або відмовляємось від сетапу.

---

## 📊 Scoring (наслідує master, тюн)
Стартуємо на **Standard профілі** (≥8 full / 5-7 half / <5 skip).
**Корекція для ТС-1:** додати +1 бал якщо POI = H4 OB або Weekly Open (не просто H1).

---

## 🛡️ Risk
Базовий 1% з master. **Tilt protection** і **correlation cap** діють як завжди.

---

## 🎯 Backtest план

| Параметр | Значення |
|----------|----------|
| Sample size | **30 трейдів** мінімум |
| Період | 6 міс історії (Manual Bar Replay) |
| Watchlist | EURUSD, GBPUSD, XAUUSD (3 пари — швидкість набору) |
| Журнал | `20-Trading/Backtest/trades/YYYY-MM-DD-NN-[pair]-ts1-[model].md` |
| Ціль часу | ≤10 хв/трейд |

### Success criteria (для go-live)
- WR ≥ 45%
- Expectancy ≥ +0.4R після costs
- Max DD ≤ 10%
- Adherence ≥ 90% full

### Retirement criteria
- WR < 40% на 30+ трейдах → пауза, ревізія правил R1-R4

---

## 🏷️ Journal tag
```yaml
ts: ts-1-reversal-poi
model: classic | delayed | breaker
```

---

## 📌 Status
🟡 **Queued** — створено 2026-04-22, очікує запуску бектесту.

---

## 🔗
- [[20-Trading/Strategies/smc-playbook-v2]] — master playbook
- [[20-Trading/Strategies/ts-2-session-manipulation]]
- [[20-Trading/Strategies/ts-3-inner-fvg-sniper]]
- [[20-Trading/Strategies/ts-tracker]]
- [[20-Trading/Backtest/README]]
