# 💻 Agent-Claude-Code

**Claude Code CLI агент**

---

## 📋 Інформація

- **Назва**: Claude-Code (CLI tool)
- **Мета**: Кодування, развитие, автоматизація через терміна
- **Платформа**: Claude Code CLI
- **Статус**: Ready for setup

---

## 🧠 Skills

Навички для Claude Code:

| Skill | Папка | Назначення |
|-------|-------|-----------|
| CLI Automation | cli-automation/ | Автоматизація команд |
| Code Generation | code-generation/ | Генерація коду |
| Project Setup | project-setup/ | Ініціалізація проектів |
| Obsidian Integration | (додайте) | Запис в Obsidian через AGENT-PROMPT |

---

## 📦 MCP Серверів

| Сервер | Файл | Назначение |
|--------|------|-----------|
| Shell Executor | shell-executor.py | Виконання shell команд |
| Git Integration | git-integration.js | Робота з Git |

---

## ⚙️ Конфігурація

**Файл**: `config/settings.json`

```json
{
  "name": "Claude-Code",
  "type": "cli",
  "version": "2026-04-19",
  "skills_enabled": [
    "cli-automation",
    "code-generation"
  ],
  "mcp_servers": [
    "shell-executor",
    "git-integration"
  ],
  "features": {
    "vault_integration": "manual",
    "documentation": "auto"
  }
}
```

---

## 🔄 Як працює

1. **Запуск**: `claude code [command]`
2. **Виконання**: Claude Code виконує задачу
3. **Запис в Obsidian**:
   - ⚠️ Потребує вручної: передайте агенту `~/MyVault/AGENT-PROMPT.md`
   - Агент прочитає правила
   - На кінець сесії напиші файл в Obsidian

---

## 📝 Як використовувати

### Запуск з основного Claude

```bash
# В терміналі Claude Code передайте агенту:

"Прочитай файл: ~/MyVault/AGENT-PROMPT.md

Це інструкції як записувати сесії в Obsidian vault.
Дотримуйся цих правил для цього проекту.

На кінець сесії напиши файл у:
~/MyVault/10-Work/Projects/[назва]/sessions/YYYY-MM-DD-*.md"
```

### Додавання нового skill

```bash
# 1. Копіюйте шаблон
cp -r ../shared/templates/skill-template skills/new-skill

# 2. Напишіть SKILL.md для CLI

# 3. Напишіть скрипт
# (Обов'язково сумісний з Claude Code)

# 4. Оновіть settings.json
```

---

## 🔗 Інтеграція з основним Claude

### Як отримати автоматичні записи

**Крок 1**: Передайте цьому агенту файл `AGENT-PROMPT.md`
```bash
claude read ~/MyVault/AGENT-PROMPT.md
```

**Крок 2**: На кінець сесії скажіть агенту:
```bash
"Запиши результати в Obsidian за правилами з CLAUDE-RULES.md
Папка: ~/MyVault/10-Work/Projects/[project-name]/sessions/"
```

**Крок 3**: Агент напише файл автоматично

---

## 📚 Структура папок

```
Agent-Claude-Code/
├── README.md              ← Цей файл
├── skills/
│   ├── cli-automation/
│   ├── code-generation/
│   └── [додавайте]
├── mcp/
│   ├── shell-executor.py
│   ├── git-integration.js
│   └── config.json
└── config/
    └── settings.json
```

---

## 🎯 Приклади

### Приклад 1: Запуск проекту

```bash
claude code
# В Claude Code скажіть:
"Ініціалізуй новий Python проект для API server.

Після цього запиши в Obsidian:
- Які були кроки
- Яку структуру створив
- Які залежності встановив

Файл: ~/MyVault/10-Work/Projects/api-server/sessions/YYYY-MM-DD-init.md"
```

### Приклад 2: Написання коду

```bash
claude code
# Скажіть:
"Напиши Flask API endpoint для користувачів.

Потім:
- Запиши в Obsidian як зробив
- Яких рішень прийняв
- Які використав libraries

За схемою: ~/MyVault/CLAUDE-RULES.md"
```

---

## ⚠️ Важливо

### Це НЕ автоматичний запис

На відміну від Claude (Cowork), Claude Code **НЕ пише автоматично** в Obsidian.

**Потрібна вручна команда** на кінець сесії:
```
"Запиши все в Obsidian за правилами"
```

### Як це виправити?

1. **Варіант 1**: Завжди просіть агента писати (вручну)
2. **Варіант 2**: Напишіть claude-code-hook.py (автоматичний)
3. **Варіант 3**: Передайте основному Claude (буде автоматично)

---

## 📌 Статус

- ✅ Папка структурована
- ✅ Config готовий
- ⏳ Skills можуть додаватись
- ⏳ MCP серверів можуть додаватись
- ⚠️ Запис в Obsidian потребує ручної команди

---

**Версія**: 2026-04-19  
**Статус**: Ready for usage (manual Obsidian logging)
