---
title: "TradingView MCP — Pine Script Trade Plan + Obsidian Memory Setup"
date: 2026-04-21
tags: [work, session, tradingview, mcp, pine-script, obsidian, memory]
category: work
project: tradingview-mcp
status: completed
pinecone_indexed: false
---

## 🎯 Мета сесії
1. Знайти найкращий спосіб малювати Trade Plan на TradingView графіку через MCP
2. Налаштувати глобальну систему пам'яті (Obsidian vault) для Claude

## ✅ Виконано

### Trade Plan на графіку — Pine Script (Варіант B)
- Протестовано підходи: draw_shape → native TV Long Position tool → Pine Script
- **Обраний підхід**: `pine_set_source` + `pine_smart_compile` + клік "Добавить на график"
- Pine Script v6 (v5 deprecated) — шаблон із boxes + labels готовий

### Координати UI (verified через DOM query)
- **"Добавить на график"** кнопка: `x=2400, y=79` (title="Добавить на график")
- **Pine Editor** кнопка (відкрити): `x=2548, y=1290`
- Pine Editor відкривається **знизу**, не в правій панелі

### Налаштування глобальної пам'яті
- Прочитано `~/MyVault/AGENT-PROMPT.md`, `CLAUDE-RULES.md`, `CLAUDE-SETUP.md`
- Створено `~/.claude/CLAUDE.md` з правилом: "запиши в пам'ять" → писати в Obsidian vault
- Оновлено `~/AI/Projects/Trading/CLAUDE.md` з виправленими координатами

## 🔑 Важливі рішення (ADR)

| Рішення | Причина | Альтернатива |
|---------|---------|-------------|
| Pine Script для Trade Plan | Повний контроль над рівнями, розрахунки RR/pips/P&L автоматичні | Native TV Long Position tool — не автоматизується через CDP |
| `draw_shape` не використовувати для Trade Plan | Підтримує тільки 5 базових форм, немає callout/annotation | Використовувати тільки для простих ліній |
| Obsidian vault як пам'ять | Структурована, searchable, з YAML frontmatter | CLAUDE.md — тільки для технічних інструкцій |

## 🐛 Проблеми й як вирішили

### Баг 1: pine_smart_compile повертає study_added: false
- **Причина**: Компіляція проходить, але індикатор не додається на графік автоматично
- **Вирішення**: Після compile клікнути `ui_mouse_click(x=2400, y=79)`
- **Верифікація**: `chart_get_state()` → перевірити "Trade Plan" в `studies[]`

### Баг 2: Невірні координати кнопки "Добавить на график"
- **Старі**: x=2383, y=62 — не спрацьовували
- **Нові (verified)**: x=2400, y=79 — знайдено через DOM query `title="Добавить на график"`

### Баг 3: Pine Script v5 deprecated
- **Причина**: TradingView вимагає v6
- **Вирішення**: Замінити `//@version=5` на `//@version=6`

### Баг 4: Права панель — не Pine Editor
- **Контекст**: В скріншотах права панель виглядала як Pine Editor
- **Реальність**: Це інший UI (scripts/ideas panel)
- **Pine Editor**: Відкривається знизу, кнопка y≈1290

## 📎 Артефакти

### Pine Script шаблон (Trade Plan)
```pine
//@version=6
indicator("Trade Plan — [SYMBOL] [DIRECTION]", overlay=true, max_boxes_count=10, max_labels_count=20, max_lines_count=10)

entry = input.float(0.0, "Entry",     step=0.00001)
sl    = input.float(0.0, "Stop Loss", step=0.00001)
tp1   = input.float(0.0, "TP1",       step=0.00001)
tp2   = input.float(0.0, "TP2",       step=0.00001)
tp3   = input.float(0.0, "TP3",       step=0.00001)
lots  = input.float(0.0, "Lot Size",  step=0.01)

risk_pips = math.round((entry - sl)    * 10000, 1)
tp1_pips  = math.round((tp1   - entry) * 10000, 1)
...
if barstate.islast
    t1 = bar_index - 3
    t2 = bar_index + 80
    box.new(...)   // Risk zone (red)
    box.new(...)   // TP1 zone (green)
    box.new(...)   // TP2 zone (green darker)
    line.new(...)  // TP3 dashed line
    label.new(...) // SL / Entry / TP1 / TP2 / TP3 labels
```

### Workflow "Add to chart"
```
1. pine_set_source(source=PINE_CODE)
2. pine_smart_compile()
3. Якщо study_added: false → ui_mouse_click(x=2400, y=79)
4. chart_get_state() → перевірити studies[]
```

### Конфігураційні файли
- `~/.claude/CLAUDE.md` — глобальні правила (Obsidian memory)
- `~/AI/Projects/Trading/CLAUDE.md` — правила для Trading проекту
- `~/tradingview-mcp-jackson/rules.json` — торгова стратегія SMC

## 🔗 Пов'язані нотатки
- [[10-Work/Projects/tradingview-mcp/sessions/2026-04-21-tradingview-mcp-tools-reference]]
- [[20-Trading/Journal/2026-04-21-trading-session]]
