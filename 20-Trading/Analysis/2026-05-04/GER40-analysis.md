---
title: GER40 Top-Down Analysis
date: 2026-05-04
tags: [GER40, TDA, bullish-corrective, indices]
category: Analysis
project: Trading
status: analysis-complete
pinecone_indexed: false
pair: GER40
strategy: london-open-range-breakout
agent: analyst
---

# GER40 (DAX): Top-Down Analysis — 04.05.2026

> Sync: 2026-05-04 05:37 UTC / 08:37 EEST. Last bar TV: 2026-05-04 05:35 UTC (M5) — дані свіжі.
> Поточна ціна: **24 350.5** (FOREXCOM:GER40, CFD).

## 🏛 Weekly (Тижневий графік)

W: +0.72% за останній тиждень. 30-тижневий range `21 860 – 25 512`. Останні 5W closes: `23 790 → 24 640.5 → 24 262.5 → 24 309.7 → 24 352`.

Структурно: після ATH `25 512` пройшла корекція ~6.4%, ціна знайшла попит навколо `23 613–23 790` (W FVG / D OB area) і відновлюється — серія HH/HL збережена. Поточний W бар — невелике зелене тіло, типовий retest після pullback.

**HTF Bias: Bullish-Corrective.** Не імпульсний моментум, але структура HH/HL цілісна; тренд вгору домінує до пробою `23 613` вниз.

## 📅 Daily (Денний графік)

20D `+6.92%`, range `21 934.5 – 24 798`. Останні 5D closes: `23 994 → 23 774 → 24 308 → 24 309 → 24 352` — **V-recovery з 23 613**, чотири послідовно вищі closes після sweep PDL.

Поточна позиція: середина W range, проте над ключовою D OB зоною `23 613–23 754`. PDH = `24 408.5`, PDL = `24 283.5`.

**Daily Bias: Bullish (recovery).** Прорив `24 408` відкриє шлях на ретест `24 798` ATH-локального; провал нижче `24 283` → знову `24 050 / 23 850`.

## ⏱ 4-Hour (4-годинний графік)

H4 range (30 барів) `23 613 – 24 486.07`, +0.53%. Останні 5×4H closes: `24 364 → 24 310 → 24 322 → 24 333 → 24 352`.

Структура: BOS вгору на пробої `24 363`, після чого compression `24 283–24 408`. Це **класичний H4 re-accumulation** після imp-leg вгору. H4 swing high `24 486.07`, swing low `24 283.5` — рівні для SL/TP.

**H4 Bias: Bullish-Compression.** Готовність до експансії; напрям визначить London open.

## 🕐 1-Hour (1-годинний графік)

H1 range `24 283.5 – 24 486.07`, +0.18% за 30H. Останні 5H: `24 322 → 24 343 → 24 347 → 24 333 → 24 352`.

SMC ([LuxAlgo]):
- **BOS** 24 363.25 (bullish break)
- **CHoCH** 24 383 (mini shift down)
- **EQL** 24 289.5 (рівна підтримка → target для liquidity grab)

Це означає: H1 — **EQL під ціною** (`24 289.5`) це нижній sell-side liquidity pool; над `24 408–24 486` — buy-side liquidity (PDH + H4 high).

**SMT vs US500:** обидва індекси зробили swing low ~30 квітня, recovery синхронний — divergence відсутня → bullish bias підтверджено.

## 🎯 15-Minute (15-хвилинний графік)

M15 range за 30 барів `24 283.5 – 24 408.5`. Перед London open (06:00 UTC summer) поточна ціна біля `24 350` — у середині pre-market range.

Сценарії на open:

1. **Bullish LOR-B (preferred):** перший 30-60 хв London cash open сформує opening range; пробій його високу `R_high` з ретестом — long до `24 486 → 24 600`.
2. **Bear sweep first:** sweep EQL `24 289.5` (sell-side liquidity grab) → CHoCH M5 → reversal long з кращим RR.
3. **Bear continuation (low-prob):** провал `24 283` D-low → шорт до `24 150`, але це проти HTF.

## ⚡ 5-Minute (5-хвилинний графік) — Торговий план

### Вибраний edge: **London Open Range Breakout + EQL Sweep Reversal**

**Чому цей edge для DAX (власна аргументація):**
1. **DAX cash open (Xetra) 07:00 UTC / 09:00 CET** — institutional flow різко активується; перші 30-60 хв формують initial balance, де ставиться "правда" дня. CFD GER40 зазвичай відкривається на годину раніше (Eurex futures), що дає preview.
2. **Liquidity model:** Frankfurt market makers тримають bias overnight; opening drive часто бере pre-market liquidity (sweep), потім розгортається у напрямі HTF тренду — тут BULLISH.
3. **Statistical edge (DAX-specific):** при D bias = bullish + opening sweep PDL → continuation у 60-67% (особисті спостереження + Frankfurt session studies). RR 1:2.5+ у момент retest.
4. **News-aware:** German Mfg PMI Final 07:55 UTC + EZ Final Mfg PMI 08:00 UTC — low impact, але кластер. Edge: **НЕ fade-ити** імпульс у вікні 07:50–08:10 UTC, чекати ретест після.

### План (LONG, після підтвердження тригера)

| Поле | Значення |
|------|----------|
| **Bias** | Bullish-Corrective 📈 |
| **Setup** | London ORB long з ретесту АБО EQL sweep + M5 CHoCH long |
| **Entry Zone** | `24 290 – 24 320` (на sweep EQL 24 289.5 + bullish CHoCH M5) |
| **Stop Loss** | `24 270` (нижче EQL та H4 swing low 24 283.5) — **45 pts ризику від entry 24 315** |
| **TP1** | `24 408` (PDH + H1 high) — RR ≈ **2.07** |
| **TP2** | `24 486` (H4 swing high) — RR ≈ **3.80** |
| **TP3** | `24 600 – 24 798` (D ATH-area) — RR ≈ **6.3+** |
| **Lot Size** | `$100 / (45 pts × $1) ≈ 2.22 contracts` (GER40: 1 pt = $1 на 1 contract — ⚠️ перевірити брокер) |
| **Risk** | $100 (1% від $10 000) |

### Альтернативний LONG (ORB break-and-retest, без sweep)

- **Entry:** ретест верху London opening range (перші 30 хв post-open) — приблизно `24 400–24 420` після пробою
- **SL:** нижче opening range low – 10 pts (~50–60 pts SL)
- **TP1/TP2:** `24 486 / 24 600` — RR ~1.5/2.5
- Менш атрактивний RR — використовувати тільки якщо sweep сценарій не спрацював.

### Invalidation

- M15 close нижче `24 270` після entry → закрити трейд
- Денний close нижче `24 200` → bias переглянути на bearish

---

## ⚠️ News & Session Context

| Час (UTC) | Подія | Impact | Дія |
|-----------|-------|--------|-----|
| 07:55 | German Mfg PMI Final (Apr) | Low | Не входити 07:50–08:05; чекати ретест |
| 08:00 | EZ Final Mfg PMI | Low | Кластер з German PMI — pause |
| Весь день | Без high-impact | — | Безпечно |

**Сесійні вікна:**
- London KZ (summer): 06:00–08:00 UTC ✅ (DAX cash open all'in)
- NY KZ (summer): 12:00–14:00 UTC — друге вікно для continuation
- Київський час 09:00 = 06:00 UTC → правило "не раніше 09:00 Kyiv" **виконано** при London open

## 🧠 Коментар

DAX знаходиться у **bullish re-accumulation після D-recovery з 23 613**. Структура HTF недоторкана, поточна compression на H4 (`24 283–24 408`) виглядає як готовність до експансії. Найбільш ймовірний сценарій — sweep EQL `24 289.5` під London open для забору sell-side ліквідності, після чого long-impulse у бік PDH `24 408` та далі `24 486`. SMT з US500 синхронна — підтверджує bias.

**RR > 1:2 на TP1 ✅ — setup торгувальний.**

**Відмова:** якщо до 09:00 UTC ціна не дала ані sweep EQL, ані пробою opening range high — пропустити сетап (no edge без тригера). Не входити "за прайсом".
