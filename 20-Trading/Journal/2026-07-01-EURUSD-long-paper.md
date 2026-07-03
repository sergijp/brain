---
title: "EURUSD LONG — 2026-07-01 Paper (Confirmation-entry, SMC+PA Combo)"
date: 2026-07-01
time_kyiv: "17:30"
time_utc: "14:30"
tags: [trading, journal, eurusd, smc-price-action-combo, paper, signal, forward-test]
category: trading
pair: EURUSD
direction: long
strategy: smc-price-action-combo
status: planned   # planned → open → closed
agent: journal-writer
type: paper-trade
paper: true
real_account_touched: false
risk_override: false
repeated_focus_attempt: 4
repeated_focus_pattern: "EURUSD-long discretionary-SMC"
hold_type: swing-paper
observation_deadline: "2026-07-02 (кінець London)"
pinecone_indexed: false
---

# EURUSD LONG — 2026-07-01 (PAPER / SIGNAL)

> 🧪 **PAPER-угода — форвард-тест, real $0.** Це НЕ реальний вхід. Реальний рахунок недоторканий (`real_account_touched: false`).
> Risk-manager дав **OK(PAPER)** — гейт пройдено умовно. Реальний ризик-стан не змінюється.
> ⚠️ Це **contra-Weekly** сетап (W bearish) — саме тому лише paper.

## Status

**PLANNED — pending confirmation trigger.** Позиція ще не заповнена. Чекаємо тап PDL + M15 reclaim.

## Plan

| Field | Value |
|-------|-------|
| Trigger | Тап **PDL 1.13827** → M15 rejection + reclaim close **вище PDL** → вхід |
| Entry | 1.13870 |
| SL | 1.13770 (−10 pips) |
| TP1 | 1.14004 (RR 1.34) — partial 30% + BE |
| TP2 | 1.14219 / Daily Open (RR 3.49) — commitment target |
| TP3 | 1.14367 / PDH (RR 4.97) |
| Blended RR | ~3.3 |
| Paper Lot | 1.0 (симуляція) |
| Risk (paper) | $100 (умовно) · **REAL $0** |
| Утримання | swing-paper, **без 17:45 flat**; дедлайн спостереження — кінець London ср 02.07 |
| Strategy | [[Strategies/smc-price-action-combo]] |

## Why

- **W bearish** (макро-даунтренд від 1.185) — це КОНТР-тренд лонг, тому виключно paper.
- **D bullish-corrective** — денний recovery bounce (higher lows 1.13335 → 1.13827 → 1.14018), сетап іде в бік денної корекції.
- **USD-негативний фон** підтримує EUR-лонг: ADP 98K (слабко), S&P PMI 53.9, ISM 53.3, ISM Prices 73.0.
- **PDL 1.13827 = ключова SSL / низ H4-range** — очікуваний свіп ліквідності знизу + reclaim (класичний SMC+PA sweep + reclaim).
- **Confirmation-entry** (тап + M15 reclaim), не сліпа лімітка → тісний SL 10 pips і кращий blended RR.

## Risk check (paper — умовний)

- Day risk used: **0.0% / 3%** (paper $0 не враховується у реальний ризик-стан)
- Correlation: PASS (paper — не впливає на реальний стан; реальних open_positions немає)
- News: ⚠️ **Lagarde (ECB) blackout** активний — якби REAL, це BLOCK
- Session: тригер очікується в London/NY-вікні; утримання overnight (свідомо, paper swing)

> ⚠️ **Note від risk-manager:** якби це був REAL — **VERDICT: BLOCK**. Три блокери:
> 1. **News-blackout** — виступ Lagarde (ECB).
> 2. **Repeated-focus #4** (див. нижче) — 4-та спроба патерну без чистого win.
> 3. **Overnight hold** проти intraday-only політики (no-overnight, flat 17:45).
>
> **OK видано ЛИШЕ тому, що real $0.** Це нативний paper (форвард-тест), **НЕ override** реального гейту.

## 🔁 REPEATED-FOCUS — attempt #4

Це **4-та спроба** патерну **EURUSD-long discretionary-SMC** за ~30 днів. Історія (`clean_wins = 0`):

| # | Дата | Результат | Нотатка |
|---|------|-----------|---------|
| 1 | 2026-05-07 | loss | широкий SL |
| 2 | 2026-05-12 | blocked → paper | BLOCK через SMT дивергенцію → paper |
| 3 | 2026-06-17 | loss (paper) | override paper, SL вибито проколом 1.16008 |
| **4** | **2026-07-01** | **paper (цей запис)** | **contra-W, news-blackout, overnight — тому paper** |

За правилом repeated-focus (3+ спроб / ~30 днів без чистого win → 4-та = BLOCK до бектесту) — **реальний вхід заблоковано**. Патерн потребує `performance-analyst` бектесту перед будь-яким live. Поточна спроба легітимна лише як форвард-тест на $0.

## 🧪 Гіпотези форвард-тесту

**Гіпотеза А — контр-W D-корекція на USD-негативному фоні.**
Чи здатна денна корекція (D bullish) проти Weekly bearish відпрацювати на слабкому USD (ADP/ISM/PMI)? Тест ваги фундаментального фону як тимчасового драйвера проти HTF-структури.

**Гіпотеза Б — confirmation-entry vs сліпа лімітка.**

| Підхід | Fill | SL | Blended RR |
|--------|------|-----|-----------|
| Сліпа лімітка | 1.13815 | 22.5 pips | 1.71 |
| **Confirmation (цей план)** | 1.13870 | 10 pips | **3.3** |

Гіпотеза: очікування M15 reclaim жертвує ~5.5 pips гіршим fill, але вдвічі тісніший SL дає ~2x кращий blended RR. Форвард-тест перевіряє, чи виправдовує підтвердження пропущені сліпі філи.

## Invalidation

- Тап PDL **без reclaim** → **no-trade** (сетап не активується).
- M15-close **< 1.13800** після філу → **SL** (вихід).
- H1-close **< 1.13618** до тригера → **сетап мертвий** (структура зламана).

## Links

- Analysis: [[Analysis/2026-07-01/EURUSD-analysis]]
- Strategy: [[Strategies/smc-price-action-combo]]

## Execution log (paper)

(заповнюється при активації тригера)

- [ ] Тап PDL 1.13827 @ <time>
- [ ] M15 rejection + reclaim close > PDL @ <time>
- [ ] Opened at 1.13870 @ <time>
- [ ] TP1 1.14004 hit — partial 30% + SL→BE @ <time>
- [ ] TP2 1.14219 (Daily Open) hit @ <time>
- [ ] TP3 1.14367 (PDH) hit @ <time>
- [ ] Closed at <price> @ <time> — result <pips> / $<paper>

## Lessons (post-trade)

(заповнюється після закриття / на дедлайні спостереження 02.07)

---

> Chart: намальована `long_position` id **rPgmI2** на TV-графіку.
> Позиція для форвард-логу: **discretionary SMC+PA**, НЕ ASR — тому окремий discretionary-paper запис у `Journal/` (не в `Forward/asr-orb-forward-log.md`).
