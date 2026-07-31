---
title: GER40 Top-Down Analysis
date: 2026-07-29
tags: [GER40, TDA, bullish-corrective, indices]
category: Analysis
project: Trading
pair: GER40
strategy: asr-orb-intraday-system
agent: analyst
status: analysis-complete
pinecone_indexed: false
---

# GER40 (DAX): Top-Down Analysis — 29.07.2026

> Час аналізу: 05:50 UTC / 08:50 Kyiv (пре-Xetra). Депозит $10 000, ризик 1%.
> Дані TradingView свіжі (last bar 08:50 Kyiv). Ціна: **25 388**.

## 🏛 Weekly
15W range `23 613 – 25 923`, W **+3.05%**. Останні 5W: `25 806 → 25 097 → 24 829 → 25 077 → 25 391`.
Серія HH/HL, ATH встановлено 2 тижні тому на `25 923`, далі корекція до `24 829` і відновлення. **HTF Bullish** — тренд не зламано, ціна консолідує під ATH.

![[img/ger40_w.png]]

## 📅 Daily
20D range `24 610 – 25 923`, D **+1.45%** (поточний бар -0.49%). Останні 5D: `24 794 → 25 077 → 25 483 → 25 516 → 25 390`.
Rising lows (24 610 → 24 692 → 24 696) + вищі закриття = **Daily Bullish, momentum**. Відновлення від тижневого лоу, підхід до `25 609 / 25 923` опору. Сьогоднішній бар — pullback від `25 609` до `25 270`, зараз bounce. Позиція: верхня третина 20D-діапазону.

![[img/ger40_d.png]]

## ⏱ 4-Hour
H4 range `24 692 – 25 609`, +0.88%. Останні 5×4H: `25 535 → 25 515 → 25 471 → 25 328 → 25 393`.
**BOS UP** зберігається (structure з 24 692). Тап `25 609` (BSL) → відкат у демандну зону `25 270–25 330` → зараз реакція вгору. H4 демонструє HL-логіку в межах бичачого імпульсу.

![[img/ger40_h4.png]]

## 🕐 1-Hour
H1 range `25 270 – 25 609`, поточний бар -0.28%. Ціна відскочила від `25 270.5` (SSL swept) до `25 388`.
Внутрішня структура H1: HH `25 609` → різкий злам до LL `25 270.5` (забрано sell-side ліквідність) → LH `25 413`. Тобто **інтрадей — corrective/bearish micro-shift** усередині бичачого HTF.
**SMT (з watchlist):** US500 -0.09%, EU50 -0.29%, GER40 -0.49%, DXY -0.11%, EURUSD +0.12%. GER40 слабший за EU50/US500 → **легка bearish-дивергенція** вранці; сильніший EUR тисне на експортерів DAX. Контекст змішаний, HTF bullish переважає.

![[img/ger40_h1.png]]

## 🎯 15-Minute — ключові рівні (SMC-індикатори на чарті)

**Діапазон дня (fib 0–1):** `25 270.5 (0 / SSL)` — `25 609.27 (1 / BSL)`. Mid 0.5 = `25 439.9`, OTE 0.705 = `25 509`.
Поточна ціна `25 388` — у **DISCOUNT** (нижче 0.5).

| Рівень | Ціна | Тип |
|--------|------|-----|
| BSL / H4 swing high | **25 609.27** | Liquidity above / ATH-підхід |
| Supply OB | 25 597 | Продажний OB |
| PDH / ORB-ref high | **25 553.5** | Ліквідність, опір |
| Daily Open | 25 515.79 | Магніт |
| BOS SHORT trigger | 25 458 | Структурний |
| Mid 0.5 | 25 439.9 | Equilibrium |
| BOS LONG trigger | 25 424 | Структурний |
| **Поточна ціна** | **25 388** | discount |
| PDL / demand | **25 301.5** | Підтримка |
| NY Open | 25 304.5 | Рівень |
| OTE demand zone | 25 313 | Зона входу long |
| Demand OB | 25 298.5 | Order block |
| **SSL / day low** | **25 270.5** | Liquidity below (swept) |

Структура (Cryptology): `HH 25 609 → LL 25 270.5 → LH 25 413`.

![[img/ger40_m15.png]]

## ⚡ 5-Minute — Торговий план (ІНТРАДЕЙ, закриття ввечері)

**Статус: PENDING / WATCH.** Час 08:50 Kyiv — вікна ASR (10:05) та Xetra ORB (10:00–10:30) ще НЕ відкрились. Тригера немає.

### Сценарій A — ASR LONG (пріоритетний, за HTF bias) 📈
Умова: на відкритті Xetra/London ціна робить провальний свіп нижче `25 270.5` (Asian/day low) → M15 reclaim назад над `25 300` + rejection candle + BOS.
- **Entry Zone:** `25 300 – 25 330` (reclaim над PDL/NYO)
- **Stop Loss:** `25 255` (нижче SSL 25 270.5) — **~70 pts**
- **TP1:** `25 440` (0.5 mid) — RR ~2.0
- **TP2:** `25 553.5` (PDH/ORB-ref/BSL) — RR ~3.5
- **TP3:** `25 609` (day high / BSL) — RR ~4.4
- **Lot:** `$100 / (70 × $1) ≈ 1.4 контракти` (GER40: 1 pt = $1/контракт — перевірити брокер)

### Сценарій B — ASR SHORT (контр-HTF, тільки при чіткому свіпі) 📉
Умова: свіп над `25 553.5` (PDH) / `25 609` (BSL) → reclaim вниз + CHoCH на M15.
- Entry: `25 540 – 25 560`, SL `25 620` (~70 pts)
- TP1 `25 440`, TP2 `25 305` (PDL), TP3 `25 270` (SSL). RR до ~3.5.
- Нижчий пріоритет — проти денного бичачого bias.

### Сценарій C — Xetra ORB-30 (сателіт GER40)
Діапазон 10:00–10:30 Kyiv ще не сформований. Дочекатись закриття 30-хв бару → торгувати пробій діапазону в бік HTF (long перевага). Індикатор дає reference ORB `25 434 – 25 553.5` (F1-fail watch) — використати лише як орієнтир, не як фактичний ORB дня.

![[img/ger40_m5.png]]

---
**Коментар:**
- **Bias:** HTF Bullish (W+D+H4 узгоджені), інтрадей — corrective pullback у discount після свіпу SSL.
- **Найкращий сценарій:** ASR long зі свіпу `25 270.5` на Xetra-open з ціллю PDH `25 553.5` — все досяжно в межах дня, закриття до 17:45 Kyiv (flat).
- **Ризики:** легка bearish SMT (GER40 слабший за EU50/US500), сильніший EUR. Перевірити ForexFactory на німецьку/US-статистику (кінець липня — можливі US GDP/PCE/FOMC-тиждень) перед входом; за high-impact ±30 хв — no-trade.
- **Сесія:** Xetra/London open 10:00 Kyiv. Вхід не раніше 10:05 Kyiv (ASR-вікно). NY KZ як alt-драйвер після 15:00.
- **Setup score: 6/10** — чиста HTF-структура і рівні, але тригер ще не сформований + інтрадей-momentum поки corrective.
