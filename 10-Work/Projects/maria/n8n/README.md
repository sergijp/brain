---
title: "Марія — n8n конфіг (README)"
date: 2026-07-01
tags: [maria, n8n, config, setup]
category: docs
project: maria
status: active
aliases: ["maria-n8n"]
pinecone_indexed: false
---

# Марія — n8n конфіг

Файли:
- `maria-hub-workflow.json` — головний воркфлоу (вхідне → нічне вікно → AI Agent (OpenRouter + CRM tools) → лог у журнал → відповідь)
- `maria-system-prompt.md` — промпт Марії (той самий для n8n / Vapi / Telethon)

## Що робить воркфлоу

```
POST /webhook/maria-incoming   {channel, contact, name, text}
        │
   Normalize + Shift Check      # час Києва 22–08 або MARIA_SHIFT=on
        │
   Is Night Shift? ──ні──► Day: No-op (human)   # вдень мовчить, віддає людям
        │так
   Maria Brain (AI Agent)       # OpenRouter + пам'ять по контакту + CRM-tools
        │
   Log to Journal (ERP)         # запис звернення + статус
        │
   Reply                         # {reply: "..."} назад у канал
```

## Передумови — створити 3 credentials у n8n

| Credential | Тип | Для чого |
|---|---|---|
| **OpenRouter (Maria)** | OpenRouter API | LLM |
| **CRM API (Maria, scoped)** | Header Auth | розклад/місця/заявка (least-privilege) |
| **ERP Journal API** | Header Auth | запис у «Журнал звернень» |

## Плейсхолдери — замінити перед запуском

| У файлі | На що |
|---|---|
| `REPLACE_OPENROUTER_CRED` | id credential OpenRouter |
| `REPLACE_CRM_CRED` | id credential CRM |
| `REPLACE_ERP_CRED` | id credential ERP |
| `https://YOUR_CRM_HOST/api/schedule` | реальний ендпоінт розкладу |
| `https://YOUR_CRM_HOST/api/requests` | реальний ендпоінт заявок |
| `https://YOUR_ERP_HOST/api/journal` | ендпоінт журналу звернень |
| `anthropic/claude-3.5-sonnet` | обрана модель OpenRouter (актуальний slug) |

> Ендпоінти й поля CRM/ERP — узгодити з розробником (Фаза 0). Тут — приклад-каркас.

## Імпорт (кроки)

1. n8n → **Workflows** → **Import from File** → обрати `maria-hub-workflow.json`
2. Створити 3 credentials (вище) → у кожному вузлі підставити свій credential
3. Замінити плейсхолдери URL/модель
4. Відкрити **Incoming Message** → скопіювати **Production Webhook URL** (це його дає канал: Telethon userbot / WhatsApp BSP / Instagram Trigger)
5. **Save** → **Activate**

## Як під'єднуються канали

- **Telegram (реальний):** Telethon userbot робить `POST` на цей webhook `{channel:"telegram", contact, name, text}` і відправляє `reply` назад у чат.
- **WhatsApp (Coexistence/BSP):** BSP шле вхідні на цей webhook; відповідь `reply` → назад через API BSP. (Або окремий WA-вузол.)
- **Instagram:** Instagram Trigger → цей флоу → Send DM.
- **Телефон:** окремо (Бінотел → Vapi), той самий промпт+tools.

## Нічний режим / зміна

- **Авто:** час Києва 22:00–08:00 (вузол `Normalize + Shift Check`).
- **Ручний перекрив:** змінна оточення `MARIA_SHIFT=on|off|auto`.
- Команду «приступаєш/закінчуєш зміну» можна зробити окремим міні-флоу, що ставить цю змінну / прапорець у БД.

## Ще зробити (окремі воркфлоу)

- [ ] **Ранковий дайджест** — Cron 08:00 → GET журнал за ніч → підсумок → Telegram тобі
- [ ] **Команди зміни** — вхідний тригер «приступаєш/закінчуєш зміну» → перемикач прапорця
- [ ] Розрізнення каналів на відповіді (гілки WhatsApp/IG send)

## ⚠️ Нюанс версій

Типи вузлів LangChain (`@n8n/n8n-nodes-langchain.*`) і `typeVersion` залежать від версії n8n. Якщо при імпорті вузол «червоний» — відкрий його, обери актуальну версію/модель, збережи. Каркас і зв'язки лишаються.

## Пов'язані
- [[maria-plan]] · [[maria-tz]] · [[maria-checklist]]
