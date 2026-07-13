---
title: EURUSD Top-Down Analysis
date: 2026-07-13
tags: [EURUSD, TDA, bearish-corrective, forex]
category: Analysis
project: Trading
pair: EURUSD
strategy: smc-price-action-combo
agent: analyst
status: analysis-complete
pinecone_indexed: false
---

# EURUSD: Top-Down Analysis — 13.07.2026

> Час аналізу: 06:16 UTC / 09:16 Kyiv. Ціна на момент: **1.13966**. Дані TV свіжі (last bar 5m = поточна година). Сесія: **London KZ** (літо, 06:00–08:00 UTC) — вікно активне.

## 🏛 Weekly (Тижневий графік)
W: **−1.1%**. 15W range `1.13246 – 1.18492`. Останні 5W closes: `1.14712 → 1.13850 → 1.14376 → 1.14150 → 1.13966`. Після топу 1.185 — затяжний відкат, останні тижні дрейф униз у діапазоні 1.138–1.147, ціна тисне на багатотижневий low **1.13246**. **HTF Bearish-Corrective** (корекція в межах старшого uptrend, тест ключової підтримки).

![[img/eurusd_w.png]]

## 📅 Daily (Денний графік)
20D **−1.7%**, range `1.13246 – 1.16198`. Останні 5D closes: `1.14114 → 1.14162 → 1.14302 → 1.14150 → 1.13967`. Тісна консолідація 1.141–1.143 зламалась вниз: сьогоднішня свічка open 1.14018 → low 1.13844. Ціна в **discount** (нижче EMA, далеко під premium/OTE зоною 1.16–1.19). LuxAlgo demand нижче: 1.108–1.114 та 1.073–1.079. **Bias: bearish-continuation** до range low 1.13246 (sell-side liquidity).

![[img/eurusd_d.png]]

## ⏱ 4-Hour (4-годинний графік)
H4 range `1.13844 – 1.14608`, ≈ −0.2%. Останні 5×4H: `1.14296 → 1.14150 → 1.13955 → 1.14038 → 1.13980`. **BOS вниз** (пробій підтримки 1.1412), далі невеликий відскок. Ціна в blue **demand зоні 1.138–1.140**. Ключове: **"Weak Low" ~1.132** (ICT — слабкий лоу, ймовірний до зняття = магніт для ціни). Supply зверху **1.145–1.147**, Strong High 1.170.

![[img/eurusd_h4.png]]

## 🕐 1-Hour (1-годинний графік)
H1 ≈ −0.36%. Тісна акумуляція **1.1384 – 1.1399**, ціна відбивається від EMA/рівня **1.14105**. OB/OTE жовта зона 1.1384–1.1399; "Weak Low" H1 = 1.1384. Supply red 1.145–1.146.
**SMT:** пряме крос-порівняння цієї сесії не виконане (TV-tab залочений на EURUSD, `quote_get` повертав дані чарту). Якісно: EUR тисне на тижневі лоу → широка сила USD/DXY bid, дивергенції не зафіксовано. Перевірити GBPUSD/DXY окремим вікном перед входом.

![[img/eurusd_h1.png]]

## 🎯 15-Minute (15-хвилинний графік)
CHoCH біля 1.1399, ціна в OTE-зоні 1.1393–1.1399. Магента-рівні: **BSL 1.14082** (зверху), **SSL 1.13898 / weak low 1.1381** (знизу).
Сценарії:
1. **Основний (SHORT, консервативно):** sweep BSL `1.14082 → 1.1420` + rejection candle + retest → short до `1.1384 → 1.132`.
2. **Агресивно (SHORT continuation):** пробій `1.1384` + retest знизу → short до `1.132`.
3. **Контр-сценарій (LONG):** sweep weak low `1.13246` + reclaim з CHoCH → long до supply `1.1445`.

![[img/eurusd_m15.png]]

## ⚡ 5-Minute (5-хвилинний графік) — Торговий план

- **Bias:** Bearish-Corrective (short, continuation) 📉
- **Тип:** SMC+PA Combo — Sweep + OB Rejection + Retest (умовний, потрібен тригер)
- **Entry Zone:** `1.1405 – 1.1412` (retest після M15 sweep BSL 1.14082/1.1420 + rejection)
- **Stop Loss:** `1.1428` (вище sweep high / minor supply) — **≈ 20 pts**
- **TP1:** `1.1384` (H1 weak low / край demand) — RR **1.2**
- **TP2:** `1.1355` — RR **2.65**
- **TP3:** `1.1325` (над sell-side liquidity 1.13246) — RR **4.15**
- **Lot Size:** `$100 / (20 pts × $10) = 0.5 lot` (FX major: 1 pt = $10 на 1 lot — перевірити брокер OANDA)

![[img/eurusd_m5.png]]

---
**Коментар:** HTF bearish-corrective, ціна в discount, під BOS-вниз на H4. Головна ціль — sell-side liquidity під "Weak Low" 1.132 (магніт). Проте ціна затиснута у demand-зоні на H1/M15 — **потрібен тригер** (sweep BSL + rejection), без нього угоди немає. RR≥2 досягається ТІЛЬКИ через тісний sweep-based SL; при вході "по ринку" з широким SL сетап не торгувальний.
**Ризики:** ціль 1.132 близька для інтрадей (~50–80 pts) — реалістично закрити в межах дня (NY KZ). Контр-ризик: demand-зона може дати відскок до 1.1445 (LONG-сценарій при reclaim weak low).
**News:** перевірити ForexFactory на USD/EUR high-impact (CPI/ECB/FOMC) до входу — блекаут ±30 хв.
**Сесія:** зараз London KZ; продовження руху ймовірніше в NY KZ 12:00–14:00 UTC. Вхід ≥ 09:00 Kyiv — OK.
</content>
</invoke>
