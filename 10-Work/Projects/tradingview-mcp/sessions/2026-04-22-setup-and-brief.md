---
title: "Проект: tradingview-mcp — Встановлення, налаштування та перший брифінг"
date: 2026-04-22
tags: [work, session, code, tradingview-mcp, setup, brief]
category: work
project: tradingview-mcp
status: completed
pinecone_indexed: false
---

## 🎯 Мета сесії
Встановити та налаштувати MCP сервер для TradingView, синхронізувати його зі стратегією користувача та провести перший ринковий аналіз.

## ✅ Виконано
- Репозиторій `tradingview-mcp-jackson` клоновано та перенесено до `~/AI/` → успішно.
- Всі залежності встановлено (`npm install`) та створено глобальний лінк `tv` → успішно.
- MCP сервер додано до Gemini CLI (`gemini mcp add`) → успішно.
- Оновлено `rules.json` на основі стратегії SMC + PA Combo v2 з Obsidian → успішно.
- Проведено перший ранковий брифінг (`tv brief`) для всього списку спостереження → отримано Bullish bias по Majors та Gold.

## 🔑 Важливі рішення (ADR)
| Рішення | Причина | Альтернатива |
|---------|---------|-------------|
| Використання Pine Script для малювання Trade Plan | CDP не дозволяє стабільно взаємодіяти з нативними інструментами малювання (drag-and-drop) | Нативні інструменти TV |
| Глобальна пам'ять для правил Obsidian | Щоб агент завжди дотримувався структури ваулту в усіх нових сесіях | Проектна пам'ять |

## 📎 Артефакти
- Файли: `~/AI/tradingview-mcp-jackson/rules.json`
- Команда: `tv brief`

## 🔗 Пов'язані нотатки
- [[10-Work/Projects/tradingview-mcp/project-overview]]
- [[20-Trading/Strategies/smc-playbook-v2]]
- [[20-Trading/Journal/2026-04-21-morning-brief]]
