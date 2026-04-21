---
title: "TradingView MCP — EURUSD Short Setup ICT OTE"
date: 2026-04-21
tags: [work, session, tradingview-mcp, trading, eurusd, ict]
category: work
project: tradingview-mcp
status: completed
pinecone_indexed: false
---

## Мета сесії
Дослідити можливості TradingView MCP (78 інструментів), проаналізувати EURUSD 1H та 15m, побудувати Short сетап з R:R ≥ 1:3 використовуючи ICT OTE стратегію.

## Виконано

| Задача | Результат |
|--------|-----------|
| Запуск TradingView через MCP | ✅ `tv_launch()` → CDP порт 9222 |
| Аналіз EURUSD 1H (100 свічок) | ✅ Bearish тренд після спайку до 1.18492 |
| Переключення на 15m для входу | ✅ Визначено ICT OTE зону |
| Розміщення Short Position drawing | ✅ Стандартний `short_position` + 3 підписані лінії |
| Налаштування R:R 1:3 | ✅ Entry 1.17880 / SL 1.18100 / TP 1.17220 |
| Drawing "завжди видимий" | ✅ Time span Apr 19 → Sep 2027 через `setPoints` |
| Фікс stop/profit точок | ✅ `setRawPoint(2/3)` для точних рівнів |

## Важливі рішення (ADR)

| Рішення | Альтернатива | Причина |
|---------|-------------|---------|
| Short сетап (не Long) | Long від OTE | Відкидання від 1.185, ринок слабкий |
| Вхід на 15m | Вхід на 1H | Точніший entry, менший стоп |
| R:R 1:3 | R:R 1:2 | Вимога користувача |
| ICT OTE стратегія | Supply/Demand | OTE зона вже є на графіку |

## Активний сетап

```
Пара:      EURUSD
Таймфрейм: 15m (аналіз: 1H)
Стратегія: ICT OTE Short

Entry:     1.17880
Stop Loss: 1.18100  (+220 пунктів)
Take Profit: 1.17220  (-660 пунктів)
R:R:       1:3
```

**Логіка:** Після новинного спайку до 1.18492 різке відкидання. Ринок не може відновити 1.180+. OTE зона на 15m підтверджує. Чекати ретест до 1.17880 з bearish патерном підтвердження.

## Проблеми й як вирішили

| Проблема | Рішення |
|----------|---------|
| `RiskRewardShort` створює `flag` shape | Правильна назва: `'short_position'` |
| Stop/profit не відображались | `setRawPoint(2, stopPrice)` і `setRawPoint(3, profitPrice)` |
| Drawing зникав за межами екрану | `setPoints` з time span від Apr 19 до Sep 2027 |
| CDP connection failed | `tv_launch()` перед будь-якими MCP командами |

## Артефакти

- TradingView drawings на графіку EURUSD 15m (збережені в сесії)
- Screenshots: `~/tradingview-mcp-jackson/screenshots/eurusd_fixed_levels.png`

## Технічні паттерни (для повторного використання)

```javascript
// Правильне створення short_position
cw.createMultipointShape(
  [{ time: lastBarTime, price: entryPrice }],
  { shape: 'short_position', overrides: { stopLevel, profitLevel } }
);

// Фікс stop/profit точок
const obj = cw.getShapeById(id);
obj.setRawPoint(2, { index: 241, price: 1.18100 }); // stop
obj.setRawPoint(3, { index: 241, price: 1.17220 }); // profit

// Завжди видимий drawing
obj.setPoints([
  { price: entry, time: 1776470400 }, // минуле
  { price: entry, time: 1800000000 }  // далеке майбутнє
]);
```

## Пов'язані нотатки
- [[TradingView MCP Tools]]
- [[ICT Trading Strategy]]
- [[EURUSD Analysis]]
