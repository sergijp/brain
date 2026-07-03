---
title: "Марія — чекліст виконання"
date: 2026-07-02
tags: [maria, checklist, execution]
category: docs
project: maria
status: active
aliases: ["maria-checklist"]
pinecone_indexed: false
last_verified: 2026-07-02
---

# ✅ Марія — чекліст виконання (v3: після ресьорчу 07.2026)

> Клікай по чекбоксах в Obsidian. Деталі — [[maria-plan]]. Ресьорч — [[maria-research-channels-2026-07]].
> 👤 ти · 🤖 я · 🛠️ ERP-розробник · 🏢 провайдер

## ⚡ Прямо зараз
- [ ] 👤 OpenRouter — акаунт + ключ + $10–20
- [ ] 👤 Hostinger VPS (8 GB) + SSH
- [ ] 🤖 Пакет Фази 0 (CRM-ендпоінти + ТЗ журналу + критерії BSP)
- [ ] ~~Telegram api_id/api_hash~~ — **більше не треба** (Business-бот замість userbot)

## Фаза 0 — Розблокувати довгі залежності
- [ ] 👤 Meta Business + FB Page
- [ ] 👤 Подати верифікацію Meta *(1–3 тижні)*
- [ ] 🤖 Список потрібних CRM/TMS ендпоінтів
- [ ] 🛠️ CRM/TMS scoped-токен + доки
- [ ] 🤖 ТЗ на модуль «Журнал звернень»
- [ ] 🛠️ Модуль прийнято в роботу
- [ ] 🤖 Критерії вибору BSP (360dialog/Wati/YCloud; **НЕ Twilio/Infobip**)
- [ ] 👤 BSP обрано
- [ ] 👤🏢 *(опційно)* Лист у Бінотел — лише якщо йдемо «усе-в-одному»

## Фаза 1 — Інфраструктура + n8n-хаб
- [ ] 👤 OpenRouter ключ активний
- [ ] 👤 VPS по SSH (тільки ключі, ufw 22/80/443)
- [ ] 👤🤖 Docker + Docker Compose
- [ ] 🤖👤 n8n у Docker + домен + **HTTPS** (Caddy)
- [ ] 👤🤖 Імпорт `maria-hub-workflow.json` + 3 credentials (OpenRouter/CRM/ERP)
- [ ] 🤖 OpenRouter **fallback-модель** налаштована
- [ ] ✅ Acceptance: n8n-хаб відповідає на тестовий POST по https

## Фаза 2 — MVP: Марія в реальному Telegram ⭐ (Telegram Business)
- [ ] 👤 Вичитати й ухвалити промпт (`n8n/maria-system-prompt.md`)
- [ ] 👤🤖 @BotFather → бот → Bot Settings → **Business Mode → On**
- [ ] 👤 Телефон: Налаштування → Telegram Business → Чат-боти → бот + охоплення + дозвіл «Відповідати»
- [ ] 🤖 n8n: Telegram Trigger (**Business Message**) → AI Agent → reply з `business_connection_id`
- [ ] 🤖 Тимчасовий лог (до готовності ERP-модуля)
- [ ] 🤖 Реальні CRM-ендпоінти у tools (замість плейсхолдерів)
- [ ] 🤝 Прогнати тест-сьют (10 кейсів із [[maria-plan]])
- [ ] ✅ Acceptance: сьют пройдено · вдень мовчить · клієнт бачить ім'я, не «бот»

## Фаза 3 — Журнал + дайджест + зміна
- [ ] 🛠️ Модуль «Журнал звернень» + API готовий
- [ ] 🤖 Лог перемкнуто з тимчасового на ERP
- [ ] 🤖 Флоу «Команди зміни» («приступаєш/закінчуєш зміну» з твого TG)
- [ ] 🤖 Флоу «Ранковий дайджест» 08:00 Києва (спершу `needs-you`)
- [ ] 🤖 Ескалація критичного в реальному часі (не чекаючи ранку)
- [ ] ✅ Acceptance: діалог у журналі · дайджест о 08:00 · команди зміни діють миттєво

## Фаза 4 — Телефон (переадресація → SIP → AI)
- [ ] 👤🤖 Обрати шлях: A) DID + ElevenLabs Agents/Vapi EU, або B) Phonet (усе-в-одному)
- [ ] 🤝 Тест UA-голосів + розпізнавання → голос Марії обрано
- [ ] 🤖 Голосовий агент: той самий промпт + CRM-tools
- [ ] 👤🤖 +380 SIP-DID + SIP-транк у AI-платформу (вхідний дзвінок доходить)
- [ ] 👤🤖 GSM-переадресація на ніч (`**21*<DID>#` / `##002#`) + синхр. з прапорцем зміни
- [ ] 🤖 Транскрипти дзвінків → журнал
- [ ] 🤝 5 тест-дзвінків (розклад/місця/заявка/поза скоупом/перебивання)
- [ ] ✅ Acceptance: нічний дзвінок → Марія голосом + CRM-дані + транскрипт у журналі

## Фаза 5 — WhatsApp + Instagram
- [ ] 👤 Особистий WhatsApp → застосунок **WhatsApp Business** (історія зберігається)
- [ ] 👤 Покористуватись застосунком кілька днів (не лінкувати API того ж дня)
- [ ] 👤🏢 **Coexistence** onboarding: Embedded Signup → Connect existing app → QR
- [ ] 🤖 WA-адаптер: webhook (messages + `smb_message_echoes`) → n8n-хаб → відповідь (200 OK ≤5с)
- [ ] 🤖 IG-адаптер: Instagram Graph API → n8n-хаб → Send DM
- [ ] 🤖 Пропущений дзвінок у месенджері → «зателефонуйте на робочий номер»
- [ ] 🤖 Всі канали пишуть у журнал, нічне вікно спільне
- [ ] ✅ Acceptance: WA/IG уночі → Марія з реальних акаунтів · вдень люди · історія WA ціла

## Фаза 6 — Viber + обкатка й go-live
- [ ] 👤 Android (постійно вкл., battery-opt off) + Viber на робочому номері
- [ ] 🤖👤 AutoResponder for Viber (Pro) → Web Server/API → webhook n8n
- [ ] 🤝 «Тихий» тиждень: щоранку перевіряти ВСІ діалоги
- [ ] 🤖 Тюнінг промпту/guardrails по реальних кейсах
- [ ] 👤 Навчити денну зміну (дайджест, журнал, команди)
- [ ] 🤝 Тест відмовостійкості (вимкнути CRM/LLM → коректна деградація)
- [ ] 🤖 Зафіксувати фінальні правила у [[maria-tz]]
- [ ] ✅ Go-live

## 🔒 Безпека (наскрізно)
- [ ] SSH лише ключі · ufw 22/80/443
- [ ] Секрет-заголовок на webhook n8n
- [ ] Ключі тільки в credentials/env (не в коді, не у vault)
- [ ] CRM-токен scoped + відкликуваний
- [ ] Telegram Business: обмежити охоплення бота (не всі чати)
- [ ] Щотижневий бекап n8n (workflows + credentials)
- [ ] Перевірка X-Hub-Signature-256 (Meta)

## 🛡️ Надійність
- [ ] Docker restart: always на все
- [ ] Healthcheck-флоу: пінг кожні 15 хв → алерт у TG якщо мовчить
- [ ] Fallback-модель OpenRouter перевірена (вимкнути primary у тесті)
- [ ] CRM недоступна → «уточню вранці» + needs-you (НЕ вигадка)
- [ ] WA: нагадування відкривати застосунок ≥1×/13 днів
- [ ] Viber Android: battery-opt off + healthcheck живості

## Відкладено / під питанням
- [ ] Viber офіційний бот (€100/міс) — на користь AutoResponder-хака відкинуто
- [ ] Self-host голосу (LiveKit/Dograh) — лише за >~100k хв/міс
- [ ] Userbot (Kurigram/TDLib) — запас, лише якщо знадобляться групи/вихідні
- [ ] Hermes — експериментальний запас, не в основній схемі

## Пов'язані
- [[maria-plan]] · [[maria-tz]] · [[maria-research-channels-2026-07]] · [[maria-summary]] · [[README]] (n8n) · [[INDEX]]
