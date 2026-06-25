---
title: GBPUSD Top-Down Analysis
date: 2026-06-25
tags: [GBPUSD, TDA, bearish-corrective, forex]
category: Analysis
project: Trading
pair: GBPUSD
strategy: asr-orb-intraday-system
agent: analyst
status: analysis-complete
pinecone_indexed: false
---

# GBPUSD: Top-Down Analysis — 25.06.2026

> Час аналізу: 05:13 UTC / 08:13 Київ (EEST)
> Поточна ціна: **1.31817**
> Важливий контекст: HIGH-IMPACT USD news 12:30 UTC (Core PCE + GDP) — BLACKOUT 12:00–13:00 UTC

---

## Weekly (Тижневий графік)

15W range `1.31402 – 1.36578`, change **-0.42%**, avg vol 1 648 205.
Останні 5W closes: `1.34474 → 1.33296 → 1.33942 → 1.32283 → 1.31815` — серія LH/LL, чіткий bearish тренд від топу 1.36578.

Тиждень -4 сформував локальний пік 1.35091 (LH) → тиждень -1 утворив swing low 1.31630 → поточний тиждень sweep до нового 15W low 1.31402 і відкат. Дистрибуція підтверджена: кожен тижневий close нижчий за попередній (крім W-3: 1.33942 — корекція, але підтримки не дала).

**HTF Bias: Bearish-Corrective.** Основний тренд — вниз. Поточна свічка (незакрита) — відкат від 15W low.

![[img/gbpusd_w.png]]

---

## Daily (Денний графік)

20D range `1.31402 – 1.34854`, change **-1.95%**, avg vol 284 730.
Останні 5D closes: `1.32283 → 1.32481 → 1.32034 → 1.31660 → 1.31817` (сьогодні незакритий).

Понеділок (23.06): open 1.32034, high 1.32091 (LH vs попередній D high), low 1.31402 — bearish sweep до 15W low, close 1.31660.
Вівторок (24.06): open 1.32034, відкат вгору, але обмежений → bearish.
Сьогодні (25.06): open 1.31658, high 1.31852, low 1.31525 — поки inside day з bullish нахилом. Відкат від sweep low.

Key D-рівні:
- D resistance: 1.32091 (вчорашній D high / LH)
- D resistance 2: 1.32521 (high понеділок -3)
- D support: 1.31402 (15W low / PDL)
- D support 2: 1.31525 (сьогоднішній low)

![[img/gbpusd_d.png]]

---

## 4-Hour (4-годинний графік)

H4 30-bar range `1.31402 – 1.32731`, change **-0.49%**, avg vol 41 954.
Останні 5×H4 closes: `1.31705 → 1.31658 → 1.31627 → 1.31822 → 1.31808`

Структура: після sweep до 1.31402 (екстремум) H4 формує mini-accumulation / внутрішній range 1.3162–1.3185. Немає підтвердженого CHoCH вгору — лише tight consolidation після sweep. BOS вниз збережений (нижче попередніх тижневих lows).

H4 OB (bear): зона 1.3185–1.3200 — origin move вниз.
H4 swing low (свіжий): 1.31402
H4 swing high (LH): 1.32731 (понеділок morning)

![[img/gbpusd_h4.png]]

---

## 1-Hour (1-годинний графік)

H1 30-bar range `1.31402 – 1.32089`, change **-0.14%**, avg vol 10 815.
Останні 5H1 closes: `1.31708 → 1.31779 → 1.31823 → 1.31822 → 1.31814`

H1 consolidation вузького діапазону 1.3170–1.3185 після вчорашнього sweep. Ціна "зависла" під H4 OB (1.3185–1.3200). Поки немає CHoCH вгору — відкат, що витрачає час без імпульсу.

**SMT (EURUSD ↔ GBPUSD):** EURUSD @ 1.13666. Обидва інструменти синхронно консолідують після lows — SMT дивергенції немає, USD тиск симетричний для обох пар. Підтверджує загальний USD strenght (bearish для GBP).

![[img/gbpusd_h1.png]]

---

## 15-Minute — ASR Setup Watch

M15 30-bar range `1.31583 – 1.31852`, avg vol 1 617.
Останні 5M15 closes: `1.31839 → 1.31807 → 1.31822 → 1.31817 → 1.31817`

Asia range (орієнтовно з overnight M15):
- Asia High: ~1.31852
- Asia Low: ~1.31583

**ASR (Asia Sweep & Reclaim) — PRIMARY:**

**Сценарій A — SHORT (пріоритетний, відповідає HTF bias):**
London sweep Asia High (1.31852–1.31900) → rejection нижче 1.31852 → M15/M5 BOS вниз → SHORT entry @ 1.31820–1.31850.
SL: 1.31950 (вище sweep high + буфер)
TP1: 1.31583 (Asia Low) — RR 1.3
TP2: 1.31402 (PDL / 15W low) — RR 3.2
TP3: 1.31200 (ext. zone) — RR 5.6

**Сценарій B — LONG (лише якщо HTF дає CHoCH вгору):**
London sweep Asia Low (1.31583) → reclaim → M15 BOS вгору → LONG entry @ 1.31620–1.31640.
SL: 1.31480 (нижче sweep low + буфер)
TP1: 1.31852 (Asia High) — RR 1.4
TP2: 1.32091 (D resistance) — RR 3.2

⚠️ Blackout 12:00–13:00 UTC — Core PCE + GDP. Жодних входів у цьому вікні.

![[img/gbpusd_m15.png]]

---

## 5-Minute — Торговий план (Основний: ASR SHORT)

M5 30-bar range `1.31744 – 1.31852`, avg vol 523.
Ціна зараз: **1.31817** — консолідує під верхньою межею 1.31852.

- **Bias:** Bearish (HTF W/D/H4 узгоджені вниз), corrective (поточний відкат)
- **ASR Setup:** SHORT після sweep Asia High у London KZ (06:00–08:00 UTC)
- **Entry Zone:** `1.31820 – 1.31870` (після rejection від 1.31852–1.31900)
- **Stop Loss:** `1.31950` (вище sweep high) — **13 pts**
- **TP1:** `1.31583` — RR 1.7 (Asia Low)
- **TP2:** `1.31402` — RR 3.2 (15W low / PDL)
- **TP3:** `1.31200` — RR 5.0 (ext. підтримка)
- **Lot Size:** `$100 / (13 pts × $10/pip) ≈ 0.77 lot` (GBPUSD: 1 pt = $10 на 1 lot — перевірити брокера)

Альтернатива: якщо setup не активується до 11:30 UTC — пропустити сесію (blackout з 12:00).

![[img/gbpusd_m5.png]]

---

**Коментар:** GBPUSD у чіткому HTF bearish тренді з серією LH/LL на W та D. Sweep до 15W low 1.31402 (24.06) — потенційна liquidity grab перед продовженням вниз або short-term корекцією. ASR SHORT є primary setup для London KZ (06:00–08:00 UTC): якщо London відкриє вгору і sweep Asia High → очікувати rejection і short. BLACKOUT 12:00–13:00 UTC (Core PCE + GDP) — жодних входів. Після 13:00 UTC можлива підвищена волатильність — торгувати тільки якщо є чіткий setup. SMT: EURUSD синхронний, дивергенції немає — підтверджує USD тиск.

**Setup Score: 7/10**
- HTF alignment (W/D/H4): bullish для SHORT ✓
- ASR умова: залежить від London sweep ✓ (не підтверджено поки)
- Liquidity target (1.31402 PDL): ✓
- RR TP2: 3.2 ✓
- SMT: нейтральний (не дивергенція) ~
- News risk: BLOCK в 12:00-13:00 UTC ~
- Session: London KZ (06:00-08:00 UTC) — ще попереду ✓
