"""Store short notes locally."""

import asyncio
import json
import os
from pathlib import Path

NOTES_FILE = Path("memory") / "notes.json"


class Command:
    description = "Store short notes locally."
    """Store short notes locally."""

    trigger = ["notes", "note"]

    def __init__(self, context):
        self.context = context
        self.file = NOTES_FILE
        self.lock = asyncio.Lock()

    def _load(self) -> list[str]:
        if self.file.exists():
            try:
                with self.file.open("r", encoding="utf-8") as fh:
                    return json.load(fh)
            except Exception:
                pass
        return []

    def _save(self, data: list[str]) -> None:
        os.makedirs(self.file.parent, exist_ok=True)
        with self.file.open("w", encoding="utf-8") as fh:
            json.dump(data, fh)

    async def run(self, args: str) -> str:
        await asyncio.sleep(0)
        tokens = args.split(maxsplit=1)
        if not tokens:
            async with self.lock:
                notes = await asyncio.to_thread(self._load)
            if not notes:
                return "[Lex] No notes."
            return "\n".join(f"{i+1}. {n}" for i, n in enumerate(notes))
        cmd = tokens[0]
        if cmd == "add" and len(tokens) > 1:
            async with self.lock:
                notes = await asyncio.to_thread(self._load)
                notes.append(tokens[1])
                await asyncio.to_thread(self._save, notes)
            return "[Lex] Note added."
        if cmd == "clear":
            async with self.lock:
                await asyncio.to_thread(self._save, [])
            return "[Lex] Notes cleared."
        return "[Lex] Use 'notes add <text>' or 'notes' to list."
