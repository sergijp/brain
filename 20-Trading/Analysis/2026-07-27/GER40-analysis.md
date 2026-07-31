---
title: GER40 Top-Down Analysis
date: 2026-07-27
tags: [GER40, TDA, bullish-corrective, indices]
category: Analysis
project: Trading
pair: GER40
agent: analyst
status: analysis-complete
pinecone_indexed: false
---

# GER40: Top-Down Analysis — 27.07.2026

> Аналіз о 09:11 Київ (06:11 UTC). Xetra cash open — 10:00 Київ (07:00 UTC). Це **pre-session**: ASR та ORB ще не активні. German ifo Business Climate — 11:00 Київ (08:00 UTC), потенційний сплеск усередині вікна.

## 🏛 Weekly (Тижневий графік)
15W range `23 613 – 25 923`, W **+3.06%**. Останні 5W closes: `25 806 → 25 097 → 24 829 → 25 077 → 25 393`. Пік ~`25 923` (ATH-зона) 3 тижні тому, далі 3-тижнева корекція до `24 610`, зараз сильне відновлення. **HTF Bullish** — ціна ~530 pts під ATH, тренд не зламаний, корекція викуплена.

![[img/ger40_w.png]]

## 📅 Daily (Денний графік)
20D range `24 610 – 25 923`, **+2.68%**. Останні 5D closes: `25 066 → 25 153 → 24 794 → 25 077 → 25 391`. Сформований higher low `24 692`, п'ятниця — сильна бичача свічка (+314 pts, close 25 391 біля свінг-хаю). Daily momentum повертається вгору. **Bullish**.

![[img/ger40_d.png]]

## ⏱ 4-Hour (4-годинний графік)
H4 range (30 барів) `24 664 – 25 395`, **+1.94%**. Останні 5×4H closes: `25 107 → 25 077 → 25 206 → 25 320 → 25 387` — чіткий **BOS up**, серія HH/HL. Ціна на вершині діапазону, увійшла в преміум/supply-band під "Weak High" ~`26 000`. Найближча ліквідність зверху `25 500`, далі ATH `25 923`. Orange midline / OB ~`25 016`. **Bullish, extended**.

![[img/ger40_h4.png]]

## 🕐 1-Hour (1-годинний графік)
H1 range `24 696 – 25 395`, **+2.47%**. Останні 5H closes: `25 257 → 25 263 → 25 320 → 25 355 → 25 390` — стійкий підйом впритул до `25 395` (H4/тижневий swing high = buy-side liquidity). LuxAlgo SMC: demand-зони `25 148` (EMA/OB), `25 024`, deep demand `24 669`. Ціна робить новий локальний хай прямо зараз.
**SMT:** з US500/US-індексами — потрібна незалежна перевірка (quote-tool повернув символ чарту). Якісно контекст risk-on, розбіжності не зафіксовано. SMT — pending.

![[img/ger40_h1.png]]

## 🎯 15-Minute (15-хвилинний графік)
M15: range `25 178 – 25 395`. Остання свічка пробила вгору до `25 395.5` (close 25 393). Ціна тисне у "Weak High" ~`25 380–25 400`. Blue OB ~`25 000–25 200` нижче, OTE-зона (yellow) `24 800–25 000`, "Strong Low" ~`24 700`.

Сценарії (активні тільки ПІСЛЯ Xetra open 10:00 Київ):
1. **Консервативно (LONG):** відкат у `25 240–25 270` (overnight support / H1 OB) + M15 reclaim → лонг до `25 500`.
2. **ASR (пріоритет бичачий):** Frankfurt-open sweep overnight-low + reclaim → лонг у бік HTF.
3. **Агресивно (SHORT, контртренд):** sweep `25 395–25 420` (weak high) + M15 rejection/reclaim нижче `25 360` → короткий фейд до `25 240`. Тільки failed breakout.

![[img/ger40_m15.png]]

## ⚡ 5-Minute — Торговий план (бичача континуація, preliminary)

- **Bias:** Bullish (long, momentum-corrective) 📈
- **Entry Zone:** `25 240 – 25 270` (відкат у H1 OB / overnight support) АБО ORB-30 break-retest вище діапазону 10:00–10:30
- **Stop Loss:** `25 150` (нижче H1 EMA/OB та overnight-структури) — **~110 pts**
- **TP1:** `25 395` (overnight high / weak high) — RR ~1.3
- **TP2:** `25 500` (H4 weak-high liquidity) — RR ~2.3
- **TP3:** `25 700` (у бік ATH 25 923) — RR ~4.1
- **Lot Size:** `$100 / (110 × $1) ≈ 0.90 контракту` (GER40: 1 pt = $1/контракт — **перевірити брокер**)

![[img/ger40_m5.png]]

---

## 📊 Статус ASR + ORB для GER40 (основна система)

| Гілка | Статус зараз (09:11 Київ) | Умова активації |
|-------|--------------------------|-----------------|
| **ASR** (Asia Sweep & Reclaim) | ⏳ PENDING | Вікно з **10:05 Київ**. Watch overnight range low ~`25 240` / high `25 395`. Sweep + reclaim у бік HTF (пріоритет — бичача сторона). |
| **ORB** (Xetra ORB-30) | ⏳ PENDING | Діапазон формується **10:00–10:30 Київ**, пробій після 10:30. ifo о 11:00 може стати каталізатором. Signal-mode. |

**Валідний POI/тригер зараз:** НЕМАЄ. Сесія не відкрита, ціна extended на `25 395` (weak high) без підтвердженого тригера. Не переслідувати хай. Чекати Xetra open.

## Коментар
- **HTF повністю узгоджений bullish** (W/D/H4), корекція викуплена, ціна під ATH — контекст на континуацію вгору.
- **Ризик news:** German ifo Business Climate 11:00 Київ (08:00 UTC) — усередині ASR/ORB вікна. Фід low, фактично може дати medium-сплеск. **Блекаут ±30 хв** (10:30–11:30 Київ) для нових входів.
- **Сесія:** Frankfurt/London open 07:00–10:00 UTC — прайм-вікно GER40, стартує о 10:00 Київ. Зараз pre-session.
- **Правило входу:** не входити раніше 10:05 Київ (ASR) / 10:30 (ORB). ⚠️ Setup наразі "wait for trigger", не ready-entry.
- **Малюнки/зони юзера на чарті збережено** (draw_clear пропущено свідомо).
