---
title: GBPUSD Top-Down Analysis
date: 2026-07-01
tags: [GBPUSD, TDA, neutral, forex]
category: Analysis
project: Trading
pair: GBPUSD
strategy: multi
agent: analyst
status: analysis-complete
pinecone_indexed: false
---

# GBPUSD: Top-Down Analysis — 01.07.2026

> Час: 05:30 UTC / 08:30 Kyiv (pre-London, ~30 хв до London KZ 06:00 UTC).
> Мультистратегічна база для: ASR+ORB, SMC+PA Combo, VWAP pullback.
> Поточна ціна: **1.32436**. Daily Open: **1.3258**.

## 🏛 Weekly (Тижневий графік)
15W range `1.31402–1.36578`, W -0.5%. Останні 5W closes: `1.33296 → 1.33942 → 1.32283 → 1.31870 → 1.32438`.
Ціна відкотилась від піку ~1.366 до Strong Low 1.314, зараз коригувальний відскок. **HTF Bearish-Corrective** — низхідна корекція від максимумів, поточно bounce.

![[img/gbpusd_w.png]]

## 📅 Daily (Денний графік)
20D -1.29%, range `1.31402–1.34833`. Останні 5D: `1.31896 → 1.31870 → 1.32566 → 1.32580 → 1.32435`.
Ціна нижче спадної EMA (bearish lean), але відновлюється від Strong Low 1.314. Фактично **RANGE 1.314–1.342**. Наближається до денного supply OB 1.342–1.346.
Ключові зони (з чарту): supply 1.342–1.346 (OB), 1.358–1.366 (major); demand 1.329 (flip), Strong Low 1.314 (blue band 1.308–1.314).

![[img/gbpusd_d.png]]

## ⏱ 4-Hour (4-годинний графік)
H4 range `1.31402–1.32767`, +0.39%. Останні 5×4H: `1.32508 → 1.32580 → 1.32454 → 1.32414 → 1.32437`.
**BOS up**: серія higher lows від 1.319, ціна над висхідною EMA → короткостроковий bullish recovery в межах денного range. Консолідація 1.323–1.325 під найближчим supply.

![[img/gbpusd_h4.png]]

## 🕐 1-Hour (1-годинний графік)
H1 +0.14%, 24H range `1.32122–1.32767`. NY-сесія створила Strong High ~1.328 (=PDH 1.32767), потім ретрейс, зараз консолідація ~1.3244 в Tokyo/pre-London.
Внизу H1 OTE/discount zone 1.318–1.320 (FVG).
**SMT (з EURUSD):** обидві пари в **синхроні** — овернайт decline → sweep SSL → CHoCH recovery. **Дивергенції немає** → рух широкий USD-driven, bounce «чистий» (обидві погоджуються), reversal-сигналу SMT не дає.

![[img/gbpusd_h1.png]]

## 🎯 15-Minute (15-хвилинний графік)
Овернайт: злив від 1.326 до **Asian Low 1.3232**, sweep SSL + **CHoCH/BOS вгору** → відновлення до 1.3244. Малий bullish reversal усередині азійського діапазону.

**Азійський діапазон (критично для ASR):**
- **Asian High (ASH): ~1.3258** (=Daily Open)
- **Asian Low (ASL): ~1.3232** (вже свіп-нутий один раз овернайт)
- Ширина ~26 pips (tight → сприятливо для London-експансії)
- Ціна зараз у нижній половині діапазону

Сценарії:
1. **Консервативно (LONG):** London свіпить ASL 1.3232 (Judas) → reclaim в діапазон + M15 CHoCH → лонг до ASH 1.3258 → 1.32767 (PDH).
2. **Агресивно (SHORT):** свіп ASH/1.3258 + rejection від denденного open → шорт назад до ASL 1.3232 / PDL 1.32120.

![[img/gbpusd_m15.png]]

## ⚡ 5-Minute (5-хвилинний графік) — тригер-контекст
Мікро-консолідація 1.3240–1.3245, дуже низький обсяг (pre-London). Чекати London open (06:00 UTC / 09:00 Kyiv) для експансії й тригера.

![[img/gbpusd_m5.png]]

---

## 📊 Зведення рівнів (ціни)

**Resistance / Supply (зверху):**
| Рівень | Тип |
|--------|-----|
| 1.32767 | PDH + H1 Strong High (BSL) |
| 1.329 | round + demand-flip (top yellow band 1.32944) |
| 1.342–1.346 | Daily/H4 supply OB |
| 1.350 | Strong High |
| 1.358–1.366 | major weekly supply |

**Support / Demand (знизу):**
| Рівень | Тип |
|--------|-----|
| 1.3232 | Asian Low (SSL, свіп-нутий) |
| 1.32120 | PDL |
| 1.318–1.320 | H1 OTE/discount + FVG |
| 1.314–1.315 | Strong Low / Weak Low (daily demand) |

**Ліквідність:** зверху — PDH 1.32767 / PWH 1.32731 / 1.329 / Strong High 1.350; знизу — ASL 1.3232 / PDL 1.32120 / PWL 1.31402 / Strong Low 1.314.

**Референси:** Daily Open 1.3258 · PDH/PDL 1.32767 / 1.32120 · PWH/PWL 1.32731 / 1.31402.

**VWAP:** session VWAP ≈ **1.3247** (індикатор не додався через API — оцінка з овернайт-консолідації). Ціна тулиться до VWAP = balance/no-deviation. Для VWAP-pullback потрібно чекати London-напрям + тег deviation-бенду.

**Режим ринку:** **RANGE** (Daily 1.314–1.342) з короткостроковим bullish-bounce (H4). НЕ чистий тренд. Pre-London компресія → ймовірна експансія.

---

## 🎯 Що це означає для 3 стратегій

**1. ASR (Asia Sweep & Reclaim) — ⭐ найкраща умова сьогодні.**
Tight Asian range 1.3232–1.3258, pre-London. M15 вже показав sweep ASL + reclaim овернайт. Класичний ASR-сетап: чекати, щоб London свіпнув один бік діапазону й reclaim-нув. Bias лонг-приоритет (H4 bullish, ASL вже раз свіпнутий) → sweep 1.3232 + reclaim = лонг до 1.3258/1.32767. Вікно 09:00–13:00 Kyiv.

**2. SMC+PA Combo (Sweep+OB Rejection+Retest).**
HTF mixed/range — не ідеальний тренд-фон. Найкраще: якщо ціна дійде до supply 1.342–1.346 (Daily OB) з BSL-свіпом → short-сетап у бік HTF-корекції. Або demand-реакція на 1.321/1.314 для лонга. Зараз confluence-OB для входу немає — ціна в середині range. Чекати роботи на границях.

**3. VWAP pullback.**
Наразі no-trade: ціна на VWAP (~1.3247), deviation немає, range-баланс. Стратегія активується лише після London-експансії й формування напряму — тоді pullback до VWAP/бенду в бік London-руху.

---
**Коментар:** HTF корекція від максимумів у розрізі даного тижня; DXY-контекст — синхронна USD-слабкість (EURUSD у тому ж патерні, SMT без дивергенції). Best session: London KZ (06:00–08:00 UTC / 09:00–11:00 Kyiv) — головне вікно для GBPUSD. News-ризик перевірити (початок місяця/тижня — можливі PMI/BoE спікери). Pip value GBPUSD: 1 pt = $10/lot (OANDA) — перевірити брокер.

**Setup score: 6/10** — ASR-фон відмінний (tight range, pre-London, reclaim-патерн), але HTF без сильної конвікції (range/mixed).
