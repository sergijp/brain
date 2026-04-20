# 🚀 Claude Integration Setup

Цей файл описує як запустити й налаштувати систему автоматичного запису Claude в Obsidian.

---

## 📦 Встановлення

### Крок 1: Скопіювати файли

```bash
# Скрипт вже в корні vault:
cp ~/MyVault/vault_writer.py ~/obsidian-ai/
chmod +x ~/obsidian-ai/vault_writer.py
```

### Крок 2: Налаштувати алиаси (bash/zsh)

Додати в `~/.zshrc` або `~/.bashrc`:

```bash
# Запис в Obsidian з Claude
alias vault-write-project='python ~/MyVault/vault_writer.py --type work'
alias vault-write-trading='python ~/MyVault/vault_writer.py --type trading'

# Приклади:
# vault-write-project --project "api-v2" --tasks "Setup DB" "Add auth" --date 2026-04-19
# vault-write-trading --action journal --date 2026-04-19
```

Потім:
```bash
source ~/.zshrc
```

---

## 💻 Використання

### Для ПРОЕКТІВ

```bash
# Прості задачи
vault-write-project --project "my-api" \
  --tasks "Setup database" "Configure auth" "Write tests"

# З рішеннями
vault-write-project --project "frontend" \
  --tasks "Build components" \
  --decisions '{"decision":"React hooks","reason":"Better state management","alternative":"Redux"}' \
  --decisions '{"decision":"Tailwind CSS","reason":"Faster styling","alternative":"CSS modules"}'

# З баґами
vault-write-project --project "backend" \
  --bugs '{"name":"Migration timeout","context":"Running init script","reason":"Large dataset","solution":"Increased timeout to 30s"}' \
  --bugs '{"name":"Memory leak","solution":"Fixed circular reference in cache"}'
```

### Для ТРЕЙДИНГУ

#### Journal (сесія):
```bash
vault-write-trading --action journal \
  --trades '{"pair":"EURUSD","entry":"1.0950","exit":"1.0970","pnl":"+200"}' \
  --trades '{"pair":"GBPUSD","entry":"1.2650","exit":"1.2620","pnl":"-150"}' \
  --observations "EUR trending up" "GBP consolidating" \
  --mistakes "Held trade too long on GBPUSD" "Entered without full confirmation"
```

#### Analysis (перед входом):
```bash
vault-write-trading --action analysis --pair "EURUSD" \
  --levels '{"S2":"1.0880","S1":"1.0920","R1":"1.1000","R2":"1.1050"}' \
  --trend "Uptrend since Feb, testing R1" \
  --entry-conditions "Close above 1.0980" "RSI > 60" "MACD bullish" \
  --tp-sl '{"Entry":"1.0985","TP":"1.1030","SL":"1.0950"}'
```

---

## 🤖 Автоматичне збереження з Claude (Cowork)

### Опція 1: Вручну (простий варіант)

На кінець сесії я запитаю:
> "Писати результати в vault?"

Ви кажете "так" → я запущу скрипт

### Опція 2: Автоматично (складніше)

Створити Python hook, який запускається після кожної Claude сесії:

**Файл**: `~/obsidian-ai/claude_session_hook.py`

```python
#!/usr/bin/env python3
"""
Hook для автоматичного запису Claude сесій в Obsidian
Читає лог сесії → витягує задачи → пише в vault
"""

import os
import json
from pathlib import Path
from datetime import datetime
import subprocess

VAULT_PATH = os.path.expanduser("~/MyVault")
SESSION_LOG = os.path.expanduser("~/.claude/session.log")  # Приклад

def extract_session_data(log_file):
    """Витягти інформацію з логу сесії"""
    # Тут логіка парсингу логу
    # Повинна повернути dict з типом сесії, проектом, задачами, тощо
    pass

def run_vault_writer(session_type, **kwargs):
    """Запустити vault_writer.py з параметрами"""
    cmd = ["python", f"{VAULT_PATH}/vault_writer.py"]
    cmd += ["--type", session_type]
    
    for key, value in kwargs.items():
        if value:
            if isinstance(value, list):
                cmd.extend([f"--{key}"] + value)
            else:
                cmd.extend([f"--{key}", value])
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0

def main():
    # Цей скрипт буде запущений після кожної Claude сесії
    # Поки заповничу логіку потім
    print("📝 Claude session hook ready")

if __name__ == "__main__":
    main()
```

---

## 📋 Приклади

### Приклад 1: Проект React компонент

```bash
vault-write-project --project "frontend-ui" \
  --tasks "Create Button component" "Add Storybook stories" "Write unit tests" \
  --decisions '{"decision":"Headless UI","reason":"Full accessibility","alternative":"MUI - too heavy"}' \
  --bugs '{"name":"Props not typed","solution":"Added TypeScript interface"}' \
  --date 2026-04-19
```

**Результат**: Файл `10-Work/Projects/frontend-ui/sessions/2026-04-19-create-button.md`

---

### Приклад 2: Трейдинг день

```bash
vault-write-trading --action journal \
  --trades '{"pair":"EURUSD","entry":"1.0950","exit":"1.0965","pnl":"+150"}' \
  --observations "Morning gap up on ECB news" "Volatility increased 15%" \
  --mistakes "Didn't use TP order - closed manually" \
  --date 2026-04-19
```

**Результат**: Файл `20-Trading/Journal/2026-04-19-trading-session.md`

---

### Приклад 3: Аналіз перед входом

```bash
vault-write-trading --action analysis --pair "GBPUSD" \
  --levels '{"S2":"1.2580","S1":"1.2610","Current":"1.2640","R1":"1.2680","R2":"1.2720"}' \
  --trend "Consolidating in 50-pip range, BoE decision pending" \
  --entry-conditions "Break above 1.2680 with volume" "RSI > 65" \
  --tp-sl '{"Entry":"1.2685","TP":"1.2750","SL":"1.2650","RR":"1:2.6"}' \
  --date 2026-04
```

**Результат**: Файл `20-Trading/Analysis/gbpusd-analysis-2026-04.md`

---

## 🔗 Інтеграція з Claude

### Коли я буду писати в vault:

1. **Автоматично на кінець сесії**:
   - Я прочитаю чим займався
   - Видобуду ключову інформацію
   - Запущу `vault_writer.py` з параметрами
   - Повідомлю вас про результат

2. **Вручну по команді**:
   - "збережи в vault"
   - "записати в проект [назва]"
   - "додати трейдинг аналіз"

---

## 📊 Структура файлів після запису

```
10-Work/Projects/my-api/
├── project-overview.md          ← один раз
└── sessions/
    ├── 2026-04-19-setup-db.md
    ├── 2026-04-18-add-auth.md
    └── 2026-04-17-configure.md

20-Trading/Journal/
├── 2026-04-19-trading.md        ← щоденна сесія
├── 2026-04-18-trading.md
└── ...

20-Trading/Analysis/
├── eurusd-analysis-2026-04.md   ← перед входом
├── gbpusd-analysis-2026-04.md
└── ...
```

---

## 🔍 Перевірка

Після запису перейдіть в Obsidian:
1. Відкрийте відповідну папку (Projects, Journal, Analysis)
2. Побачите новий файл з датою
3. Файл буде мати правильну структуру й YAML

---

## ⚙️ Налаштування (опційно)

### Якщо потрібно змінити структуру:

Редагуйте `~/MyVault/vault_writer.py`:
- Функція `format_yaml_header()` — YAML
- Функції `write_project_session()`, `write_trading_journal()` — контент

### Якщо потрібна локалізація:

Замініть англійські назви на українські у файлі.

---

## 🐛 Проблемування

**Проблема**: "Vault not found"
```bash
python vault_writer.py --type work --vault ~/MyVault
```

**Проблема**: "Invalid JSON for..."
```bash
# Правильно:
--decisions '{"decision":"X","reason":"Y"}'

# Неправильно:
--decisions {"decision":"X","reason":"Y"}
```

**Проблема**: Файл не створився
- Перевірте права доступу на папку `~/MyVault`
- Переконайтесь, що папка існує: `ls ~/MyVault/10-Work/Projects/`

---

## 📚 Документація

- `CLAUDE-RULES.md` — Правила запису (як все організовано)
- `vault_writer.py` — Сам скрипт (можна редагувати)
- `CLAUDE-SETUP.md` — Цей файл (інструкція)

---

**Версія**: 2026-04-19  
**Статус**: Готово до використання  
**Контакт**: sergij.p@gmail.com
