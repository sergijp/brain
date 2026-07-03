---
title: "Проект: Марія — ресьорч каналів 07.2026 + план v3"
date: 2026-07-02
tags: [maria, work, session]
category: session
project: maria
status: completed
aliases: []
pinecone_indexed: false
---

# Сесія 2026-07-02 — ресьорч каналів «з чистого аркуша» + план v3

## Мета сесії
1. Зафіксувати поради виконання й відомі проблеми (продовження 30.06)
2. **Не дивлячись на план** — проресьорчити: AI на дзвінки по звичайному телефону
   + відповіді з ОСОБИСТИХ акаунтів Viber/Telegram/WhatsApp (реальні, прив'язані
   до номера, роками веде людина)
3. Оновити план під знахідки
4. Проаналізувати Hermes Agent — чим допоможе

## Виконано
| Задача | Результат |
|--------|-----------|
| Поради + проблеми → vault | [[maria-advice]] (7 порад, 3 таблиці проблем) |
| Ресьорч 4 паралельними агентами (телефон/TG/WA/Viber) | [[maria-research-channels-2026-07]] з джерелами |
| План оновлено v2 → v3 | [[maria-plan]] (нові фази, Viber у Фазі 6) |
| Чекліст синхронізовано | [[maria-checklist]] v3 |
| ADR каналів v3 | [[2026-07-02-kanaly-v3-pislya-researchu]] + створено `decisions/INDEX` |
| Аналіз Hermes Agent v0.18.0 (01.07.2026) | вердикт: ops-наглядач/аналітик для власника, НЕ клієнтський канал |
| Auto-memory pointer оновлено | `architecture_maria.md` (канали v3, last_verified 2026-07-02) |

## Важливі рішення (ADR)
→ [[2026-07-02-kanaly-v3-pislya-researchu]] — 5 рішень: Telegram Business бот
замість Telethon · переадресація→SIP замість обов'язкового Бінотел · Viber через
AutoResponder-хак · WA через конвертацію в Business app + Coexistence ·
Hermes = опційний ops-помічник після Фази 3.

## Ключові знахідки ресьорчу
- **Telegram Business connected bot безкоштовний з 08.05.2026** (Bot API 10.0) —
  головне відкриття, userbot не потрібен, ризик бану 0
- **WhatsApp Coexistence глобальний, Україна ✅**; Twilio/Infobip/Gupshup НЕ вміють
- **Viber: API до особистого акаунта не існує взагалі** (навіть Wappi не має) —
  тільки notification-listener хак
- **SIM-номер у AI-платформу напряму не заводиться** — завжди переадресація → +380 SIP-DID
- Bland AI відпадає (без української); ElevenLabs — найкраща укр. озвучка

## Проблеми й як вирішили
| Проблема | Рішення |
|----------|---------|
| Userbot = ризик заморозки багаторічного акаунта (freeze-хвилі з 2025) | офіційний Telegram Business бот |
| Дзвінок на SIM не доходить до AI | GSM-коди `**21*`/`**61*` → SIP-DID (Zadarma ~$3) → ElevenLabs/Vapi EU |
| Viber глухий по API | AutoResponder for Viber Pro: нотифікація → POST у n8n → `{"replies":[...]}` |

## Артефакти
- `docs/maria-research-channels-2026-07.md` — новий
- `docs/maria-plan.md` — v3 (переписано)
- `docs/maria-checklist.md` — v3 (переписано)
- `docs/maria-advice.md` — новий
- `decisions/2026-07-02-kanaly-v3-pislya-researchu.md` + `decisions/INDEX.md` — нові
- `docs/INDEX.md` — +2 рядки

## Наступні кроки
1. 🤖 Пакет Фази 0: CRM-ендпоінти + ТЗ «Журнал звернень» + критерії BSP
2. 🤖 n8n-флоу Telegram Business (тригер Business Message) + docker-compose
3. 👤 OpenRouter + VPS + Meta-верифікація (день 1)

## Пов'язані нотатки
[[maria-plan]] · [[maria-research-channels-2026-07]] · [[maria-advice]] ·
[[maria-checklist]] · [[maria-tz]] · [[2026-06-30-tz-planuvannya]] · [[INDEX]]
