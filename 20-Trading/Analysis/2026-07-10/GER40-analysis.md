---
title: GER40 Top-Down Analysis
date: 2026-07-10
tags: [GER40, TDA, bullish-continuation, Analysis]
category: Analysis
project: Trading
pair: GER40
strategy: asr-orb-intraday-system
agent: analyst
status: analysis-complete
pinecone_indexed: false
---

# GER40 (DAX): Top-Down Analysis — 10.07.2026

> Час аналізу: 05:54 UTC / 08:54 Kyiv. Дані свіжі (last bar 05:5x UTC). Поточна ціна **25075** (FOREXCOM:GER40).
> News: **CLEAR** — жодних DE/EZ high-impact подій сьогодні. GER40 CLEAR для ASR/ORB.
> До відкриття Xetra cash (10:00 Kyiv / 07:00 UTC) ще ~1 год — тригер ще не сформувався.
> Скріншоти: генеруються окремим manual-флоу `tda-screenshot` (потребує "готово" від юзера при перемиканні TF).

## 🏛 Weekly (Тижневий графік)
15W range `21934.5–25923`, **+13.15%**. Поточний тижневий бар: open 25806.5, high 25923 (ATH), low 24825.5, close 25078.5 — **корективний тиждень усередині bull-тренду**. Серія HH/HL, ATH-структура. **HTF Bullish** (без змін з учора).

## 📅 Daily (Денний графік)
20D range `24549–25923`. Останні 5D closes: `25827(ATH) → 25464 → 24974 → 25111 → 25078`.
- **Вчора (09.07):** open 24974, low **24862**, high 25144, close **25111** — бичачий день, закриття біля хаїв. **Очікуваний учора глибокий sweep 24980/24825 НЕ відбувся** — замість цього ринок поставив **higher low 24862** і виріс до 25111. Bull-bias підтвердився, але discount-вхід ринок не дав.
- **Сьогодні (10.07):** open 25111, high 25146.5, low 25072, поточна 25078 — малий inside-day, легка коректива. **Daily Bullish, база higher-lows.**

## ⏱ 4-Hour (4-годинний графік)
H4 range `24825.5–25923`. Після лоу 24825 будується **база higher lows** (24825 → 24862 → coiling 25072–25146). Ціна вийшла з глибокого H4 OTE discount вгору — тепер сидить під локальним BSL 25146.5. BOS вгору H4 ще не підтверджено — тригер: пробій + утримання 25146 → 25202/25334. Peak High 25923, Strong Low (LuxAlgo) нижче ~24520.

## 🕐 1-Hour (1-годинний графік)
H1 24h range `24862–25146.5` (тісний). За ніч компресія `25072–25146`. Higher low 24862 (вище за учорашній SSL 24825 — ринок не дотягнувся до нижньої ліквідності = ознака сили). LuxAlgo: серія мікро-BOS/CHoCH біля хаїв (choppy range під 25146).
**SMT:** GER40 у bull-контексті узгоджений з US-індексами; HTF-дивергенцій немає.

## 🎯 15-Minute — Азійський діапазон
M15 останні 10 год: **range `25072–25146.5` (~74 пт)** — **дуже щільна нічна консолідація**, ще тісніша за вчорашні 128 пт. Це **Азійський діапазон на сьогодні**. Ціна зараз (25075) — **прямо біля нижньої межі 25072** → пробій вниз може статися на Frankfurt open.

Сценарії:
1. **Консервативно (LONG, HTF-aligned):** Frankfurt/London sweep нижче Asian low `25072` (глибший — до higher low `24862` або SSL `24825`) → M15 reclaim + CHoCH → LONG на 25146/25334. **Основний.**
2. **Агресивно (SHORT, counter-HTF):** sweep вище `25146.5` → fail на supply `25202/25334` → reclaim вниз. Тільки при явному rejection, нижча ймовірність.

## ⚡ 5-Minute — Торговий план (preliminary, тригер ще не сформувався)

- **Bias:** Bullish (corrective-continuation, база higher-low) 📈
- **Entry Zone:** `24980 – 25072` (ASR: sweep Asian low → reclaim; кращий — з M15 CHoCH; глибший sweep 24862 = кращий RR)
- **Stop Loss:** `24845` (нижче higher low 24862 / над key SSL 24825) — ~135–225 пт залежно від глибини sweep
- **TP1:** `25146` (Asian high / ORB ref) — RR ~0.9–1.4
- **TP2:** `25334` (H1 LH liquidity / BSL) — RR ~2.5–3.5
- **TP3:** `25408` (D broken support → supply) — RR ~3–4.5
- **Lot Size:** `$100 / (SL_пт × $1)` → при SL ~90 пт ≈ **1.1 контракт**, при SL 200 пт ≈ **0.5 контракти** (GER40: 1 пт = $1/контракт — перевірити брокер)

---

## 🎯 ASR + ORB (основна система — GER40 єдина з обома компонентами)

**ASR (Asia Sweep & Reclaim)** — вікно з 10:05 Kyiv (07:05 UTC):
- Азійський діапазон: high **25146.5**, low **25072** (глибші SSL: 24862, 24825).
- Основний план — **bullish**: провалений пробій Asian low → reclaim → M15 CHoCH → LONG. Узгоджено з HTF bull + база higher-lows + чиста SSL нижче.
- Якість сетапу висока: діапазон дуже щільний (74 пт), ціна вже біля нижньої межі.

**ORB (Xetra ORB-30)** — тільки GER40:
- Діапазон 10:00–10:30 Kyiv (07:00–07:30 UTC), пробій торгується після 10:30.
- Дочекатись фактичного 30-хв діапазону. За bull-контекстом фаворит — пробій ORB-high вгору. Live заблоковано до вересня 2026 (signal-mode).

## Ключові рівні

| Тип | Рівень | Опис |
|-----|--------|------|
| Resistance | 25146.5 | Asian high / вчорашній high / ORB ref (immediate BSL) |
| Resistance | 25202.5 | LuxAlgo supply |
| Resistance | 25334 | H1 LH liquidity (BSL) |
| Resistance | 25408 / 25464 / 25531 | D broken support → supply |
| Resistance | 25923 | ATH / Weak High (BSL) |
| Support | 25072 | Asian low today (immediate SSL) |
| Support | 24980 | prior Asian low / round zone |
| Support | 24917 | recent CHoCH / H1 demand |
| Support | **24862** | overnight/вчорашній H1 higher low (key) |
| Support | **24825** | вчорашній D-low / resting SSL |
| Support | 24520 | H1/D Strong Low (LuxAlgo) |
| Liquidity ↑ | 25146.5, 25334, 25923 | buy-side |
| Liquidity ↓ | 25072, 24862, 24825 | sell-side (resting SSL) |

## Що змінилось з учора (09.07 → 10.07)

| Аспект | 09.07 | 10.07 | Висновок |
|--------|-------|-------|----------|
| HTF bias | Bullish-corrective | Bullish-continuation | Без змін, тренд міцніший |
| Discount sweep 24825 | Очікувався | **НЕ відбувся** (low 24862) | Ринок сильніший, ніж думали |
| Daily close | 25076 | вч. закрито 25111 (біля хаїв) | Бичаче |
| Asian range | 24980–25108 (128 пт) | **25072–25146.5 (74 пт)** | Тісніша компресія = кращий ASR |
| Структура | база формується | higher low 24862 підтверджено | Continuation, не глибша коректива |
| Позиція ціни | mid-range discount | верхня частина, під BSL 25146 | Менше discount-edge, ближче до пробою |

## Setup Score: 7/10
HTF bull міцно узгоджений, higher-low база (24862) підтверджена, Азійський діапазон дуже щільний (74 пт — якісний ASR-сетап), news CLEAR, ціна вже біля нижньої межі діапазону. Мінус: ринок вийшов з глибокого H4 OTE discount вгору (менше discount-edge, ніж учора), тригер (sweep + reclaim) ще не сформувався (pre-Frankfurt) — потрібне підтвердження після 10:00 Kyiv.
