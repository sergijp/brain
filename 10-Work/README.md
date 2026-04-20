# 💼 10-Work

**Робота, проекти, код, дослідження**

---

## 📋 Призначення

Все що пов'язано з роботою:
- 🏗️ **Projects/** — реальні проекти з сесіями
- 💻 **Code-Snippets/** — корисні фрагменти коду
- 🔬 **Tech-Research/** — технічні дослідження

---

## 📁 Структура

```
10-Work/
├── Projects/
│   ├── api-v2/
│   │   ├── project-overview.md      (один раз, детальна інформація)
│   │   └── sessions/
│   │       ├── 2026-04-19-setup.md
│   │       ├── 2026-04-18-auth.md
│   │       └── ...
│   ├── frontend-ui/
│   │   ├── project-overview.md
│   │   └── sessions/
│   │       └── ...
│   └── [project-name]/
│       ├── project-overview.md
│       └── sessions/
│
├── Code-Snippets/
│   ├── typescript-utils.md
│   ├── postgres-queries.md
│   └── ...
│
└── Tech-Research/
    ├── react-18-migration.md
    ├── rust-performance.md
    └── ...
```

---

## 🏗️ Projects/ — Як створювати

### Структура проекту

```
Projects/[project-name]/
├── project-overview.md     ← Один раз, при створенні проекту
└── sessions/              ← Сесії роботи над проектом
    └── YYYY-MM-DD-[task].md
```

### project-overview.md

Використовувати шаблон `tpl-project.md`:

```markdown
---
title: "[Назва проекту]"
date: 2026-04-19
tags: [work, project, tech-stack]
category: work
project: project-name
status: active
pinecone_indexed: false
---

## 🗺 Огляд
Що це за проект і яку проблему вирішує?

## 🛠 Технічний стек
- **Мова**: Python, TypeScript, Rust
- **Фреймворк**: Django, React, FastAPI
- **БД**: PostgreSQL, Redis
- **Інфраструктура**: Docker, AWS, Kubernetes

## 🏗 Архітектура
Ключові компоненти і як вони взаємодіють

## ✅ Поточний стан
- [ ] Перша фаза
- [ ] Друга фаза
- [ ] Третя фаза

## ⚠️ Важливі нюанси
Підводні камені, обмеження, неочевидні рішення

## 🔑 Команди
```bash
# Запуск
# Тести
# Deploy
```

## 📝 Рішення (ADR)
| Дата | Рішення | Причина |
|------|---------|---------|
| 2026-04-19 | PostgreSQL замість MongoDB | Масштабованість |

## 🔗 Пов'язані нотатки
- [[10-Work/Projects/project-name/sessions/2026-04-19-...]]
- [[10-Work/Tech-Research/...]]

## 📌 Відкриті питання
- [ ] Як впровадити ...?
- [ ] Що робити з ...?
```

### sessions/ — Сесії роботи

**Файл**: `sessions/YYYY-MM-DD-[задача].md`

```markdown
---
title: "Проект: [назва] — Сесія [дата]"
date: 2026-04-19
tags: [work, session, code, project-name]
category: work
project: project-name
status: completed
pinecone_indexed: false
---

## 🎯 Мета сесії
Що робили в цій сесії?

## ✅ Виконано
- Задача 1 → результат (гіт лінк)
- Задача 2 → результат

## 🔑 Важливі рішення
| Рішення | Причина | Альтернатива |
|---------|---------|-------------|
| X | Y | Z |

## 🐛 Проблеми й як вирішили
### Баг 1: [назва]
- **Контекст**: де це виникло
- **Причина**: чому сломалось
- **Вирішення**: як зафіксили
- **Час**: X хвилин

## 📎 Артефакти
- Commit: [лінк]
- PR: [лінк]
- Файли: [список змінених файлів]

## 🔗 Пов'язані
- [[10-Work/Projects/project-name/project-overview]]
- [[10-Work/Tech-Research/...]]

## 📊 Статистика
- **Час**: X годин
- **Строк коду**: +150 / -30
- **Баґів вирішено**: 3
```

---

## 💻 Code-Snippets/ — Корисні фрагменти

**Ім'я файлу**: `[мова]-[тема].md`

```markdown
---
title: "TypeScript: Utility Types"
date: 2026-04-19
tags: [work, code-snippet, typescript, types]
category: work
status: active
pinecone_indexed: false
---

## 🎯 Тема
Корисні utility types в TypeScript

## 💡 Сниппет 1: Pick
```typescript
type User = {
  id: number;
  name: string;
  email: string;
};

type UserPreview = Pick<User, "id" | "name">;
```

## 💡 Сниппет 2: Partial
```typescript
type UpdateUser = Partial<User>;
```

## 📚 Джерело
https://www.typescriptlang.org/docs/handbook/utility-types.html

## 🔗 Проекти де використовується
- [[10-Work/Projects/api-v2]]
```

---

## 🔬 Tech-Research/ — Дослідження

**Ім'я файлу**: `[тема]-[дата].md` або просто `[тема].md`

**Для чого?** Технічні дослідження, які **НЕ прив'язані до конкретного проекту**:
- Nginx, Apache, Linux настройки
- Docker, Kubernetes
- AWS, Azure, GCP
- Database optimization
- DevOps практики
- Architecture decisions
- Performance tuning

### Формат

```markdown
---
title: "React 18: Concurrent Features"
date: 2026-04-19
tags: [work, research, react, performance]
category: work
status: active
pinecone_indexed: false
---

## 🎯 Тема
Вивчення Concurrent Features в React 18

## 📚 Дослідження
- Як це працює?
- Коли використовувати?
- Переваги і недоліки

## 💾 Висновки
[Ключові висновки дослідження]

## 📈 Можливість застосування
Де це можна використати в наших проектах?

## 🔗 Посилання
- [Стаття 1]
- [Стаття 2]
- [Документація]

## 🔗 Проекти де застосовується
- [[10-Work/Projects/frontend-ui]]
```

### Приклад: Nginx настройка

```markdown
---
title: "Nginx: Performance Optimization"
date: 2026-04-19
tags: [work, research, devops, nginx, server]
category: work
status: active
pinecone_indexed: false
---

## 🎯 Тема
Оптимізація Nginx для high-load

## 📚 Best Practices
1. worker_processes = CPU cores
2. Tune worker_connections
3. Enable gzip compression
4. Configure expires headers

## 🔗 Проекти що використовують
- [[10-Work/Projects/api-v2]]
- [[10-Work/Projects/backend-service]]
```

---

## 🔄 Потік роботи

### Для нового проекту:
1. **Створити папку**: `Projects/[назва]/`
2. **Написати**: `project-overview.md` — один раз
3. **Створити**: папку `sessions/`

### Для кожної робочої сесії:
1. **Напишіть** файл: `sessions/YYYY-MM-DD-[задача].md`
2. **Залізьте** на project-overview в секції "Пов'язані"
3. **Залізьте** на Tech-Research якщо відповідні

### Для коду:
1. **Додайте** в `Code-Snippets/[мова]-[тема].md`
2. **Залізьте** на проекти де використовується

### Для дослідження:
1. **Додайте** в `Tech-Research/[тема]-[дата].md`
2. **Залізьте** на проекти де застосовується

---

## 📊 Статистика

- **Активних проектів**: [кількість]
- **Завершених сесій**: [кількість]
- **Снипетів**: [кількість]
- **Досліджень**: [кількість]

---

## 🎯 Best Practices

✅ **ПИСАТИ**: Ключові рішення, багі, результати  
❌ **НЕ писати**: Поточний код (він у гіті), дрібні коміти  
📌 **Теги**: Мінімум 2-3 (work, session, category)  
🔗 **Лінки**: На гіт, на пов'язані проекти, на дослідження  
📅 **Дати**: Завжди YYYY-MM-DD для сортування  

---

**Версія**: 2026-04-19  
**Останнє оновлення**: 2026-04-19
