---
title: "Проект: SMC Dashboard — Glassmorphism редизайн + сканер"
date: 2026-04-27
tags: [work, session, dashboard, trading, smc]
category: work
project: dashboard
status: completed
pinecone_indexed: false
---

## Мета сесії
Переробити SMC Trading Dashboard з новим glassmorphism дизайном із шаблону, виправити сканер `claudescaner.mjs`, налаштувати pm2 автозапуск.

## Виконано

### Дизайн дашборду
- Повний перепис `dashboard.html` під glassmorphism шаблон (template/index.html)
- CSS змінні точно як у шаблоні: `--text-strong`, `--glass-panel`, `--glass-hover`, `--glass-solid`, `--solid-bg`
- Видалено `font-size: 13px` з body (причина некоректних розмірів шрифтів)
- `font-family: 'Inter', -apple-system, sans-serif` — точно як у шаблоні
- Темна тема: `rgba(30,41,59,0.6)` glass замість прозорого білого
- Розміри: `.price` 2.2rem, `.badge` 0.75rem, `.filters` 0.9rem, `.widget-header` 0.85rem
- Графіки: SVG з `preserveAspectRatio="xMidYMid meet"`, ViewBox 250×140, все всередині одного SVG
- Новини переїхали в sidebar (вертикально), нижньої панелі немає
- Lucide іконки замість emoji

### Сканер claudescaner.mjs
- **Причини вильотів виправлено:**
  - `ohlcv --count=20 --timeframe=60` → `ohlcv --count=20` (`--timeframe` не існує в CLI)
  - Верифікація `quote` без символу → `state` (надійніше)
  - Відсутній `try/catch` у `scanPair` → додано
  - `main()` без `.catch()` → `main().catch(...)`
  - Таймаут `execSync` → `spawnSync` з `SIGKILL` та 25s таймаут
- Скрипт стабільно проходить всі 5 пар (~70 сек/цикл)

### pm2 налаштування
- `pm2 start claudescaner.mjs --name claudescaner --restart-delay=5000 --max-restarts=100`
- `pm2 save` — стан збережено
- При вильоті автоматично перезапускається через 5 сек

## Важливі рішення (ADR)

| Рішення | Обґрунтування |
|---|---|
| `spawnSync` + SIGKILL замість `execSync` | `execSync` на macOS ігнорує SIGTERM, процес зависає назавжди |
| Верифікація через `state` а не `quote` | `quote` без аргументу не повертає `symbol` поле |
| Без `--timeframe` у ohlcv | CLI не підтримує цей прапор |
| pm2 без `--log` редіректу | Скрипт сам пише в лог-файл; подвійний редірект дублює рядки |
| Темна тема glass: `rgba(30,41,59,0.6)` | Прозорий білий на темному фоні не читається |

## Проблеми й як вирішили

| Проблема | Рішення |
|---|---|
| Шрифти не ті — менші ніж у шаблоні | `font-size: 13px` на body скорочував rem. Видалено |
| Графіки виглядали по-іншому | Перехід на один SVG з `xMidYMid meet` як у шаблоні |
| Сканер зависав на GBPUSD | `execSync` timeout не вбивав процес → `spawnSync` + SIGKILL |
| ETIMEDOUT у перший цикл | TradingView "прокидається" повільно → таймаут 12s → 25s |
| Подвійні рядки в лозі | pm2 + fs.appendFileSync писали в один файл → прибрано `--log` з pm2 |

## Артефакти

| Файл | Опис |
|---|---|
| `/Users/serhiin/AI/dashboard/dashboard.html` | Головний SPA дашборду |
| `/Users/serhiin/AI/dashboard/claudescaner.mjs` | Сканер TradingView MCP |
| `/Users/serhiin/AI/dashboard/server.js` | Express сервер (порт 8765) |
| `/Users/serhiin/AI/dashboard/pairs/*.json` | Дані по кожній парі |
| `/Users/serhiin/AI/dashboard/claudescaner.log` | Лог сканера |
| `/Users/serhiin/AI/dashboard/template/` | Оригінальний дизайн-шаблон |

## Команди

```bash
# Сервер
node /Users/serhiin/AI/dashboard/server.js

# Сканер через pm2
pm2 start claudescaner   # запустити
pm2 stop claudescaner    # зупинити
pm2 restart claudescaner # перезапустити
pm2 status               # статус

# Лог сканера
tail -f /Users/serhiin/AI/dashboard/claudescaner.log

# Автостарт після перезавантаження Mac (один раз з sudo)
sudo env PATH=$PATH:/Users/serhiin/.nvm/versions/node/v23.11.1/bin \
  /Users/serhiin/.nvm/versions/node/v23.11.1/lib/node_modules/pm2/bin/pm2 \
  startup launchd -u administrator --hp /Users/serhiin
```

## Пов'язані нотатки
- [[dashboard]] — проект дашборду
