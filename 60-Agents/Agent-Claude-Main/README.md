# 🤖 Agent-Claude-Main

**Основний Claude агент у Cowork режимі**

---

## 📋 Інформація

- **Назва**: Claude-Main (Cowork)
- **Мета**: Основний AI агент для роботи з проектами, трейдингом, навчанням
- **Платформа**: Cowork desktop app
- **Статус**: Active

---

## 🧠 Skills

Основні навички цього агента:

| Skill | Папка | Назначення |
|-------|-------|-----------|
| Obsidian Session Logger | obsidian-session-logger/ | Автоматичний запис сесій |
| Project Analyzer | (додайте) | Аналіз проектів |
| Code Reviewer | (додайте) | Перегляд коду |

---

## 📦 MCP Серверів

| Сервер | Файл | Назначение |
|--------|------|-----------|
| Obsidian Connector | obsidian-connector.py | Запис/читання Obsidian |
| Vault API | vault-api.py | API для роботи з vault |

---

## ⚙️ Конфігурація

**Файл**: `config/settings.json`

```json
{
  "name": "Claude-Main",
  "model": "claude-opus-4-6",
  "version": "2026-04-19",
  "skills_enabled": [
    "obsidian-session-logger",
    "project-analyzer"
  ],
  "mcp_servers": [
    "obsidian-connector",
    "vault-api"
  ],
  "features": {
    "auto_logging": true,
    "graph_integration": true,
    "vault_sync": true
  }
}
```

---

## 🔄 Як працює

1. **На початку сесії**: Агент готовий до роботи
2. **Під час роботи**: Виконує завдання користувача
3. **На кінець сесії**: 
   - Читає чим займався
   - Записує в Obsidian автоматично (skill: obsidian-session-logger)
   - Повідомляє користувача

---

## 📝 Як додати новий skill

```bash
# 1. Копіюйте шаблон
cp -r ../shared/templates/skill-template skills/new-skill

# 2. Напишіть SKILL.md
nano skills/new-skill/SKILL.md

# 3. Напишіть код у scripts/
nano skills/new-skill/scripts/main.py

# 4. Оновіть config/settings.json
# Додайте "new-skill" у skills_enabled

# 5. Готово!
```

---

## 🔧 Запуск MCP серверів

```bash
# Запустити Obsidian connector
cd mcp
python obsidian-connector.py

# В іншому терміналі запустити Vault API
python vault-api.py
```

---

## 📚 Структура папок

```
Agent-Claude-Main/
├── README.md              ← Цей файл
├── skills/
│   ├── obsidian-session-logger/
│   │   ├── SKILL.md
│   │   ├── scripts/
│   │   └── references/
│   └── [додавайте більше]
├── mcp/
│   ├── obsidian-connector.py
│   ├── vault-api.py
│   ├── config.json
│   └── README.md
└── config/
    ├── settings.json
    └── hooks.json
```

---

## 🎯 Приклади використання

### Додавання skill для аналізу проектів

```bash
# 1. Копіюйте шаблон
cp -r ../shared/templates/skill-template skills/project-analyzer

# 2. Напишіть SKILL.md з описом

# 3. Напишіть скрипт análizy.py

# 4. Додайте в settings.json:
# "skills_enabled": ["obsidian-session-logger", "project-analyzer"]
```

### Додавання MCP для доступу до GitHub

```bash
# 1. Створіть github-api.py в mcp/

# 2. Напишіть MCP сервер для GitHub API

# 3. Додайте в mcp/config.json:
# "github": {"type": "mcp", "file": "github-api.py"}
```

---

## 📌 Статус

- ✅ Основна структура готова
- ✅ Obsidian connector готовий
- ⏳ Додатків skills можуть додаватись
- ⏳ Додатків MCP серверів можуть додаватись

---

**Версія**: 2026-04-19  
**Статус**: Active & Ready for expansion
