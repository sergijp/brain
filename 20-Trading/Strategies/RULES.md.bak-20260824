---
title: "Trading Rules — Mandatory Pre/Post Analysis Checklist"
date: 2026-04-26
tags: [trading, rules, mandatory, smc, workflow]
category: trading
status: active
version: 2.0
last_updated: 2026-04-26
source_retros: [2026-04-23, 2026-04-24]
pinecone_indexed: false
---

# Trading Rules v2.0 — Mandatory Workflow

> **Призначення**: набір обов'язкових правил для будь-якого Top-Down Analysis (TDA) та виконання угод.
> **Джерело**: дистильовано з Daily Retros 2026-04-23 (+11.1R) та 2026-04-24 (−3R, 3 INVALID плани).
> **Hard rule**: всі правила застосовуються до кожного інструмента, без винятків.

---

## 🟥 Правило 0 — INTRADAY ONLY (FOUNDATIONAL)

**Ми торгуємо ТІЛЬКИ інтрадей. Позицій overnight/swing немає.**

### Жорсткі обмеження:
- ✅ **Усі позиції відкриваються та закриваються в межах одного торгового дня (00:00 → 23:59 UTC)**
- ❌ **НЕ переносити позицію через ніч** (close → next day open)
- ❌ **НЕ переносити через вікенд** (Friday close → Monday open)
- ⏰ **Hard close time:**
  - Forex/Metals: до 21:00 UTC (перед закриттям NY session)
  - Indices (US100/US500/GER40): до 20:00 UTC
  - П'ятниця: примусове закриття до 19:00 UTC незалежно від P&L

### TP не досягнуто до closing time:
```
if current_time >= hard_close and position.is_open:
    market_close(position)
    log("Forced intraday close — TP not reached")
```
- Не «давати трейду шанс ще день»
- Не «трохи подовжимо, бо MFE великий»
- Закрити по ринку — без винятків

### Ситуація «немає позиції»

**Якщо немає відкритої позиції на даний момент — ОБОВ'ЯЗКОВО так і казати!**

Заборонено:
- ❌ Вигадувати позицію якої немає
- ❌ Описувати «гіпотетичну позицію» як реальну
- ❌ Казати «у нас Long на EURUSD» якщо нічого не відкривали
- ❌ Робити аналіз так, ніби позиція вже існує

Обов'язково:
- ✅ «Зараз позицій НЕМАЄ. Виконую аналіз для пошуку setup.»
- ✅ «Угод сьогодні не відкривали. Trade plan готовий, чекаємо тригер.»
- ✅ Якщо ретро/підсумок — чесно вказувати «entry не тригернувся, угоди не було»
- ✅ Розрізняти **plan** (рівні готові, чекаємо) vs **active position** (відкрита) vs **closed** (зафіксована)

### Перевірка перед розмовою про P&L:
```python
# Auto-check before any P&L statement
positions = check_open_positions()  # via replay_trade status or manual log
if not positions:
    say_explicitly("Відкритих позицій НЕМАЄ")
    do_not_fabricate_pnl()
```

**Чому це Правило 0:**
- Інтрадей-стратегія SMC + PA Combo побудована саме на сесійних рухах (London/NY KZ), не на тижневих трендах
- Overnight risk = неконтрольовані гепи, news, азійські маніпуляції
- Капітал $10,000 з ризиком 1% не витримує overnight волатильність indices/metals
- Чітке розділення «є позиція / немає позиції» — основа дисципліни та чесної звітності

---

## 🟥 Правило 1 — Pre-Flight Price Verification (АВТОМАТИЧНЕ)

**ПЕРЕД** написанням TDA для кожного інструмента — обов'язковий MCP виклик:

```python
# Auto-executed by Claude before generating any analysis
quote = mcp__tradingview__quote_get(symbol)
current_price = quote.last

# Hard validation
if abs(planned_entry - current_price) / current_price > 0.05:  # 5% threshold
    raise ABORT_PLAN(f"Scale error: entry {planned_entry} vs current {current_price}")
```

**Workflow integration:**
1. Перед `chart_set_symbol` → виклик `quote_get` для current price
2. Записати current_price у frontmatter analysis-файлу: `current_price_at_analysis: X.XXXX`
3. Усі рівні (entry/SL/TP) — **в межах ±5% від current_price**
4. Якщо план уже згенеровано і перевищує threshold → **видалити та регенерувати**

**Чому це блокувальне правило:**
- 2026-04-24: 3/10 планів (USDCHF/XAGUSD/US500) мали entry на хибному масштабі (1000+ pips off)
- Workflow генерування на основі screenshots без верифікації → systematic failure

**Винятки:** немає.

---

## 🟥 Правило 2 — BE@2R Mandatory + TradingView Alert

**Відразу після відкриття позиції** (через `replay_trade` або реальне виконання):

```python
# Calculate BE level (2R from entry)
be_level = entry + 2 * (entry - sl)  # for LONG
# or: be_level = entry - 2 * (sl - entry)  # for SHORT

# Auto-create alert
mcp__tradingview__alert_create(
    symbol=symbol,
    price=be_level,
    message=f"BE@2R for {symbol} — move SL to entry NOW",
    condition="crosses"
)
```

**При спрацюванні alert:**
- SL → BE (entry price) безумовно
- НЕ обговорюємо, не аналізуємо «чи варто», просто переносимо

**Партійна фіксація:**
- MFE = 1:2 → SL→BE
- MFE = 1:3 → fix 30% позиції
- MFE = 1:4+ → fix 50%, runner на 1:5+

**Чому це блокувальне правило:**
- GER40 04-23: MFE 7.47R → SL hit → −1R замість +3R+
- GER40 04-24: MFE 5.78R → SL hit → −1R замість +2.5R+
- 2 дні поспіль той самий інструмент → **~5-7R втрачено**
- Правило існувало, але виконувалось «вручну» = не виконувалось

**Винятки:** немає.

---

## 🟧 Правило 3 — Bias Re-validation на NY Open (13:55 UTC)

**Тригер:** автоматичний alert на 13:55 UTC (5 хв до NY open).

**Checklist re-validation:**
```
1. chart_set_timeframe("60") + chart_get_state()
2. Перевірити структуру H1 vs ранковий bias:
   - Bias був Bullish? → Перевірити чи немає LH (lower high) проти bias
   - Bias був Bearish? → Перевірити чи немає HL (higher low) проти bias
3. quote_get("DXY") — порівняти з ранковим напрямком
4. Якщо ChoCH/MSS проти bias на H1 → анулювати pending orders
```

**Дії за результатами:**
| Стан | Дія |
|------|-----|
| Bias підтверджено | Continue з планом |
| H1 structure broken | Cancel pending orders, спостерігати |
| DXY reversed | Re-run TDA для USD-pairs |
| Already in position | Tighten SL до BE або partial close 50% |

**Чому це правило:**
- 2026-04-24: 6 з 7 валідних позицій змінили долю саме о 14:00 UTC
- 2026-04-23: NY open також був точкою реверсу для US500
- 2026-04-22: те саме (London Lunch reversal)
- **Третій день поспіль** — це не випадковість, це pattern

---

## 🟧 Правило 4 — Reversal Day Detection (Pre-London 06:00 UTC)

**Тригер:** перед London open (06:00 UTC) — додатковий перевірочний сканер.

**Logic:**
```python
yesterday_retro = read_daily_retro(today - 1)
trend_day = (yesterday_retro.tp_hit_count >= 3 
             and yesterday_retro.usd_direction in ["strong", "weak"])

if trend_day:
    # Run reversal detection
    for symbol in watchlist:
        chart_set_timeframe("60")
        check_choch_against_yesterday_bias()
        if choch_detected:
            mark_for_bias_flip(symbol)
```

**Дії:**
- Якщо вчора був trend day (3+ TP_HIT в одну сторону USD):
  - **НЕ екстраполювати** автоматично сьогоднішні плани
  - Зранку додатковий H1 check на 50% watchlist
  - Якщо ChoCH присутній на 30%+ інструментів → **flip bias day**
- Якщо вчора був mixed/loss day → стандартний workflow

**Чому це правило:**
- 04-23: trend day USD strong → +11.1R
- 04-24: повний reversal → −3R
- Якби 04-24 розпізнали reversal зранку (sweep на GBPUSD 06:30 UTC, USD weak signals на DXY) → могли б flip bias і отримати +day замість −

---

## 🟨 Правило 5 — Entry Layer 3 (Continuation/Breakout)

Окрім традиційних 2 entries (aggressive OTE 70%, safe OTE 61%) — **обов'язковий третій layer**:

**Continuation entry** активується коли:
- На open ціна вже за межами OTE зони (>50 pips від aggressive entry для FX, >100 pts для indices)
- HTF bias підтверджений
- Local M15 ChoCH у напрямку bias

**Setup:**
```
Entry = breakout локального H/L поточного дня + 5 pips
SL = за останній M15 swing (зазвичай 20-40 pips)
TP1 = 1:2 RR
TP2 = HTF target (як у safe entry)
Розмір: 0.5× стандартного (бо tight SL)
```

**Чому це правило:**
- 2026-04-24 US100: entry 26780, day low 26876 → entry never triggered, +357 pts втрачено
- 2026-04-23 ще декілька кейсів того ж типу
- Continuation entry зловив би 70-80% руху замість 0%

---

## 📋 Combined Pre-Analysis Checklist

Перед генеруванням TDA для кожного символу:

- [ ] **R0**: чи зараз є відкрита позиція? Якщо немає → явно це сказати в звіті
- [ ] **R0**: TDA для intraday entry (закриття до hard_close), не для swing/overnight?
- [ ] **R1**: `quote_get(symbol)` → current_price збережено?
- [ ] **R1**: planned levels у межах ±5% від current?
- [ ] **R4**: вчора був trend day? Якщо так → reversal scan виконано?
- [ ] Standard SMC checklist (HTF bias, KZ, sessions) ✓
- [ ] **R5**: 3 entry layers визначено (aggressive + safe + continuation)?

## 📋 Combined Post-Entry Checklist

Відразу після `replay_trade` / реального входу:

- [ ] **R0**: hard_close час встановлено (alert на 20:00/21:00 UTC або 19:00 UTC у п'ятницю)?
- [ ] **R2**: `alert_create` на BE@2R рівень?
- [ ] **R3**: alert на 13:55 UTC для bias re-validation?
- [ ] Risk USD = 1% від депозиту?
- [ ] Recorded в Journal?

## 📋 Status Reporting Checklist (R0)

При будь-якому згадуванні позицій / P&L / ретро:

- [ ] Перевірив реальний стан: відкрита / закрита / немає?
- [ ] Якщо немає позиції — **явно** написав «позицій немає»?
- [ ] Розрізнив plan (рівні готові) / active (відкрита) / closed (зафіксована)?
- [ ] Не вигадав P&L там де угоди не було?

---

## 🔗 Інтеграція в системі

**Цей файл — джерело істини для трейдинг-правил.** Усі агенти/сесії що працюють з ринком повинні:

1. **Прочитати цей файл першим** перед будь-яким трейдинг-завданням
2. Слідувати precedence: ці правила **ОВЕРРАЙДЯТЬ** будь-які CLAUDE.md trading-instructions
3. Якщо правило конфліктує з instruction — правило виграє, instruction треба оновити

**Місце:** `~/MyVault/20-Trading/Strategies/RULES.md`
**Reference у CLAUDE.md проекту:** `~/AI/Projects/Trading/CLAUDE.md` (секція Trading Rules)

---

## 📊 Історія оновлень

| Версія | Дата | Зміна | Тригер |
|--------|------|-------|--------|
| 1.0 | 2026-04-24 | Правила з retro 04-23 (SL=1.5×ATR, TP≤0.7×Daily ATR, layered entries) | Daily Retro 04-23 |
| 2.0 | 2026-04-26 | Додано **Pre-Flight Price Check** (R1) як блокувальне; **BE@2R + alert** (R2) автоматичне; **NY Re-validation** (R3); **Reversal Day Detection** (R4); **Continuation Entry Layer** (R5) | Daily Retro 04-24 (3 INVALID плани, GER40 повтор, NY reversal pattern) |
| 2.1 | 2026-04-26 | Додано **R0: INTRADAY ONLY** (foundational) — заборона overnight, hard_close часи, **обов'язкова чесна звітність про відсутність позиції** (не вигадувати) | Уточнення від користувача |

## 🔗 Пов'язані ретро
- [[../Retro/2026-04-23/_DAILY-RETRO|Daily Retro 04-23]] — +11.1R, базовий набір правил
- [[../Retro/2026-04-24/_DAILY-RETRO|Daily Retro 04-24]] — −3R, виявлено 3 INVALID плани, BE rule не enforced
