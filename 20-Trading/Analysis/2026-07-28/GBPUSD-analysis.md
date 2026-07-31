---
title: GBPUSD Top-Down Analysis
date: 2026-07-28
tags: [GBPUSD, TDA, bullish-corrective, forex]
category: Analysis
project: Trading
pair: GBPUSD
strategy: asr-orb-intraday-system
agent: analyst
status: analysis-complete
pinecone_indexed: false
---

# GBPUSD: Top-Down Analysis — 28.07.2026

> Час аналізу: 07:40 UTC / 10:40 Київ. London KZ активна (літо, 06:00–08:00 UTC хвіст). Депозит $10 000, ризик 1%.
> Контекст: GBPUSD лідирує сьогодні, EURUSD дав ASR sweep+reclaim long на London open. Новини по GBP чисті.

## 🏛 Weekly (Тижневий графік)
W: -1.39% (поточний тиждень корективний). 15W range `1.31402 – 1.36578`. Останні 5W closes: `1.33536 → 1.34021 → 1.34522 → 1.33239 → 1.33018` — ралі до 1.3558 (wick), потім 2-тижневий відкат. **HTF Bullish-Corrective**: структура вища, але зараз відкат до середини діапазону. Ціна ~1.3300 = mid-range.

![[img/gbpusd_w.png]]

## 📅 Daily (Денний графік)
20D range `1.3219 – 1.35582`, +0.33% сьогодні. Останні 5D closes: `1.33756 → 1.33144 → 1.33239 → 1.32882 → 1.33011`. Тиждень дистрибуції нижче від 1.3375. **Ключове:** сьогодні свіп нижче PDL (1.32845 → low 1.32836), потім reclaim до 1.3301 — бичачий reclaim на нижньому краю денного діапазону. Daily bias: **bearish-corrective, але з ознаками виснаження/reclaim на support**.

![[img/gbpusd_d.png]]

## ⏱ 4-Hour (4-годинний графік)
H4 range `1.32836 – 1.3434`, -0.97%. Останні 5×4H closes: `1.33032 → 1.32882 → 1.3293 → 1.32941 → 1.32986`. Був BOS down з 1.3434, зараз **консолідація/базування біля 1.3284 demand** (triple-tap 1.32836/45/57). CHoCH вгору ще НЕ підтверджено — структура down, але стабілізується на floor.

![[img/gbpusd_h4.png]]

## 🕐 1-Hour (1-годинний графік)
H1 -0.48%, range `1.32836 – 1.33637`. Мікроструктура LH/LL (bearish) від 1.33637, але останні 2 бари відскок від 1.3286 demand з reclaim (low 1.32857 → close 1.32987). H1 = базування на нижній межі.
**SMT:** з EURUSD — **узгоджено бичаче** (обидві пари дали London-open reclaim = широка слабкість USD). Це підтвердження (не дивергенція).

![[img/gbpusd_h1.png]]

## 🎯 15-Minute (15-хвилинний графік) — ASR фокус
**Азійський діапазон:** `~1.3286 – 1.3304` (тісний, ~18 pt).
**Послідовність ASR:**
1. Pre-London (08:00–09:00 Київ): свіп ліквідності азійського low → 1.32857/1.3286 (SSL grab).
2. Reclaim назад у діапазон (06:15 UTC close 1.32959 → 06:45 close 1.32987).
3. London open (10:00 Київ / 07:00 UTC): пробій азійського high 1.3304 → друк **1.33052 → M15 BOS UP**.

Сценарії:
1. **Консервативно (LONG):** ретест зони reclaim `1.3290–1.3299` + утримання → продовження до 1.3334/1.3364.
2. **Агресивно:** вже в лонг з ретесту 1.3304 breakout, SL під sweep low.

⚠️ Свіп був неглибокий (утримав 1.32857, не пробив екстремум 1.32836) — це **reclaim/reversal long проти H4-down**, не trend-continuation. ASR B-grade.

![[img/gbpusd_m15.png]]

## ⚡ 5-Minute (5-хвилинний графік) — Торговий план

- **Bias:** Bullish intraday reclaim (long, counter-H4 на HTF support) 📈
- **Entry Zone:** `1.3290 – 1.3299` (ретест reclaim / M15 OB від London-open імпульсу)
- **Stop Loss:** `1.3279` (нижче sweep low 1.32836 + H4 floor) — **~16 pts** від 1.3295
- **TP1:** `1.3312` — RR ~1.1 (перший H1 опір, часткова фіксація)
- **TP2:** `1.3334` — RR ~2.6 (H4 minor опір)
- **TP3:** `1.3364` — RR ~4.6 (PDH / H1 range high)
- **Lot Size:** `$100 / (16 pt × $10) ≈ 0.62 lot` (FX major: 1 pt = $10 на 1 lot — перевірити брокер OANDA)

![[img/gbpusd_m5.png]]

---
**Коментар:** Setup = інтрадей ASR-style LONG reclaim на HTF demand floor (W/D support 1.3284). Confluence: азійський свіп+reclaim, M15 BOS up на London open, EURUSD SMT підтвердження (обидві USD-down), новини GBP чисті, London KZ активна, NY KZ (12:00–14:00 UTC) — вікно для продовження. **Ризики:** контр-H4/D down-структура (reversal, не continuation), неглибокий свіп, тісний choppy range, RR до TP1 лише ~1.1 (потрібен TP2 для 1:2+). Вихід до вечора (інтрадей) — TP2 1.3334 реалістична за London+NY день. Setup score: **6.5/10**. Playbook (preliminary): `asr-orb-intraday-system` (ASR long) — на верифікацію strategy-picker.
