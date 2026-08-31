---
title: "EURUSD LONG (PAPER) — FVG entry, AMD watch attempt #10, risk-override forward-test"
date: 2026-08-26
time_kyiv: "10:53"
time_utc: "07:53"
tags: [trading, eurusd, long, smc-combo, fvg-entry, paper, forward-test, risk-override, repeated-focus]
category: trading
pair: EURUSD
direction: long
order_type: manual-trigger (M5 close confirmation, не resting limit ордер брокера)
strategy: smc-price-action-combo
strategy_pattern: SECONDARY (AMD + M15 Structure Break + FVG Entry) — НЕ бектестована
status: closed   # planned → open → closed — FILLED 06:55 UTC, ЗАКРИТО SL 10:45-11:00 UTC 26.08
agent: journal-writer
paper: true
real_account_touched: false
risk_state_touched: false
risk_override: true
override_scope: paper/demo-only
override_reason: "Risk-gate BLOCK (real) — repeated_focus_watch EURUSD-long-AMD HARD-BLOCK, 0/5 clean wins (буде attempt #10), бектест-передумова невиконана (механічний трек закрито 25.08). Override дозволено лише paper."
repeated_focus_attempt: 10
repeated_focus:
  scope: EURUSD-long-AMD
  level: ACTIVE-BLOCK-WATCH / HARD-BLOCK
  attempt: 10
  clean_wins: 0
  window_days: 30
  note: "10-та спроба того самого дискреційного EURUSD-long тезису (AMD/discretionary-SMC) за ~4 місяці. Тепер РЕАЛІЗОВАНА (6-та реалізована спроба): FILLED 06:55 UTC 26.08, закрито LOSS через SL 10:45-11:00 UTC 26.08. clean_wins лишається 0/6."
tv_position_id: "hdlnex"
tv_symbol: "OANDA:EURUSD"
entry_fvg_zone: [1.16654, 1.16670]
entry_planned: 1.16662
entry_actual: 1.16670
filled_time_utc: "06:55"
fill_note: "Filled по close бару sweep-and-reclaim (manual-trigger M5 close confirmation), НЕ по плановому мідпоінту 1.16662 — виконання, не resting limit"
rr_planned_tp1: 2.29
rr_planned_tp2: 2.62
rr_planned_tp3: 4.24
rr_actual_tp1: 1.76
rr_actual_tp2: 2.04
rr_actual_tp3: 3.40
tp1_status: touched-not-closed
closed_at: 2026-08-26
closed_time_utc_approx: "10:45-11:00"
closed_reason: sl_hit_intrabar
exit_price_sl: 1.16620
exit_price_actual_low_breach: 1.16611
result: loss
result_pips: -5.0
result_R: -1.0
result_usd_paper: -50
retro_close_note: "Запис висів status=open/planned без фактичного закриття. Закрито заднім числом 2026-08-28 journal-writer'ом на основі незалежної OHLCV-верифікації (M15 OANDA:EURUSD)."
pinecone_indexed: false
---

# EURUSD LONG (PAPER) — 2026-08-26

> 🧪 **PAPER / FORWARD-TEST.** Real risk $0. `real_account_touched: false`, `risk_state_touched: false` — реальний `_risk-state.json` (day/week risk, open_positions) НЕ змінюється цим записом. Позиція фіксується лише в `paper_positions` / `repeated_focus_watch.attempts`.
> ⚠️ **Risk override applied:** Risk-gate повернув 🔴 BLOCK (real) — `repeated_focus_watch` EURUSD-long-AMD, HARD-BLOCK, 0/5 clean wins, бектест-передумова (performance-analyst) не виконана, механічний трек закрито 25.08. Override дозволено ЛИШЕ як paper/demo — власник явно попросив поставити позицію.
> ✅ **FILLED — 1.16670 @ 06:55 UTC** (замість планового мідпоінту 1.16662; виконання по close бару sweep-and-reclaim, manual-trigger M5, не resting limit). SL 1.16620.
> 🔴 **ЗАКРИТО LOSS ЗАДНІМ ЧИСЛОМ (retro-close 2026-08-28).** TP1 (1.16758) торкнуто інтрабар о 08:30 UTC (touched-not-closed), після чого ціна розвернулась і **SL 1.16620 пробито інтрабар на M15-барі 10:45-11:00 UTC** (low 1.16611). Закрито до примусового flat 19:00 UTC — прапорець "flat forced-close" НЕ застосовується, позиція закрита по SL значно раніше. Результат: **-5.0пп / -1.0R (paper -$50)**.

## Plan

| Field | Value |
|-------|-------|
| Pattern | SMC+PA Combo — **SECONDARY** (AMD + M15 Structure Break + FVG Entry), НЕ бектестована |
| Entry trigger | M5 **close вище 1.16662** (мідпоінт FVG 1.16654–1.16670) **ПІСЛЯ дотику в зону** — реакційна свічка, не перший дотик |
| Entry (planned ref.) | 1.16662 |
| **Entry (actual, FILLED)** | **1.16670 @ 06:55 UTC** — по close бару sweep-and-reclaim, manual-trigger M5, не resting limit |
| Скасування паттерну | M5 close **нижче 1.16639** без реакції → паттерн мертвий, ордер знімається — інвалідація формально не тестувалась окремо: SL 1.16620 пробито раніше/одночасно з тим самим рухом вниз |
| SL | 1.16620 (без змін) — від фактичного входу **-5.0 пп** |
| SL (для розрахунку лота) | буферизовано до **6 пп** за прецедентом 07-16 |
| TP1 | 1.16758 — **+8.8 пп від факт. входу, RR 1:1.76** (планово було 1:2.29 від референсної ціни; трохи нижче порогу 1.8, але угода вже тригернута, заднім числом не скасовується) |
| TP2 (гейт-варіант, TP2-A) | 1.16772 — **+10.2 пп від факт. входу, RR 1:2.04** (планово 1:2.62) |
| TP3 (опортуністичний) | 1.16840 — **+17.0 пп від факт. входу, RR 1:3.40** (планово 1:4.24) — TP reachability WARN, не критерій входу |
| Lot | ≈**0.83** (розрахунок на буферизованому SL 6 пп, без змін) |
| Risk | **$50 (0.5% від $10 000)** — **paper**, real $0 |
| Strategy | [[Strategies/smc-price-action-combo]] |
| TV position | `hdlnex` (OANDA:EURUSD, long_position drawing через internal childs entryPrice/stopPrice/targetPrice) |

Валідація drawing (read-back через `_source.properties().childs()`): entry `1.16662` (reference), stop `1.1662`, target `1.16772` — план збігається; фактичний філ відрізняється від reference-ціни (див. вище).

### Статус на 08:32 UTC (проміжна нотатка, актуальна на момент того запису)

- **TP1 (1.16758) вже пробитий інтрабар** — high бару 08:30 UTC = 1.16768. Наразі відкат до ~1.16749.
- **TP2 (1.16772) не досягнуто.**
- **TP1 touched-not-closed** — частковий вихід на TP1 не виконано автоматично (paper, drawing без OCO-логіки).
- Інвалідація (M5 close < 1.16639) — жодного разу не спрацювала від входу до 08:32 UTC.

### Фінальний результат (RETRO-CLOSE, зафіксовано 2026-08-28)

Незалежна перевірка M15 OHLCV OANDA:EURUSD за 26.08.2026:

| Момент | Бар (M15, UTC) | O/H/L/C | Подія |
|---|---|---|---|
| 08:15–08:30 | `1787732100` | 1.16750 / **1.16770** / 1.16743 / 1.16768 | TP1 (1.16758) touched intrabar — збігається з журналом (high 1.16768 @ 08:30) |
| 08:30–08:45 | `1787733000` | 1.16768 / 1.16768 / 1.16717 / 1.16736 | Відкат почався одразу після дотику TP1 |
| 10:45–11:00 | `1787741100` | 1.16648 / 1.16649 / **1.16611** / 1.16619 | **SL 1.16620 пробито інтрабар** (low 1.16611, -0.9пп понад номінал) |
| 18:00–19:00 (для довідки, flat-момент) | H1 `1787767200` | 1.16528 / 1.16545 / 1.16502 / **1.16514** | Ціна на 19:00 UTC — суттєво нижче SL і entry, підтверджує стійкість розвороту (не фітиль) |

**Висновок:** позиція закрита по SL 1.16620 приблизно о **10:45–11:00 UTC 26.08.2026** — задовго до примусового flat (19:00 UTC / 22:00 Kyiv). Прапорець "закрито примусово на flat" НЕ застосовується — flat-логіка стала неактуальною, бо SL спрацював раніше. Результат за конвенцією SL-дистанції (як у прецеденті 2026-07-16 — нетто = повна SL-дистанція, без урахування слиппеджу понад номінал): **-5.0 пп / -1.0R (paper -$50)**.

## Чому саме такий SL/лот

SL 4.2 пп номінально від референсної ціни (5.0 пп від фактичного входу) — тісний, під самим мідпоінтом FVG. Лот розрахований на буферизованих 6 пп (не на номінальних), щоб не переоцінити розмір позиції на випадок проковзування/сліпеджу в зоні входу — той самий підхід, що застосовувався 2026-07-16 (buffered SL для розрахунку лота при вузькому номінальному стопі). Ретроспективно: навіть буферизовані 6 пп не покрили б реальний прохід (низ бару 1.16611 = 5.9 пп від входу) — SL все одно спрацював би.

## Why (Dixie ⇄ Kassandra, узгоджено)

- Дискреційний трек `smc-price-action-combo`, **SECONDARY PATTERN** (AMD + M15 Structure Break + FVG Entry) — вхід на реакцію в FVG-зону, що лишилась після імпульсу вгору без відкату.
- Ранковий **sweep-план сьогодні (entry 1.1655–1.1662) НЕ тригернувся** — ціна пішла імпульсом вгору без відкату до зони sweep, залишивши натомість FVG вище — це і є поточний сетап.
- HTF bias лишається bullish (W/D bullish, H4 impulse-correction-impulse з підтвердженим SMT-звіреним sweep-reversal 25.08 на 1.16511) — вхід у напрямку HTF, не проти нього.
- **Kassandra CHALLENGE (real):** repeated-focus EURUSD-long-AMD у статусі HARD-BLOCK, 0/5 clean wins за 9 попередніх спроб, бектест-передумова (performance-analyst) не виконана, механічний трек закрито 25.08 — на реальному рахунку це прямий BLOCK, без винятків.
- **Kassandra accept (paper):** форвард-спостереження статистично цінне саме тому, що це вже 10-та спроба того самого тезису — потрібен ще один задокументований датапоінт (WIN або LOSS) для питання ретро "чи існує взагалі шлях, яким EURUSD-long дійшов би до чистого win".
- Конвергенція: **real — BLOCK, paper — OK WITH CONDITIONS** (див. Risk check).
- **RETRO-CLOSE висновок (2026-08-28):** датапоінт #10 дав відповідь — LOSS. HTF bullish bias і якісний контекст входу (реакційна свічка на FVG підтвердилась, TP1 навіть був пробитий інтрабар) не врятували угоду: розворот після 08:30 UTC був різким і стійким, SL пробито за ~2.5 год після TP1-touch. Це шостий реалізований результат репітед-фокус кластера EURUSD-long-AMD і шостий loss/loss-paper поспіль.

## Risk check (🔴 BLOCK real → override PAPER WITH CONDITIONS)

- **VERDICT: 🔴 BLOCK (real).** Override → **paper only**, real рахунок недоторканий (`real_account_touched: false`, `risk_state_touched: false`).
- **Підстава BLOCK (real):** `repeated_focus_watch` EURUSD-long-AMD — статус **ACTIVE-BLOCK-WATCH / HARD-BLOCK**, 9 попередніх спроб (5 реалізованих, усі loss/loss-paper/blocked-then-paper; 4 blocked-not-taken/expired-not-filled), `clean_wins 0`. Ця спроба — **#10**, FILLED, тепер **ЗАКРИТА LOSS**. `next_attempt_action`: BLOCK до бектесту performance-analyst (передумова невиконана, механічний трек закрито 25.08).
- **Стратегія не бектестована:** SECONDARY PATTERN (FVG entry) не має статусу `validated` — діє звичайний `Min RR 1.8`, а не expectancy-гейт. RR від факт. входу: TP1 1.76 (трохи нижче порогу 1.8), TP2 2.04 (PASS), TP3 3.40 (PASS, опортуністичний). Жодна з цілей не досягнута — угода закрита по SL.
- **TP reachability:** TP1/TP2 — PASS/WARN у межах денного залишку; TP3 (17.0 пп від факт. входу) — WARN. Не критично — позиція закрилась по SL задовго до будь-якої цілі.
- **News check:** ордер filled 06:55 UTC — до 12:00 UTC → діяв сценарій «вже filled» (беззбиток + відхід убік перед Core PCE/Prelim GDP 12:30 UTC). SL спрацював о 10:45-11:00 UTC — **ДО** новинного вікна 12:30 UTC, тобто закриття не пов'язане з новинним блекаутом.
- **Session check:** запис зроблено о 07:53 UTC / 10:53 Kyiv — після London KZ open (06:00–08:00 UTC). Фактичний filled 06:55 UTC — усередині London KZ. SL спрацював о 10:45-11:00 UTC — між London KZ і NY KZ (поза обома вікнами).
- **Day/week risk (real):** 0% / 0% — паперовий ризик $50 на це не впливає, `_risk-state.json.day_risk_used_pct` НЕ змінювався.
- **Consecutive losses (real):** 0/3 — не зачіпається paper-угодою.
- **override_scope:** paper/demo only — real_risk_usd 0, real_account_touched false, risk_state_touched false.

### 📰 Інструкція керування новинним блекаутом (застаріла — SL спрацював до 12:30 UTC)

| Умова | Дія |
|---|---|
| Ордер **НЕ filled** до **12:00 UTC** | ~~Знімати / не давати озброїтись у вікні 12:00–13:00 UTC~~ — неактуально, ордер вже filled |
| **Ордер вже filled до 12:00 UTC** | ~~Вивести в беззбиток і відійти вбік за 5–10 хв до 12:30 UTC~~ — неактуально: позиція закрилась по SL о 10:45-11:00 UTC, ДО настання цього вікна |
| Будь-який сценарій | ~~Flat: 19:00 UTC / 22:00 Kyiv~~ — неактуально: SL спрацював за ~8 годин до flat-часу |

## Kassandra challenge (resolved)

- **Real:** CHALLENGE утримано — repeated-focus HARD-BLOCK #10 і невиконана бектест-передумова достатні для BLOCK без винятків. Дискреційна теза (навіть якісна за HTF-контекстом) не скасовує статистичну підставу відмови на реальному рахунку.
- **Paper:** ACCEPT — форвард-датапоінт цінний саме через повторюваність невдалих спроб; SECONDARY PATTERN (FVG) відрізняється механікою входу від попередніх 9 спроб (Asia sweep+reclaim, contra-W confirmation тощо), тож дав нову інформацію, а не повторив той самий провальний вхід.
- Резолюція: **real — SKIP, paper — TAKE з умовами** (буферизований лот, активне керування новинним вікном, hard flat 19:00 UTC).
- **RETRO-CLOSE (2026-08-28):** датапоінт #10 закрито офіційно — **LOSS**, -5.0пп/-1.0R, SL hit ~10:45-11:00 UTC 26.08 (не flat). Kassandra-теза підтверджена ще раз: якісний HTF-контекст і навіть тимчасовий пробій TP1 не є достатньою підставою для real-входу при HARD-BLOCK репітед-фокусі — новий механізм входу (FVG замість Asia sweep) дав той самий клас результату (loss), що й 5 попередніх реалізованих спроб.

## Links

- Analysis: [[Analysis/2026-08-26/EURUSD-analysis]]
- Strategy: [[Strategies/smc-price-action-combo]]
- Risk state: [[Journal/_risk-state]]
- Precedent (buffered SL, override paper conventions): [[Journal/2026-07-16-EURUSD-long-paper]]

## Screenshots (озброєння плану — Screenshot Policy)

![[Analysis/2026-08-26/img/eurusd_h4.png]]
![[Analysis/2026-08-26/img/eurusd_h1.png]]
![[Analysis/2026-08-26/img/eurusd_m15.png]]
![[Analysis/2026-08-26/img/eurusd_position_armed_m5.png]]

## Execution log (PAPER)

- [x] Long position drawing озброєно на TV (`hdlnex`, OANDA:EURUSD) @ entry 1.16662 / SL 1.16620 / TP 1.16772 @ 10:53 Kyiv (07:53 UTC) — reference-позначка
- [x] M5 close вище 1.16662 після дотику в зону — тригер входу підтверджено (sweep-and-reclaim close)
- [x] **Filled @ 1.16670 @ 06:55 UTC** — фактична ціна відхилилась від референсної 1.16662 (виконання по close бару, не resting limit)
- [ ] Moved SL to BE — **НЕ виконано** (не встигли до розвороту; SL спрацював на номінальному рівні 1.16620, а не в беззбитку)
- [x] **TP1 touched-not-closed** @ 1.16768 (high M15-бару 08:15-08:30 UTC), частковий вихід не виконано автоматично
- [ ] TP2-A hit @ 1.16772 — не досягнуто
- [ ] Скасовано за інвалідацією (M5 close нижче 1.16639 без реакції) — окремо не тестувалось, SL спрацював у тому ж русі вниз
- [x] **SL hit @ 1.16620 (breach low 1.16611) @ ~10:45-11:00 UTC 26.08** — LOSS **-5.0пп / -1.0R (paper -$50)**
- [ ] ~~Закрито примусово на flat 19:00 UTC / 22:00 Kyiv~~ — **НЕ ЗАСТОСОВУЄТЬСЯ**: позиція вже закрита по SL за ~8 год до flat-часу. RETRO-CLOSE 2026-08-28 зафіксовано вище.

## Lessons (post-trade)

**Проміжна нотатка (08:34 UTC, історична):** фактична ціна входу (1.16670) відхилилась від референсного мідпоінту плану (1.16662) на +0.8 пп через механіку виконання "close бару sweep-and-reclaim" замість resting limit — це знизило RR TP1 з планового 2.29 до факт. 1.76 (нижче Min RR 1.8). Для майбутніх FVG-entry сетапів варто явно фіксувати в плані, що manual-trigger M5-close вхід може виконатись гірше референсної ціни на величину, порівнянну з розміром SL-буфера — і враховувати це в попередньому RR-розрахунку, а не постфактум.

**RETRO-CLOSE висновок (2026-08-28):**

- Угода тригернулась і навіть торкнулась TP1 інтрабар (08:30 UTC) — вхід технічно "спрацював" на короткому горизонті. Але SL 1.16620 (5.0 пп) виявився занадто тісним відносно подальшої волатильності: розворот від максимуму TP1-touch до пробою SL зайняв лише ~2.5 години.
- Це **шоста реалізована спроба** (з 10 зафіксованих) кластера `EURUSD-long-AMD`, і **шоста поспіль loss/loss-paper**. `clean_wins` лишається 0/6 реалізованих. Новий механізм входу (SECONDARY FVG-pattern замість Asia sweep+reclaim) дав ту саму якість результату — це аргумент, що проблема кластера НЕ в конкретній техніці входу, а в чомусь спільному для всього тезису "EURUSD-long-AMD" (HTF bias читання, розмір SL відносно реальної волатильності, або сам сетап-клас).
- **Процедурний урок:** запис висів у стані `status: open` / `planned-armed-paper` без фактичного закриття протягом ~2 днів (26.08 → 28.08), хоча дані для закриття (SL-брейч) вже існували в барах з 26.08. Закриття угод має відбуватись того ж дня (при flat-моніторингу) — відкладене адміністративне закриття через кілька днів є відхиленням від процесу, навіть якщо результат вдалось відновити точно з OHLCV.
