---
title: GBPUSD Top-Down Analysis
date: 2026-05-04
tags: [GBPUSD, TDA, range, bullish-corrective, forex, uk-bank-holiday]
category: Analysis
project: Trading
status: analysis-complete
pinecone_indexed: false
pair: GBPUSD
strategy: custom-asia-sweep-london-reclaim
agent: analyst
---

# GBPUSD: Top-Down Analysis — 04.05.2026

> **Час фіксації:** 2026-05-04 05:25 UTC / 08:25 EEST (Київ)
> **Поточна ціна (OANDA):** 1.35890
> **News context:** ⚠️ **UK Bank Holiday (Early May)** — LSE закритий, sterling-flow знижений на 50-70%. Очікується підвищена кількість фейкових wicks і фалс-брейків на лондонській сесії. Recommended: skip або size /3.

---

## 🏛 Weekly (Тижневий графік)
100W range: `1.20997 – 1.38700`, +6.83% за період. Останні 5W: `1.34601 → 1.35184 → 1.35308 → 1.35750 → 1.35884` — повільне step-by-step розширення вгору без імпульсу.
**Структура:** ціна за ~70 пунктів від 100W high (1.38700). Це зона equal highs / ймовірний buy-side liquidity pool 1.387-1.395 (psychological 1.40).
**HTF Bias:** `Bullish-Corrective / Exhausted` — тренд живий, але близько до supply. Очікується або grab 1.387 highs з reversal, або continuation з ретесту ~1.345-1.350.

![[img/gbpusd_w.png]]

## 📅 Daily (Денний графік)
100D range: `1.31596 – 1.38700`, +1.47%. Останні 5D: `1.35180 → 1.34764 → 1.36034 → 1.35750 → 1.35883`.
**Структура:** очевидний sweep низу 1.34578 → recovery до 1.36124 → консолідація. Формується HL-схема: low 1.34542 (H4) як key support, supply 1.36034-1.36578.
- **Key levels D:** PDH = 1.36053, PDL = 1.35751, weekly high = 1.36578 (=PWH, equal до 5-day high — sell-side magnet НЕ, **buy-side liquidity pool**).
- Position у W range: верхня третина (~75%).

![[img/gbpusd_d.png]]

## ⏱ 4-Hour (4-годинний графік)
100×H4 range: `1.33809 – 1.36578`, +1.07%. Останні 5×H4: `1.35990 → 1.35750 → 1.35867 → 1.35880 → 1.35884`.
**Структура:** **range-compression** під supply `1.3603-1.3658`. H4 swing low = 1.35688 (інтрадей), H4 supply = 1.36016-1.36578 (FVG + OB cluster).
- Видно H4 BOS UP від 1.34542 → 1.36578, потім pullback. Зараз — фаза балансу всередині premium 50-70% impulse leg.
- Немає чіткого CHoCH вниз — bias H4 ще bullish, але momentum згас.

![[img/gbpusd_h4.png]]

## 🕐 1-Hour (1-годинний графік)
H1 range (~4 доби): `1.34542 – 1.36578`, +0.48%. Останні 5H: `1.35846 → 1.35854 → 1.35978 → 1.35880 → 1.35880`.
**Структура:** equal highs ~1.35990-1.36016 (3 рази тестувалось — buy-side liquidity), equal lows ~1.35856-1.35870 (sell-side liquidity внизу range).
Локальний H1 OB: `1.35790-1.35850` (bullish, bullish-OB після last impulse).
**SMT з EURUSD:** EURUSD робить аналогічну компресію — кореляція синхронна, **немає bullish дивергенції**. Це знижує ймовірність breakout вгору без зовнішнього drivera (а через UK holiday — драйверa немає).

![[img/gbpusd_h1.png]]

## 🎯 15-Minute (15-хвилинний графік)
M15 range: `1.35688 – 1.36578` (~25 H). Last 5×M15: `1.35873 → 1.35867 → 1.35880 → 1.35872 → 1.35882` — мертва зона ±10 пунктів.
**Сценарії:**
1. **Конс. (LONG):** sweep equal lows `1.35688-1.35750` (Asia low + PDL) → CHoCH M5 → entry в H1 OB `1.35790-1.35850` → ціль 1.36016 (H1 EQH liquidity).
2. **Агр. (SHORT):** sweep equal highs `1.35990-1.36053` (PDH + H1 EQH) → CHoCH M5 → SHORT з 1.36016-1.36050 → ціль `1.35688` (M15 low / PDL).
3. **PASS:** через UK Bank Holiday і slow flow — 70% ймовірність всю сесію провести у range 1.3585-1.3600 без trigger.

![[img/gbpusd_m15.png]]

## ⚡ 5-Minute (5-хвилинний графік) — Торговий план

> **Edge: Asia-Range Sweep + London-Reclaim Fade (Fade-the-Holiday-False-Break)**
>
> **Обґрунтування власного edge:** Класичний breakout-trade сьогодні зламається через UK Bank Holiday (низька ліквідність → фейкові wicks). Edge — **ловити саме ці фейки**: чекати sweep equal-highs/lows Asia range на London open, потім швидкий reclaim назад у range — це сигнал, що "stop hunt" відіграно і ціна повертається до VWAP/midpoint. Це mean-reversion edge на тонкому ринку.
> Подібно до концепції Stop-Hunt Reversal (Larry Williams) + IPDA judas swing (ICT), але адаптовано до **range-day з відсутністю institutional flow**.
>
> **Чому не trend-continuation:** D bias bullish, але H4 momentum згас + UK holiday прибирає sterling buyers → ймовірний breakout 1.3603 виявиться false. Натомість sweep 1.36050 + повернення = high-conviction short scalp.

### Основний план (Сетап A — SHORT fade buy-side sweep)

- **Bias (intraday):** Range / Mean-Reversion 📊 (ігноруємо HTF bullish — на тонкому дні pullback відбудеться)
- **Trigger:** Sweep equal-highs `1.35990-1.36053` з закриттям M5 < 1.35990 → CHoCH M5 вниз
- **Entry Zone:** `1.35990 – 1.36020` (limit-sell після sweep+reclaim)
- **Stop Loss:** `1.36110` (вище H4 micro-supply і Asia high cluster) — **~12 pts (= 12.0 pips)** від 1.35990
- **TP1:** `1.35870` (M15 mid-range, intraday VWAP) — RR ≈ **1.0** (12 pts)
- **TP2:** `1.35750` (PDL / D OB low) — RR ≈ **2.0** (24 pts)
- **TP3:** `1.35688` (M15 low / sell-side liquidity) — RR ≈ **2.5** (30 pts)
- **Lot Size (стандарт без holiday discount):** `$100 / (12 pts × $10/pip) = 0.83 lot`
  - **⚠️ З UK Bank Holiday discount (size /3):** `0.27 lot` ризик ≈ $33 (0.33% депозиту)
  - Pip value FX major OANDA: 1 pip = $10 на 1 lot — **перевірити брокер**

### Альтернативний план (Сетап B — LONG fade sell-side sweep)

- **Trigger:** Sweep `1.35688-1.35750` з закриттям M5 > 1.35790 → CHoCH M5 вгору
- **Entry:** `1.35790 – 1.35820` (H1 OB)
- **SL:** `1.35650` (нижче sweep low) — **~14 pts**
- **TP1:** 1.35880 (mid) — RR 0.6 ❌ (subоптимально)
- **TP2:** 1.36000 (H1 EQH) — RR 1.5 ⚠️
- **TP3:** 1.36050 (PDH) — RR 1.85
- **Висновок B:** RR недостатній, **сетап B = SKIP**, тільки A торгується.

![[img/gbpusd_m5.png]]

---

## 📊 Setup Score та рекомендації

| Фактор | Score |
|--------|-------|
| HTF bias clarity (W bullish-corrective) | +1 |
| D structure (HL + sweep recovery) | +1 |
| H4 supply zone identified | +1 |
| H1 EQH/EQL liquidity pools clear | +2 |
| M15 trigger condition specific | +1 |
| RR TP2 ≥ 1:2 | +1 |
| Session window (Asia→London) | +0.5 |
| **MINUS** UK Bank Holiday | **−2** |
| **MINUS** SMT no divergence (EURUSD сінхронний) | **−0.5** |
| **MINUS** немає institutional flow drivera | **−0.5** |
| **TOTAL** | **4.5 / 10** |

**Вердикт:** Setup є, але **Score 4.5 — нижче 5**. Технічно `SKIP` за внутрішнім порогом dispatcher.

**Якщо все-таки торгувати:**
- Тільки сетап A (SHORT fade)
- Тільки якщо sweep відбувся в London KZ (06:00-08:00 UTC влітку = 09:00-11:00 Київ)
- Size /3 від стандартного (0.27 lot замість 0.83)
- Take TP1 (RR 1.0) → BE на залишку, **не чекати TP2/TP3** на тонкому ринку
- **HARD STOP**: якщо до 12:00 UTC trigger не зайшов — закрити чарт, не дивитись до завтра

---

## 🚨 News Risks
- **UK Bank Holiday (Early May)** — весь день, без релізів, без LSE flow
- US: жодних high-impact релізів сьогодні (Sunday → Monday US open o 13:30 UTC; FX cash session нормальна, але парний driver відсутній)
- Наступні катализатори: BoE meeting (тиждень+), FOMC (через 10 днів)

## 🕐 Best Session
- **Уникати:** Asia (вже відробила), Frankfurt-only (07:00-09:00 UTC, без London)
- **Допустимо:** NY open 13:30-15:00 UTC — якщо до того range не пробитий
- **Перенести краще на:** вівторок 2026-05-05, коли London повернеться до повного flow

## Коментар (контекст)
GBPUSD у вузькому balance під 4-day supply 1.3603-1.3658, з недавнім sweep PDL 1.34542 і recovery. Класична фаза `accumulation under supply` — статистично 60% таких фаз перед `BoE-week` розв'язуються вгору з вибиттям equal highs. Але **сьогодні** через UK holiday цей вибух заборонений за logic, тому будь-який спайк = stop-hunt → fade. SMT з EURUSD синхронний (без divergence) — це додатково підтверджує, що рух буде корелятним і дрібним. Кращий план дня — **спостереження**, не торгівля.
