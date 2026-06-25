---
title: "onchul — Фікс фільтрації неактивних зупинок у пошуку рейсів"
date: 2026-06-19
tags: [onchul, work, session, bugfix]
category: session
project: onchul
status: completed
aliases: []
pinecone_indexed: false
---

## Мета сесії
Розслідувати та виправити баг: рейси з неактивними зупинками (поле `active` в таблиці `trip_station`) знаходились при пошуку, хоча не повинні були. Фільтр мав пропускати лише рейси, у яких початкова і кінцева зупинки є активними.

## Виконано

| Задача | Результат |
|--------|-----------|
| Debugger: root cause аналіз | Знайдено, що `Trip::scopeStationsQuery()` не вибирає/не фільтрує поле `active` з таблиці `trip_station` |
| Developer: фікс у Trip.php | Додано SELECT аліаси `from_station_active`, `to_station_active` до JOIN |
| Developer: фікс у TripsService.php | Розширено PHP-фільтр в 2 місцях (основний пошук ~рядок 121 + back-trip ~рядок 151) |
| Developer: фікс у Route.php | Додано SELECT аліаси `active` до JOIN на `trip_station` для інтегрованості |

## Важливі рішення (ADR)

| Рішення | Варіанти | Обрано | Причина |
|---------|----------|--------|---------|
| Де фільтрувати `active` | SQL WHERE у JOIN vs PHP filter на рядку 121 | PHP filter (SELECT аліас + умова в TripsService) | Фільтрація `active` вже розташована в PHP поряд з логікою `boarding`/`unboarding`, простіше утримувати логіку в одному місці |

## Root Cause

`Trip::scopeStationsQuery()` (рядки 274–314 у Trip.php) будує JOIN на таблицю `trip_station` з аліасами `from_stations`/`to_stations`. Поля `boarding` і `unboarding` фільтрувались у PHP (TripsService, рядок 121), але поле `active` — ні. Колонка `active` існувала в таблиці з міграції `2025_08_12_135606_create_trip_station_table.php` і була її частиною, однак SELECT не вибирала цю колонку.

Результат: при пошуку рейсів, навіть якщо від початкової або кінцевої зупинки था `active = 0`, рейс все одно повертався клієнтові.

## Проблеми й як вирішили

| Проблема | Рішення |
|----------|---------|
| Рейси з неактивними зупинками повертались у пошуку | Додано SELECT аліас `from_station_active`, `to_station_active` до JOIN; розширено PHP-фільтр в TripsService на 2 місцях |
| Back-trip також не фільтрував `active` | Та ж логіка додана до другого фільтру (~рядок 151) |

## Артефакти

| Файл | Зміна |
|------|-------|
| `app/Entities/System/Trip.php` | SELECT аліаси `from_station_active`, `to_station_active` у `scopeStationsQuery()` |
| `app/Services/TripsService.php` | PHP-фільтр розширено: рядки ~121 (основний) і ~151 (back-trip) — перевірка на `$trip['from_station_active']` і `$trip['to_station_active']` |
| `app/Entities/System/Route.php` | SELECT аліас `active` у JOIN (для аналогії; Route не потребує PHP-фільтру, але було збільшено інтегрованість) |

## Edge Cases

- **Проміжна неактивна зупинка**: рейс A→B→C, де B неактивна — рейс повинен залишитись, т.к. фільтр дивиться лише на from/to. ✓ Правильна поведінка.
- **Back-trip**: при зворотному маршруті фільтр також змінюється (т.к. from/to розміняються) — обидва фільтри (~121 та ~151) синхронізовані.

## Пов'язані нотатки
- [[onchul-architecture]] — загальна архітектура пошуку рейсів
