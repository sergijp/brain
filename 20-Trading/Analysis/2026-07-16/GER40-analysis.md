---
title: GER40 Top-Down Analysis
date: 2026-07-16
tags: [GER40, TDA, range, indices]
category: Analysis
project: Trading
pair: GER40
agent: analyst
status: analysis-complete
pinecone_indexed: false
---

# GER40: Top-Down Analysis — 16.07.2026

> Час аналізу: 09:07 Kyiv / 06:07 UTC. Xetra open 10:00 Kyiv (07:00 UTC) — до відкриття ~53 хв.
> Дані TradingView свіжі (last bar 06:05 UTC). Ціна: **25 001**.

## 🏛 Weekly (Тижневий графік)
15W **+8.09%**, range `22 835 – 25 923`. Останні 5W: `24 997 → 24 642 → 25 806 → 25 097 → 25 006` — сильний аптренд зробив ATH **25 923** два тижні тому, потім відкат і бічняк ~25 000. Довгі верхні тіні на топі + weak high 25 923 = **HTF Bullish, але з ознаками exhaustion/distribution** біля ATH. Тренд не зламаний (над Strong Low ~21 700).

![[img/ger40_w.png]]

## 📅 Daily (Денний графік)
20D **-0.30%**, range `24 549 – 25 923`. Останні 5D: `25 097 → 24 979 → 25 043 → 24 998 → 25 009` — щільна консолідація/акумуляція на OTE-зоні після BOS вгору. Weak High **25 923** = основна BSL зверху. Overhead supply рівень `25 827`, demand знизу `24 050`. Strong Low D ~24 000. **Bias D: neutral-to-bullish, balance.**

![[img/ger40_d.png]]

## ⏱ 4-Hour (4-годинний графік)
H4 range `24 770 – 25 223`, **+0.28%**. CHoCH відпрацьовано на `24 803` (низ), ціна відновилась. Зараз бічняк `24 900 – 25 070`, weak high ~25 069. Supply зверху `25 400 – 25 500` (червона зона), demand/Strong Low ~24 000. Дрібна demand-OTE `24 850 – 24 950`. **Структура H4: range/balance**, momentum нейтральний (EMA плоска).

![[img/ger40_h4.png]]

## 🕐 1-Hour (1-годинний графік)
H1 **-0.33%**, range `24 832 – 25 140`. Класичний баланс: Strong High ~25 220 (BSL), demand-зона `24 770 – 24 870` (синя, SSL внизу). Останній low **24 919** = найближча SSL. CHoCH зліва ~25 100. **SMT з US500/EURUSD:** US500 в аналогічному risk-on балансі, EURUSD стабільний (немає HIGH EUR-новин) — розбіжності немає, підтверджує range, не reversal. **H1: чистий діапазон 24 920 – 25 070.**

![[img/ger40_h1.png]]

## 🎯 15-Minute (15-хвилинний графік)
M15 OTE-зона `24 950 – 25 000` (yellow). Weak High local ~**25 055**, Strong Low ~**24 830**. Ціна коилиться `24 999 – 25 055` перед Xetra open — компресія азійського діапазону. Межі Asia range: **high ≈ 25 069 / low ≈ 24 920**.

Сценарії (реактивні, після 10:00 Kyiv):
1. **ASR Long:** sweep Asia low `24 920` → reclaim + M15 CHoCH → long до `25 069 → 25 220`.
2. **ASR Short:** sweep Asia high `25 069` → rejection + M15 close нижче → short до `24 920 → 24 830`.

![[img/ger40_m15.png]]

## ⚡ 5-Minute (5-хвилинний графік) — Реактивний план

Pre-open. Виражений напрямний edge відсутній — **чекати тригер на відкритті Xetra**.

- **Bias:** Neutral / Range (HTF bull-exhausted, D/H4/H1 balance) ⚖️
- **ASR Long (пріоритет за upside-sweep):**
  - Entry: `24 960` (reclaim після sweep 24 920)
  - SL: `24 890` (нижче sweep low) — **70 pts**
  - TP1 `25 069` (RR 1.6) · TP2 `25 220` (RR 3.7) · TP3 `25 400` (RR 6.3)
- **ASR Short (за upside-sweep 25 069 + reject):**
  - Entry: `25 020` · SL: `25 090` — **70 pts**
  - TP1 `24 920` (RR 1.4) · TP2 `24 830` (RR 2.7) · TP3 `24 770` (RR 3.6)
- **Lot Size:** `$100 / (70 pts × $1) ≈ 1.43 contract` (GER40: 1 pt = $1/contract — перевірити брокер)

![[img/ger40_m5.png]]

---
**ASR-сетап (ядро системи):** ARMED / PENDING. Вікно ASR 10:05–13:00 Kyiv, flat 17:45. Asia range стиснутий: `24 920 – 25 069`. Тригер — провалений пробій однієї з меж на London/Xetra open + reclaim на M15. Сигналу ще немає (до відкриття).

**ORB-сетап (Xetra ORB-30, сателіт):** PENDING. Opening range формується **10:00–10:30 Kyiv**. Торгувати пробій діапазону тієї 30-хв свічки після 10:30. Рівні визначаться на відкритті. Нагадування: ORB live не раніше вересня 2026 — сьогодні signal-mode.

**News:** HIGH-impact EUR подій немає, календар чистий для GER40. **USD MED-кластер 12:30 UTC (15:30 Kyiv)** — потрапляє в кінець ASR-вікна; уникати нових входів ±30 хв навколо. **Сесія:** London KZ активна, найкращий driver для GER40 — London open 07:00–10:00 UTC. Інтрадей: закрити позицію до вечора (flat 17:45).

**Repeated-focus:** GER40 у балансі кілька днів — не форсувати вхід без чистого sweep+reclaim.
