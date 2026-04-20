---
title: "Obsidian + AI System — налаштування і концепція"
date: 2026-04-19
tags: [work, obsidian, ai, pinecone, chromadb, ollama, trading, setup]
category: work
status: active
pinecone_indexed: false
---

## 💡 Про що

Налаштування персональної бази знань на базі Obsidian з AI-пошуком через ChromaDB + Ollama (безкоштовно і локально). Система охоплює роботу, програмування, трейдинг і навчання. Підтримує мульти-LLM підхід.

---

## 🏗 Архітектура системи

```
Obsidian Vault (~/MyVault)
        ↓
local_indexer.py — читає .md файли, генерує embeddings через Ollama
        ↓
ChromaDB (локально, ~/obsidian-ai/chroma_db)
        ↓
local_query.py — семантичний пошук → Claude / GPT / Ollama
```

---

## 📁 Структура Vault

```
~/MyVault/
├── 00-Inbox/          ← швидкі нотатки, Web Clipper
├── 10-Work/
│   └── Projects/      ← проекти, синхронізуються через vault-sync.py
├── 20-Trading/
│   ├── Journal/       ← денний журнал угод
│   ├── Analysis/      ← аналіз пар
│   └── Strategies/
├── 30-Learning/       ← книги, відео, статті
├── 40-Personal/
└── 50-Resources/
    └── Templates/     ← 7 шаблонів нотаток
```

---

## 🛠 Python проект (~/obsidian-ai/)

| Файл | Призначення |
|------|-------------|
| `local_indexer.py` | Індексація vault → ChromaDB через Ollama |
| `local_query.py` | Семантичний пошук + відповідь через LLM |
| `watcher.py` | Автоіндексація нових/змінених нотаток |
| `vault-sync.py` | Проект (Claude Code/Antigravity) → vault |
| `vault-pdf.py` | PDF/книги → нотатка у vault |
| `vault-youtube.py` | YouTube транскрипт → нотатка у vault |
| `trading_summary.py` | Тижневий звіт по трейдингу |

---

## 🆓 Безкоштовний стек

- **ChromaDB** — локальна vector DB (замість Pinecone)
- **Ollama + nomic-embed-text** — локальні embeddings (~270 MB)
- **Ollama + llama3** — локальний LLM для відповідей (~4.7 GB, опційно)
- Платиш тільки якщо використовуєш Claude/GPT для відповідей

---

## 📥 Потоки контенту → Vault

| Джерело | Інструмент | Куди |
|---------|-----------|------|
| Веб-сторінки | Obsidian Web Clipper (розширення) | 00-Inbox або тема |
| PDF / книги | `vault-pdf` alias | Learning або Trading |
| YouTube | `vault-yt` alias | Learning або Trading |
| Проекти | `vault-sync` + Claude Code Hook | 10-Work/Projects |
| Швидкі думки | `note "текст"` в терміналі | 00-Inbox |
| Трейдинг | `note-trading "текст"` | 20-Trading/Journal |
| Робота | `note-work "текст"` | 10-Work |
| Телефон | Obsidian Mobile | 00-Inbox |
| Чати/розмови | Вручну або "збережи в нотатку" | 00-Inbox |

---

## 📋 Шаблони нотаток (Templater, Ctrl+T)

| Шаблон | Коли використовувати |
|--------|---------------------|
| `tpl-inbox` | Швидка думка, ідея |
| `tpl-project` | Новий або існуючий проект |
| `tpl-bug` | Вирішена проблема в коді |
| `tpl-trading-journal` | Щоденно перед торгівлею |
| `tpl-trading-analysis` | Перед входом в угоду |
| `tpl-learning` | Книга, курс, відео, стаття |
| `tpl-meeting` | Зустріч або дзвінок |

---

## 🔄 Синхронізація проектів → Vault

`vault-sync.py` читає з проекту: `CLAUDE.md`, `README.md`, `docs/**/*.md` → LLM генерує структуровану нотатку → зберігає в `10-Work/Projects/{назва}/project-overview.md`.

**Claude Code Hook** (автозапуск після кожної сесії):
```json
// ~/.claude/settings.json
{
  "hooks": {
    "Stop": [{"matcher": "", "hooks": [{"type": "command",
      "command": "python ~/obsidian-ai/vault-sync.py --dest auto"}]}]
  }
}
```

---

## 💻 Основні команди (aliases)

```bash
# Пошук
ask-work "питання"          # пошук по робочих нотатках
ask-trading "питання"       # пошук по трейдингу
ask-all "питання"           # пошук по всьому vault
ask-local "питання"         # через локальний Ollama

# Індексація
reindex                     # переіндексувати весь vault

# Додавання контенту
note "текст"                # швидка нотатка → Inbox
note-trading "текст"        # → Trading/Journal
note-work "текст"           # → Work

# Синхронізація
vault-sync                  # проект → vault (з поточної папки)
vault-inbox                 # проект → Inbox

# PDF і YouTube
vault-pdf file.pdf          # PDF → vault
vault-yt "youtube url"      # відео → vault

# Звіти
trading-report              # тижневий аналіз трейдингу
```

---

## 🔌 Плагіни Obsidian

| Плагін | Навіщо |
|--------|--------|
| **Templater** | Інтерактивні шаблони з Ctrl+T (обов'язковий) |
| **Dataview** | SQL-запити по vault, живі таблиці статистики |
| **Tag Wrangler** | Управління тегами (перейменування, злиття) |
| **Calendar** | Навігація по датах, особливо для trading journal |
| **Web Clipper** | Зберігання веб-сторінок одним кліком |

---

## 🚀 Як зберігати розмови з AI

Після корисної розмови в будь-якому чаті (Cowork, ChatGPT, etc.):
- Сказати "збережи це в нотатку" → отримуєш готовий `.md` файл
- Або вручну: `note "ключові висновки з розмови"`
- Файл кидаєш у `~/MyVault/00-Inbox/` → watcher автоіндексує

---

## ⚙️ Налаштування (~/obsidian-ai/.env)

```env
OBSIDIAN_VAULT_PATH=~/MyVault
DEFAULT_LLM=local           # local | claude | gpt4 | gemini
DEFAULT_NAMESPACE=          # порожньо = всі namespace
ANTHROPIC_API_KEY=          # опційно
OPENAI_API_KEY=             # опційно
```

---

## 📦 Установка (одна команда)

```bash
chmod +x setup.sh && ./setup.sh
```

Потім вручну:
1. Obsidian → Open folder → `~/MyVault`
2. Встановити плагіни: Templater, Dataview, Tag Wrangler, Calendar
3. Templater → Template folder → `50-Resources/Templates`
4. Ollama: `ollama pull nomic-embed-text`
5. `source ~/.zshrc` → `reindex`
