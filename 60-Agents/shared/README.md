# 📦 shared/

**Спільні ресурси для всіх агентів**

---

## 📋 Це містить:

```
shared/
├── base-skills/        ← Best practices для skills
├── common-mcp/         ← Шаблони MCP серверів
└── templates/          ← Шаблони для нових агентів/skills
```

---

## 🧠 base-skills/

Документація по розробці skills:

- **obsidian-integration.md** — Як інтегруватись з Obsidian
- **logging-patterns.md** — Best practices для логування
- **error-handling.md** — Обробка помилок
- **api-integration.md** — Робота з API
- **testing-patterns.md** — Написання тестів

**Використання**: Читайте перед написанням нового skill!

---

## 📦 common-mcp/

Готові компоненти для MCP:

```
common-mcp/
├── base-mcp-template.py       ← Скопіюйте для нового MCP
├── common-connectors.js       ← Готові функції для MCP
├── auth-patterns.py           ← Шаблони для аутентифікації
├── config-template.json       ← Шаблон конфіг файла
└── error-handlers.py          ← Обробка помилок
```

**Використання**:
```bash
# Для нового Python MCP:
cp common-mcp/base-mcp-template.py ../Agent-[NAME]/mcp/new-server.py

# Для Node.js MCP:
# Використовуйте common-mcp/common-connectors.js як основу
```

---

## 📋 templates/

### agent-template/

**Шаблон для нового агента**:

```bash
cp -r templates/agent-template ../Agent-New-Name
```

Містить:
```
agent-template/
├── README.md              ← Заповніть інформацію про агента
├── skills/
│   └── [додайте skills]
├── mcp/
│   └── [додайте MCP]
└── config/
    ├── settings.json      ← Налаштування агента
    └── hooks.json         ← Hooks (опційно)
```

### skill-template/

**Шаблон для нового skill**:

```bash
cp -r templates/skill-template ../Agent-[NAME]/skills/new-skill
```

Містить:
```
skill-template/
├── SKILL.md               ← Опис & інструкції
├── scripts/
│   ├── main.py            ← Основний код
│   ├── utils.py           ← Допоміжні функції
│   └── requirements.txt    ← Залежності (якщо Python)
├── references/
│   ├── documentation.md   ← Документація
│   └── examples.json      ← Приклади
└── evals/                 ← Тести (опційно)
    └── evals.json
```

---

## 🚀 Як використовувати

### Додавання нового агента

```bash
# 1. Копіюйте шаблон
cp -r 60-Agents/shared/templates/agent-template \
      60-Agents/Agent-Trading-Bot

# 2. Відредагуйте README.md
nano 60-Agents/Agent-Trading-Bot/README.md

# 3. Додайте skills
cp -r 60-Agents/shared/templates/skill-template \
      60-Agents/Agent-Trading-Bot/skills/market-analyzer

# 4. Налаштуйте config/settings.json
nano 60-Agents/Agent-Trading-Bot/config/settings.json

# 5. Готово!
```

### Додавання нового skill

```bash
# 1. Копіюйте шаблон
cp -r 60-Agents/shared/templates/skill-template \
      60-Agents/Agent-Claude-Main/skills/new-skill

# 2. Напишіть SKILL.md
nano 60-Agents/Agent-Claude-Main/skills/new-skill/SKILL.md

# 3. Напишіть code в scripts/
nano 60-Agents/Agent-Claude-Main/skills/new-skill/scripts/main.py

# 4. Оновіть config/settings.json батьківського агента
# Додайте "new-skill" у skills_enabled

# 5. Готово!
```

### Додавання нового MCP сервера

```bash
# 1. Копіюйте шаблон
cp 60-Agents/shared/common-mcp/base-mcp-template.py \
   60-Agents/Agent-Claude-Main/mcp/new-server.py

# 2. Відредагуйте
nano 60-Agents/Agent-Claude-Main/mcp/new-server.py

# 3. Додайте в config.json
nano 60-Agents/Agent-Claude-Main/mcp/config.json

# 4. Тестуйте
python 60-Agents/Agent-Claude-Main/mcp/new-server.py

# 5. Готово!
```

---

## 📝 Структура для запам'ятовування

```
shared/
├── base-skills/           ← ЧИТАЙТЕ перед написанням!
├── common-mcp/            ← КОПІЮЙТЕ для MCP
└── templates/             ← КОПІЮЙТЕ для агентів/skills

Новий агент?      → cp -r templates/agent-template
Новий skill?      → cp -r templates/skill-template
Новий MCP?        → cp common-mcp/base-mcp-template.py
```

---

## 🎯 Best Practices

✅ **РОБІТЬ**:
- Читайте base-skills/ перед написанням
- Копіюйте з templates/ для нових агентів/skills
- Намагайтесь переробляти код з common-mcp/
- Документуйте свої skills у SKILL.md

❌ **НЕ РОБІТЬ**:
- Не пишіть все з нуля (використовуйте templates!)
- Не дублюйте код (використовуйте common-mcp/)
- Не забувайте про README.md

📌 **Організація**:
- shared/ як центр знань
- Копіюйте шаблони в нові папки агентів
- Оновлюйте шаблони якщо знайдете улучшення

---

## 📊 Файлова структура для паттернів

### common-mcp/base-mcp-template.py

```python
"""
Base MCP Server Template

Скопіюйте цей файл та модифікуйте для вашого MCP сервера
"""

class MCPServer:
    def __init__(self, name, version="1.0"):
        self.name = name
        self.version = version
    
    def handle_request(self, method, params):
        """Основний метод для обробки запитів"""
        pass
    
    def start(self, host="localhost", port=8000):
        """Запустити MCP сервер"""
        pass
```

### base-skills/obsidian-integration.md

```markdown
# Obsidian Integration for Skills

## Як писати в Obsidian з вашого skill

### Варіант 1: Використовувати vault_writer.py
```python
from sys import path
path.append('/home/user/MyVault')
from vault_writer import VaultWriter

writer = VaultWriter(vault_path='~/MyVault')
writer.write_project_session(...)
```

### Варіант 2: Звратися до MCP сервера
Якщо у вас є MCP сервер який пише в Obsidian...
```

---

**Версія**: 2026-04-19  
**Статус**: Ready for use
