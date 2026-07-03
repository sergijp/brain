---
title: "Проект: Марія — планування ТЗ AI нічного диспетчера"
date: 2026-06-30
tags: [work, session, maria]
category: session
project: maria
status: completed
aliases: []
pinecone_indexed: false
---

# Марія — планування ТЗ (AI нічний диспетчер)

## Мета сесії

Дослідити і спланувати AI-агента, що відповідає на дзвінки та повідомлення
(телефон, Instagram, Telegram, WhatsApp, Viber) на реальних акаунтах. У ході
сесії визначилось: це **нічний диспетчер «Марія»** для автобусних перевезень.

## Виконано

| # | Задача | Результат |
|---|--------|-----------|
| 1 | Дослідити інструменти по каналах | Voice (Retell/Vapi), WA (офіц. API vs Baileys), TG (Telethon/userbot), IG (офіц. API), Viber (Bot API) |
| 2 | Знайти базовий агент | Nous Research hermes-agent (MIT); Hostinger one-click VPS 389 ₴/міс |
| 3 | Звірити можливості Hermes з вимогами | cron + пам'ять (Honcho) покривають нічний режим та історію; phone/IG/Viber — ні |
| 4 | Зібрати бюджет | MVP ~$20–30/міс, з телефоном ~$55–95/міс |
| 5 | Скласти guardrails під автобусний домен | 3 списки: може / не може / відкладає |
| 6 | Оформити ТЗ у vault | [[maria-tz]] + INDEX + auto-memory pointer |

## Важливі рішення (ADR)

| # | Питання | Рішення | Чому |
|---|---------|---------|------|
| 1 | Акаунти особисті vs бізнес | Гібрид | TG особистий безпечно; WA/IG офіц. бізнес — інакше бан |
| 2 | Базовий агент | Nous hermes-agent на Hostinger VPS | MIT, self-host, вбудовані cron+пам'ять, підтримка OpenAI |
| 3 | LLM | OpenAI (gpt-4o-mini дефолт) | Вибір користувача; mini дешевий для чату |
| 4 | Режим роботи | Нічний, вкл/викл командою зміни | Жива передача зміни від денного диспетчера |
| 5 | Представлення | «Я нічний диспетчер Марія» | Не людина, не наголошує AI |
| 6 | Доступ до даних | Власна CRM через API, least-privilege | Реальні перевірки місць/статусу/заявок, безпечно |
| 7 | Автономію Hermes обмежити | Так | Learning-loop суперечить «строгому скоупу» диспетчера |

## Проблеми й як вирішили

- **Blocker:** Hermes НЕ вміє телефон/Instagram/Viber (всупереч очікуванню «все в одному»).
  - **Рішення:** ці канали — окремими сервісами (Retell/Vapi, офіц. API) поряд із Hermes.
- **Ризик:** WhatsApp-конектор Hermes неофіційний → бан номера.
  - **Рішення:** для WA планувати офіційний Business API окремо.
- **Конфлікт:** автономність Hermes vs строгий скоуп диспетчера.
  - **Рішення:** обмежити learning-loop/автоскіли, жорсткий system-prompt + whitelist.

## Артефакти

- **ТЗ:** `~/MyVault/10-Work/Projects/maria/docs/maria-tz.md`
- **Upstream:** https://github.com/nousresearch/hermes-agent
- **Hostinger:** https://www.hostinger.com/ua/applications/hermes-agent/1

## Пов'язані нотатки

- [[10-Work/Projects/maria/docs/INDEX]]
- [[10-Work/Projects/maria/docs/maria-tz]]
- [[bustrek]], [[buktrek]], [[bustick-admin]]
