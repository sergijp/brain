---
title: "Марія — docs INDEX"
date: 2026-06-30
tags: [maria, docs, index]
category: docs
project: maria
status: active
aliases: []
pinecone_indexed: false
---

# Марія — Документація (точка входу)

AI нічний диспетчер автобусних перевезень на базі Nous Hermes Agent (self-host, OpenAI).

| Тема | Документ | Статус |
|------|----------|--------|
| Коротке зведення (summary) | [[maria-summary]] | active |
| Детальний план виконання | [[maria-plan]] | active |
| ✅ Чекліст (відмічати кліком) | [[maria-checklist]] | active |
| Поради виконання + відомі проблеми | [[maria-advice]] | active |
| 🔬 Ресьорч каналів 07.2026 (телефон + особисті акаунти) | [[maria-research-channels-2026-07]] | active |
| ТЗ / архітектура (повне) | [[maria-tz]] | active |
| n8n конфіг (воркфлоу + промпт) | [[README]] (папка `n8n/`) | active |

## Швидкі факти
- **Що:** AI нічний диспетчер (Марія), канали: телефон, Telegram, WhatsApp, Instagram, Viber
- **База:** [Nous hermes-agent](https://github.com/nousresearch/hermes-agent) (MIT) на Hostinger VPS 389 ₴/міс
- **LLM:** OpenAI · **Дані:** власна CRM через API (least-privilege)
- **Режим:** нічний, вкл/викл командою зміни від денного диспетчера
