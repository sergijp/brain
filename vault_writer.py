#!/usr/bin/env python3
"""
Claude Session Logger — автоматично пише сесії в Obsidian vault

Використання:
    python vault_writer.py --type work --project my-project --tasks "Task 1, Task 2" --decisions "Decision 1" --bugs "Bug 1"
    python vault_writer.py --type trading --action journal --date 2026-04-19
"""

import os
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict
import argparse
import re


class VaultWriter:
    def __init__(self, vault_path: str = "~/MyVault"):
        self.vault_path = Path(vault_path).expanduser()
        if not self.vault_path.exists():
            raise FileNotFoundError(f"Vault not found at {vault_path}")

    def sanitize_slug(self, text: str) -> str:
        """Перетворити текст в kebab-case для імен файлів"""
        text = text.lower().strip()
        text = re.sub(r'[^\w\s-]', '', text)
        text = re.sub(r'[-\s]+', '-', text)
        return text.strip('-')

    def format_yaml_header(self, data: Dict) -> str:
        """Створити YAML frontmatter"""
        yaml = "---\n"
        for key, value in data.items():
            if isinstance(value, list):
                yaml += f"{key}: {json.dumps(value)}\n"
            elif isinstance(value, bool):
                yaml += f"{key}: {'true' if value else 'false'}\n"
            else:
                yaml += f"{key}: {value!r}\n"
        yaml += "---\n\n"
        return yaml

    def write_project_session(self, project_name: str, date: Optional[str] = None,
                            tasks: Optional[List[str]] = None,
                            decisions: Optional[List[Dict]] = None,
                            bugs: Optional[List[Dict]] = None) -> Path:
        """Написати сесію проекту в 10-Work/Projects/[project]/sessions/"""

        date = date or datetime.now().strftime("%Y-%m-%d")
        project_slug = self.sanitize_slug(project_name)

        # Створити структуру папок
        project_dir = self.vault_path / "10-Work" / "Projects" / project_slug
        sessions_dir = project_dir / "sessions"
        sessions_dir.mkdir(parents=True, exist_ok=True)

        # Ім'я файлу
        task_summary = self.sanitize_slug(tasks[0][:30]) if tasks else "session"
        filename = f"{date}-{task_summary}.md"
        filepath = sessions_dir / filename

        # YAML header
        yaml_data = {
            "title": f"Проект: {project_name} — Сесія {date}",
            "date": date,
            "tags": ["work", "session", "code", project_slug],
            "category": "work",
            "project": project_slug,
            "status": "completed",
            "pinecone_indexed": False
        }

        content = self.format_yaml_header(yaml_data)

        # Мета
        content += "## 🎯 Мета сесії\n"
        content += "[Вручну додайте або автоматично填нено]\n\n"

        # Виконано
        if tasks:
            content += "## ✅ Виконано\n"
            for task in tasks:
                content += f"- {task}\n"
            content += "\n"

        # Рішення
        if decisions:
            content += "## 🔑 Важливі рішення (ADR)\n"
            content += "| Рішення | Причина | Альтернатива |\n"
            content += "|---------|---------|-------------|\n"
            for dec in decisions:
                content += f"| {dec.get('decision', '')} | {dec.get('reason', '')} | {dec.get('alternative', '')} |\n"
            content += "\n"

        # Помилки
        if bugs:
            content += "## 🐛 Проблеми й як вирішили\n"
            for bug in bugs:
                content += f"### {bug.get('name', 'Баг')}\n"
                content += f"- **Контекст**: {bug.get('context', '')}\n"
                content += f"- **Причина**: {bug.get('reason', '')}\n"
                content += f"- **Вирішення**: {bug.get('solution', '')}\n\n"

        # Артефакти
        content += "## 📎 Артефакти\n"
        content += "- Файли: [додайте посилання]\n\n"

        # Пов'язані
        content += "## 🔗 Пов'язані нотатки\n"
        content += f"- [[10-Work/Projects/{project_slug}/project-overview]]\n"

        # Записати файл
        filepath.write_text(content, encoding="utf-8")
        return filepath

    def write_trading_journal(self, date: Optional[str] = None,
                             trades: Optional[List[Dict]] = None,
                             observations: Optional[List[str]] = None,
                             mistakes: Optional[List[str]] = None) -> Path:
        """Написати трейдинг journal в 20-Trading/Journal/"""

        date = date or datetime.now().strftime("%Y-%m-%d")
        journal_dir = self.vault_path / "20-Trading" / "Journal"
        journal_dir.mkdir(parents=True, exist_ok=True)

        filename = f"{date}-trading-session.md"
        filepath = journal_dir / filename

        yaml_data = {
            "title": f"Трейдинг: {date}",
            "date": date,
            "tags": ["trading", "journal", "session"],
            "category": "trading",
            "status": "completed",
            "pinecone_indexed": False
        }

        content = self.format_yaml_header(yaml_data)

        # Огляд
        content += "## 📊 Огляд дня\n"
        content += "- **Депозит**: $10,000\n"
        content += f"- **Дата**: {date}\n\n"

        # Угоди
        if trades:
            content += "## 📈 Угоди виконані\n"
            content += "| Пара | Вхід | Вихід | P&L | Статус |\n"
            content += "|------|------|-------|-----|--------|\n"
            for trade in trades:
                pnl_str = str(trade.get('pnl', '0'))
                # Спробуємо перевести в число для порівняння
                try:
                    pnl_val = float(pnl_str.replace('+', '').replace('$', ''))
                    status = "✅ win" if pnl_val > 0 else "❌ loss"
                except:
                    status = "⚪ pending"
                content += f"| {trade.get('pair', '')} | {trade.get('entry', '')} | {trade.get('exit', '')} | {pnl_str} | {status} |\n"
            content += "\n"

        # Спостереження
        if observations:
            content += "## 💡 Ключові спостереження\n"
            for obs in observations:
                content += f"- {obs}\n"
            content += "\n"

        # Помилки
        if mistakes:
            content += "## ⚠️ Помилки й навчання\n"
            for i, mistake in enumerate(mistakes, 1):
                content += f"### Помилка {i}\n"
                content += f"{mistake}\n\n"

        # План
        content += "## 🎯 План на завтра\n"
        content += "- [Додайте план]\n"

        filepath.write_text(content, encoding="utf-8")
        return filepath

    def write_trading_analysis(self, pair: str, date: Optional[str] = None,
                              levels: Optional[Dict] = None,
                              trend: Optional[str] = None,
                              entry_conditions: Optional[List[str]] = None,
                              tp_sl: Optional[Dict] = None) -> Path:
        """Написати трейдинг аналіз в 20-Trading/Analysis/"""

        date = date or datetime.now().strftime("%Y-%m")
        analysis_dir = self.vault_path / "20-Trading" / "Analysis"
        analysis_dir.mkdir(parents=True, exist_ok=True)

        pair_slug = self.sanitize_slug(pair)
        filename = f"{pair_slug}-analysis-{date}.md"
        filepath = analysis_dir / filename

        yaml_data = {
            "title": f"{pair} — Аналіз {date}",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "tags": ["trading", "analysis", pair_slug],
            "category": "trading",
            "status": "active",
            "pinecone_indexed": False
        }

        content = self.format_yaml_header(yaml_data)

        content += f"## 🎯 Пара: {pair}\n\n"

        # Рівні
        if levels:
            content += "## 📊 Технічні рівні\n"
            for key, value in levels.items():
                content += f"- **{key}**: {value}\n"
            content += "\n"

        # Тренд
        if trend:
            content += "## 📈 Тренд\n"
            content += f"{trend}\n\n"

        # Сценарії
        content += "## 💡 Сценарії\n"
        content += "1. **Bullish**: [Опис] → Ціль: ...\n"
        content += "2. **Bearish**: [Опис] → Ціль: ...\n\n"

        # Умови входу
        if entry_conditions:
            content += "## ✅ Умови входу (Bullish)\n"
            for cond in entry_conditions:
                content += f"- {cond}\n"
            content += "\n"

        # TP/SL
        if tp_sl:
            content += "## 🎯 Технічна угода\n"
            for key, value in tp_sl.items():
                content += f"- **{key}**: {value}\n"
            content += "\n"

        content += "## 📝 Примітки\n"
        content += "- [Додайте контекст, новини, тощо]\n"

        filepath.write_text(content, encoding="utf-8")
        return filepath


def main():
    parser = argparse.ArgumentParser(
        description="Claude Session Logger для Obsidian vault",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Приклади:
  # Проект сесія
  python vault_writer.py --type work --project "my-api" \\
    --tasks "Setup database" "Configure auth" \\
    --decisions '{"decision": "Used PostgreSQL", "reason": "Better scaling"}' \\
    --bugs '{"name": "Migration timeout", "solution": "Increased timeout to 30s"}'

  # Трейдинг журнал
  python vault_writer.py --type trading --action journal \\
    --trades '{"pair": "EURUSD", "entry": "1.0950", "exit": "1.0970", "pnl": "200"}' \\
    --observations "EUR trending up" "Bank news impact"

  # Трейдинг аналіз
  python vault_writer.py --type trading --action analysis --pair EURUSD \\
    --levels '{"S2": "1.0880", "S1": "1.0920", "R1": "1.1000"}' \\
    --entry-conditions "RSI > 60" "MACD bullish"
        """
    )

    parser.add_argument("--vault", default="~/MyVault", help="Path to vault")
    parser.add_argument("--type", choices=["work", "trading"], required=True)

    # Для work
    parser.add_argument("--project", help="Project name")
    parser.add_argument("--tasks", nargs="+", help="List of completed tasks")
    parser.add_argument("--decisions", nargs="+", help="List of decisions (JSON)")
    parser.add_argument("--bugs", nargs="+", help="List of bugs (JSON)")

    # Для trading
    parser.add_argument("--action", choices=["journal", "analysis"], help="Journal or Analysis")
    parser.add_argument("--pair", help="Trading pair (EURUSD, etc)")
    parser.add_argument("--trades", nargs="+", help="List of trades (JSON)")
    parser.add_argument("--observations", nargs="+", help="Trading observations")
    parser.add_argument("--mistakes", nargs="+", help="Mistakes made")
    parser.add_argument("--levels", help="Technical levels (JSON)")
    parser.add_argument("--trend", help="Trend description")
    parser.add_argument("--entry-conditions", nargs="+", help="Entry conditions")
    parser.add_argument("--tp-sl", help="Take Profit & Stop Loss (JSON)")

    parser.add_argument("--date", help="Date (YYYY-MM-DD or YYYY-MM)")

    args = parser.parse_args()

    try:
        writer = VaultWriter(args.vault)

        if args.type == "work":
            if not args.project:
                print("Error: --project required for work type")
                sys.exit(1)

            decisions = []
            if args.decisions:
                for d in args.decisions:
                    try:
                        decisions.append(json.loads(d))
                    except json.JSONDecodeError:
                        print(f"Warning: Invalid JSON for decision: {d}")

            bugs = []
            if args.bugs:
                for b in args.bugs:
                    try:
                        bugs.append(json.loads(b))
                    except json.JSONDecodeError:
                        print(f"Warning: Invalid JSON for bug: {b}")

            filepath = writer.write_project_session(
                project_name=args.project,
                date=args.date,
                tasks=args.tasks,
                decisions=decisions,
                bugs=bugs
            )
            print(f"✅ Project session written: {filepath.relative_to(writer.vault_path)}")

        elif args.type == "trading":
            if args.action == "journal":
                trades = []
                if args.trades:
                    for t in args.trades:
                        try:
                            trades.append(json.loads(t))
                        except json.JSONDecodeError:
                            print(f"Warning: Invalid JSON for trade: {t}")

                filepath = writer.write_trading_journal(
                    date=args.date,
                    trades=trades,
                    observations=args.observations,
                    mistakes=args.mistakes
                )
                print(f"✅ Trading journal written: {filepath.relative_to(writer.vault_path)}")

            elif args.action == "analysis":
                if not args.pair:
                    print("Error: --pair required for analysis action")
                    sys.exit(1)

                levels = None
                if args.levels:
                    try:
                        levels = json.loads(args.levels)
                    except json.JSONDecodeError:
                        print("Warning: Invalid JSON for levels")

                tp_sl = None
                if args.tp_sl:
                    try:
                        tp_sl = json.loads(args.tp_sl)
                    except json.JSONDecodeError:
                        print("Warning: Invalid JSON for TP/SL")

                filepath = writer.write_trading_analysis(
                    pair=args.pair,
                    date=args.date,
                    levels=levels,
                    trend=args.trend,
                    entry_conditions=args.entry_conditions,
                    tp_sl=tp_sl
                )
                print(f"✅ Trading analysis written: {filepath.relative_to(writer.vault_path)}")

    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
