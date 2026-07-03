---
title: GER40 Top-Down Analysis
date: 2026-07-01
tags: [GER40, TDA, bullish-corrective, indices]
category: Analysis
project: Trading
pair: GER40
agent: analyst
status: analysis-complete
pinecone_indexed: false
---

# GER40 (DAX): Top-Down Analysis — 01.07.2026

> Час аналізу: 08:41 Київ / 05:41 UTC. Мультистратегічна база для ASR+ORB / SMC+PA / VWAP.
> Ціна на момент аналізу: **24 979**. Xetra cash open — 10:00 Київ (ASR-вікно з 10:05, ORB 10:00–10:30).

## 🏛 Weekly (Тижневий графік)
W: +40.95% за ~рік (17 020 → 25 512 ATH). Останні 5W closes: `24 574 → 24 671 → 24 997 → 24 642 → 24 976`.
Ціна консолідується під ATH **25 512** (Strong High). Структура HTF бичача (серія HH/HL), але останні 5 тижнів — сайдвей 24 549–25 364 під максимумами → **distribution/re-accumulation під ATH**.
**HTF verdict: Bullish, але виснажений біля стелі (Bullish-Corrective).**

![[img/ger40_w.png]]

## 📅 Daily (Денний графік)
20D range `~24 100 – 25 446`, D зараз −0.08%. Останні 5D closes: `24 980 → 24 642 → 24 730 → 24 996 → 24 977`.
У п'ятницю 26.06 був sweep вниз до **24 549** (забрано PWL-ліквідність), далі 3 бичачі дні реклейму назад до 25 000. Ціна над 20D MA (~24 811). Свічки останніх днів дрібнотілі → нерішучість під опором.
- **PDH 25 042 / PDL 24 677** (30.06)
- **Daily Open 24 996.5**
- **PWH 25 180 / PWL 24 549**

![[img/ger40_d.png]]

## ⏱ 4-Hour (4-годинний графік)
H4 range `23 950 – 25 180` (30 барів), +1.57%. Останні 5×4H closes: `25 005 → 24 996 → 25 008 → 24 976 → 24 976`.
Реклейм із 24 549 → higher highs → зараз тісний coil 24 976–25 010 **прямо під опором 25 040**. Структура бичача, але momentum згас (дрібні тіла впритул до supply).
**H4: BOS UP збережений, консолідація під 25 040.**

![[img/ger40_h4.png]]

## 🕐 1-Hour (1-годинний графік)
H1 +0.9%, range `24 549 – 25 093`. Вчора London→NY розгін: Frankfurt low ~24 700 → **NY BOS до 25 024** (локальний BSL). Далі Tokyo/overnight — консолідація в H1 OB-зоні `24 956 – 25 024`, ціна тримається над висхідною 50-EMA (~24 956).
- Supply зверху: **25 100 – 25 200** (Strong High H1)
- Demand знизу: **24 860 – 24 956** (H1 OB), Weak Low ~24 520
**SMT:** з US500 / EURUSD — потрібна перевірка на дивергенцію на open (індекси корельовані; при розгоні DAX без підтвердження US500 — сигнал слабкості).

![[img/ger40_h1.png]]

## 🎯 15-Minute + ⚡ 5-Minute (тригери + овернайт-структура)
Овернайт (Tokyo) — тісний коридор. LuxAlgo фіксує **EQH ~25 016–25 021** (рівні максимуми = BSL зверху) та **EQL ~24 968** знизу. OTE-зона (long) **24 917 – 24 942** (62–70.5% ретрейс), extension цілі 1.618 = **25 125**, 2.0 = **25 182**.
LuxAlgo OB/зони:
- Supply: `25 031–25 042`, `25 007–25 024`
- Demand: `24 894–24 922`, `24 805–24 828`, `24 756–24 772`

**Сценарії на open:**
1. **Bullish ASR (пріоритет, за HTF):** sweep < 24 948 (overnight low) у demand 24 894–24 956 → reclaim назад > 24 948 → long до 25 024 / 25 042, далі 25 125 / 25 182.
2. **Bearish ASR:** sweep > 25 024/25 042 (overnight high/PDH) у supply 25 031–25 042 → fail + reclaim < 25 024 → short до 24 894–24 860.

![[img/ger40_m15.png]]

![[img/ger40_m5.png]]

---

## 📐 Зведення ключових рівнів

| Тип | Ціна | Джерело |
|-----|------|---------|
| ATH / Strong High | **25 512** (W) / ~25 600 (D-лінія) | Weekly max |
| Resistance / BSL | **25 180 (PWH)** | Прев. тижневий max |
| Supply / OTE ext | 25 125 / 25 182 | OTE 1.618 / 2.0 |
| Supply (H1) | 25 100 – 25 200 | H1 Strong High |
| **PDH / overnight high** | **25 042** | LuxAlgo OB 25 031–25 042 |
| **BSL (EQH / NY high)** | **25 024** | LuxAlgo EQH, локальна ліквідність |
| **Daily Open** | **24 996.5** | сьогодні |
| Ціна | 24 979 | поточна |
| **Overnight low / EQL** | **24 948 / 24 968** | H1 OB база |
| Demand (H1/EMA) | 24 894 – 24 956 | H1 OB + 50-EMA |
| OTE long zone | 24 917 – 24 942 | OTE 62–70.5% |
| Demand (LuxAlgo) | 24 805 – 24 828 | OB |
| **PDL** | **24 677** | 30.06 low |
| M15 swing low / SSL | 24 756 | локальний low |
| **PWL / Weak Low** | **24 549 / 24 520** | прев. тижневий low |

**Овернайт-діапазон (Asian/Tokyo):** `24 948 – 25 024` (~76 pts), екстремум зверху 25 042 (PDH).
**Ліквідність зверху:** 25 024 (EQH) → 25 042 (PDH) → 25 180 (PWH).
**Ліквідність знизу:** 24 948 (overnight low) → 24 677 (PDL) → 24 549 (PWL).

## 📊 VWAP
Окремого VWAP-індикатора на чарті немає. Овернайт-консолідація центрована ~**24 985**; ціна 24 979 = фактично НА овернайт-mean (нейтрально, без девіації). Session VWAP формуватиметься від Xetra open 10:00. Для VWAP-стратегії: якщо сесія піде вгору (за HTF) — купувати відкати до session-VWAP; наразі відхилення немає → чекати відкриття.

## 🧭 Режим ринку
**HTF Trend-Bullish (W/D/H4/H1) + внутрішньоденний Range/coil під опором.**
Тобто «trend continuation pending breakout»: усе вище тримається бичачим, але ціна затиснута між 24 948 (overnight low) і 25 024/25 042 (BSL/PDH). Тригер — реакція на Xetra open.

---
**Коментар:** DAX впритул під ATH, momentum на HTF згасає — ризик false breakout вгору (sweep 25 042 → reversal). За HTF пріоритет — bullish sweep&reclaim знизу. News-ризик перевірити (ForexFactory EUR/DE + US ISM/NFP-тиждень). Найкраще вікно: Frankfurt/London open 10:00–12:00 Київ. Вхід не раніше 09:00 Київ (зараз 08:41 — до open лишилось ~1h20).
