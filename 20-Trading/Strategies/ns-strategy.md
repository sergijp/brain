---
title: "NS — Власна SMC стратегія"
date: 2026-04-22
tags: [trading, strategy, smc, ns, top-down, amd]
category: trading
status: draft
journal_tag: ns
pinecone_indexed: false
---

# 📊 NS — Власна SMC стратегія

**Філософія:** повний top-down SMC pipeline — від D1 bias до m5 entry, з AMD-каркасом дня, opens (NYM / DO / WO / MO) як структурними якорями, pre-mapped мапою ліквідності та sweep як тригером розвороту.

**Незалежна стратегія.** Self-contained — НЕ успадковує `smc-playbook-v2`. Власні risk, scoring, gates, journal.

**Style:** semi-scalp / intraday  |  **Ринки:** Forex + Indices/Commodities (DXY, SPX, Gold)  |  **Min RR:** 1:3 (hard gate)  |  **EOD:** 21:00 UTC

---

## 🧭 7 фундаментальних принципів NS

1. **Top-Down аналіз** W1 → D1 → H4 → H1 (для intraday виконання: entry на m15/m5/m1)
2. Знаючи напрямок — знаємо **магістраль руху**, куди ринок йде далі
3. **Зони S/R** (POI): куди ціна дійде і звідки відштовхнеться у наш бік
4. **Мапа всіх ліквідностей** (external / internal / EQH-EQL / trendline / PDH-PWH)
5. **Opens** як якорі: NYM (true daily open), DO, WO, MO + TSO (session opens)
6. **AMD-каркас** дня: Accumulation (Asia) → Manipulation (London) → Distribution (NY)
7. **Liquidity sweep** / пересвіп — тригер для пошуку входу (не пробій сам по собі)

---

## ⏱️ Робочі таймфрейми (top-down каркас)

| Рівень | ТФ | Що робимо |
|--------|----|-----------| 
| Context (Long Term) | **D1** | Напрямок розширення денної свічки, PDH/PDL, денний профіль, DO |
| Structure (Intermediate) | **H4 / H1** | Поточна структура, HTF POI (OB/BB/FVG H1+), цілі на пули ліквідності |
| Trigger + Entry (Short) | **m15 / m5 / m1** | Shift (первинний злам) всередині HTF POI → SMR / IFVG / OB wick entry |

> *W1 — опційний sanity-check для контексту тижневого bias і WO, але вхід усе одно у intraday.*

**Hold time:** межа сесії (London або NY), **no cross-session**, **no overnight**.

---

## 🧠 BIAS — як визначається

**Базове правило:** ціна йде **від ліквідності до ліквідності**, по дорозі балансуючи FVG.

**Визначення напрямку:**
1. Знайти **«Причину»** — недавній sweep ключового пулу або тест старшого FVG
2. Визначити **«Результат»** — протилежний пул ліквідності або найближчий HTF FVG як магніт
3. **Order Flow** між цими точками = поточний bias

### Continuation vs Reversal — правило закриття

| Ознака | Інтерпретація |
|--------|---------------|
| Свічка знімає PDH/PDL/PWH/PWL і **закривається тілом за екстремумом** | ✅ Continuation поточного напрямку |
| Свічка знімає рівень, але **тіло всередині (залишає тінь)** | 🔄 Reversal, розворот очікується з наступної свічки |

---

## 📐 Opens як структурні якорі

| Open | Час (Kyiv) | Роль |
|------|------------|------|
| **NYM** (New York Midnight) | 07:00 | **True daily open для Forex** — головний референс |
| **DO** (Daily Open) | 00:00 брокера | Магніт; лонги акумулюються нижче DO, шорти вище |
| **WO** (Weekly Open) | Понеділок 00:00 | HTF магніт тижня |
| **MO** (Monthly Open) | 1-й торговий день місяця | HTF магніт місяця |
| **TSO Азія** | 02:30 | Справжнє відкриття Azure sesion |
| **TSO London** | 08:30 | Справжнє відкриття London |
| **TSO NY** | 14:30 | Справжнє відкриття NY |

**Правило взаємодії:** валідна маніпуляція **повинна зачепити** (sweep) один з цих opens або PDH/PDL, інакше — не маніпуляція, а continuation.

---

## 🎯 Мапа POI (Order Block / Breaker / FVG / IFVG)

### Order Block (OB)
- **Валідація:** імпульсне поглинання — тіло наступної свічки (або серії) закривається **за тілом** OB (bullish: вище; bearish: нижче)
- **Маркування:**
  - Мале тіло + велика тінь → виділяємо від тіні до тіні
  - Широке тіло + мала тінь → по тілу
- **Входи з OB:** 3 рівні
  - **Open** (найбалансованіший, wider SL)
  - **50% / Mean Threshold** (оптимальний RR, найчастіша реакція)
  - **Wick** (tight SL, але ризик не дочекатись mitigation)
- **Mitigation:** OB валідний поки ціна **не закрілась тілом за 50%**. Пробій тінню — допустимо.

### Breaker Block (BB)
- OB, який був пробитий і спричинив **BOS** у протилежному напрямку
- Змінює полярність (bullish OB → bearish BB і навпаки)
- Торгується на ретесті як OB

### FVG / IFVG (Fair Value Gap)
- 3 типи ребалансу:
  - **IOFED** (тінь, без 50%) — частковий, зона ще валідна
  - **50% Mean Threshold** — **найсильніша реакція**
  - **Full Fill** — зона відпрацьована, виходимо
- FVG найсильніший у **discount** для лонгу / **premium** для шорту (relative до HTF range)

### Ієрархія HTF → LTF
**HTF OB/FVG** = контекст (POI, куди чекаємо ціну).  
**LTF Shift** всередині HTF POI = тригер для входу.

---

## 💧 Мапа ліквідності

| Тип | Де шукати | Як маркувати |
|-----|-----------|--------------|
| **External BSL/SSL** | За swing high/low | Горизонтальна лінія над/під екстремумом |
| **Internal** | Всередині range/імпульсу | Менші зони між key max/min |
| **EQH/EQL** | Рівні екстремуми субструктури (left higher than right для EQH) | Рівна лінія на touch |
| **Trendline liquidity** | Компресія в корекції | Trendline як «паливо» |
| **PDH/PDL** | Max/min попереднього дня | Щоденний маркап |
| **PWH/PWL** | Max/min попереднього тижня | Тижневий маркап |

**Правило:** пул ліквідності **втрачає силу** після зняття. Якщо зняли PDH — ціль уже не PDH, а наступний ліквідний рівень.

---

## 🔄 AMD-каркас + квартальна теорія

### Класичний AMD (Power of 3)

| Фаза | Сесія (Kyiv) | Що робить |
|------|--------------|-----------|
| **Accumulation** | Азія (~02:00-08:00) | Боковик, формування ліквідності біля DO |
| **Manipulation** | London / LOKZ (~09:00-12:00) | Хибний рух, sweep Asia-range. Bullish day → low of day; bearish → high of day |
| **Distribution** | NY / NYKZ (~14:30-19:00) | Істинний імпульсний рух до цілі |

### Квартальна теорія (AMDX)

| Q | Час (Kyiv) | Функція за замовчуванням |
|---|------------|-------------------------|
| Q1 | 01:00-07:00 | Consolidation (Asia) |
| Q2 | 07:00-13:00 | Manipulation (London) |
| Q3 | 13:00-19:00 | Distribution (NY) |
| Q4 | 19:00-01:00 | Retracement (PM) |

**Fallback:** якщо Q2 консолідується → маніпуляція зсувається на Q3.

### 90-min мікро-цикли

Кожен Q ділиться на 4 × 90m. Приклад Q2 (London): 07:00-08:30 / 08:30-10:00 / 10:00-11:30 / 11:30-13:00 — очікуємо маніпуляцію зазвичай у другому 90m.

---

## 📅 Денні профілі доставки — що торгуємо

| Профіль | Ознака | Торгуємо? |
|---------|--------|-----------|
| **Trending** (classic buy/sell day) | Asia accum → London sweep → NY continuation | ✅ **Ядро NS** |
| **Reversal** (London Swing → NY Reversal) | London досяг H1+ POI → NY 15:00 розворот у протилежний бік | ✅ |
| **Expansion** (news raid) | Consol Asia+London → imp impulse на news 15:30/17:00 | ⚠️ **Тільки з newsflag**, skip якщо unplanned |
| **Consolidation** (Seek & Destroy) | Sweep з обох боків, без напрямку | ❌ **Skip** |

---

## 🎯 Sweep / пересвіп — підтвердження

**Як підтверджений sweep виглядає:**
- **Rejection Block** — мале тіло + довга тінь, що знімає BSL/SSL
- Тіло закривається **назад** за рівнем (не закріплюється за пулом)
- **Посилення:** LTF BOS (Shift) на m15/m5 одразу після девіації

**Відмінність від справжнього пробою:**
- Справжній BOS/пробій → тіло **закріплюється** за рівнем
- Sweep/Raid → пробій **тільки тінню** (wick-only)

**SMT divergence:** якщо корельовані пари/індекси (EURUSD vs GBPUSD; XAUUSD vs DXY inverse; SPX vs NAS) роблять non-confirmation — sweep сильніший.

---

## ✅ Confluence Checklist — 5-крокова воронка входу

Вхід ТІЛЬКИ при проходженні **всіх 5** кроків. Якщо хоч один не виконано — **skip**.

| # | Крок | Що перевірити |
|---|------|---------------|
| 1 | **HTF Bias** | D1/H4/H1 Order Flow визначений (від A до B) |
| 2 | **HTF POI** | Ціна підходить до валідної зони H1+ (OB / BB / FVG) |
| 3 | **Liquidity Sweep** | Зняття BSL/SSL / Asia high-low / PDH-PDL / EQH-EQL. +SMT bonus |
| 4 | **LTF Shift (BOS)** | На m15/m5/m1: імпульсне поглинання, злам найближчого слабкого свінгу |
| 5 | **LTF Entry** | Відкат до FVG (SMR) / IFVG / OB wick. **SL** за край тіні моделі. **TP** ≥ 1:3 RR або наступний пул |

---

## 🎲 Моделі / варіації входу

| Модель | Коли застосовується | Entry точка |
|--------|---------------------|-------------|
| **SMR** (Smart Money Reversal) | Ціна в HTF POI, stress → Shift → pullback | FVG, що утворився після Shift |
| **IFVG** (Inversion FVG) | FVG пробитий тілом, став inversed | Ретест IFVG у протилежному напрямку |
| **OB Wick Entry** | OB у HTF POI з tight wick | Від wick OB (найменший SL) |
| **OB Open/50%** | Widenier SL прийнятний, RR ≥ 1:3 | Open або Mean Threshold |

---

## 🌐 Cross-market фільтри

- **DXY correlation:** для longs EUR/GBP/AUD — DXY має бути в bearish context або робити sweep high
- **SMT indices vs FX:** NAS/SPX розходження з DXY = додатковий confluence для FX reversal
- **Gold (XAUUSD):** inverse до DXY; XAU long = DXY sweep high + bearish shift
- Cross-link: [[20-Trading/Strategies/correlation-table]]

---

## 📊 Scoring (NS-own)

Бали за confluence на сетапі:

| Фактор | +балів |
|--------|--------|
| HTF POI = D1 або H4 (не тільки H1) | +1 |
| Sweep ключового open (NYM / WO / MO) | +1 |
| SMT divergence confirmed | +1 |
| Trending daily profile | +1 |
| RR ≥ 1:5 | +1 |
| Sweep + LTF BOS в одній сесії (не cross-session) | +1 |

| Сума балів | Вердикт |
|-----------|---------|
| ≥ 5 | ✅ **Full size** (1% risk) |
| 3-4 | ⚠️ **Half size** (0.5% risk) |
| < 3 | ❌ **Skip** |

---

## 🛡️ Risk (NS-own)

- **Per trade:** 1% (full) / 0.5% (half size)
- **Daily stop:** -3% → припиняємо торгівлю до наступного дня
- **Max одночасних позицій:** 3 (враховуючи correlation cap: не більше 2 в одному currency cluster)
- **Correlation cap:** не дублюємо directional exposure EUR + GBP одночасно на long
- **Tilt protection:** 2 поспіль збитки → пауза 1 година, переглянути checklist

---

## 🚪 Gates (hard-blocks, NS-own)

- ❌ **Consolidation day** (Seek & Destroy профіль) → skip
- ❌ **High-impact news ±15min** (red flag NFP / CPI / FOMC) → no new entries
- ❌ **RR < 1:3** на checklist → skip незалежно від інших балів
- ❌ **Missed Shift** (LTF BOS не підтвердився) → ніяких «на око» входів
- ❌ **Cross-session hold** → жодна позиція не йде через kill zone boundary без TP

---

## 🎯 Backtest план

| Параметр | Значення |
|----------|----------|
| **Sample size** | 30 трейдів **Forex** + 15 трейдів **Indices/Commodities** перед go-live |
| **Період** | 6 міс історії (Manual Bar Replay у TradingView) |
| **Watchlist Forex** | EURUSD, GBPUSD, XAUUSD |
| **Watchlist Indices** | DXY, NAS100, SPX500 |
| **Журнал** | `20-Trading/Backtest/trades/YYYY-MM-DD-NN-[asset]-ns-[model].md` |
| **Ціль часу** | ≤ 15 хв/трейд |

### Success criteria (для go-live)

| Метрика | Поріг |
|---------|-------|
| WR | ≥ 40% (при min RR 1:3) |
| Expectancy | ≥ +0.6R після costs |
| Max DD | ≤ 10% |
| Adherence (checklist followed) | ≥ 92% |
| Avg hold time | ≤ 2h |

### Retirement criteria

- WR < 35% на 30+ трейдах → пауза, ревізія 5-крокового checklist
- Adherence < 85% → проблема з дисципліною, не стратегією

---

## 🏷️ Journal tag

```yaml
ts: ns
model: smr | ifvg | ob-wick | ob-open
profile: trending | reversal | expansion
session: asia | london | ny
markets: forex | indices | commodities
confluence_score: 0-6
```

---

## 📌 Status

🟡 **Draft** — створено 2026-04-22, очікує запуску бектесту після ТС-1.

---

## 🔗 Cross-links

- [[20-Trading/Strategies/ts-tracker]] — реєстр ТС
- [[20-Trading/Strategies/correlation-table]] — DXY / SMT пари
- [[20-Trading/Strategies/smc-price-action-combo]] — PA-комбо патерни
- [[20-Trading/Strategies/smc-playbook-v2]] — master playbook (reference, не inherited)
- [[20-Trading/Strategies/ts-1-reversal-at-poi]] — суміжна ТС (reversal)
- [[20-Trading/Strategies/ts-2-session-manipulation]] — суміжна ТС (AMD)
- [[20-Trading/Backtest/README]] — 4-етапний процес

**NotebookLM lineage (Trading CT):** 1-14 Top-Down, 1-5 Структура, 1-6 Ліквідність, 1-9 FVG, 1-10 OB/BB, 1-13 Range, 2-2 MMSM/MMBM, 2-5 PO3/AMD/DO-WO-MO, 2-11 Forex setups, 3-1 BIAS, 3-4 Денні профілі, 3-5 Квартальна теорія.
