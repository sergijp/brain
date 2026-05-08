---
title: "Trading Skills — README"
date: 2026-05-08
tags: [trading, agent, skills, infra]
category: agent
status: active
aliases: ["trading-skills", "skills-readme"]
pinecone_indexed: false
---

# Trading Skills — інфраструктура

Цей каталог — **source of truth** для трейдинг-skills. Кожен skill = окрема папка з `SKILL.md` всередині.

## Активні skills

| Папка | Тригери | Призначення |
|-------|---------|-------------|
| `dixie/` | `/dixie`, `/діксі`, "що на ринку?", "розбери [PAIR]" | Dixie — трейдер з 20р досвіду, SMC + Price Action на H1/M15 |
| `kassandra/` | `/kassandra`, `/касандра`, авто-виклик з Dixie | Kassandra — критик/CRO, debate з Dixie до convergence (max 3 раунди) |
| `tda-bias/` | викликається з dixie | Базовий bias-аналіз (W/D/H4) перед screenshots |
| `tda-screenshot/` | `/tda-screenshot`, "зроби скрін" | Скріни TV для Top-Down Analysis (W/D/H4/H1/M15/M5) |
| `tv-position/` | `/tv-position`, `/long`, `/short`, "постав лонг X сл Y тп Z" | Малює native Long/Short Position drawing у TV через MCP |
| `tv-levels/` | (внутрішнє делегування) | Рівні підтримки/опору |

## Делегування

```
dixie → tda-bias → tda-screenshot → kassandra (debate) → tv-position → retro у vault
```

## Стек

- **TradingView MCP** (78 інструментів) — основний канал; reference у [[60-Agents/shared/tradingview-mcp-reference]]
- TradingView Desktop з CDP
- **НЕ** Finnhub (deprecated)

## Critical: симлінки до Claude/Gemini

Skills мають бути доступні через CLI Claude/Gemini. Перевір розташування:

| CLI | Очікуваний шлях |
|-----|-----------------|
| Claude Code | `~/.claude/skills/<name>/SKILL.md` |
| Gemini | `~/.gemini/skills/<name>/SKILL.md` |

### Перевірити стан симлінків

```bash
ls -la ~/.claude/skills/ | grep -E "dixie|kassandra|tda-bias|tda-screenshot|tv-position|tv-levels"
ls -la ~/.gemini/skills/ | grep -E "dixie|kassandra|tda-bias|tda-screenshot|tv-position|tv-levels"
```

> **Поточний стан 2026-05-08:** `~/.claude/skills/` **не містить** трейдинг-symlinks (присутні лише `notebooklm` та `_disabled_gsd`). Якщо symlinks потрібні для активації через CLI — треба створити заново:

```bash
for s in dixie kassandra tda-bias tda-screenshot tv-position tv-levels; do
  ln -sf "$HOME/MyVault/20-Trading/skills/$s" "$HOME/.claude/skills/$s"
  ln -sf "$HOME/MyVault/20-Trading/skills/$s" "$HOME/.gemini/skills/$s"
done
```

> **⚠ ПОПЕРЕДЖЕННЯ:** не перейменовуй папки skills у vault без оновлення симлінків — CLI-активація через `/dixie` тощо просто перестане працювати без жодного помітного попередження.

## Hard rules (з SKILL.md Dixie)

- Sync clock first
- Memory recall before analysis
- Debate з Kassandra обов'язковий
- Risk max 1% на угоду
- RR min 1:2 на TP2
- Не входити раніше 09:00 Kyiv
- Після 3 збиткових угод за тиждень — стоп

## Vault paths для трейдингу

- `~/MyVault/20-Trading/Analysis/<date>/<PAIR>-analysis.md` — поточний аналіз
- `~/MyVault/20-Trading/Journal/<date>-trading-session.md` — щоденник
- `~/MyVault/20-Trading/Retro/<YYYY-MM-DD>-retro.md` — ретро
- `~/AI/Projects/Trading/CLAUDE.md` — project rules

## Пов'язані

- [[60-Agents/shared/tradingview-mcp-reference]] — повний MCP-довідник
- [[../../CLAUDE-RULES]] — TDA Standard + Position Setup
- Project rules для AI/Trading: `~/AI/Projects/Trading/CLAUDE.md`
