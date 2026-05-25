---
title: "Проект: 3g — Сесія Busfor API transfer fixes"
date: 2026-05-19
tags: [work, session, code, 3g, busfor, api, transfer]
category: work
project: 3g
status: completed
pinecone_indexed: false
---

## 🎯 Мета сесії
Виправити відображення внутрішніх трансферів у Busfor API `/trips`, прибрати `bus_transfer`, узгодити документацію з кодом, розслідувати кейс `from=32, to=10`.

## ✅ Виконано

- **TripListResource**: внутрішній трансфер визначається через `$this->originalStations->firstWhere('transplantation', true)` — отримує station_id, time_arrival, time без додаткової логіки
- **TripsService**: `getAdditionalOptionsTrip()` тепер просто ставить `$trip->is_internal_transfer = true`; всі обчислення перенесено в ресурс
- **`bus_transfer`** — видалено з API і документації
- **Назва рейсу**: для внутрішнього трансферу береться `$this->name` (назва маршруту), для мульти-рейсу — конструюється з станцій
- **Документація** (`public/docs/v1/busfor/index.html`): звірено з кодом, додано відсутнє поле `discounts` у таблицю Response fields ендпоінту `/route`
- **Розслідування `from=32, to=10`**: поведінка коректна — пасажир їде до точки пересадки (station_id=10), другий автобус не потрібен, `is_transfer: false` правильно

## 🔑 Важливі рішення (ADR)

| Рішення | Причина | Альтернатива |
|---------|---------|-------------|
| Дані пересадки брати з `transplantation=true` TripStation | Не залежить від напрямку рейсу, уникає directional logic | Обчислювати в TripsService і передавати як property |
| `is_internal_transfer = true` — єдине що ставить TripsService | Мінімальний код, вся логіка в ресурсі | Передавати готові дані arrival/departure |
| Умова `transfer_station.station_id != to_id` | Якщо пункт призначення = точка пересадки, другий автобус не потрібен | Завжди показувати трансфер |

## 🐛 Проблеми й як вирішили

### Баг: невірна трансферна станція в одному напрямку
- **Причина**: `transfer_station_id` вказував на пункт призначення (Istanbul=24) замість точки пересадки (Chernivtsi=10)
- **Вирішення**: використати `transplantation=true` TripStation напряму — не залежить від напрямку

### Баг: `from=32, to=10` показував відсутність трансферу
- **Причина**: не баг — station 10 є точкою пересадки І пунктом призначення, умова `transfer_station.station_id != to_id` коректно повертає false
- **Вирішення**: підтверджено логами (from_order=0, to_order=8 = order трансферної станції)

## 📎 Артефакти
- `app/Services/Api/v1/Busfor/Resources/TripListResource.php`
- `app/Services/TripsService.php`
- `public/docs/v1/busfor/index.html`

## 🔗 Пов'язані нотатки
- [[10-Work/Projects/3g/project-overview]]