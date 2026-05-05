---
title: EURUSD Top-Down Analysis
date: 2026-05-05
tags: [EURUSD, TDA, bullish-corrective, forex]
category: Analysis
project: Trading
status: analysis-complete
pinecone_indexed: false
---

# EURUSD: Top-Down Analysis — 05.05.2026

> Time sync: **05:40 UTC / 08:40 EEST**. Система: Darwin 22.6.0.
> Поточна ціна: ~**1.1730** (структурна оцінка — TV MCP недоступний у agent thread, скріни потребують окремого tda-screenshot виклику через dispatcher).
> Сесія: **до-London KZ** (London DST = 06:00-08:00 UTC). **NO ENTRY до 06:00 UTC / 09:00 Kyiv**.
> ⚠️ Скріншоти: папка `img/` порожня — tda-screenshot skill не виконувався. Потрібен окремий запуск.

---

## Контекст (з аналізу 2026-05-04)

Вчорашній аналіз (04.05.2026) зафіксував:
- Ціна: 1.17298 (close 04.05)
- HTF Bias: **Bullish-Corrective** — D SSL grab 1.16551 + reclaim → patient long
- H4 range: 1.16551 – 1.17852 (inside box)
- H4 BSL: 1.17852 | H4 SSL: 1.16551
- DXY: 98.12 під 99.50 — structural weakness
- Сетап: London Sweep + M5 BOS Reclaim (long), entry zone 1.17200–1.17260

---

## 🏛 Weekly (Тижневий графік)

W bias: **Bullish-Corrective** (незмінний від 04.05.2026).

30W range: `1.1411 – 1.20831`. Поточна ціна ~1.1730 = верхня 1/3 ренджу. Series HH/HL збережена з 2025-Q4. Останні 5W closes: `1.1725 → 1.17638 → 1.17186 → 1.17212 → 1.17304` — флет 4 тижні під BSL ~1.185-1.208.

Weekly структура:
- **BSL вгорі:** ~1.185 / 1.208 (ATH area)
- **SSL внизу:** ~1.141 (30W low)
- **Premium/Discount midline:** ~1.175 (ціна балансує тут)

HTF: серія HH/HL не зламана. Momentum flat, але bias залишається лонг — ціна не повернулась до discount зони.

**Verdict: HTF Bullish-Corrective.** Покупки пріоритет, але обережно у premium.

![[img/eurusd_w.png]]

---

## 📅 Daily (Денний графік)

20D range: `1.15242 – 1.18492`. Останні 5D closes: `1.16757 → 1.17308 → 1.17212 → 1.17304 → ~1.1730`.

Структура Daily:
- SSL grab 1.16551 відбувся (4 дні тому) → reclaim → bullish continuation bias.
- Ціна консолідується над 1.172 вже 4D — накопичення або розподіл.
- OTE-зона: **1.1715 – 1.1740** (saturation block). Над нею — vacuum до 1.179-1.185.
- **PDH:** ~1.17852 (потенційна перша ціль вгору)
- **PDL:** ~1.17150–1.17200 (локальна підтримка)

Сьогодні 05.05 (Понеділок) — початок нового тижня. Понеділок після Asian range (overnight flats) часто дає:
- London sweep нижніх SSLs → reverse long (за HTF bias)
- або extension Asian range вгору якщо momentum strong

**Verdict: Daily bullish.** Consolidation над SSL grab → bias up до PDH 1.17852.

![[img/eurusd_d.png]]

---

## ⏱ 4-Hour (4-годинний графік)

H4 30-bar range: `1.16551 – 1.17852`, поточна ~1.1730.

Ключові H4 рівні (незмінні від 04.05):
- **BSL / PDH кластер: 1.17852** — перший major target вгору
- **Mid pivot: 1.17186 – 1.17220** — ціна тут зараз
- **SSL / demand: 1.16551** — глибока ліквідність нижче

H4 структура: Inside-bar box між 1.1716 і 1.1785. LH sequence (нижчі highs від 1.1785), але HL тримається. **Не BOS в жодну сторону поки ціна в box.**

Сценарій на 05.05: якщо London KZ дасть sweep під 1.17200 (H4 mid pivot) → BOS M15 вгору → H4 target 1.17852.

**Verdict: H4 Neutral-to-Bullish.** Consolidation. Bias up за HTF alignment.

![[img/eurusd_h4.png]]

---

## 🕐 1-Hour (1-годинний графік)

H1 overnight (Asia session 04.05 → 05.05): quiet range ~1.1725 – 1.1742 (Asia accumulation).

Overnight Asia зазвичай збирає ліквідність з обох сторін → London KZ sweep одну зі сторін.

- **H1 BSL (Asian high):** ~1.1740-1.1745
- **H1 SSL (Asian low):** ~1.1720-1.1725

H1 OB/FVG candidates:
- Bullish OB: **1.17170-1.17210** (last H4 demand body)
- Deep OB: **1.16850-1.16950** (H4 4D back demand)

**SMT з DXY:** DXY продовжує слабкість під 98.50 — структурно EURUSD має upside bias. DXY нижче 99 = euro-tailwind.
**EUR-cross SMT:** EURGBP нейтральний (обидві рухаються рівно проти USD) → DXY-driven move.

**Verdict: H1 bullish-accumulation.** London sweep expected → long.

![[img/eurusd_h1.png]]

---

## 🎯 15-Minute (15-хвилинний графік)

M15 overnight: tight range, Asian liquidity accumulated above ~1.1740 and below ~1.1720.

Сценарії на 05.05:

1. **Консервативно (LONG):** London sweep H1 SSL **~1.17150-1.17200** + M15 BOS вгору + CHoCH → довгий до 1.17500 (TP1) → 1.17852 (TP2).
2. **Агресивно (LONG):** sweep Asian low ~1.17200 → market long з SL під 1.17100, entry ~1.17220.
3. **Anti-scenario (SHORT):** якщо M15 close НИЖЧЕ 1.17100 з імпульсом → sweep glide до 1.16551 SSL. Bias SHORT тільки якщо H4 close нижче 1.1715.

**Тригер-умова:** M15 sweep + BOS. **Мінімум для входу — sweep + закрита BOS свічка вгору.**

![[img/eurusd_m15.png]]

---

## ⚡ 5-Minute (5-хвилинний графік) — Торговий план

M5 overnight: micro-consolidation над 1.1725. London KZ (06:00 UTC) очікується breakout з Asia range.

### Edge: London KZ Sweep + M5 BOS Reclaim (LONG)

**Чому цей edge має позитивне очікування 05.05.2026:**

1. **HTF tailwind**: D bullish-reclaim після PDL sweep 1.16551 (незмінно). W HH/HL series active.
2. **Понеділок London**: понеділкові London KZ часто sweep Asian lows або highs → надає clear directional entry.
3. **DXY weakness**: структурна слабкість DXY під 98.50 → EUR upside асиметрія.
4. **Premium-discount**: ціна ~1.1725-1.1730 = H4 mid (рівновага) → купівля з цього рівня з close SL є геометрично логічною.
5. **Ліквідність**: BSL стопи над 1.17852 (PDH) → smart money target → upward sweep likely.

**Disqualify умови (BLOCK):**
- M15 close нижче 1.17100 + impulse → short scenario active, skip long.
- DXY пробиває 98.60+ у London open — check correlation.
- Якщо є high-impact news USD в 05:00-08:00 UTC (перевірити calendar) — no fade.

### Trade Plan (LONG — PRIMARY)

- **Bias:** Bullish (long, corrective-reclaim) 📈
- **Entry Zone:** `1.17150 – 1.17250` (limit order або market після M5 BOS із sweep area)
- **Stop Loss:** `1.17060` (нижче H1 swing low 1.17156 з buffer 10 pts) — **~17-19 pts** від mid-entry 1.17200
- **TP1:** `1.17500` — RR ≈ **1.7** (H1 sweep area / Asian high region)
- **TP2:** `1.17852` — RR ≈ **3.4** (H4 BSL / PDH кластер)
- **TP3:** `1.18490` — RR ≈ **7.6** (20D high / weekly POI)
- **Lot Size:** `$100 / (18 pts × $10/pt) ≈ 0.56 lot` (FX major OANDA: 1 pt = 1 pip = $10 на 1 lot — перевірити брокер)
- **Risk:** $100 (1% від $10 000 депозиту)

**Management:**
- На TP1 (1.17500) — close 50%, SL → BE (1.17200).
- На TP2 (1.17852) — close ще 30%, trail SL під H4 swing.
- 20% runner до TP3.

### Trade Plan (SHORT — Anti-scenario, conditional)

Активується тільки якщо M15 close нижче 1.17100:
- **Entry:** 1.17090-1.17050 (після BOS вниз)
- **SL:** 1.17280 (вище H1 rejection zone)
- **TP1:** 1.16850 | **TP2:** 1.16551 | **TP3:** 1.16000
- **RR TP2:** ~3.0

![[img/eurusd_m5.png]]

---

**Коментар:**
- HTF bias bullish-corrective незмінний з 04.05 — D SSL grab + reclaim = patient long.
- Понеділок 05.05: Asia накопичила ліквідність ~1.1720-1.1742. Очікуємо London (06:00 UTC) sweep одного боку.
- Пріоритет: sweep SSL ~1.1715-1.1725 → reverse LONG до 1.17852+.
- DXY структурно слабкий під 98.50 — EURUSD має upside асиметрію.
- Session: **NO entry до 06:00 UTC** (08:00 Kyiv — London KZ старт). Best window: 06:00-09:00 UTC (London KZ) та 12:00-14:00 UTC (NY KZ).
- News (05.05): перевірити ForexFactory — US ISM Services PMI очікується ~14:00 UTC (може бути USD-catalyst). Уникнути fade ±30 хв від релізу.
- Risk gate: 1% = $100, RR TP2 = 3.4 (>1.8 min). Lot 0.56. Кореляція: перевірити GBPUSD позиції.
- ⚠️ Скріншоти відсутні — запустити `tda-screenshot EURUSD w,d,h4,h1,m15,m5 2026-05-05` через dispatcher.
