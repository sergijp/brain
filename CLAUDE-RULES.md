---
title: "Claude Integration Rules — Як записується пам'ять"
date: 2026-04-19
tags: [system, claude, obsidian, rules]
category: system
status: active
pinecone_indexed: false
---

# 🤖 Claude Integration Rules

Цей файл описує як Claude (Nadolo's AI agent) записує інформацію в ваш Obsidian vault.

---

## 📋 Загальні правила

### 1. **Структура папок**
```
~/MyVault/
├── 00-Inbox/           ← швидкі нотатки, не структуровані
├── 10-Work/
│   ├── Projects/       ← проекти
│   │   └── [project-name]/
│   │       ├── project-overview.md (один раз)
│   │       └── sessions/
│   │           └── YYYY-MM-DD-*.md (сесії)
│   ├── Code-Snippets/  ← корисні фрагменти
│   └── Tech-Research/  ← дослідження
├── 20-Trading/
│   ├── Journal/        ← щоденні сесії
│   │   └── YYYY-MM-DD-trading-session.md
│   ├── Analysis/       ← аналіз пар перед входом
│   │   └── [pair]-analysis-YYYY-MM.md
│   └── Strategies/
├── 30-Learning/
├── 40-Personal/
└── 50-Resources/
    └── Templates/
```

### 2. **YAML Frontmatter** (обов'язково для кожного файлу)

```yaml
---
title: "Назва нотатки"
date: YYYY-MM-DD
tags: [category, type, detail]
category: work|trading|learning|personal
status: active|completed|archived|draft
project: назва-проекту (для work)
pinecone_indexed: false
---
```

**Значення полів:**
- `title`: Чітка назва файлу
- `date`: Дата створення
- `tags`: Для пошуку (мінімум 2)
- `category`: Робоча класифікація
- `status`: Статус роботи
- `project`: Ім'я проекту (опційно)
- `pinecone_indexed`: Завжди `false` (система розберіться)

---

## 🏢 **ДЛЯ ПРОЕКТІВ** (`10-Work/Projects/`)

### Момент 1: Новий проект
1. Створюю папку: `10-Work/Projects/[project-name-slug]/`
2. Файл `project-overview.md` — за `tpl-project.md`
3. Папка `sessions/` для сесій

### Момент 2: Кожна сесія роботи над проектом

**Файл**: `10-Work/Projects/[project-name]/sessions/YYYY-MM-DD-[короткий-опис].md`

```markdown
---
title: "Проект: [назва] — Сесія [що робили]"
date: 2026-04-19
tags: [work, session, code, project]
category: work
project: [project-name]
status: completed
pinecone_indexed: false
---

## 🎯 Мета сесії
[Що було потрібно зробити]

## ✅ Виконано
- Задача 1 → [результат/файл/лінк]
- Задача 2 → [результат]
- Задача 3 → [результат]

## 🔑 Важливі рішення (ADR)
| Рішення | Причина | Альтернатива розглянута |
|---------|---------|------------------------|
| Обрали підхід X | Швидче, ніж Y | Z не підходить, бо ... |

## 🐛 Проблеми й як вирішили
### Баг 1: [назва]
- **Контекст**: де/коли
- **Причина**: чому відбулось
- **Вирішення**: код або опис кроків
- **Час**: Х хвилин

### Баг 2: ...

## 📎 Артефакти
- Файл: `path/to/file.tsx` (гіт лінк)
- Код: [фрагмент якщо важливо]

## 🔗 Пов'язані нотатки
- [[10-Work/Projects/project-name/project-overview]]
- [[50-Resources/...]]

---
```

### Правила для проектів:
✅ **ПИСАТИ**: Виконані кроки, рішення, помилки, тайм-трекінг  
❌ **НЕ писати**: Поточний код (він у гіті), дрібні зміни  
📌 **Теги**: `work, session, code, [project-name]`  
🔗 **Лінки**: На project-overview, на пов'язані дослідження  

---

## 📊 **ДЛЯ ТРЕЙДИНГУ** (`20-Trading/`)

### Категорія 1: JOURNAL (щоденні сесії)

**Файл**: `20-Trading/Journal/YYYY-MM-DD-trading-session.md`

```markdown
---
title: "Трейдинг: YYYY-MM-DD"
date: 2026-04-19
tags: [trading, journal, session]
category: trading
status: completed
pinecone_indexed: false
---

## 📊 Огляд дня
- **Депозит**: $10,000
- **Дата**: 2026-04-19

## 📈 Угоди виконані
| Пара | Вхід | Вихід | P&L | Статус | Тайм |
|------|------|-------|-----|--------|------|
| EURUSD | 1.0950 | 1.0970 | +$200 | ✅ win | 45m |
| GBPUSD | 1.2650 | 1.2620 | -$150 | ❌ loss | 30m |

## 💡 Ключові спостереження
- [Список важливих моментів дня]

## ⚠️ Помилки й навчання
### Помилка 1: [опис]
- Як виникла
- Як не повторити

## 🎯 План на завтра
- [Рішення на основі сьогодня]

## 🔗 Пов'язані аналізи
- [[20-Trading/Analysis/eurusd-analysis-2026-04]]

---
```

### Категорія 2: ANALYSIS (перед входом)

**Файл**: `20-Trading/Analysis/[PAIR]-analysis-YYYY-MM.md`

```markdown
---
title: "[PAIR] — Аналіз YYYY-MM"
date: 2026-04-19
tags: [trading, analysis, [pair]]
category: trading
status: active
pinecone_indexed: false
---

## 🎯 Пара: [EURUSD/GBPUSD/etc]

## 📊 Технічні рівні
- **S2**: 1.0880
- **S1**: 1.0920
- **Current**: 1.0955
- **R1**: 1.1000
- **R2**: 1.1050

## 📈 Тренд
[Описание тренда, супорт/резистенс]

## 💡 Сценарії
1. **Bullish**: [Якщо...] → Ціль: ...
2. **Bearish**: [Якщо...] → Ціль: ...

## ✅ Умови входу (Bullish)
- Закриття вище 1.0980
- RSI > 60
- MACD bullish cross

## 🎯 Технічна угода
- **Entry**: 1.0985
- **TP**: 1.1030
- **SL**: 1.0950
- **Risk:Reward**: 1:2

## 📝 Примітки
- [Додатковий контекст, новини, FAA/ЕЦБ, etc]

---
```

### Правила для трейдингу:
✅ **ПИСАТИ**: Угоди, аналіз, спостереження, помилки  
❌ **НЕ писати**: Деталі розраховуєш в трейдинг-софті  
📌 **Теги**: `trading, journal/analysis, [PAIR]`  
🔗 **Лінки**: Journal посилається на Analysis  

---

## 🔄 **АВТОМАТИЧНИЙ ПРОЦЕС**

### На кінець кожної сесії:
1. Claude **прочитає** то, чим займався
2. **Напише** нотатку у правильну папку
3. **Залінкує** на пов'язані нотатки
4. **Опублікує** файл у vault

**Формат імені файлу**:
- Проекти: `10-Work/Projects/[project-name]/sessions/YYYY-MM-DD-[task].md`
- Трейдинг: `20-Trading/Journal/YYYY-MM-DD-trading.md` або `20-Trading/Analysis/[PAIR]-analysis-YYYY-MM.md`

---

## ✋ **ВРУЧНУ — Команди**

Якщо хочете записати щось прямо під час роботи:

### Варіант 1: Скажіть "збережи в vault"
```
Мене: "збережи це в vault"
Claude: Створить файл у відповідній папці за типом роботи
```

### Варіант 2: Явна команда
```
Мене: "записати в Analysis: [пара] з умовами входу..."
Claude: Створить файл `20-Trading/Analysis/[PAIR]-analysis-*.md`
```

---

## 📁 **Структура тегів**

**Обов'язкові**: мінімум 2
- **Основний**: `work`, `trading`, `learning`, `personal`
- **Підтип**: `session`, `bug`, `analysis`, `journal`, `code`
- **Дополнительно**: `[project-name]`, `[PAIR]`, інші деталі

**Приклади**:
```
tags: [work, session, code, api-integration]
tags: [trading, journal, session]
tags: [trading, analysis, eurusd]
tags: [work, bug, solution, backend]
```

---

## 🔍 **Як знайти потім?**

1. **По датам** — Calendar плагін показує щодня
2. **По тегам** — `#work` чи `#eurusd` у пошуку
3. **По проектам** — папка `10-Work/Projects/[назва]`
4. **По сумі** — Dataview SQL запити

---

## ⚙️ **Налаштування**

- **Vault**: `~/MyVault`
- **Шаблони**: `50-Resources/Templates/`
- **Плагіни**: Templater, Dataview, Calendar (обов'язкові)
- **Ollama**: Для локального пошуку (опційно)

---

## 🚀 **Запуск системи**

1. ✅ Цей файл прочитаний
2. ✅ Структура создана
3. ✅ Claude готовий писати

На кінець кожної сесії буде автоматично записуватись пам'ять.

---

**Версія**: 2026-04-19  
**Статус**: Активна  
**Остання оновлення**: 2026-04-19
