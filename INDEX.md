# 🗂️ Obsidian Vault — Повний INDEX

Це карта вашого Obsidian vault з усіма вказівками для навігації.

---

## 📍 **ЧИ ВИ НОВИЧОК?**

1. **Почніть з**: [[CLAUDE-RULES.md]] — основні правила
2. **Потім прочитайте**: [[CLAUDE-SETUP.md]] — інструкція з прикладами
3. **Передайте агентам**: [[AGENT-PROMPT.md]] — промт для інших AI

---

## 🗺️ **КАРТА VAULT'а**

```
~/MyVault/
│
├── 📋 ЦЕНТРАЛЬНІ ФАЙЛИ
│   ├── CLAUDE-RULES.md      ← Правила запису (обов'язково прочитати)
│   ├── CLAUDE-SETUP.md      ← Інструкція & приклади
│   ├── AGENT-PROMPT.md      ← Промт для агентів
│   ├── vault_writer.py      ← Python скрипт для запису
│   └── INDEX.md             ← Цей файл (карта)
│
├── 📥 00-Inbox/ [[00-Inbox/README.md]]
│   └── Швидкі нотатки, ідеї, клипи з веб
│   └── Потім переміщуються в ІНШІ папки
│
├── 💼 10-Work/ [[10-Work/README.md]]
│   ├── Projects/
│   │   └── [project-name]/
│   │       ├── project-overview.md    (один раз)
│   │       └── sessions/              (сесії роботи)
│   ├── Code-Snippets/                 (корисні фрагменти)
│   └── Tech-Research/                 (технічні дослідження)
│
├── 📊 20-Trading/ [[20-Trading/README.md]]
│   ├── Journal/                       (щоденні сесії)
│   ├── Analysis/                      (аналіз пар перед входом)
│   ├── Strategies/                    (торгівельні стратегії)
│   ├── Psychology/                    (психологічні аспекти)
│   └── Resources/                     (посилання)
│
├── 📚 30-Learning/ [[30-Learning/README.md]]
│   ├── Books/                         (конспекти книг)
│   ├── Courses/                       (курси & тренінги)
│   ├── Articles/                      (статті & блог)
│   └── Videos/                        (відео & трансрипти)
│
├── 🎯 40-Personal/ [[40-Personal/README.md]]
│   ├── Goals/                         (цілі & плани)
│   └── Health/                        (фітнес & здоров'я)
│
├── 📦 50-Resources/
│   ├── Templates/                     (шаблони нотаток)
│   ├── Attachments/                   (медіа файли)
│   └── [інші ресурси]
│
└── 🗃️ 99-Archive/                     (старі файли)
```

---

## 📖 **ІНСТРУКЦІЇ ПО ПАПКАХ**

| Папка | README | Для чого | Як додавати |
|-------|--------|----------|-----------|
| 00-Inbox | [[00-Inbox/README.md]] | Швидкі нотатки | Будь-коли, потім архівуйте |
| 10-Work | [[10-Work/README.md]] | Проекти, код, дослідження | На кінець сесії (автоматично) |
| 20-Trading | [[20-Trading/README.md]] | Трейдинг jour + analysis | Щодня журнал, перед входом analysis |
| 30-Learning | [[30-Learning/README.md]] | Книги, курси, статті | Під час/після читання |
| 40-Personal | [[40-Personal/README.md]] | Цілі, здоров'я | Щомісяця оновлювати |
| 50-Resources | - | Шаблони, ресурси | За потребою |
| 99-Archive | - | Старі файли | Перемістити сюди коли готово |

---

## 🤖 **ДЛЯ АГЕНТІВ (Claude)**

### Якщо ви агент, прочитайте:

1. **CLAUDE-RULES.md** — Как записувати (обов'язково!)
2. **Відповідний README** — Залежно від типу роботи:
   - Проект? → [[10-Work/README.md]]
   - Трейдинг? → [[20-Trading/README.md]]
   - Навчання? → [[30-Learning/README.md]]

3. **На кінець сесії**:
   - Прочитайте что ви робили
   - Видобудьте ключову інформацію
   - Напишіть файл у правильну папку
   - Повідомте користувача результат

---

## 📝 **ОСНОВНІ ПРАВИЛА**

### YAML Frontmatter (обов'язково для ВСІХ файлів)

```yaml
---
title: "Назва нотатки"
date: YYYY-MM-DD                      # Дата створення
tags: [категорія, тип, деталь]        # Мінімум 2
category: work|trading|learning|personal
status: active|completed|draft|watching
pinecone_indexed: false               # Завжди false
---
```

### Теги

**Обов'язкові** (мінімум 2):
- **Основна**: work, trading, learning, personal
- **Підтип**: session, bug, analysis, journal, strategy, goal, health

**Приклади**:
```
tags: [work, session, code, api-integration]
tags: [trading, journal, eurusd]
tags: [learning, book, psychology, trading]
tags: [personal, goal, finance]
```

### Лінки

Використовуйте wiki-style:
```markdown
- [[10-Work/Projects/назва/project-overview]]
- [[20-Trading/Analysis/eurusd-analysis-2026-04]]
- [[30-Learning/Books/market-wizards]]
```

---

## 🔄 **СТАНДАРТНІ ПОТОКИ**

### Для ПРОЕКТІВ (10-Work/Projects/)

```
1. Новий проект → Створити папку → project-overview.md
2. Кожна сесія → sessions/YYYY-MM-DD-[task].md
3. Рішення, багі, артефакти → Записати в сесію
4. Залізти на project-overview
```

### Для ТРЕЙДИНГУ (20-Trading/)

```
1. Перед торговлею → Analysis/[PAIR]-analysis-*.md
2. Після торговлі → Journal/YYYY-MM-DD-trading.md
3. Зв'язати journal з analysis
4. Щотижня - огляд помилок
```

### Для НАВЧАННЯ (30-Learning/)

```
1. Прочитати/переглянути матеріал
2. Конспектувати в Books/Courses/Articles/Videos/
3. Залізти на пов'язані проекти
4. Застосувати в реальних проектах
```

### Для ОСОБИСТОГО (40-Personal/)

```
1. Встановити мету → Goals/[назва]-2026.md
2. Щомісяця → Оновляти прогрес
3. Щокварталу → Переглядати & коригувати
4. Щорічно → Нові цілі
```

---

## 🎯 **ШВИДКА НАВІГАЦІЯ**

### Я хочу...

**...записати сесію роботи**
→ [[10-Work/README.md]] → Projects/ → sessions/

**...додати аналіз паршої**
→ [[20-Trading/README.md]] → Analysis/

**...написати трейдинг журнал**
→ [[20-Trading/README.md]] → Journal/

**...конспектувати книгу**
→ [[30-Learning/README.md]] → Books/

**...встановити особисту ціль**
→ [[40-Personal/README.md]] → Goals/

**...дати швидку ідею**
→ [[00-Inbox/README.md]] → Потім архівуйте

**...знайти стару нотатку**
→ Дивіться архіви в 99-Archive/ або використовуйте пошук

---

## 📊 **СТАТИСТИКА VAULT'а**

```
Загальна структура:
├── Основних категорій: 5 (Work, Trading, Learning, Personal, Inbox)
├── Підкатегорій: 15+
├── Шаблонів: 8 (у 50-Resources/Templates/)
└── Агентів що пишуть: Більше ніж 1

Файли для Claude Integration:
├── CLAUDE-RULES.md      - Повна документація
├── CLAUDE-SETUP.md      - Інструкція з кодом
├── AGENT-PROMPT.md      - Промт для передачі
├── vault_writer.py      - Python скрипт
└── [INDEX.md] цей файл  - Карта
```

---

## 🔍 **ЯК ШУКАТИ**

### Методи пошуку:

1. **По датам** → Calendar плагін показує щодня
2. **По тегам** → Пошук `#work` чи `#eurusd`
3. **По проектам** → Папка `10-Work/Projects/[назва]`
4. **По сумі** → Dataview SQL запити (якщо встановлено)
5. **По словах** → Ctrl+Shift+F у Obsidian

### Приклади запитів:

```
tag:#work tag:#session              → Мої робочі сесії
tag:#trading tag:#journal          → Трейдинг журнал
tag:#eurusd                         → Все про EURUSD
tag:#personal tag:#goal            → Мої особисті цілі
```

---

## ⚙️ **НАЛАШТУВАННЯ OBSIDIAN**

### Обов'язкові плагіни:

- **Templater** — Інтерактивні шаблони (Ctrl+T)
- **Dataview** — SQL запити по vault
- **Calendar** — Навігація по датам
- **Web Clipper** — Збереження веб-сторінок

### Папка шаблонів:

→ Settings → Templater → Template folder → `50-Resources/Templates/`

---

## 🆘 **ЯКЩО ЩОСЬ НЕ ЗРОЗУМІЛО**

1. **Про структуру** → Прочитайте [[CLAUDE-RULES.md]]
2. **Про приклади** → Прочитайте [[CLAUDE-SETUP.md]]
3. **Про конкретну папку** → Прочитайте відповідний README
4. **Для агентів** → Передайте [[AGENT-PROMPT.md]]

---

## 📋 **CHECKLIST ДЛЯ ПЕРШОГО ЗАПУСКУ**

- [ ] Прочитав CLAUDE-RULES.md
- [ ] Прочитав CLAUDE-SETUP.md
- [ ] Мають встановлені плагіни (Templater, Dataview, Calendar)
- [ ] Папка Templates налаштована
- [ ] Понимаю структуру (00-Inbox до 99-Archive)
- [ ] Знаю як записувати файли для своєї категорії
- [ ] Готовий передавати AGENT-PROMPT.md іншим агентам

---

## 📞 **КОНТАКТ & ІНФОРМАЦІЯ**

- **Власник**: Nadolo
- **Email**: sergij.p@gmail.com
- **Vault**: ~/MyVault
- **Версія системи**: 2026-04-19

---

## 🔗 **ШВИДКІ ЛІНКИ**

| Що? | Де? |
|-----|-----|
| Правила запису | [[CLAUDE-RULES.md]] |
| Інструкція & приклади | [[CLAUDE-SETUP.md]] |
| Промт для агентів | [[AGENT-PROMPT.md]] |
| Python скрипт | [[vault_writer.py]] |
| 10-Work інструкція | [[10-Work/README.md]] |
| 20-Trading інструкція | [[20-Trading/README.md]] |
| 30-Learning інструкція | [[30-Learning/README.md]] |
| 40-Personal інструкція | [[40-Personal/README.md]] |
| 00-Inbox інструкція | [[00-Inbox/README.md]] |

---

**Версія**: 2026-04-19  
**Статус**: Активна система  
**Останнє оновлення**: 2026-04-19  
**Готовність**: ✅ 100%
