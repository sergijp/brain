---
title: GER40 Top-Down Analysis
date: 2026-07-09
tags: [GER40, TDA, bullish-corrective, Analysis]
category: Analysis
project: Trading
pair: GER40
strategy: asr-orb-intraday-system
agent: analyst
status: analysis-complete
pinecone_indexed: false
---

# GER40 (DAX): Top-Down Analysis — 09.07.2026

> Час аналізу: 06:05 UTC / 09:05 Kyiv. Дані свіжі (last bar 06:05 UTC). Поточна ціна **25084**.
> News: CLEAR весь день (German Trade Balance 06:00 UTC — low impact, вже вийшов). Xetra cash open 10:00 Kyiv (07:00 UTC).

## 🏛 Weekly (Тижневий графік)
15W range `21934.5–25923`, **+13.16%**. Останні 5W closes: `24671 → 24997 → 24642 → 25806 → 25080`. Чіткий bull-тренд (серія HH/HL), ціна щойно поставила ATH **25923**. Поточний тиждень — **корективний**: відкрився 25806, торкнувся ATH, впав до 24825, зараз 25080. **HTF Bullish** (ATH-структура, коректива всередині тренду).

![[img/ger40_w.png]]

## 📅 Daily (Денний графік)
20D range `24414–25923`, **+1.87%**. Останні 5D: `25806 → 25827(ATH) → 25464 → 24974 → 25076`. Класичний **2-денний корективний pullback** від ATH 25923: топінг-день → великий bearish reversal день (25841→25408) → продовження вниз (тест 24825) → сьогодні малий відскок (H25108). Ціна у верхній частині W-range. **Daily Bullish, режим коректива в discount.**

![[img/ger40_d.png]]

## ⏱ 4-Hour (4-годинний графік)
H4 range `24825.5–25923`, -0.31%. Останні 5×4H: `25003 → 24974 → 25033 → 25057 → 25075` — після лоу 24825 формується **база з higher lows** (24846→24956→24980→25021). Ціна сидить у **H4 OTE golden zone `25075–25256`** (62–79% ретрейс останнього імпульсу) — типова discount buy-зона в аптренді. BOS вгору ще НЕ підтверджено — тригер: пробій 25108 → 25334. Peak High 25923, Strong Low (LuxAlgo) 24000.

![[img/ger40_h4.png]]

## 🕐 1-Hour (1-годинний графік)
H1 24h range `24825.5–25334`, -0.92%. За ніч: LH **25334** → провал до **24825** (ключовий SSL low) → відновлення до 25108. Видно **CHoCH** та нічну акумуляцію в Tokyo-сесії `24920–25108`. Праворуч — Frankfurt open band (~10:00 Kyiv): ціна коілиться прямо перед відкриттям Xetra. H1 OTE-supply зверху 25400–25600.
**SMT:** GER40 узгоджений з US-індексами по bull-контексту; дивергенцій на HTF немає.

![[img/ger40_h1.png]]

## 🎯 15-Minute (15-хвилинний графік)
M15 range `24980–25108.5` (~128 пт, щільна нічна консолідація = **Азійський діапазон**). Відскок від discount `24972` + mini-**BOS вгору** до 25105. Weak Low 24815. ICT HTF 30m-проекція праворуч.

Сценарії:
1. **Консервативно (LONG, HTF-aligned):** Frankfurt/London sweep нижче Asian low `24980` (або глибше SSL `24825`) → M15 reclaim + CHoCH → LONG у напрямку 25334/25408. **Основний.**
2. **Агресивно (SHORT, counter-HTF):** sweep вище `25108` → fail на supply `25334/25408` → reclaim вниз до 24825. Тільки при явному rejection, нижча ймовірність.

![[img/ger40_m15.png]]

## ⚡ 5-Minute — Торговий план (preliminary, тригер ще не сформувався)

- **Bias:** Bullish (long, corrective-in-discount) 📈
- **Entry Zone:** `24825 – 25010` (ASR: sweep Asian low → reclaim; кращий — на sweep 24980/24825 з M15 CHoCH)
- **Stop Loss:** `24790` (нижче Weak Low / yesterday D-low 24825) — ~70–210 пт залежно від глибини sweep
- **TP1:** `25108` (Asian high) — RR ~1.4
- **TP2:** `25334` (H1 LH liquidity) — RR ~3–4.6
- **TP3:** `25408` (D broken support → resistance) — RR ~4–5.7
- **Lot Size:** `$100 / (SL_пт × $1)` → при SL 70 пт ≈ **1.4 контракти**, при SL 210 пт ≈ **0.48 контракти** (GER40: 1 пт = $1/контракт — перевірити брокер)

![[img/ger40_m5.png]]

---

## 🎯 ASR + ORB (основна система — GER40 єдина з обома компонентами)

**ASR (Asia Sweep & Reclaim)** — вікно з 10:05 Kyiv (07:05 UTC):
- Азійський діапазон: high `25108`, low `24980` (глибший SSL `24825`).
- Основний план — **bullish**: провалений пробій вниз Asian low → reclaim → M15 CHoCH → LONG. Узгоджено з HTF bull + H4 OTE discount + чистий SSL 24825 під ринком.

**ORB (Xetra ORB-30)** — тільки GER40:
- Діапазон формується 10:00–10:30 Kyiv (07:00–07:30 UTC), пробій торгується після 10:30.
- Дочекатись фактичного 30-хв діапазону. За bull-контекстом фаворит — пробій ORB-high вгору. Live заблоковано до вересня 2026 (signal-mode).

## Ключові рівні

| Тип | Рівень | Опис |
|-----|--------|------|
| Resistance | 25108 | Asian high (immediate) |
| Resistance | 25334 | H1 LH liquidity (BSL) |
| Resistance | 25408 / 25531 | D broken support → supply |
| Resistance | 25923 | ATH / Weak High (BSL) |
| Support | 24980 | Asian low |
| Support | **24825** | yesterday D-low / H4 swing / Weak Low (**key SSL**) |
| Support | 24520 | H1 Strong Low (LuxAlgo) |
| Support | 24414 | 20D low |
| Liquidity ↑ | 25334, 25923 | buy-side |
| Liquidity ↓ | 24825 | sell-side (resting SSL) |

## Setup Score: 7/10
HTF bull сильно узгоджений, ціна в H4 OTE discount, щільний Asian range готовий до sweep, чистий SSL 24825, news CLEAR. Мінус: тригер (sweep + reclaim) ще не сформувався (pre-Frankfurt), ціна mid-range — потрібне підтвердження після 10:00 Kyiv.
