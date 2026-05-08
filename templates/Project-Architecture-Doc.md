---
title: "{{topic}} — архітектура"
date: {{date:YYYY-MM-DD}}
tags: [{{project}}, architecture, {{subdomain}}]
category: docs
project: {{project}}
status: active
aliases: ["{{project}}-{{topic}}"]
pinecone_indexed: false
last_verified: {{date:YYYY-MM-DD}}
---

# {{topic}}

## Контекст

_Чому ця підсистема існує. Який бізнес-процес обслуговує. Що треба знати, щоб не зламати._

## Діаграма / модель

```
A → B → C
```

_Або таблиця сутностей з ролями._

## Ключові контракти

1. **Контракт 1:** _опис, інваріант_
2. **Контракт 2:** _опис, інваріант_

## Callsite-и (точки виклику в коді)

| Файл | Метод/Лінія | Призначення |
|------|-------------|-------------|
| `app/Services/...` | `methodName()` L42 | _коротко_ |

## Матриці видалень / станів (опційно)

| Подія | Що з A | Що з B |
|-------|--------|--------|
|       |        |        |

## Gotchas / підводні камені

- _Сюрприз 1: чому це не очевидно_
- _Сюрприз 2_

## Пов'язані

- [[INDEX]]
- [[<other-topic>]]
- Tier-2 pointer: `~/.claude/projects/<slug>/memory/architecture_<topic>.md`
- Сесії з тегом `{{project}}` + `{{topic}}`: `~/MyVault/10-Work/Projects/{{project}}/sessions/`
