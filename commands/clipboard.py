import asyncio
import json
import os
from pathlib import Path

import pyperclip

HISTORY_FILE = Path("memory") / "clipboard.json"


class Command:
    """Maintain a simple clipboard history."""

    trigger = ["clipboard"]

    def __init__(self, context):
        self.context = context
        self.file = HISTORY_FILE
        self.max_items = 20
        self._cache: list[str] | None = None

    def _load(self) -> list[str]:
        if self._cache is not None:
            return self._cache
        if self.file.exists():
            try:
                with self.file.open("r", encoding="utf-8") as fh:
                    self._cache = json.load(fh)
                    return self._cache
            except Exception:
                pass
        self._cache = []
        return self._cache

    def _save(self, data: list[str]) -> None:
        os.makedirs(self.file.parent, exist_ok=True)
        with self.file.open("w", encoding="utf-8") as fh:
            json.dump(data, fh)

    async def run(self, args: str) -> str:
        await asyncio.sleep(0)
        tokens = args.split(maxsplit=1)
        history = self._load()
        if not tokens:
            return "\n".join(history[-5:]) if history else "[Lex] Clipboard empty."

        cmd = tokens[0]
        if cmd == "add" and len(tokens) > 1:
            text = tokens[1]
            history.append(text)
            history = history[-self.max_items :]
            self._save(history)
            try:
                pyperclip.copy(text)
            except Exception:
                pass
            return "[Lex] Copied."
        if cmd == "clear":
            history.clear()
            self._save(history)
            return "[Lex] Cleared."
        if cmd == "paste":
            if not history:
                return "[Lex] Clipboard empty."
            text = history[-1]
            try:
                pyperclip.copy(text)
            except Exception:
                pass
            return text
        if cmd == "show":
            return "\n".join(history[-5:]) if history else "[Lex] Clipboard empty."
        return "[Lex] Use 'clipboard add <text>', 'show', 'paste', or 'clear'."
