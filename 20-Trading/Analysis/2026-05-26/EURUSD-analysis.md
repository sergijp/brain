---
title: EURUSD Top-Down Analysis
date: 2026-05-26
tags: [EURUSD, TDA, bullish-corrective, forex]
category: Analysis
project: Trading
status: analysis-complete
pair: EURUSD
agent: analyst
strategy: smc-price-action-combo
pinecone_indexed: false
---

# EURUSD: Top-Down Analysis — 26.05.2026

> **Поточна ціна:** 1.16360 @ 06:48 UTC (M5 close)
> **Сесія:** London KZ активна (06:00-08:00 UTC влітку) — оптимально для EURUSD
> **Київ:** 09:48 EEST — entry дозволено (≥ 09:00)

## 🏛 Weekly (Тижневий графік)

15W range `1.14110 – 1.18728`. Останні 5W closes: `1.17212 → 1.17852 → 1.16252 → 1.16023 → 1.16356` — **distribution з 1.17967 (10 May high), -1.6% і -0.4% подряд два тижні, поточний W consolidation біля 1.163**. HTF структура: bearish corrective leg у межах ширшого March-May ranging (не пробите 1.14110 березневе дно). **HTF Bearish-Corrective** — корекція в межах коридору, не реверс тренду.

## 📅 Daily (Денний графік)

20D range `1.15763 – 1.17967`, change `-0.44%`. Останні 5D closes: `1.16255 → 1.16175 → 1.16023 → 1.16433 → 1.16356`.
- 21 May low **1.15883** (sub-1.16 sweep) → reversal D-bar
- 24 May D bullish reclaim +0.36% close 1.16433
- 25 May indecisive doji 1.16273-1.16443
- **D-Bias:** accumulation з sweep 1.158 → формується HL на D, готується bounce до 1.17 OB
- PDH `1.16443`, PDL `1.16273`

## ⏱ 4-Hour (4-годинний графік)

H4 range за останні 30 барів `1.15763 – 1.17967`, `-0.87%`. Останні 5×4H closes: `1.16412 → 1.16433 → 1.16387 → 1.16298 → 1.16356`.
- **H4 BOS UP** 24 May з 1.15883 → 1.16528 (significant low → significant high)
- Pullback 25 May, mini-CHoCH down на 1.16273
- **Tight accumulation 1.16273-1.16528** — стиснення волі перед наступним leg
- **H4 Key levels:**
  - Resistance: `1.16528` (H4 swing high, D high)
  - Support: `1.16273` (Asia low, M15 sweep low)
  - Liquidity above: `1.16618` (W high 17 May)
  - Liquidity below: `1.15883` (D low 21 May)

## 🕐 1-Hour (1-годинний графік)

H1 `+0.33%`. Останні 5H closes: `1.16340 → 1.16360 → 1.16298 → 1.16280 → 1.16360`.
- Asia (04:00-05:00 UTC) sweep H1 low **1.16273-1.16294** → reversal +9 pips
- H1 BOS UP @ 06:00 (1.16364 > попередній H1 high 1.16352)
- **H1 OB (демандна зона):** `1.16280 – 1.16310` (тіло H1 з sweep)
- Класичний Asia liquidity grab з London reversal — точка входу за SMC+PA Combo PRIMARY PATTERN

**SMT (vs GBPUSD H1):** GBPUSD +0.65% за день, EURUSD +0.33% — **обидва ↑ синхронно, no divergence**. USD weakness підтверджено через обидві USD-major пари → bullish confluence.

## 🎯 15-Minute (15-хвилинний графік)

Останні 5×M15 closes: `1.16280 → 1.16300 → 1.16329 → 1.16361 → 1.16359`.
- 05:45 M15 LL `1.16273` (final sweep)
- 06:00-06:30 BOS UP до `1.16364`
- 06:45 stall на 1.16360 — готується ретест

**Сценарії:**
1. **Консервативно (LONG) ⭐ PRIMARY:** ретест H1 OB `1.16290-1.16310` + M15 CHoCH/BOS confirmation → entry на reclaim 1.16320. Ціль: 1.16528 → 1.16618.
2. **Агресивно (LONG):** ринковий вхід зараз 1.16360 (без ретесту), SL на 1.16240 — гірший RR, але швидше тригер на London open.
3. **Invalidation:** close H4 < 1.16240 → flip до bearish, ціль 1.15883 (D liquidity).

## ⚡ 5-Minute (5-хвилинний графік) — Торговий план

**Bias:** Bullish-Corrective (LONG, intraday continuation на London KZ) 📈

> SMC+PA Combo PRIMARY PATTERN: HTF bias mixed, але D+H4 BOS up після Asia sweep + H1 OB confluence + London KZ active + SMT clean.

### Trade Plan (DRAFT — for strategy-picker + dixie review)

| Поле | Значення |
|------|----------|
| **Entry Zone** | `1.16290 – 1.16320` (H1 OB + M15 retest) |
| **Stop Loss** | `1.16240` (під Asia sweep low 1.16273, буфер 3 pip) |
| **SL distance** | **70 pts (7 pips)** |
| **TP1** | `1.16438` — RR ≈ **1.83** (PDH 25 May / H1 swing high) |
| **TP2** | `1.16528` — RR ≈ **3.11** (D high 24 May / H4 swing high) |
| **TP3** | `1.16618` — RR ≈ **4.40** (W high 17 May / liquidity above) |

### Position sizing

- Deposit: `$10 000`
- Risk: `1%` = `$100`
- Pip value EURUSD (OANDA): `1 pt = $1` на 1 lot
- **Lot:** `$100 / (70 pts × $1) = 1.43 lot` → округлити до **1.40 lot** (ризик $98)

⚠️ **Перевірити брокер** — pip value може відрізнятись на іншому брокері/account currency.

---

## Коментар

- **Сесійне вікно:** ✅ London KZ active (06:00-08:00 UTC влітку), час Київ 09:48 — підходить.
- **News risks:** ⚠️ Перевірити ForexFactory на сьогодні (вівторок) — потенційно German Consumer Confidence, US Conference Board CCI ~14:00 UTC. Не входити за 30 хв до red-folder подій.
- **Correlation:** GBPUSD синхронно ↑ → можна торгувати обидві як USD-shorts, але це 2 позиції в одній групі USD-major (ліміт за risk-rules).
- **Intraday only:** позиція має закритись до вечора (інтрадей правило). TP3 1.16618 = +250 pips від entry — досяжно при London + NY rally сьогодні; інакше частковий close на TP1/TP2 + перенесення SL в BE.
- **Setup score: 7/10** — confluence добрий (HTF bias-flip на D + H4 BOS + H1 sweep + SMT clean + KZ), мінус: HTF bias W bearish-corrective робить план "проти Weekly", тому потрібен tight management.

---

## 🎯 Summary для strategy-picker / dixie

- **Bias:** Bullish-Corrective (intraday LONG)
- **Regime:** **Trend (continuation) post sweep** → playbook `smc-price-action-combo` (PRIMARY PATTERN)
- **Entry:** 1.16290-1.16320 (limit) або market на BOS confirmation
- **SL:** 1.16240
- **TP1/2/3:** 1.16438 / 1.16528 / 1.16618 (RR 1.83 / 3.11 / 4.40)
- **Lot:** 1.40
- **Risk:** $98 (0.98% deposit)
- **Score:** 7/10
- **Watch trigger:** M15 close > 1.16364 з ретестом 1.16310 → market enter
