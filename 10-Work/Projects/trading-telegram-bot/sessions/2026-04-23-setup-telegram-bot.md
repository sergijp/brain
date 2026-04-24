---
title: Розробка Telegram-бота для TradingView & Gemini
date: 2026-04-23
tags: [trading, bot, telegram, gemini, mcp, voice, python]
category: Development
project: trading-telegram-bot
status: Completed
pinecone_indexed: false
---

# 🤖 Trading Analitic Bot: Технічний огляд

Цей проект реалізує інтелектуального помічника в Telegram, який виступає містком між користувачем та локальною системою аналізу TradingView через Gemini CLI.

## 🌟 Основні можливості
- **Голосове керування (UA):** Використання Python-скрипта `transcribe.py` для розпізнавання української мови через Google Speech API (безкоштовно).
- **Короткострокова пам'ять:** Бот зберігає останні 50 повідомлень у `history.json`, що дозволяє вести контекстний діалог.
- **Пряма інтеграція з TradingView:**
    - Зміна символів (євро, золото, фунт тощо).
    - Створення скріншотів у реальному часі.
    - Виконання ранкового брифінгу (`brief`).
    - Отримання статусу підключення.
- **Чистий вивід:** Автоматичне очищення відповідей Gemini від технічного сміття CLI та ANSI-кольорів.

## 🛠 Технічний стек
- **Runtime:** Node.js (v23)
- **Бот-фреймворк:** `telegraf`
- **Процеси:** `pm2` для 24/7 роботи.
- **Аудіо:** `ffmpeg` (системний) + `pydub` (python) + `SpeechRecognition` (python).
- **ШІ:** Gemini CLI (через системні виклики).

## 📁 Структура файлів
- `/Users/serhiin/AI/telegram-bot/bot.js` — основна логіка бота.
- `/Users/serhiin/AI/telegram-bot/transcribe.py` — місток для розпізнавання голосу.
- `/Users/serhiin/AI/telegram-bot/.env` — конфігурація токенів та ID.
- `/Users/serhiin/AI/telegram-bot/history.json` — база даних пам'яті.

## 🚀 Команди PM2
```bash
pm2 delete trading-bot
pm2 start /Users/serhiin/AI/telegram-bot/bot.js --name "trading-bot"
pm2 restart trading-bot
pm2 logs trading-bot
```

## 📝 Нотатки по налаштуванню
Для роботи голосу на Mac необхідно:
1. `brew install ffmpeg`
2. `python3 -m pip install SpeechRecognition pydub --break-system-packages`

---
**Посилання:** [[~/MyVault/CLAUDE-RULES.md|Правила сесії]]
