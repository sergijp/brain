---
title: GBPUSD Top-Down Analysis
date: 2026-07-08
tags: [GBPUSD, TDA, range, forex]
category: Analysis
project: Trading
pair: GBPUSD
strategy: asr-orb-intraday-system
agent: analyst
status: analysis-complete
pinecone_indexed: false
---

# GBPUSD: Top-Down Analysis — 08.07.2026

> Час аналізу: 06:11 UTC / 09:11 Kyiv. Поточна ціна: **1.3356**. London KZ (літо 06:00–08:00 UTC) — активна. ASR-вікно (06:00–10:00 UTC / 09:00–13:00 Kyiv) — живе.

## 🏛 Weekly (Тижневий графік)
W: **+0.72%**. 15W range `1.31402–1.36578`. Останні 5W: `1.34066 → 1.32335 → 1.31974 → 1.33536 → 1.33573` — провал до LL 1.319, потім відскок від Strong Low **1.3140** назад до 1.335. Ціна в середині широкого діапазону, під супплаєм 1.36–1.37 (Weak High 1.386) і над демандом 1.314. **HTF: Neutral / corrective-bullish (відновлення від strong low, але без пробою супплаю).**

![[img/gbpusd_w.png]]

## 📅 Daily (Денний графік)
20D range `1.31402–1.34610`, **−0.11%**. Останні 5D: `1.3347 → 1.33536 → 1.33897 → 1.3359 → 1.33576` — leg відновлення від 1.314 до ~1.339, тепер консолідація 1.335–1.339. Прямо над ціною — **D EQH / supply 1.340–1.348** (ключова зона рішення), вище Weak High 1.386. Знизу — Strong Low 1.314 + деманд-бокс 1.302–1.313. Була BOS вниз (1.34→1.314), далі recovery. **D: corrective-bullish у діапазоні, підходить знизу до супплаю 1.340–1.348.**

![[img/gbpusd_d.png]]

## ⏱ 4-Hour (4-годинний графік)
H4 range `1.3219–1.34018`, **+0.84%**. BOS вгору від 1.322, але імпульс глохне: сформовано **LH під 1.340**, ціна відкотилась у 1.335 під жовту H4 supply/OB зону **1.338–1.341**. **H4: recovery → стагнація, потенційний LH/range під 1.340.**

![[img/gbpusd_h4.png]]

## 🕐 1-Hour (1-годинний графік)
H1 **−0.23%**, range `1.33423–1.34018`. Ціна відвалилась від London/Frankfurt хая **1.340 (Weak High / BSL)** вниз до 1.334, під спадним EMA — короткостроково ведмежо (LH). Зараз сидить на H1 деманд-зоні **1.333–1.334**. Нижче: 1.330, далі кластер 1.320–1.328.
**SMT:** GBPUSD ↔ EURUSD/DXY — обидва мажори у середині діапазону після відскоку від лоу, USD загалом м'який/консолідує. Явної дивергенції не зафіксовано *(quote-крос по chart-символу недоступний без перемикання табу — оцінка якісна).*

![[img/gbpusd_h1.png]]

## 🎯 15-Minute (15-хвилинний графік)
Азійський діапазон вузький: **~1.3344–1.3362** (жовта зона). Над ним ліквідність — Weak High **1.340 (BSL)** + стек супплаю 1.337–1.340. Знизу — **Strong Low 1.3326 (SSL)**. Ціна затиснута, легкий бід (зелені бари).

Сценарії ASR (London open):
1. **Основний — LONG (sweep SSL + reclaim):** провал 1.3326 → M15 reclaim-close назад у діапазон → лонг до 1.340 BSL. Узгоджено з W-відскоком від strong low.
2. **Альтернатива — SHORT (sweep BSL + reclaim):** ралі в 1.340 Weak High → M15 rejection-close назад під 1.337 → шорт до 1.333/1.330. Узгоджено з D-супплаєм 1.340–1.348 та H1 LH.

![[img/gbpusd_m15.png]]

## ⚡ 5-Minute (5-хвилинний графік) — Торговий план (ASR, попередній)

- **Bias:** Mixed / range — corrective-bullish HTF vs H1 LH 📉📈
- **Основний сетап (ASR long):** sweep 1.3326 SSL → M15 reclaim
- **Entry Zone:** `1.3340 – 1.3348` (після reclaim-close вище 1.3345)
- **Stop Loss:** `1.3316` (під Strong Low 1.3326) — **~29 pts**
- **TP1:** `1.3400` (Weak High / BSL) — RR ~1.9
- **TP2:** `1.3440` (нижній край D EQH supply) — RR ~3.3
- **TP3:** `1.3480` (D EQH supply core) — RR ~4.6 *(поза інтрадей-таргетом, до flat 17:45)*
- **Lot Size:** `$100 / (29 × $10) ≈ 0.34 lot` (GBPUSD: 1 pt = $10/lot — перевірити брокер)

![[img/gbpusd_m5.png]]

---
**Коментар:** Пара в середині широкого W/D-діапазону — чистого HTF-тренду немає, тому setup — це ASR-watch, а не A+ сетап. Ключ дня: реакція на азійські екстремуми (1.3326 SSL / 1.340 BSL) на London open. HTF-supply 1.340–1.348 обмежує апсайд → фейд 1.340 (short) технічно валідний, але відскок від Strong Low робить long-off-sweep 1.3326 актуальнішим на open. **News:** high-impact лише FOMC Minutes 18:00 UTC — після інтрадей-flat, blackout під час вікна немає. Kyiv 09:11 > 09:00 ✓. Best session: London KZ + NY KZ. Playbook: **asr-orb-intraday-system** (ASR-варіант).
