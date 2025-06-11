"""Manage a simple local profile (`show`, `set`, `delete`)."""

import asyncio
import json
import os
from pathlib import Path


PROFILE_FILE = Path("memory") / "profile.json"


class Command:
    description = "Manage a simple local profile (`show`, `set`, `delete`)."
    """Manage a simple local user profile."""

    trigger = ["profile"]

    def __init__(self, context):
        self.context = context
        self.file = PROFILE_FILE
        self.lock = asyncio.Lock()

    def _load(self) -> dict:
        if self.file.exists():
            try:
                with self.file.open("r", encoding="utf-8") as fh:
                    return json.load(fh)
            except Exception:
                pass
        return {}

    def _save(self, data: dict) -> None:
        os.makedirs(self.file.parent, exist_ok=True)
        with self.file.open("w", encoding="utf-8") as fh:
            json.dump(data, fh)

    async def run(self, args: str) -> str:
        await asyncio.sleep(0)
        tokens = args.split(maxsplit=2)
        async with self.lock:
            profile = await asyncio.to_thread(self._load)

            if not tokens or tokens[0] == "show":
                if not profile:
                    return "[Lex] Profile empty."
                return "\n".join(f"{k}: {v}" for k, v in profile.items())

            if tokens[0] == "set" and len(tokens) == 3:
                profile[tokens[1]] = tokens[2]
                await asyncio.to_thread(self._save, profile)
                return "[Lex] Profile updated."

            if tokens[0] == "delete" and len(tokens) == 2:
                if tokens[1] in profile:
                    del profile[tokens[1]]
                    await asyncio.to_thread(self._save, profile)
                    return "[Lex] Deleted."
                return "[Lex] Not found."

            return "[Lex] Use 'profile show', 'profile set <key> <val>' or 'profile delete <key>'."
