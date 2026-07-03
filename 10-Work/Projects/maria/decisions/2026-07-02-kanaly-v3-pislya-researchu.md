---
title: "ADR: Канали v3 після ресьорчу 07.2026 — офіційні шляхи замість userbot"
date: 2026-07-02
tags: [maria, adr, decision, channels]
category: decision
project: maria
status: accepted
aliases: ["adr-kanaly-v3"]
pinecone_indexed: false
---

# ADR: Канали v3 — офіційні шляхи замість userbot (2026-07-02)

## Контекст
Свіжий ресьорч «з чистого аркуша» ([[maria-research-channels-2026-07]]) показав, що
з травня 2026 ландшафт змінився: з'явились офіційні шляхи до реальних акаунтів.

## Рішення

| # | Рішення | Замість чого | Чому |
|---|---------|--------------|------|
| 1 | **Telegram: Telegram Business connected bot** | Telethon-userbot | з 08.05.2026 (Bot API 10.0) безкоштовно, без Premium, офіційно; відповідає від імені акаунта; ризик бану 0; n8n нативно |
| 2 | **Телефон: GSM-переадресація → SIP-DID → ElevenLabs Agents/Vapi EU/Phonet** | Бінотел як обов'язковий фронт | SIM напряму в AI не заводиться; переадресація `**21#`/`**61#` + дешевий DID достатні; Бінотел → опційний |
| 3 | **Viber: AutoResponder for Viber (Android notification-listener) + webhook n8n** | «відкладено» / бот €100/міс | API до особистого акаунта не існує (навіть неофіційного); reply-only хак дешевий і робочий |
| 4 | **WhatsApp: особистий → WA Business app → Coexistence → Cloud API** | (уточнення v2) | Coexistence глобальний з ~04-05.2026, Україна ✅; BSP: 360dialog/Wati/YCloud; Twilio/Infobip НЕ вміють |
| 5 | **Hermes Agent: опційний ops-наглядач/аналітик ДЛЯ ВЛАСНИКА** (після Фази 3) | роль у клієнтських каналах | v0.18.0: shell+cron+Telegram-бот = моніторинг інфри + тижневий аналіз журналу; клієнтам не відповідає |

## Наслідки
- Фаза 2 (MVP Telegram) спростилась до 1–2 днів, api_id/api_hash не потрібні
- Бінотел зійшов з критичного шляху Фази 0
- Viber переїхав у Фазу 6 як реальний канал
- План: [[maria-plan]] v3 · Чекліст: [[maria-checklist]] v3

## Пов'язані
[[maria-research-channels-2026-07]] · [[maria-plan]] · [[maria-tz]]
