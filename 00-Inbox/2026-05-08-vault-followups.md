---
title: "Vault — follow-ups після реорганізації 2026-05-08"
date: 2026-05-08
tags: [vault, followups, hygiene, infra]
category: inbox
status: active
aliases: ["vault-followups-2026-05-08"]
pinecone_indexed: false
---

# Vault — що ще потрібно зробити

Список залишкових задач після реорганізації пам'яті 2026-05-08. Не блокувальне, але до накопичення.

## 🔴 Критичне (раз і назавжди)

### 1. Створити симлінки trading skills
`~/.claude/skills/` і `~/.gemini/skills/` зараз **не містять** трейдинг-symlinks. Активація через `/dixie`, `/kassandra` тощо може не працювати через CLI.

```bash
for s in dixie kassandra tda-bias tda-screenshot tv-position tv-levels; do
  ln -sf "$HOME/MyVault/20-Trading/skills/$s" "$HOME/.claude/skills/$s"
  ln -sf "$HOME/MyVault/20-Trading/skills/$s" "$HOME/.gemini/skills/$s"
done
```

### 2. Перший git commit з новою convention

```bash
cd ~/MyVault
git add -A
git status
git commit -m "chore: 2026-05-08 vault docs/decisions skeleton + frontmatter standard"
```

Далі — усі коміти за форматом з `CLAUDE-RULES.md` (секція **Git Commit Convention**).

## 🟡 Структурні (до наступного циклу)

### 3. Pinecone-pipeline — рішення
`pinecone_indexed: false` — dead marker. Два варіанти:
- **Реалізувати** — Python-скрипт що бере файли з `pinecone_indexed: false`, відправляє в Pinecone, виставляє `true`. Потрібна Pinecone API key, embedding model (наприклад `text-embedding-3-small`).
- **Прибрати поле** — з `vault_writer.py` і шаблонів. Простіше, якщо векторний пошук не потрібен.

### 4. Привести існуючі sessions/ до нової taxonomy
`category: work` → `category: session`, додати `aliases: []`. Постепенно — при наступному торканні файлу. **Без масової міграції**.

### 5. Vault root INDEX.md
Перевірити, чи `~/MyVault/INDEX.md` згадує всі активні проекти + нові точки входу (`docs/INDEX`, `decisions/INDEX`). Якщо ні — додати.

### 6. Vault-doctor — script-валідатор (опційно)
Python-скрипт що:
- Перевіряє наявність `aliases`, `category` з закритого набору, `pinecone_indexed` у кожному `.md`.
- Шукає orphan wiki-links (`[[...]]` що ведуть у нікуди).
- Попереджає про `last_verified` старіше 90 днів.
- Шукає sessions без посилання на жоден ADR/doc.

Запускати раз на місяць як гігієнічна перевірка.

## 🟢 Quality of life (без термінів)

### 7. ADR-міграція зі старих session-нотаток
Сесії з `## Важливі рішення (ADR)` таблицями ще є — не переносити масово. **При наступному торканні** конкретної теми → винести ADR у `decisions/YYYY-MM-DD-<slug>.md` за шаблоном і поставити wiki-link із сесії. Поступово.

### 8. air-trans — додати ще арх-доки
В auto-memory `~/.claude/projects/-Users-serhiin-Data-Source-air-trans/memory/` ще є топіки без vault-doc:
- `ticket_checked_nullable_fix.md` — checked 3-стани (true/false/null), синхронізація з ticket_statuses.
- `vault_session_logging.md` / `vault_system_docs.md` — meta, можна не виносити (вже в global CLAUDE.md).

При наступній сесії на air-trans — створити `docs/ticket-checked-states.md` за шаблоном.

### 9. Auto-memory cleanup (опційно)
- Видалити `~/.claude/projects/-Users-serhiin-Data-Source-tmp/` — застаріле, дублює global CLAUDE.md.
- Видалити дублі feedback про Obsidian (`-Users-serhiin-Data-Source-3g/memory/feedback_obsidian_required.md`, `-Users-serhiin/memory/feedback_obsidian_always.md`) — правило вже в global.
- Перенести 6 trading-файлів з `-Users-serhiin/memory/` → `-Users-serhiin-AI/memory/` — щоб все trading-знання підтягувалось у будь-якій trading-сесії.
- Інші slug'и (`travy`, `vts`, `agent`) — окремою сесією переглянути на застарілість.

> Цього у поточному циклі **не робив**, бо користувач сказав "не забираючи зайвого". Залишається як свідомий вибір на майбутнє.

### 10. Tier-2 pointer'и в auto-memory — переписати під новий стандарт
Зараз arch-знання в auto-memory `project_*.md` — це повноцінні документи. Оптимально переписати їх у короткі (≤30 рядків) pointer'и виду:

```markdown
---
name: architecture_<topic>
description: ...
type: project | reference
last_verified: 2026-05-08
---
3-5 канонічних правил.

**Vault doc (source of truth):** `~/MyVault/10-Work/Projects/<p>/docs/<topic>.md`
**Файли коду:** `app/Services/...:42`
```

Оригінали тримати у vault docs (вже зроблено), pointer'и зменшити.

### 11. Bustrek — наповнити коли стартує
Зараз `~/MyVault/10-Work/Projects/bustrek/` має лише skeleton (`docs/INDEX.md`, `decisions/INDEX.md`, пуста `sessions/`). При першій сесії на проекті — створити `project-overview.md` за шаблоном `Project-Session.md` і перші arch-доки.

### 12. Шаблони — інтегрувати з Obsidian Templater
Поточні `templates/*.md` містять `{{date}}`, `{{project}}` — синтаксис Obsidian Templater plugin. Якщо плагін не встановлений — placeholder'и не замінюються автоматично, треба міняти руками. Перевірити плагіни Obsidian і налаштувати.

## Пов'язані

- [[../CLAUDE-RULES]] — оновлені правила (Frontmatter, Git Commit, Pinecone статус)
- [[../10-Work/Projects/buktrek/docs/INDEX]]
- [[../10-Work/Projects/3g/docs/INDEX]]
- [[../10-Work/Projects/air-trans/docs/INDEX]]
- [[../60-Agents/shared/tradingview-mcp-reference]]
- [[../20-Trading/skills/README]]
