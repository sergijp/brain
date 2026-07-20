---
title: EURUSD Top-Down Analysis
date: 2026-07-17
tags: [EURUSD, TDA, bearish-corrective, forex]
category: Analysis
project: Trading
pair: EURUSD
strategy: asr-orb-intraday-system
agent: analyst
status: analysis-complete
pinecone_indexed: false
---

# EURUSD: Top-Down Analysis — 17.07.2026 (П'ятниця)

> Час аналізу: 05:15 UTC / 08:15 Kyiv (пре-London, азійська сесія). Ціна: **1.14359–1.14373**.
> Депозит $10 000, ризик 1% ($100). Інтрадей, flat раніше (п'ятниця, weekend-gap ризик).

## 🏛 Weekly (Тижневий графік)
15W range `1.13246 – 1.18492`. Тиждень **-0.75%**. Останні 5W closes: `1.14712 → 1.13850 → 1.14376 → 1.14150 → 1.14379` — важкий боковик під ATH-зоною 1.18+, серія нижчих закриттів після відкату від вершини. **HTF Bearish-Corrective / Distribution** під незнятою стелею.

![[img/eurusd_w.png]]

## 📅 Daily (Денний графік)
20D range `1.13246 – 1.14824`, **-0.23%** сьогодні (форм. бар low 1.14346). Останні 5D: `1.13804 → 1.14209 → 1.14636 → 1.14431 → 1.14376` — відновлення з Strong Low 1.13775, тик у стелю **Weak High 1.14824/1.14870** і розворот вниз. Останні 2 дні — **LH під стелею** (розподіл). Стеля 1.14824/1.14870 **НЕ знята вже 22 дні** — головний BSL-магніт зверху. Ціна в середині діапазону з ведмежим ухилом.

![[img/eurusd_d.png]]

## ⏱ 4-Hour (4-годинний графік)
H4 range `1.13775 – 1.14824`, **+0.06%**. Останні 5×4H: `…1.14348 → 1.14431 → 1.14468 → 1.14362 → 1.14375` — консолідація в середині H4-діапазону, плоска MA. Demand OB `1.14128–1.14058` (відскок 16.07 встояв), Supply `1.14700–1.14870`. **Range-bound**, без імпульсу.

![[img/eurusd_h4.png]]

## 🕐 1-Hour (1-годинний графік)
H1 24h **-0.23%**, range `1.14310 – 1.14764`. Пік 1.14800 (Weak High) сформовано 16.07 → **CHoCH вниз** → серія LH, ціна під помаранчевою MA і під supply `1.14700–1.14739`. **H1 короткостроково ведмежий.** Нижче — OTE `1.14000–1.14200`, Strong Low 1.13804 (SSL).
**SMT:** USD широко сильний (Philly Fed 41.4 вчора), DXY bid → підтверджує слабкість EUR. Бичачої дивергенції під EUR-лонги немає — SMT на боці USD-strength.

![[img/eurusd_h1.png]]

## 🎯 15-Minute (15-хвилинний графік)
Азійський діапазон **вузький: `1.14346 – 1.14482`** (~13.6 pips) — ідеальна прекондиція для ASR. Ціна коілиться на мікро-demand шельфі 1.14300–1.14380.
Сценарії (ASR — Asia Sweep & Reclaim, London open):
1. **Пріоритет — SHORT (за HTF):** sweep **Asia high 1.14482** (Judas вгору) → M15 reclaim/rejection close назад під 1.14460 → шорт до 1.14300 → 1.14128.
2. **Контр (нижча ймовірність):** sweep Asia low 1.14346 → reclaim → лонг (проти USD-strength, є offside paper long 1.14602 — не пріоритет).

![[img/eurusd_m15.png]]

## ⚡ 5-Minute (5-хвилинний графік) — Торговий план (ПОПЕРЕДНІЙ, conditional на ASR-тригер)

- **Bias:** Bearish-corrective (short, intraday) 📉
- **Entry Zone (post-sweep 1.14482):** `1.14450 – 1.14465` (reclaim short)
- **Stop Loss:** `1.14540` (над sweep Asia high + буфер) — **~9 pts**
- **TP1:** `1.14350` (Asia low) — RR ~1.2
- **TP2:** `1.14250` (M15 demand/OTE) — RR ~2.3
- **TP3:** `1.14128` (H4 demand OB) — RR ~3.8
- **Lot Size:** `$100 / (9 pips × $10) ≈ 1.1 lot` (EURUSD: 1 pip = $10/lot — перевірити брокер)

⚠️ Тісний SL → великий лот; dixie фіналізує розмір/рівні. Тригер **ще не відбувся** — план активується тільки на sweep+reclaim у вікні 09:00–13:00 Kyiv.

![[img/eurusd_m5.png]]

---
**Коментар:** П'ятниця — flat раніше (17:45 Kyiv / weekend-gap BLOCK після 18:00). Інтрадей: TP має бути досягнутий за скорочену сесію — від 1.1437 до 1.14128 ~24 pips, реалістично для London KZ. London KZ (літо) 06:00–08:00 UTC, входи ≥09:00 Kyiv (зараз 08:15 — рано, WARN). Untested Weak High 1.14824/1.14870 зверху = ризик London-виносу вгору за BSL перед розворотом (це і є ASR sweep-high сценарій). Paper positions на чарті: long teaOOk @1.14602 (offside), long Zj9yNp @1.14128 (на H4 demand) — не чіпати. News/ECB/US-дані перевірити через news-watcher перед входом.

**Зміна проти вчора (16.07):** картина зсунулась **більш ведмеже**. Вчора був bull-corrective, London свінув Asia low → відскок від 1.14425 demand до 1.14569. Сьогодні USD продовжив зростати вночі → ціна **пробила вчорашній 1.14425 demand** і торгується 1.1437 нижче; H1 перейшов у CHoCH-down / LH. Стеля 1.14870 так і не знята (тепер 22 дні). Bias: bull-corrective → **bearish-corrective / range з ведмежим ухилом**.
