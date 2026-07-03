---
title: "Марія — свіжий ресьорч каналів (липень 2026): реальний телефон + особисті акаунти"
date: 2026-07-02
tags: [maria, research, channels, telegram, whatsapp, viber, phone]
category: docs
project: maria
status: active
aliases: ["maria-research-channels"]
pinecone_indexed: false
last_verified: 2026-07-02
---

# Марія — ресьорч «з чистого аркуша» (липень 2026)

> Питання: як підключити AI-агента (1) на дзвінки по звичайному телефону
> і (2) на відповіді з ОСОБИСТИХ акаунтів Viber / Telegram / WhatsApp,
> які прив'язані до номера й роками ведуться живою людиною.
> 4 паралельні веб-дослідження, стан на 2026-07.

## 🏆 Головні відкриття (міняють план!)

1. **Telegram: userbot більше не потрібен.** З **8 травня 2026 (Bot API 10.0)**
   Telegram Business дозволяє підключити бота до особистого акаунта
   **БЕЗ Premium, безкоштовно, офіційно**. Бот відповідає від імені акаунта,
   клієнт не бачить позначки «бот». Ризик бану = нуль. n8n підтримує нативно
   (Telegram Trigger → "Business Message").
2. **WhatsApp Coexistence доступний глобально** (з ~квітня-травня 2026),
   **Україна підтримується**. Але спершу особистий WhatsApp → WhatsApp Business
   **застосунок** (історія зберігається, ~10 хв). Відповіді через API — безкоштовні.
3. **Viber — як і раніше, глухо.** Жодного API до особистого акаунта не існує
   (навіть неофіційного — Wappi та інші Viber не підтримують). Робочий хак:
   **AutoResponder for Viber** (Android, notification listener) + webhook на
   власний AI-бекенд.
4. **Телефон:** SIM-номер напряму в AI-платформу не заводиться. Схема завжди:
   **умовна переадресація GSM → український SIP-номер → AI-агент**.

---

## 📱 Telegram (особистий акаунт) — ✅ офіційно і безкоштовно

**Шлях: Telegram Business connected bot** (з травня 2026 без Premium):
1. @BotFather → свій бот → Bot Settings → **Business Mode → On**
2. Телефон: **Налаштування → Telegram Business → Чат-боти** → username бота →
   вибрати охоплення (нові чати / не-контакти / виключити контакти) →
   дозвіл «Відповідати на повідомлення»
3. n8n: Telegram Trigger (подія Business Message) → AI Agent →
   відповідь з `business_connection_id`

**Обмеження:** тільки приватні 1-на-1 чати (не групи), не ініціює нові розмови
(відповідь лише в чатах, активних за останні 24 год), один бот на акаунт.
Для нашого кейсу (вхідні від клієнтів) — ідеально.

**Userbot (Telethon/Kurigram/TDLib)** — лишається тільки якщо потрібні групи
або вихідні. Стан: Pyrogram мертвий; Telethon переїхав на Codeberg; найживіші —
Kurigram і TDLib. Ризик: з 2025 Telegram морозить акаунти (FROZEN) — небезпечно
для багаторічного особистого акаунта. **Висновок: Telethon-адаптер з плану v2
замінюємо на Telegram Business бота.**

## 💬 WhatsApp (особистий акаунт) — ✅ через Coexistence

**Шлях (найбезпечніший):**
1. Особистий WhatsApp → **WhatsApp Business застосунок** (той самий номер,
   бекап → міграція, вся історія і контакти зберігаються; клієнти бачать
   одноразову плашку «бізнес-акаунт»)
2. Покористуватись кілька днів/тижнів (не лінкувати API в той самий день)
3. Meta Business Portfolio → Embedded Signup → «Connect existing WhatsApp
   Business app» → QR з телефона → синк 6 міс історії (~6 год)
4. Webhook (messages + `smb_message_echoes`) → n8n WhatsApp node → AI

**Факти:** людина далі користується застосунком як завжди (двосторонній
дзеркальний синк); відповіді у 24-год вікні — **безкоштовні**; треба відкривати
застосунок раз на ≤13 днів, інакше лінк відпадає. Групи через API НЕ працюють;
вимикаються edit/revoke/зникаючі/view-once.

**BSP:** підтримують Coexistence — 360dialog, Wati, respond.io, YCloud (або
напряму Meta Cloud API без BSP). **НЕ підтримують — Twilio, Infobip, Gupshup.**

**Політика Meta (15.01.2026):** заборонені general-purpose чат-боти (ChatGPT
тощо), але **бізнес-агенти підтримки/бронювання явно дозволені** — Марія легальна.

**Неофіційні API** (Evolution API, WAHA, Baileys, Green API): живі, для
reply-only на старому акаунті бан-рейт <2%/рік, АЛЕ хвиля банів жовтня 2025
косила навіть 3-річні reply-боти. Втрата багаторічного номера незворотна →
не варто, коли є Coexistence.

## 🟣 Viber (особистий акаунт) — ⚠️ тільки хак

- API до особистого акаунта **не існує** — ні офіційного, ні реверснутого,
  ні SaaS (Wappi Viber не має). Аналога Telegram Business / Coexistence немає.
- Офіційний Viber-бот: **€100/міс** мінімум (актуально і у 2026) + верифікація;
  це окрема сутність, не особистий акаунт.
- **Робочий варіант: AutoResponder for Viber** (TK Studio, Android):
  читає нотифікації (NotificationListenerService), відповідає через inline-reply.
  Pro-фіча «Connect to Web Server»: POST JSON {sender, message} → наш n8n →
  `{"replies":[{"message":"..."}]}` → повний AI. Дешево (кілька $).
  - Потрібен постійно увімкнений Android з Viber (вимкнути battery optimization)
  - Тільки відповіді на вхідні; довгі повідомлення можуть обрізатись у нотифікації
  - Сіра зона ToS, але reply-only малооб'ємно — ризик низький
- Аналогічні застосунки TK Studio є для WhatsApp/Telegram — запасний план Б
  для всіх месенджерів одразу (якщо захочемо максимально просто).

## ☎️ Телефон (звичайний мобільний номер)

**Базова схема:** `Клієнт → SIM-номер → переадресація → +380 SIP-номер → AI`

**Переадресація GSM (всі оператори):**
- `**21*380XXXXXXXXX#` — безумовна (вмикати на ніч, вимикати вранці `##002#`)
- `**61*…**20#` — якщо не відповіли за 20 с; `**67*` — зайнято; `**62*` — недоступний
- Київстар/Vodafone: хвилини за тарифом (у пакеті = безкоштовно);
  lifecell: +~1 грн/дзвінок. Kyivstar prepaid — лише безумовна.
- ⚠️ Переадресовувати ТІЛЬКИ на український номер (на закордонний = міжнародні тарифи)

**Куди переадресовувати (варіанти за простотою):**

| # | Варіант | Що це | Ціна | Коментар |
|---|---------|-------|------|----------|
| 1 | **Phonet AI-асистент** | укр. АТС з готовим AI | АТС ~200-500 грн/міс + ~9.15 грн/хв | найпростіше, все українською, є freemium |
| 2 | **Zadarma** UA-номер + AI/IVR | дешевий DID + вбудований бот | ~$2-5/міс номер | DIY, є укр. розпізнавання |
| 3 | **DIDWW/Binotel SIP DID → ElevenLabs Agents** | SIP-транк у AI-платформу | ~$0.08-0.10/хв | найкраща укр. озвучка (Multilingual v2) |
| 4 | те саме → **Vapi (EU: sip.eu.vapi.ai)** | BYO SIP transport безкоштовний | $0.12-0.25/хв | Deepgram Nova-3 має укр. + гнучкі tools |
| 5 | **Kyivstar FMC** (Віртуальна мобільна АТС) | SIM-номер стає внутр. лінією АТС з API | бізнес-пакет | без переадресації взагалі, найчистіше, але треба конвергентний контракт |
| 6 | sip-gsm.in.ua | контрактний Kyivstar-номер → чистий SIP | від 1050 грн/міс | тільки юрособи/ФОП |
| 7 | GSM-шлюз (GoIP) | SIM у залізці → SIP | ~$50-200 разово | якість/блокування SIM — не для продакшену |

- **Bland AI — відпадає** (немає української). Retell — укр. не підтверджена.
- Українська STT — найслабша ланка (суржик, назви міст) — тест до запуску.
- Жоден укр. оператор нативного AI-автовідповідача не має (Ringostat AI = аналітика).

---

## 🧭 Зведена рекомендація (липень 2026)

| Канал | Шлях | Ризик бану | Вартість |
|-------|------|-----------|----------|
| Telegram | **Telegram Business бот** (офіційно) | 0 | $0 |
| WhatsApp | особистий → **WA Business app → Coexistence → Cloud API** | ~0 | $0 (відповіді) |
| Viber | **AutoResponder for Viber** + webhook → n8n | низький (сіра зона) | ~$5 разово + Android |
| Телефон | переадресація → SIP DID → **ElevenLabs Agents / Phonet** | 0 | ~$0.10-0.22/хв |

Мозок для всіх чотирьох — той самий n8n-хаб (webhook → AI Agent → CRM tools → журнал).

## Наслідки для плану ([[maria-plan]])
- Фаза 2: **Telethon-адаптер → замінити на Telegram Business бота** (простіше, офіційно, n8n нативно; MVP стає ще швидшим)
- Фаза 4: Бінотел не обов'язковий — достатньо GSM-переадресації на SIP DID; Бінотел/Phonet — як варіант «усе в одному»
- Фаза 5: Coexistence підтверджено для України; BSP-список: 360dialog/Wati/YCloud або напряму Meta; Twilio/Infobip виключити
- Viber: із «відкладено» → у план як AutoResponder-хак (дешевий)

## Пов'язані
- [[maria-plan]] · [[maria-tz]] · [[maria-advice]] · [[INDEX]]

## Джерела (ключові)
- Telegram: core.telegram.org/bots/api-changelog (Bot API 10.0, 2026-05-08) · core.telegram.org/api/bots/connected-business-bots · docs.n8n.io Telegram Trigger
- WhatsApp: docs.360dialog.com/docs/resources/phone-numbers/coexistence · developers.facebook.com Embedded Signup · chakrahq.com coexistence support checker · twilio.com/docs/whatsapp/self-sign-up (не підтримує)
- Viber: help.viber.com Bot commercial model (€100/міс) · autoresponder.ai/viber (webhook API)
- Телефон: docs.vapi.ai/advanced/sip/sip-trunk · elevenlabs.io SIP trunking · phonet.ua AI-асистент · zadarma.com · didww.com · fmc.kyivstar.ua
