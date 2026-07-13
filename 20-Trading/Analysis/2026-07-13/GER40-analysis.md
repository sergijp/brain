---
title: GER40 Top-Down Analysis
date: 2026-07-13
tags: [GER40, TDA, bias-mixed, Analysis, ASR-ORB]
category: Analysis
project: Trading
pair: GER40
strategy: asr-orb-intraday-system
agent: analyst
status: analysis-complete
pinecone_indexed: false
---

# GER40 (DAX): Top-Down Analysis — 13.07.2026

> Час аналізу: 09:26 Kyiv / 06:26 UTC. Понеділок, DE/EZ high-impact новин немає (день чистий).
> Поточна ціна: **24893.5**. Xetra open ~10:00 Kyiv (ORB-30: 10:00–10:30). ASR-вікно GER40 з 10:05.
> Депозит $10 000, ризик 1% ($100). Pip GER40: 1 pt = $1 / 1 контракт (перевірити брокер).

## 🏛 Weekly
15W range `22835.5–25923`, **+7.6%**. Останні 5W closes: `24997.5 → 24642.5 → 25806.5 → 25097.5 → 24894.5`.
Довгостроковий аптренд, але останні 2 тижні — корективні LH одразу під ATH **25923** (довгі верхні тіні = exhaustion біля вершини).
**HTF Bias: Bullish-Exhausted** (структурно бичачий, але біля ATH формується розподіл).

![[img/ger40_w.png]]

## 📅 Daily
20D range `24549–25923`, +0.19%. Останні 5D closes: `25464 → 24974 → 25111 → 25097 → 24890.5`.
Відкид від ATH 25923 → серія lower highs → консолідація `24770–25200`. Сьогодні відкрились на 25097 і продали до **24770** (session low).
**Daily: короткостроково bearish/distribution**, ціна в нижній половині діапазону тижня.

![[img/ger40_d.png]]

## ⏱ 4-Hour
H4 range `24770–25860.5`, **−3.63%** за вікно. Останні 5×H4: `25112 → 25097.5 → 24948 → 24803 → 24890.5`.
Чіткий **BOS DOWN** з 25860 до 24770 — імпульсна ведмежа нога. Наразі перший відскок від 24770.
**H4: Bearish (BOS down), retest supply зверху = висока ймовірність продовження вниз.**

![[img/ger40_h4.png]]

## 🕐 1-Hour
H1 range `24770–25199.5`, −0.91%. Останні 5H: `24888 → 24844 → 24803 → 24848 → 24891`.
Провал у 24770 (Asian/overnight low) + реклейм — будуються higher lows.
**SMT (індекси):** узгодити з US100/US500 на London open — розбіжність підсилить/послабить reversal.
**H1: реклейм від 24770 у процесі** — рання ознака ASR-розвороту вгору всередині H4-даунтренду.

![[img/ger40_h1.png]]

## 🎯 15-Minute
Range `24770–25065`. Останні 5×M15: `24804 → 24834 → 24848 → 24861 → 24892` — послідовні higher lows від sweep-low 24770.
**ICT HTF candle**: high **25105** / low **24770** (15m/30m/1H збігаються) — це операційний діапазон дня.

Сценарії (тригер після Xetra open 10:05 Kyiv):
1. **ASR LONG (система, primary):** утримання/реклейм 24770 → M15 CHoCH bullish вище 24924 → ретест demand OB `24797–24818` → long до 25046/25098.
2. **SHORT (H4-aligned, alt):** рел ап у supply `25046–25098` → M15 rejection + CHoCH down → short назад до 24770 і нижче.

![[img/ger40_m15.png]]

## ⚡ 5-Minute — Торговий план (preliminary)

M5: ціна 24893.5, higher lows, відновлення від 24770. Тригер ще НЕ підтверджений (до Xetra open ~34 хв).

### Сценарій A — ASR LONG (primary, узгоджено з ASR+ORB)
- **Bias:** intraday reversion (провалений пробій Asian low 24770 + реклейм) 📈
- **Entry Zone:** ретест demand OB `24800 – 24818` (після M15 CHoCH вище 24924)
- **Stop Loss:** `24745` (під sweep-low 24770) — **~65 pts**
- **TP1:** `24928` (OTE / micro-high) — RR ≈ 1.8
- **TP2:** `25046` (supply low / mid-range) — RR ≈ 3.6
- **TP3:** `25098` (ICT candle high / supply OB) — RR ≈ 4.4
- **Lot:** `$100 / (65 × $1) ≈ 1.5 контракти` (GER40: 1 pt = $1 — перевірити брокер)
- ⚠️ Проти H4-даунтренду — обов'язкове M15-підтвердження, без CHoCH не входити.

### Сценарій B — SHORT (alt, узгоджено з H4 BOS down)
- **Bias:** trend-continuation вниз 📉
- **Entry Zone:** rejection у supply `25046 – 25098`
- **Stop Loss:** `25160` (над OB high 25128) — **~100 pts** від 25060
- **TP1:** `24924` — RR ≈ 1.4
- **TP2:** `24770` (session low) — RR ≈ 2.9
- **TP3:** `24633` (Fib 1.618) — RR ≈ 4.3
- **Lot:** `$100 / (100 × $1) ≈ 1.0 контракт`

![[img/ger40_m5.png]]

---

## Ключові рівні (зведення)
| Рівень | Тип | Ціна |
|--------|-----|------|
| ATH / Weekly BSL | Liquidity above | 25923 |
| Daily swing high | Resistance | 25199.5 |
| Supply OB (ICT candle high) | Resistance | 25098–25128 |
| Supply / OTE | Resistance | 25046–25066 |
| Minor OB | Intraday R | 24914–24924 |
| **Поточна ціна** | — | **24893.5** |
| Demand OB | Support (entry LONG) | 24797–24818 |
| **Sweep low (Asian/SSL)** | **Support / Liquidity below** | **24770** |
| Fib 1.618 | Downside target | 24633 |
| Fib 2.0 | Downside target | 24532 |

## Вердикт
- **HTF (W/D):** mixed — W bullish-exhausted, D короткостроково bearish.
- **H4:** bearish (BOS down), перший відскок від 24770.
- **Intraday:** ASR-реклейм 24770 у процесі — конфлікт із H4.
- **Рекомендація:** дочекатись Xetra open (10:00–10:30 Kyiv). ASR LONG як primary тільки з M15 CHoCH; інакше SHORT з supply. До тригера — не входити.
