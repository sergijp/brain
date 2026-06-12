---
title: "Backtest Trade Journal — YAML Template"
date: 2026-04-22
tags: [trading, backtest, template, journal, smc, v2]
category: trading
status: template
pinecone_indexed: false
---

# 📝 Backtest Trade Template

**Ім'я файлу:** `20-Trading/Backtest/trades/YYYY-MM-DD-NN-[pair]-[model].md`
Приклад: `2026-04-22-01-EURUSD-inner-fvg.md`

**Заповнюється до входу** (секції Setup-Entry) і після виходу (Exit-Review). Скопіюй блок нижче.

---

## Шаблон (copy-paste)

```yaml
---
# === IDENTITY ===
trade_id: 2026-04-22-01
date: 2026-04-22
pair: EURUSD
session: London        # Asian | London | NY | Overlap
model: inner-fvg-bos   # classic-bos-retest | delayed-entry | inner-fvg-bos | amd | breaker | silver-bullet | london-reversal
direction: short       # long | short
scoring_profile: Standard   # Conservative | Standard | Aggressive
grade: A               # A (1% risk) | B (0.5%) | C (skipped)

# === BIAS & CONTEXT ===
htf_bias: bearish      # H4/D напрямок
htf_bias_reason: "H4 BOS вниз + Weekly Open нижче ціни"
key_levels:
  - "Weekly Open 1.0850"
  - "PWL 1.0820"
  - "Asian High 1.0875 (BSL)"
poi_used: "H1 OB 1.0870-1.0878"
dxy_confluence: bullish   # bullish | bearish | neutral — має підтверджувати direction
dxy_screenshot: "screenshots/2026-04-22-dxy.png"
news_window: clear     # clear | red-folder-within-30min (блокуюче)

# === ENTRY ===
entry_time_utc: "2026-04-22T08:15:00Z"
entry_price: 1.08760
sl_price: 1.08920
tp1_price: 1.08600
tp2_price: 1.08440
risk_pips: 16
rr_tp1: 1.0
rr_tp2: 2.0
lot_size: 0.62
risk_usd: 100       # 1% від $10k
cost_R: -0.1        # spread + commission у R

# === CONFLUENCE (scoring) ===
confluence_score: 8
confluence_items:
  - "H4 bias bearish (+2)"
  - "Sweep Asian High (+2)"
  - "M15 BOS down (+2)"
  - "Inner FVG retest (+1)"
  - "DXY bullish confirm (+1)"
# 6-point gate (pre-trade checklist)
gate_bias: pass
gate_poi: pass
gate_sweep: pass
gate_bos: pass
gate_rr: pass          # ≥1:2
gate_psychology: pass  # AM I CALM? → Calm

# === MANAGEMENT ===
trail_events:
  - { time: "08:47Z", action: "TP1 hit → SL to BE (1.08760)" }
  - { time: "09:32Z", action: "TP2 partial at 1.08500 (manual)" }
final_exit_price: 1.08500
final_exit_time_utc: "2026-04-22T09:32:00Z"
final_exit_reason: "TP2 partial + runner trailed 15m swing"

# === RESULT ===
outcome: win           # win | loss | be | skip
r_result: 2.3          # у R (враховано cost_R)
usd_result: 230
notes_short: "Чистий Inner FVG від H1 OB, ніяких hesitation на BOS"

# === PSYCHOLOGY & ADHERENCE ===
emotion_pre: Calm      # Calm | Tilted | Angry | Manic | Impatient
emotion_during: Calm
rule_adherence: full   # full | partial | broken
adherence_deviations: []   # якщо partial/broken — список відхилень

# === REVIEW ===
lessons: "Inner FVG модель дає tighter SL vs broad OB retest — підтверджено"
screenshots:
  - "screenshots/2026-04-22-h1-setup.png"
  - "screenshots/2026-04-22-m15-entry.png"
  - "screenshots/2026-04-22-exit.png"
mistakes: []           # якщо є — короткий опис
---
```

---

## Контекст трейду (вільна форма)

### Setup narrative
Опиши логіку: чому POI, як чекав sweep, що тригернуло вхід, що робив з управлінням. 3-5 речень достатньо.

### Alternate scenario / invalidation
Що було би якби setup не спрацював? Який рівень / подія інвалідувала би бік?

### Screenshots

---

## 📊 Аналітичні поля — для Dataview

Dashboard `[[Dashboards/live-stats]]` агрегує по цих YAML-полях:
- `pair`, `model`, `session`, `grade`, `outcome`, `r_result`, `rule_adherence`, `emotion_pre`, `scoring_profile`, `dxy_confluence`

**Обов'язкові поля** (без них трейд не потрапить у статистику):
`trade_id`, `pair`, `model`, `direction`, `grade`, `outcome`, `r_result`, `rule_adherence`

---

## 🔗 Пов'язані

- [[Backtest/README]] — 4-етапний процес
- [[Strategies/smc-playbook-v2]] — models + scoring
- [[Checklists/pre-trade-checklist]] — 6-point gate (заповнення полів `gate_*`)
