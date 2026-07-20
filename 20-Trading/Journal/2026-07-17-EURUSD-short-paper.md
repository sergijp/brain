---
title: "EURUSD SHORT (PAPER) — ASR Asia Sweep&Reclaim short, CLOSED WIN (TP2-A hit, full close) — risk-override forward"
date: 2026-07-17
time_kyiv: "09:08"
time_utc: "06:08"
time_kyiv_filled: "~11:5x-12:00"
time_utc_filled: "~08:5x-09:00"
time_kyiv_tp1: "13:34"
time_utc_tp1: "10:34"
time_kyiv_closed: "13:54"
time_utc_closed: "10:54"
tags: [trading, journal, eurusd, asr, paper, forward-test, risk-override]
category: trading
pair: EURUSD
direction: short
order_type: sell-stop
order_state: filled
strategy: asr-orb-intraday-system
status: closed   # planned → open → closed
result: win
agent: journal-writer
paper: true
real_account_touched: false
risk_state_touched: false
risk_override: true
override_reason: "Risk-gate BLOCK (real): ASR signal-mode/форвард live заблоковано + pair-heat EURUSD 7/0 цього тижня. Override дозволено ЛИШЕ як paper/demo для форвард-спостереження. Real рахунок недоторканий (real_risk_usd 0)."
override_scope: paper/demo-only
risk_usd_real: 0
risk_usd_paper: 100
rr_planned: 2.05
entry_fill: 1.14450
tp1_hit: true
partial_tp1_hit: true
sl_moved_to_be: true
sl_current: 1.14450
partial_closed_pct: 50
realized_pips_partial: 10.4
realized_usd_paper_partial: 62
runner_lot: 0.595
tp2_hit: true
closed_price: 1.14278
result_pips: 13.8
result_R: 1.64
result_usd_real: 0
result_usd_paper: 164
forward_candidate: "N=1 (перший закритий ASR-сигнал форварду — резолюція WIN)"
asr_signal: "перший ASR-сигнал в історії форварду — РЕЗОЛЮЦІЯ: TP1+TP2 повний WIN, forward-log N: 0→1"
tv_position_id: "sXGFx4"
tv_symbol: "OANDA:EURUSD"
pinecone_indexed: false
---

# EURUSD SHORT (PAPER) — 2026-07-17

> 🧪 **PAPER / FORWARD-TEST.** Real risk $0. `real_account_touched: false`. Реальний `_risk-state.json` day/week-risk НЕ змінюється.
> ⚠️ **Risk override applied:** Risk-gate повернув 🔴 BLOCK (real). Override дозволено ЛИШЕ як paper/demo (`override_scope: paper/demo-only`). Real рахунок недоторканий (real_risk_usd 0, real_account_touched false).
> ⛔ Real-гілка заблокована: ASR signal-mode/форвард live-BLOCK (до бектесту) + pair-heat EURUSD 7/0 цього тижня. **Paper-win НЕ знімає real-block** — потрібен performance-analyst бектест (це форвард-датапоінт на користь розблокування).
> ✅ **CLOSED / WIN** — обидві цілі взято. TP1 1.14346 HIT о 13:34 (50% +10.4p) → SL@BE → **TP2-A 1.14278 ДОСЯГНУТО** (low бара 1.14267 проколов ціль на 1.1p), runner 0.595 lot закрито @ 1.14278 (+17.2p). Повне закриття о **~13:54 Kyiv** (природно, задовго до flat 17:00). Blended на 1.19 lot екв ≈ **+13.8p / +1.64R** (~+$164 paper). Це **перший закритий ASR-сигнал форварду — forward-log N: 0→1**.
> 🔄 Напрям **ПРОТИЛЕЖНИЙ** вчорашньому paper-long [[Journal/2026-07-16-EURUSD-long-paper]] (той вибило стопом −1R). Урок: торгувати з домінантним USD-потоком, не проти.

## Plan

| Field | Value |
|-------|-------|
| Order type | **SELL STOP** → **FILLED** |
| Entry | 1.14450 (fill @ 1.14450) |
| SL | ~~1.14534~~ → **BE 1.14450** (переведено у беззбиток на runner після TP1; ризик 0) |
| TP1 | 1.14346 ✅ **HIT 13:34** (AL, RR 1:1.24, часткова 50% + BE — механіка форварду; +10.4p realized) |
| TP2-A | 1.14278 ✅ **HIT ~13:54** (RR 1:2.05, runner-ціль; low бара 1.14267 проколов на 1.1p; runner 0.595 lot закрито; +17.2p) |
| Lot | 1.19 (paper) |
| Risk (real) | **$0 (0%) — PAPER, реальний депозит недоторканий** |
| Risk (paper) | ~$100 (1%) |
| RR planned | 1:2.05 |
| RR realized | **1:1.64 (blended)** |
| Strategy | [[Strategies/asr-orb-intraday-system]] (ASR — Asia Sweep & Reclaim, short-варіант) |
| TV position | `sXGFx4` (OANDA:EURUSD) |

Валідність: **ASR-вікно 09:00–13:00 Kyiv**. Hard flat **17:00** (перенесено з 17:45 перед UoM Michigan medium 17:00). Обидві цілі взято о ~13:54 — задовго до flat.

## Результат (закриття 13:54 Kyiv / 10:54 UTC — TP2-A HIT, повний WIN)

- **TP2-A 1.14278 ДОСЯГНУТО** — low бара 1.14267 проколов ціль на 1.1p. Runner 0.595 lot закрито @ 1.14278.
- Розклад по частинах: **TP1-half** (0.595 lot) **+10.4p**; **TP2-runner** (0.595 lot) **+17.2p**.
- **Blended** на 1.19 lot екв ≈ **+13.8p / +1.64R** (~**+$164 paper**). Real $0.
- Ціна зупинилась **ВИЩЕ** H4 demand 1.14128 (**G3 спрацював** — не тягнули в пащу, вийшли на TP2-A, і ціна відскочила від demand). Вихід о ~13:54 — природний, задовго до flat 17:00.
- `status`: **CLOSED**, `result`: **WIN**.

## Стан (оновлення 13:34 Kyiv / 10:34 UTC — TP1 HIT + BE)

- **TP1 1.14346 ДОСЯГНУТО о 13:34 Kyiv.** Зафіксовано **50% обсягу**: ~**+10.4p** на половині → ~**+$62 paper realized** на 0.595 lot.
- **SL переведено у BE 1.14450** на залишку (0.595 lot runner) — ризик на runner став 0.
- Runner прямував до **TP2-A 1.14278**, M15 тиснув вниз, відкату не було.

## Стан (оновлення 12:07 Kyiv / 09:07 UTC)

- **Filled** @ 1.14450 ~11:5x-12:00 Kyiv. Тригер: sweep Asia high 1.14520 (торкнув поріг 1.14516) → reclaim M15 close тілом <1.14482 → крізь entry-стоп 1.14450.
- **EUR CPI Final 12:00 Kyiv** (2.8% vs 3.2% prev — дезінфляція, in-line з прогнозом) підштовхнув униз, за short-тезою.
- **G2 anti-double-sweep НЕ спрацював** — deep sweep >1.14700 не було, тригер чистий/валідний.

## Why (Dixie — форвард-кандидат, знижений грейд)

- **Shallow sweep форвард-кандидат** за USD-потоком (на відміну від вчорашнього невдалого long — напрям тепер збігається з потоком).
- ASR short-варіант: провалений пробій азійського діапазону вгору (sweep BSL > 1.14516) + reclaim close тілом < 1.14482 → sell-stop під low reclaim-бару.
- SL структурний та тісний (−8.4 pips за sweep-high), TP2-A до відскоку від H4 demand 1.14128 → RR 2.05 валідний.
- **Deep sweep > 1.14700 = auto NO-TRADE** (глибокий прокол ≠ shallow reclaim-сетап) — не спрацював, тригер чистий.
- Грейд знижено у дебаті: **НЕ A-setup**, forward-кандидат.

## Risk check (🔴 BLOCK real → override PAPER)

- **VERDICT REAL: 🔴 BLOCK.** Override → **paper/demo only**, real рахунок недоторканий.
  1. **ASR signal-mode / форвард** — live заблоковано до проходження бектесту (`asr_live_status`).
  2. **Pair-heat EURUSD 7 / 0** цього тижня.
- **VERDICT PAPER: 🟢 OK** за умов 6 гейтів (нижче).
- **WARN:** TP1 RR **1.24 < 1.8** — частковий вихід, механіка форварду (не самостійний вхід). TP2-A **2.05 PASS**.
- **override_scope:** paper/demo only — real_risk_usd 0, real_account_touched false.
- **Paper-win НЕ знімає real-block.** Пара під pair-heat, розблокування real-гілки ASR — тільки після performance-analyst бектесту. Це — форвард-датапоінт на користь розблокування (N=1 WIN).

### 6 гейтів (умови PAPER-OK)

| # | Гейт | Умова | Статус |
|---|------|-------|--------|
| G1 | Грейд | forward-кандидат (не A-setup) | ✅ |
| G2 | Anti-double-sweep | 2-й тап > 1.14516 **до** філа = **CANCEL** | ✅ не спрацював (deep >1.14700 не було) — тригер чистий |
| G3 | TP2 механіка | вийти на TP2-A **до** H4 demand 1.14128 | ✅ **СПРАЦЮВАВ** — ціна відскочила від demand, ми вже вийшли на TP2-A вище |
| G4 | TP1 механіка | часткова 50% на TP1 + перевід у BE | ✅ виконано 13:34 |
| G5 | Flat | **17:00** перед UoM Michigan (medium) 17:00 | ✅ вийшли на TP2-A о ~13:54, задовго до flat |
| G6 | Cap 1% | ізольований 1%: GBPUSD **SKIP**, GER40 **wait** — жодної кореляційної надбавки | ✅ |

## Kassandra challenge (resolved → convergence R2)

- **R1 challenge → convergence R2** після узгодження 6 гейтів.
- Це **8-й захід у EURUSD за тиждень (0/7)** — range-fade, не trend-flip.
- АЛЕ: напрям **за USD-потоком** і **RR валідний** як форвард → прийнято як **paper forward-signal**, не real.
- Резолюція: НЕ ставити real (BLOCK лишається). Взяти лише як **paper forward-signal** для збору ASR-статистики.
- **Пост-фактум:** сетап відпрацював чисто — перший clean paper-win у EURUSD за тиждень. Теза «напрям за USD-потоком» підтвердилась.

## Links

- Analysis: [[Analysis/2026-07-17/EURUSD-analysis]]
- Strategy: [[Strategies/asr-orb-intraday-system]]
- Forward-log: [[Journal/Forward/asr-orb-forward-log]]
- Вчорашній протилежний напрям (LOSS): [[Journal/2026-07-16-EURUSD-long-paper]]
- Risk state: [[Journal/_risk-state]]

## Execution log (PAPER)

- [x] Sell-stop виставлено @ 1.14450 (pending) — тригер London-sweep > 1.14516 + reclaim close < 1.14482
- [x] **Filled @ 1.14450** ~11:5x-12:00 Kyiv (sweep Asia high 1.14520 торкнув 1.14516 → reclaim M15 close <1.14482 → крізь 1.14450). EUR CPI Final 12:00 (2.8% дезінфляція, in-line) підштовхнув униз.
- [x] **Moved SL to BE 1.14450** @ TP1 (13:34 Kyiv) — runner 0.595 lot risk-free
- [x] **TP1 hit @ 1.14346** о 13:34 Kyiv — часткова 50% (~+10.4p, ~+$62 paper realized)
- [x] **TP2-A hit @ 1.14278** о ~13:54 Kyiv — low бара 1.14267 проколов на 1.1p, runner 0.595 lot закрито (+17.2p)
- [x] **Closed** @ 1.14278 о ~13:54 Kyiv — result **+13.8p blended / +1.64R** (~+$164 paper). Ціна відскочила від H4 demand 1.14128 (G3 спрацював).
- ~~CANCEL (G2)~~ / ~~deep sweep > 1.14700~~ — не спрацювали, тригер чистий

_Закрито 13:54 Kyiv: TP2-A 1.14278 hit (повний WIN). TP1-half +10.4p + TP2-runner +17.2p → blended +13.8p / +1.64R (~+$164 paper). Real $0. Перший закритий ASR-сигнал форварду — N: 0→1._

## Lessons (post-trade)

- **Урок #1 — торгувати з домінантним USD-потоком, не проти.** КОНТРАСТ: вчорашній paper-long (2026-07-16) вибило −1R (лонг проти потоку у стелю під незнятим Weak High). Сьогодні short **за потоком** = +1.64R WIN. Той самий інструмент, той самий тиждень — різниця лише в узгодженні з домінантним потоком.
- **Урок #2 — G3 (не тягнути в пащу) працює.** Вийшли на TP2-A 1.14278 ВИЩЕ H4 demand 1.14128, і ціна відскочила від demand. Якби тягнули на TP2-B / глибшу ціль — віддали б відкат.
- **Урок #3 — ASR shallow-sweep reclaim за потоком + новинний каталізатор (EUR CPI дезінфляція) = чистий сетап.** Перший датапоінт форварду на користь ASR (N=1 WIN, +1.64R). Real-block ЗАЛИШАЄТЬСЯ до бектесту — paper-win не знімає.
