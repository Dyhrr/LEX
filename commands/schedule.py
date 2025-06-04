import asyncio
import json
from pathlib import Path
from datetime import datetime


SCHEDULE_FILE = Path("memory") / "schedule.json"


class Command:
    """Manage a very small local schedule of dated notes."""

    trigger = ["schedule"]

    def __init__(self, context):
        self.context = context
        self.file = SCHEDULE_FILE

    def _load(self) -> list[dict]:
        if self.file.exists():
            try:
                with self.file.open("r", encoding="utf-8") as fh:
                    return json.load(fh)
            except Exception:
                pass
        return []

    def _save(self, data: list[dict]) -> None:
        self.file.parent.mkdir(parents=True, exist_ok=True)
        with self.file.open("w", encoding="utf-8") as fh:
            json.dump(data, fh)

    async def run(self, args: str) -> str:
        """Add, list or remove scheduled items."""
        await asyncio.sleep(0)
        tokens = args.split()
        if not tokens or tokens[0] == "list":
            events = self._load()
            if not events:
                return "[Lex] No events scheduled."
            events.sort(key=lambda e: e.get("time", ""))
            lines = [
                f"{i+1}. {e['time']} - {e['text']}" for i, e in enumerate(events)
            ]
            return "\n".join(lines)

        cmd = tokens[0]

        if cmd == "add" and len(tokens) >= 3:
            dt_str = f"{tokens[1]} {tokens[2]}"
            try:
                dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
            except ValueError:
                return "[Lex] Use 'YYYY-MM-DD HH:MM' for the date/time."
            text = " ".join(tokens[3:]) or "(no details)"
            events = self._load()
            events.append({"time": dt.strftime("%Y-%m-%d %H:%M"), "text": text})
            self._save(events)
            return f"[Lex] Event added for {dt_str}."

        if cmd == "remove" and len(tokens) >= 2:
            try:
                idx = int(tokens[1]) - 1
            except ValueError:
                return "[Lex] Give me a valid number to remove."
            events = self._load()
            if 0 <= idx < len(events):
                removed = events.pop(idx)
                self._save(events)
                return f"[Lex] Removed: {removed['text']}"
            return "[Lex] No event with that number."

        if cmd == "clear":
            self._save([])
            return "[Lex] Schedule cleared."

        return (
            "[Lex] Use 'schedule add YYYY-MM-DD HH:MM <text>', 'list', "
            "'remove <num>' or 'clear'."
        )
