import asyncio
import json
import os


class Command:
    trigger = ["remind"]

    def __init__(self, context):
        self.context = context
        self.file = os.path.join("memory", "reminders.json")

    def _read_json(self):
        if not os.path.exists(self.file):
            return []
        with open(self.file, "r", encoding="utf-8") as fh:
            try:
                return json.load(fh)
            except Exception:
                return []

    def _write_json(self, data):
        with open(self.file, "w", encoding="utf-8") as fh:
            json.dump(data, fh)

    async def _load(self):
        return await asyncio.to_thread(self._read_json)

    async def _save(self, data):
        await asyncio.to_thread(self._write_json, data)

    async def run(self, args: str) -> str:
        args = args.strip()
        reminders = await self._load()
        if not args or args.lower() == "list":
            if not reminders:
                return "[Lex] No reminders saved."
            return "\n".join(f"- {r}" for r in reminders)
        reminders.append(args)
        await self._save(reminders)
        return f"[Lex] Reminder saved: {args}"
