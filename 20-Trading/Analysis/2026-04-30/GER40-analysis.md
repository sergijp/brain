---
title: GER40 Top-Down Analysis
date: 2026-04-30
tags: [GER40, TDA, bullish-corrective, indices]
category: Analysis
project: Trading
pair: GER40
strategy: smc-price-action-combo
agent: analyst
status: analysis-complete
pinecone_indexed: false
---

# GER40 (DAX): Top-Down Analysis — 30.04.2026

> Sync: UTC 2026-04-30 05:46 / Kyiv 08:46 EEST.
> Поточна ціна: **23 717** (FOREXCOM:GER40, last quote).
> ⚠️ Дані GER40 на FOREXCOM мають volume = 0 (CFD-фід без обʼєму). Volume-аналіз неможливий.

## 🏛 Weekly (Тижневий графік)

15W range: **21 860 – 25 512** (range 3 652 pts). ATH 25 512 на лютому-2026.
Останні 5W: `23 135 → 23 790 → 24 640 → 24 262 → 23 719` — після імпульсного ралі на ATH сформувалась **distribution/exhaustion** ділянка під 25 000. Поточний тижневик: open 24 262, high 24 383, low 23 643, close **23 719** (-2.75%) — сильна bearish W candle з пробоєм W EMA21 знизу.

**HTF Bias: Bullish-Corrective** — мейджорна тенденція тижневика залишається бичачою (HH/HL за 6 місяців), але починається корекційна фаза. Ризик глибокої корекції до W demand 22 800 / 21 860.

![[img/ger40_w.png]]

## 📅 Daily (Денний графік)

20D range: **21 860 – 24 798** (2 938 pts). Останні 5D: `24 262 → 24 088 → 23 994 → 23 774 → 23 716` — **5 червоних днів поспіль**, серія LL/LH. Класичне D distribution з bearish OB 24 169–24 383 (28-29 квітня) і unmitigated FVG 24 050–24 122.

Position у W range: **mid-low** (під W EMA21 ~24 100). PDH 23 940, PDL 23 643.5 — **PDL уже свіпнуто** на азійській сесії 30 квітня.

**Daily Bias:** Bearish-Corrective короткотерміново, але близько до W demand → можлива bullish reaction зона.

**Ключові D POI:**
- **D Resistance / Bearish OB:** 24 050 – 24 169 (mitigation point для шорту, якщо повернеться)
- **D Support / Bullish OB:** 23 643 – 23 774 (поточна реактивна зона, sweep сьогодні)
- **D Liquidity below:** 23 400 (W FVG mid) → 23 135 (попередній W close)

![[img/ger40_d.png]]

## ⏱ 4-Hour (4-годинний графік)

H4 range: **23 643 – 24 383** (-1.4% за вікно). Останні 5×4H: `23 861 → 23 774 → 23 911 → 23 654 → 23 717`. На H4 чітко видно:
- **BOS DOWN** під 23 774 (попередній H4 low пробитий 30.04 рано-вранці)
- **Sweep H4 low 23 643.5** на сесії Asia/Europe open
- **Reactive recovery** до 23 717 → формується потенційний bullish CHoCH якщо закриє понад 23 733 (15m structure low)

**H4 OB / FVG:**
- **H4 Bearish OB:** 23 911 – 24 050 (mitigation для продовження шорту)
- **H4 Bullish OB / Demand:** 23 643 – 23 700 (свіжо-протестований)
- **H4 imbalance:** 23 821 – 23 891 (відкритий FVG згори)

![[img/ger40_h4.png]]

## 🕐 1-Hour (1-годинний графік)

H1: -1.27% за останні 24 H1, range **23 643 – 24 122**. Останні 5H: `23 932 → 23 821 → 23 788 → 23 654 → 23 716`.

H1 структура: серія LL з імпульсним свіпом 23 643.5 (Asia low) → бичача реакція 70+ pts. Це класичний **liquidity grab + retrace**, попередник CHoCH.

**SMT:** GER40 ↔ US500 / EURUSD — на момент аналізу пара не вдалось зчитати чисто (TV-кеш скакав між USDJPY/SPX500). За dashboard-логом: US500 також у корекції (-1% за день), EURUSD 1.166 (USD сила) — узгоджено з risk-off настроєм. **SMT neutral** (немає divergence між індексами).

**H1 Liquidity:**
- Над: 23 821 (попередній H1 high), 23 911 (4H mid)
- Під: 23 643 (свіпнуто, equal lows тепер відсутні)

![[img/ger40_h1.png]]

## 🎯 15-Minute (15-хвилинний графік)

M15: range 23 643.5 – 23 940 (-0.7% за 30 барів). Останні 5×15m: `23 691 → 23 721 → 23 722 → 23 733 → 23 720`.

Зараз ціна стискається у мікро-діапазоні 23 685 – 23 735 одразу після свіпу. Це **accumulation на M15** з потенціалом до:

**Сценарії:**
1. **Консервативно (LONG):** ретест зони `23 670 – 23 700` + M15 BOS вгору з закриттям > 23 740 → лонг до 23 821 → 23 911. Це гра від D demand з sweep як confirmation.
2. **Агресивно (SHORT після ретесту):** mitigation H4 OB `23 880 – 23 940` + M15 CHoCH вниз → шорт продовження до 23 643 → 23 400 (D liquidity).

Поточно M15 знаходиться між сценаріями — **тригер ще не сформований**.

![[img/ger40_m15.png]]

## ⚡ 5-Minute (5-хвилинний графік) — Торговий план

> Поточно: pre-trigger zone. Recommended action — **WAIT** для підтвердження.

### Plan A — LONG від D demand (preferred)

- **Bias:** Bullish (тактичний) на D demand reaction після sweep 📈
- **Trigger:** M5/M15 CHoCH з закриттям над **23 740** після retest 23 670–23 700
- **Entry Zone:** `23 685 – 23 705` (limit order у H4 OB)
- **Stop Loss:** `23 630` (під 23 643.5 sweep low) — **57 pts**
- **TP1:** `23 821` — RR ~2.4 (попередній H1 high)
- **TP2:** `23 911` — RR ~4.0 (H4 mid + bearish OB low)
- **TP3:** `24 050` — RR ~6.4 (D OB / W EMA21)
- **Lot Size:** $100 / (57 × $1) ≈ **1.75 contracts** (GER40: 1 pt = $1 на 1 contract — перевірити брокер)

### Plan B — SHORT від H4 OB (за умови mitigation)

- **Bias:** Bearish (continuation) якщо ретест не стане HL
- **Trigger:** rejection з зони 23 880–23 940 + M15 CHoCH вниз
- **Entry Zone:** `23 880 – 23 920`
- **Stop Loss:** `23 970` (над H4 OB high) — **70 pts**
- **TP1:** `23 700` — RR ~3.0
- **TP2:** `23 643` — RR ~3.6 (sweep retest)
- **TP3:** `23 400` — RR ~7.5
- **Lot Size:** $100 / (70 × $1) ≈ **1.42 contracts**

![[img/ger40_m5.png]]

---

## Підсумок

| Метрика | Значення |
|---------|----------|
| **HTF Bias (W)** | Bullish-Corrective |
| **D Structure** | Bearish (5 LL/LH поспіль) |
| **H4 Structure** | BOS DOWN + sweep + bullish reaction (потенційний CHoCH) |
| **Regime** | Pullback / Range-after-impulse |
| **Setup score** | **6 / 10** — sweep є, тригер ще ні |
| **Recommended playbook** | `smc-price-action-combo` (LONG від D demand) або `ts-1-reversal-at-poi` |

**Ключові рівні:**
- **Resistance:** 23 821 (H1) → 23 911 (H4 mid) → 24 050–24 169 (D bearish OB / unmitigated FVG)
- **Support:** 23 643.5 (свіпнутий H4/D low) → 23 400 (W FVG) → 23 135 (W demand)
- **Liquidity above:** 23 821 (PDH-1), 23 940 (PDH)
- **Liquidity below:** 23 400, 23 135

**Коментар:**
- Тиждень показує сильну bearish W candle після ATH 25 512 — увага на W exhaustion. Якщо closing 23 643 буде пробитий тижневиком — preferences flip в bear.
- D distribution + H4 sweep = класичний SMC setup на reversal long, але **тригер не сформувався** — потрібен M15 CHoCH > 23 740.
- Best session для GER40: **London open 06:00–09:00 UTC** (зараз вже завершується) і **NY open 13:30 UTC** — ймовірно тригер зʼявиться під NY.
- News risk: перевірити ForexFactory на ECB / DE CPI / Eurozone GDP сьогодні. Без news-watcher — **обовʼязково перевірити календар** перед entry.
- Risk-gate: 1% від $10 000 = $100 ризик → ~1.75 contracts на Plan A.
- Правило "не входити раніше 09:00 Київ" — зараз 08:46, найближчі 15 хв чекаємо як discovery.

⚠️ **Setup score 6/10** — для повноцінного входу потрібен trigger. Передати plan до `strategy-picker` для верифікації playbook, потім — `dixie ⇄ kassandra` debate перед risk-manager.
