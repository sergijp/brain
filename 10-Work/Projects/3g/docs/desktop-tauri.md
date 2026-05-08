---
title: "Desktop Tauri — research only"
date: 2026-05-08
tags: [3g, architecture, desktop, tauri, research]
category: docs
project: 3g
status: research
aliases: ["3g-desktop", "3g-tauri"]
pinecone_indexed: false
---

# Desktop Wrapper для адмінки 3G — Tauri research

**Стан:** research-only, не імплементовано.

**Why:** користувач питав, як перетворити адмінку на Mac/Windows додаток із захистом коду + auto-update із мінімальними витратами. Розглядали два варіанти:
- A — сервер тримає API+БД, десктоп — UI обгортка
- B — БД на сервері, логіка в клієнті

## Архітектурне рішення

**Варіант A на Tauri** (не Electron). Сервер залишається без змін. Tauri виграє:
- Розміром: ~15 MB vs ~150 MB у Electron.
- Захистом коду: Rust shell vs `app.asar`.
- Рідним підписаним updater'ом.

## Rust-складність — мінімальна

~95% коду = Vue/JS як зараз. Rust потрібен тільки якщо триматимуть:
- Друк квитків на термопринтер
- COM-порт
- Фіскальний реєстратор у десктопі

Тоді +200-500 рядків Rust і 2-3 тижні навчання.

## Phases (готовий план)

### Phase 1 — MVP за 3 години

- `tauri init`
- Окремий `vite.config.desktop.js`
- `VITE_API_BASE_URL`
- CORS `tauri://localhost`

### Phase 2 — signing (1-3 дні Identity Validation)

- Apple Developer $99/рік
- Azure Trusted Signing ~$10/міс

### Phase 3 — auto-updater

- Endpoint `/api/desktop/updates/{target}/{version}`
- ed25519 ключі
- `@tauri-apps/plugin-updater`

### Phase 4 — GitHub Actions matrix

- `macos-latest` + `macos-13` + `windows-latest`

## Безкоштовний локальний workflow

- Mac `.dmg` локально.
- Windows `.msi` через UTM (Win 11 ARM ISO безкоштовний на Apple Silicon) або GitHub Actions free tier (2000 хв/міс).
- Платити треба тільки коли йдеш у масовий продаж і не хочеш warning'ів у клієнтів.

## Артефакти

- План: `~/.claude/plans/bright-spinning-whisper.md`
- Початкова сесійна нотатка: `~/MyVault/00-Inbox/2026-05-05-3g-desktop-tauri-research.md`

## How to apply

Якщо в майбутньому повертається задача "робимо desktop app для 3G" — **НЕ** починати з нуля. Читати готовий план у `~/.claude/plans/bright-spinning-whisper.md`.

## Пов'язані

- [[INDEX]]
- [[legacy-controllers]] — апгрейд L10→L11 потрібен паралельно (хоча для Tauri це не блокер)
