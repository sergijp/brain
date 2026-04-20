# 🤖 60-Agents

**Агенти, Skills, MCP серверів, конфігурації**

---

## 📋 Призначення

Централізоване сховище для управління AI агентами та їхніми інструментами:
- 🧠 **Agent-Claude-Main/** — основний Claude (Cowork)
- 💻 **Agent-Claude-Code/** — Claude Code
- 🔧 **Agent-[Custom]/** — інші агенти
- 📦 **shared/** — спільні ресурси

---

## 📁 Структура

```
60-Agents/
│
├── README.md                         ← Цей файл (карта)
│
├── Agent-Claude-Main/                ← Основний Claude (Cowork)
│   ├── README.md                     ← Опис цього агента
│   ├── skills/
│   │   ├── skill-obsidian-logger/    ← Skill для запису в Obsidian
│   │   │   ├── SKILL.md
│   │   │   ├── scripts/
│   │   │   │   └── vault_writer.py
│   │   │   └── references/
│   │   ├── skill-project-analyzer/
│   │   │   ├── SKILL.md
│   │   │   └── scripts/
│   │   └── [інші skills]
│   │
│   ├── mcp/
│   │   ├── obsidian-mcp.py          ← MCP сервер для Obsidian
│   │   ├── trading-mcp.js            ← MCP для трейдингу
│   │   ├── database-mcp.py
│   │   └── config.json
│   │
│   └── config/
│       ├── settings.json             ← Налаштування агента
│       └── hooks.json                ← Hooks для автоматизму
│
├── Agent-Claude-Code/                ← Claude Code агент
│   ├── README.md
│   ├── skills/
│   │   ├── cli-automation/
│   │   └── code-generation/
│   ├── mcp/
│   │   └── [MCP для CLI]
│   └── config/
│       └── settings.json
│
├── Agent-Nadolo-Trading/             ← Приклад: Trading агент
│   ├── README.md
│   ├── skills/
│   │   ├── market-analysis/
│   │   ├── risk-calculator/
│   │   └── trade-logger/
│   ├── mcp/
│   │   ├── finnhub-mcp.py            ← Для ринкових даних
│   │   ├── broker-api-mcp.js         ← Для брокера
│   │   └── config.json
│   └── config/
│
├── Agent-Research-Bot/               ← Приклад: Research агент
│   ├── README.md
│   ├── skills/
│   │   ├── web-research/
│   │   ├── paper-analyzer/
│   │   └── summary-generator/
│   ├── mcp/
│   │   ├── arxiv-mcp.py
│   │   ├── google-scholar-mcp.js
│   │   └── config.json
│   └── config/
│
└── shared/                           ← Спільні ресурси
    ├── base-skills/                  ← Базові skills для всіх
    │   ├── obsidian-integration.md
    │   ├── logging-patterns.md
    │   └── error-handling.md
    │
    ├── common-mcp/                   ← Загальні MCP серверів
    │   ├── base-mcp-template.py
    │   ├── common-connectors.js
    │   └── config-template.json
    │
    └── templates/                    ← Шаблони для нових агентів
        ├── agent-template/
        │   ├── README.md
        │   ├── skills/
        │   ├── mcp/
        │   └── config/
        └── skill-template/
            ├── SKILL.md
            └── scripts/
```

---

## 🤖 Agent Папки

### Основна структура для агента:

Кожна папка агента `Agent-[NAME]/` має три компоненти:

#### 1️⃣ **skills/** — Навички агента

```
skills/
├── skill-name-1/
│   ├── SKILL.md                    ← Опис & інструкції
│   ├── scripts/
│   │   ├── main.py                 ← Основний скрипт
│   │   ├── utils.py
│   │   └── requirements.txt
│   ├── references/
│   │   ├── documentation.md
│   │   └── examples.json
│   └── evals/                      ← Тести (опційно)
│       └── evals.json
│
└── skill-name-2/
    └── ...
```

**Що це:**
- SKILL.md — Інструкції як skill працює
- scripts/ — Код (Python, JavaScript, тощо)
- references/ — Документація, приклади
- evals/ — Тесты та метрики (опційно)

#### 2️⃣ **mcp/** — MCP Серверів

```
mcp/
├── server-name-1.py               ← MCP сервер (Python)
├── server-name-2.js               ← MCP сервер (Node.js)
├── server-name-3/                 ← Папка-сервер
│   ├── index.js
│   ├── package.json
│   └── src/
├── config.json                    ← Конфіг всіх серверів
└── README.md                      ← Інструкція по MCP
```

**Що це:**
- .py / .js файли — MCP серверед
- config.json — Налаштування (ключи, урлі, тощо)
- README.md — Як запустити, як використовувати

#### 3️⃣ **config/** — Конфігурація агента

```
config/
├── settings.json                  ← Налаштування агента
│   {
│     "name": "Claude-Main",
│     "model": "claude-opus-4-6",
│     "skills_enabled": [...],
│     "mcp_servers": [...]
│   }
│
└── hooks.json                     ← Hooks для автоматизму
    {
      "on_session_start": [...],
      "on_session_end": [...],
      "on_error": [...]
    }
```

---

## 📦 shared/ — Спільні ресурси

### base-skills/
Базові patterns для всіх skills:
```
base-skills/
├── obsidian-integration.md    ← Як інтегруватись з Obsidian
├── logging-patterns.md        ← Як писати логи
├── error-handling.md          ← Обробка помилок
└── api-integration.md         ← Як працювати з API
```

### common-mcp/
Шаблони та готові компоненти:
```
common-mcp/
├── base-mcp-template.py       ← Шаблон MCP сервера
├── common-connectors.js       ← Готові коннектори
├── auth-patterns.py           ← Автентифікація
└── config-template.json       ← Шаблон конфігу
```

### templates/
Для швидкого створення нових агентів:
```
templates/
├── agent-template/            ← Копіюйте це для нового агента
│   ├── README.md
│   ├── skills/
│   ├── mcp/
│   └── config/
│
└── skill-template/            ← Копіюйте для нового skill'я
    ├── SKILL.md
    ├── scripts/
    └── references/
```

---

## 📋 Приклад: Структура реального агента

### Agent-Claude-Main (Cowork)

```
Agent-Claude-Main/
│
├── README.md
│   Тут описуємо:
│   - Який це агент
│   - Які skills включені
│   - Які MCP серверів використовує
│   - Як налаштований
│
├── skills/
│   ├── obsidian-session-logger/
│   │   ├── SKILL.md
│   │   │   "На кінець сесії пишу в Obsidian vault"
│   │   ├── scripts/
│   │   │   ├── vault_writer.py (основний скрипт)
│   │   │   └── utils.py
│   │   └── references/
│   │       └── obsidian-schema.md
│   │
│   ├── project-analyzer/
│   │   ├── SKILL.md
│   │   ├── scripts/
│   │   │   ├── analyze.py
│   │   │   └── requirements.txt
│   │   └── references/
│   │       └── patterns.json
│   │
│   └── code-reviewer/
│       ├── SKILL.md
│       ├── scripts/
│       └── evals/
│           └── evals.json
│
├── mcp/
│   ├── obsidian-connector.py
│   │   "MCP для читання/запису Obsidian"
│   ├── vault-api.py
│   ├── config.json
│   └── README.md
│       - Как запустити MCP
│       - Какие endpoints
│       - Требования (Python 3.9+, etc)
│
└── config/
    ├── settings.json
    │   {
    │     "name": "Claude-Main",
    │     "model": "claude-opus-4-6",
    │     "version": "2026-04-19",
    │     "skills": ["obsidian-session-logger", "project-analyzer"],
    │     "mcp_servers": ["obsidian-connector", "vault-api"]
    │   }
    │
    └── hooks.json
        {
          "on_session_end": [
            {"action": "run_skill", "skill": "obsidian-session-logger"}
          ]
        }
```

---

## 🚀 Як використовувати

### Запуск MCP сервера

```bash
# Python MCP
cd 60-Agents/Agent-Claude-Main/mcp
python obsidian-connector.py

# Node.js MCP
npm install
npm start
```

### Додавання нового skills

```bash
# Копіюйте шаблон
cp -r 60-Agents/shared/templates/skill-template \
      60-Agents/Agent-Claude-Main/skills/new-skill

# Редагуйте
cd 60-Agents/Agent-Claude-Main/skills/new-skill
# Напишіть SKILL.md
# Напишіть scripts/
```

### Додавання нового агента

```bash
# Копіюйте шаблон
cp -r 60-Agents/shared/templates/agent-template \
      60-Agents/Agent-New-Name

# Налаштуйте
cd 60-Agents/Agent-New-Name
# Напишіть README.md
# Додайте skills/
# Додайте mcp/
# Налаштуйте config/
```

---

## 📊 Інтеграція з основною системою

### Зв'язок з 10-Work

Skills та MCP використовуються агентами для:
- Запису сесій в Obsidian (10-Work/Projects/...)
- Аналізу проектів
- Автоматизації робочих процесів

### Зв'язок з 20-Trading

Trading агенти можуть мати:
- Skills для аналізу пар
- MCP для підключення до брокерів
- Логування в 20-Trading/Journal

### Зв'язок з 30-Learning

Research агенти могуть мати:
- Skills для збору інформації
- MCP для доступу до наукових ресурсів
- Запис в 30-Learning/

---

## 🎯 Best Practices

✅ **ПИСАТИ**:
- SKILL.md з повними інструкціями
- README.md для агентів
- config.json для налаштувань
- Коментарі в коді

❌ **НЕ писати**:
- Неструктурований код
- Без документації
- Secret ключи в коді (використовуйте config!)

📌 **Організація**:
- Один skill = одна папка
- Один MCP сервер = один файл або папка
- Спільні ресурси в shared/
- Конфіг окремо від коду

---

## 📝 Приклад: Додавання нового агента

### Крок 1: Копіюйте шаблон

```bash
cp -r 60-Agents/shared/templates/agent-template \
      60-Agents/Agent-Trading-Analyzer
```

### Крок 2: Напишіть README

```markdown
# Agent-Trading-Analyzer

Спеціалізований агент для аналізу торгівельних пар.

## Skills:
- market-analyzer — аналіз пар
- risk-calculator — розрахунок ризику
- trade-logger — запис в 20-Trading/Journal

## MCP:
- finnhub-connector.py — дані з Finnhub
- broker-api.js — підключення до брокера
```

### Крок 3: Додайте skills

```bash
cp -r 60-Agents/shared/templates/skill-template \
      60-Agents/Agent-Trading-Analyzer/skills/market-analyzer

# Напишіть SKILL.md, scripts/, references/
```

### Крок 4: Додайте MCP

```bash
# Скопіюйте базовий шаблон
cp 60-Agents/shared/common-mcp/base-mcp-template.py \
   60-Agents/Agent-Trading-Analyzer/mcp/finnhub-connector.py

# Редагуйте
```

### Крок 5: Налаштуйте config

```json
{
  "name": "Trading-Analyzer",
  "skills": ["market-analyzer", "risk-calculator", "trade-logger"],
  "mcp_servers": ["finnhub-connector", "broker-api"]
}
```

---

## 📞 Контакт & Інформація

- **Власник**: Nadolo
- **Папка**: 60-Agents/
- **Версія**: 2026-04-19
- **Статус**: Template ready

---

**Структура готова! Закидайте сюди свої skills, агентів та MCP! 🚀**
