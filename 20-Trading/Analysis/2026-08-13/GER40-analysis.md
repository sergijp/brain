---
title: GER40 Top-Down Analysis
date: 2026-08-13
tags: [GER40, TDA, bullish-strong, indices]
category: Analysis
project: Trading
status: analysis-complete
pinecone_indexed: false
---

# GER40: Top-Down Analysis — 13.08.2026

## 🏛 Weekly (Тижневий графік)
W: +8.67% (15 тижнів), range `23 630.7 – 26 581.5`. Останні 5W: `24 829 → 25 077.5 → 25 705 → 26 364 → 26 417 (у процесі)` — чіткий ланцюг HH/HL, безперервний BOS вгору кожен тиждень, поточний тиждень оновив ATH на 26 581.5. **HTF Bullish-Strong**, momentum-фаза, ознак exhaustion (довгих upper wicks на топі) поки немає.

![[img/ger40_w.png]]

## 📅 Daily (Денний графік)
20D +6.28%, range `24 610.5 – 26 581.5`. Останні 5D: `26 364 → 26 342.04 → 26 390.28 → 26 356.01 → 26 416.5 (у процесі)` — тісна консолідація/accumulation під ATH після сильного ралі. Ціна утримується в верхній третині W-діапазону, sweep-ів PDH/PDL немає, структура не зламана.

![[img/ger40_d.png]]

## ⏱ 4-Hour (4-годинний графік)
H4 range `26 101.5 – 26 581.5` (30 барів, +0.89%). Останні 5×4H: `26 338 → 26 356.01 → 26 384.5 → 26 417 → 26 417` — recovery після pullback (H4-бар з 26 470.5 впав до low 26 315, після чого йде відновлення). Формується потенційний Higher Low в зоні 26 315–26 356, BOS вниз відсутній, структура bullish pullback / consolidation під ATH, а не CHoCH.

![[img/ger40_h4.png]]

## 🕐 1-Hour (1-годинний графік)
H1 +0.11% (30H), range `26 315 – 26 581.5`. Останні 5H: `26 391.5 → 26 409 → 26 423.5 → 26 417 → 26 418.5` — тісна accumulation одразу під нещодавнім хаєм, grinding sideways-up.
**SMT:** з US500 — обидва індекси в тісній консолідації біля своїх максимумів (US500: 30-бар range 7716.9–7773.4, останні 5H4 теж grind up без різкого відхилення). Дивергенції немає — SMT підтверджує bullish confluence, а не reversal.

![[img/ger40_h1.png]]

## 🎯 15-Minute (15-хвилинний графік)
Сценарії:
1. **Консервативно (LONG):** ретест зони `26 380 – 26 420` (H1 OB / mitigation після імпульсу до 26 437.5) + M15 CHoCH вгору → продовження до `26 581.5` і вище.
2. **Агресивно:** sweep зони `26 315 – 26 356` (H4 swing low, потенційний SSL) → reversal вгору з підтвердженням bullish M15 структури.

Наразі M15 у тісному діапазоні `26 366 – 26 437.5`, останні 5×M15: `26 414 → 26 417 → 26 435.5 → 26 431.5 → 26 417.5` — невеликий відкат від локального хаю, чіткого тригера (sweep+BOS) ще немає.

![[img/ger40_m15.png]]

## ⚡ 5-Minute (5-хвилинний графік) — Торговий план

⚠️ **Тригер ще не спрацював.** До 08:38 Kyiv (05:38 UTC) активної London/Frankfurt сесії немає (London open 07:00–10:00 UTC), і Xetra ORB-вікно (10:00–10:30 Kyiv за ASR+ORB системою) ще не почалось. План нижче — **попередній/умовний**, для виконання потрібне підтвердження sweep + CHoCH на M15/M5 в межах сесійного вікна.

- **Bias:** Bullish (long, corrective pullback у межах тренду) 📈
- **Entry Zone (умовно):** `26 380 – 26 420` (retest після M15 CHoCH вгору)
- **Stop Loss:** `26 290` (нижче H4 swing low 26 315, з буфером) — **~110 pts** від середини зони входу (26 400)
- **TP1:** `26 581.5` (поточний ATH / recent high) — RR ≈ 1.65
- **TP2:** `26 700` (round-number extension за ATH) — RR ≈ 2.7
- **TP3:** `26 900` (fib-extension зона) — RR ≈ 4.5
- **Lot Size:** `$100 / (110 × $1) ≈ 0.9 lot` (GER40/DAX: 1 pt = $1 на 1 контракт — **перевірити брокера**)

![[img/ger40_m5.png]]

---
**Коментар:** GER40 у сильному бичачому тренді на W/D (+8.67%/+6.28%), торгується під свіжим ATH (26 581.5) у тісній консолідації на H4/H1 — класична pullback/continuation структура, CHoCH-сигналів на розворот немає. SMT з US500 підтверджує bullish confluence (без дивергенції). Market regime: **Trend (continuation)**, за `strategy-detection.md` для GER40 спершу перевіряється ASR+ORB Intraday System (ORB Xetra 10:00–10:30 Kyiv, сателіт GER40, статус signal-mode/форвард-тест, live не раніше вересня 2026); якщо фільтри ORB не проходять — альтернативний playbook `smc-price-action-combo` (Sweep + OB Rejection + Retest, PRIMARY PATTERN). Вхід до 09:00 Kyiv і поза London/NY KZ — WARN за session-rules; ORB-вікно сьогодні відкриється о 10:00 Kyiv. Перевірити ForexFactory на ECB/DAX-звітність перед входом (news blackout ±30 хв).
