---
title: EURUSD Top-Down Analysis
date: 2026-04-30
tags: [EURUSD, TDA, bullish-corrective, forex]
category: Analysis
project: Trading
status: analysis-complete
agent: analyst
pair: EURUSD
strategy: smc-price-action-combo
pinecone_indexed: false
---

# EURUSD: Top-Down Analysis — 30.04.2026

> Поточна ціна: **1.16626** (OANDA:EURUSD, 06:05 UTC)
> Депозит: $10 000 · Ризик: 1% · Сесія: pre-London KZ (06:00–08:00 UTC, summer DST)

## 🏛 Weekly (Тижневий графік)

W (100W back) **+7.49%**, range `1.0178 – 1.2083`.
Останні 5W closes: `1.1522 → 1.1725 → 1.1764 → 1.1719 → 1.1661` — HH досягнуто на 1.1849, далі слабкий LH 1.1791 і поточний нижчий close. Структура **HTF Bullish**, але четвертий тиждень з нижчими closes — **bullish-corrective / momentum slowing**. Жодного W BOS вниз поки немає, ціна тримається над key W demand 1.15–1.1565.

![[img/eurusd_w.png]]

## 📅 Daily (Денний графік)

D 20-day **+0.31%**, range `1.1411 – 1.2083`. Останні 5D: `1.1719 → 1.1721 → 1.1713 → 1.1676 → 1.1663` — **LH/LL серія**, retracement в межах W bull. Ціна вийшла вниз із D consolidation 1.17–1.1849 і тестує D OB demand 1.1635–1.1655 (попередній accumulation block перед імпульсом 06.04 → 14.04).

Sweeps: PDL 1.1665 sweep сьогодні (М15 low 1.16551). PDH 1.1721 цілий.
Position у W range — middle (53%), у D range — bottom третина.

![[img/eurusd_d.png]]

## ⏱ 4-Hour (4-годинний графік)

H4 30-bar range `1.1566 – 1.1849`, **+0.79%** з лоу. Останні 5×H4 closes: `1.1685 → 1.1676 → 1.1679 → 1.1660 → 1.1663` — **H4 BOS DOWN** всередині bullish контексту, ціна тестує H4 demand `1.1635–1.1655` (OB+FVG, утворений 28.04 imbalance up). Якщо ця зона тримається — формується HL відносно 1.1566 і продовжиться W bull. Якщо проб'є з closing — далі H4 demand `1.1565–1.1580` (попередній swing low + W support).

Key levels:
- **Resistance:** 1.1721 (PDH), 1.1755 (H1 high), 1.1849 (W high / D resistance)
- **Support:** 1.1655 (H4 demand top), 1.1635 (H4 demand bottom), 1.1566 (H4/W swing low)
- **Liquidity above:** 1.1755 → 1.1791 → 1.1849 (multiple equal highs)
- **Liquidity below:** 1.1655 (свіжо sweept) → 1.1566 (нижче weekly support)

![[img/eurusd_h4.png]]

## 🕐 1-Hour (1-годинний графік)

H1 30-bar range `1.1655 – 1.1755`, **−0.14%**. Останні 5×H1 closes: `1.1667 → 1.1666 → 1.1660 → 1.1659 → 1.1663` — поточний бар робить **internal sweep H1 low 1.1655** (low 1.16551) і повертається всередину. Це перший сигнал для потенційного reversal в межах H4 demand.

**SMT (Smart Money Technique):**
- **vs DXY (D):** EURUSD робить LL (1.1660 < 1.1676), DXY теж робить higher low/slight push (98.97 → 99.04) — **синхронно**, без bullish-divergence, USD-strength підтверджено.
- **vs GBPUSD (D):** GBPUSD `1.3517 → 1.3477 → 1.3465` — теж LH/LL, синхронно з EURUSD. Немає FX-divergence.
- **Висновок SMT:** наразі **нейтральний-небулліш** — EURUSD не має SMT-аргументу для негайного long. Потрібен M15 CHoCH UP як підтвердження.

![[img/eurusd_h1.png]]

## 🎯 15-Minute (15-хвилинний графік)

M15 30-bar **−0.35%**, low 1.16551 (свіжо). Поточна ціна 1.16626 — над свіпнутим лоу, але без CHoCH вгору ще.

**Сценарії:**

1. **Консервативний LONG (приоритетний, відповідає W bias):**
   Чекати reclaim 1.1670 → CHoCH UP на M15 (close > 1.1675 з підтвердженням M5 BOS) → entry ретест FVG 1.1660–1.1668 → ціль H1 OB 1.1720 та далі 1.1755.

2. **Агресивний LONG (sweep + reversal):**
   На повторному sweep 1.1655 (друге торкання) + швидкий M5 reclaim → entry 1.1660 з SL під H4 demand 1.1632.

3. **Continuation SHORT (контр-W, тільки якщо H4 close < 1.1632):**
   Очікувати breakdown H4 demand → retest 1.1640 як new supply → target 1.1566. Лише як reactive план, не пріоритет.

![[img/eurusd_m15.png]]

## ⚡ 5-Minute (5-хвилинний графік) — Торговий план (preliminary)

> ⚠️ План **preliminary**: дає `strategy-picker → dixie` визначити фінальний playbook. M15 CHoCH UP ще не відбувся.

- **Bias:** Bullish-Corrective 📈 (W bull ➜ D pullback ➜ H4 demand retest)
- **Setup:** SMC + Price Action Combo — sweep 1.1655 + ретест H4 demand → reversal
- **Entry Zone:** `1.1660 – 1.1668` (M15 FVG після CHoCH UP)
- **Stop Loss:** `1.1625` (нижче H4 demand 1.1632) — **35 pts**
- **TP1:** `1.1700` (intraday equilibrium) — RR ≈ 1.14
- **TP2:** `1.1755` (H1 high / liquidity above) — RR ≈ 2.7 ✅
- **TP3:** `1.1849` (W high) — RR ≈ 5.5
- **Lot Size:** `$100 / (35 × $10) ≈ 0.29 lot` (FX major, OANDA: 1 pt = $10/lot — перевірити брокер)

**Trigger umova:** entry лише після M15 close > 1.1670 з confirmed CHoCH UP. Без CHoCH = no-trade, ризик breakdown 1.1632.

![[img/eurusd_m5.png]]

---

## ⚠️ News risks (CRITICAL today)

| Час (UTC) | Подія | Impact |
|-----------|-------|--------|
| 11:45 | **ECB Rate Decision** | HIGH (EUR) |
| 12:30 | **ECB Press Conference (Lagarde)** | HIGH (EUR) |
| 12:30 | **US GDP / Core PCE** | HIGH (USD) |

**Blackout window: 11:45 – 13:15 UTC** — ні entries, ні modifications.

Стратегія по сесії:
- **Pre-news (06:00–11:00 UTC):** torgyvati setup тільки якщо M15 CHoCH UP до 11:00 UTC і fix part position до 11:30 UTC.
- **Blackout (11:45–13:15):** flat або wait-and-see.
- **Post-news (13:15+):** оцінити нову D structure, можливі fresh sweeps в обох сторонах.

## Коментар

- **Кореляції:** USD-major група синхронна (EUR, GBP обидві LH/LL), отже корельовану позицію long-EUR + long-GBP **не брати одночасно** (correlation cap = 2 per group).
- **Сесія:** 06:05 UTC = pre-London (літня DST, London KZ 06:00–08:00 UTC). Київ 09:05 — рівно межа правила «не входити раніше 09:00 Kyiv». Перші 30–60 хв London часто роблять stop-hunt — не fomo на першу свічку.
- **Свіжість даних TV:** last bar M5 = 06:05 UTC, актуально.
- **Repeat-focus warning:** не активно, окремих failed setups по EURUSD за останні 7 днів дашборд не зафіксував.

## Setup score (preliminary): **6 / 10**

Розклад:
- HTF bias чіткий (W bull) → +3
- D/H4 corrective, retest валідної demand → +2
- H1 sweep liquidity 1.1655 виконано → +1
- M15 CHoCH UP **ще не підтверджено** → 0 (треба чекати)
- SMT нейтральний (без bullish divergence) → 0
- News risk у window торгового дня (ECB+GDP+PCE) → −1 fudgefactor

Висновок: **wait-and-see до M15 CHoCH UP або до post-news re-evaluation**. Передаємо `strategy-picker` для вибору playbook (очікувано: `smc-price-action-combo` з варіантом `ts-1-reversal-at-poi`).
