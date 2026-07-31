---
title: EURUSD Top-Down Analysis
date: 2026-07-28
tags: [EURUSD, TDA, bearish-corrective, forex]
category: Analysis
project: Trading
pair: EURUSD
strategy: asr-orb-intraday-system
agent: analyst
status: analysis-complete
pinecone_indexed: false
---

# EURUSD: Top-Down Analysis — 28.07.2026

> Час аналізу: 07:33 UTC / 10:33 Київ. Активна сесія: **London KZ** (07:00–09:00 UTC). Дані TV свіжі (last bar 07:30 UTC). Ціна: **1.13705**.

## 🏛 Weekly (Тижневий графік)
15W range `1.13246 – 1.17967`, за період **−3.14%**. Останні 5W closes: `1.14376 → 1.14150 → 1.14382 → 1.13706 → 1.13720` — після імпульсу до 1.1797 йде глибока корекція; кілька тижнів stall біля 1.14, потім пробій вниз до 1.137. Ціна в **нижній третині** 15W діапазону. **HTF Bearish-Corrective** — низхідна корекція від ATH, над глибшою ліквідністю 1.1325.

![[img/eurusd_w.png]]

## 📅 Daily (Денний графік)
20D range `1.13618 – 1.14824`, **−0.45%**. Останні 5D closes: `1.14120 → 1.13775 → 1.13706 → 1.13683 → 1.13706` — планомірний grind вниз від 1.148 до 1.136, distribution біля лоу. **Сьогодні знято 20D/PDL ліквідність:** low дня `1.13618` пробив вчорашній PDL `1.1367` → повернення до 1.137 = **liquidity sweep sellside**. Позиція в W range — bottom.

![[img/eurusd_d.png]]

## ⏱ 4-Hour (4-годинний графік)
H4 range `1.13618 – 1.14358`, **−0.44%**. Останні 5×4H closes: `1.13798 → 1.13683 → 1.13742 → 1.13687 → 1.13705` — bearish drift, ціна тисне в лоу діапазону. За premium/discount fib (0=1.13590, 1=1.14101) ціна в **discount / OTE-зоні**. Над ринком стек weekly supply 1.15–1.19. Структура bearish, але ціна на екстремі discount після sweep.

![[img/eurusd_h4.png]]

## 🕐 1-Hour (1-годинний графік)
H1 **−0.38%**, range `1.13618 – 1.14184`. Останні 5H closes: `1.13746 → 1.13687 → 1.13659 → 1.13687 → 1.13709` — консолідація на лоу; після sweep `1.13618` ціна **реклеймила** назад вище PDL 1.1367 до 1.1371 (спроба bullish reclaim). Tight accumulation.
**SMT (EURUSD ↔ GBPUSD / DXY):** DXY `101.49 −0.02%` (USD слабкий), GBPUSD `1.3305 +0.13%` (лідирує вгору), EURUSD `+0.03%` (відстає). Cable веде — легка розбіжність, але **USD м'який → підтримує intraday reclaim/bounce**, не проти лонга.

![[img/eurusd_h1.png]]

## 🎯 15-Minute (15-хвилинний графік)
На London open знято SSL/PDL `1.13618`, CHoCH-спроба вгору, ціна в OTE/discount. Активний **ASR-патерн** (Asia Sweep & Reclaim).
Сценарії:
1. **Консервативно (LONG — ASR):** M15 close-reclaim `1.1367` + CHoCH → лонг з discount-зони `1.1368–1.1372` до premium `1.1400` / PDH `1.14184`.
2. **Агресивно (bearish HTF continuation):** ретест premium/supply `1.1400–1.1418` → шорт до `1.1362` / `1.13246`.

![[img/eurusd_m15.png]]

## ⚡ 5-Minute (5-хвилинний графік) — Торговий план (ASR long, preliminary)

- **Bias:** HTF Bearish-Corrective; **intraday LONG** (ASR sweep-reclaim, counter-HTF bounce) 📈
- **Entry Zone:** `1.1368 – 1.1372` (реклейм PDL, на M15 CHoCH-підтвердженні)
- **Stop Loss:** `1.1358` (нижче sweep-low 1.13618) — **~12 pts**
- **TP1:** `1.1385` (intraday BSL/SH) — RR ~1.2
- **TP2:** `1.14000` (premium 0.5 / round) — RR ~2.5
- **TP3:** `1.14184` (PDH — major BSL) — RR ~4.0
- **Lot Size:** `$100 / (12 × $10) ≈ 0.83 lot` (EURUSD: 1 pt = $10/lot — перевірити брокер OANDA)

![[img/eurusd_m5.png]]

---
**Коментар:** HTF (W/D) чітко bearish-corrective від 1.1797, глибша ліквідність знизу 1.13246. Але intraday на London open відбувся класичний **ASR sweep** PDL 1.1367 → low 1.13618 → reclaim, ціна в discount/OTE. EURUSD — ASR-пара, вікно 09:00–13:00 Київ активне (зараз 10:33), flat до 17:45. USD слабкий (DXY −0.02%), GBPUSD лідирує — підтримує intraday bounce. **Setup counter-HTF** — тільки intraday, TP2 1.1400 досяжний за день. Альтернатива: якщо reclaim провалиться і ціна закриється < 1.1360 — шорт-continuation до 1.1325. ⚠️ Перевірити календар (news blackout) перед входом; підтвердити M15 CHoCH-реклейм тригер. Best window: London KZ / NY KZ.
