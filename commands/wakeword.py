"""Manage wake word detection."""

from __future__ import annotations

import asyncio
import json
import os
from pathlib import Path

from voice import recognizer


WAKE_FILE = Path("memory") / "wakewords.json"


class Command:
    trigger = ["wakeword"]

    def __init__(self, context):
        self.context = context
        self.file = WAKE_FILE
        self.words: list[str] = self._load()
        self.task: asyncio.Task | None = None

    # -----------------------------------------------------
    # Persistence helpers
    # -----------------------------------------------------
    def _load(self) -> list[str]:
        if self.file.exists():
            try:
                with self.file.open("r", encoding="utf-8") as fh:
                    return json.load(fh)
            except Exception:
                pass
        return ["hey lex"]

    def _save(self) -> None:
        os.makedirs(self.file.parent, exist_ok=True)
        with self.file.open("w", encoding="utf-8") as fh:
            json.dump(self.words, fh)

    # -----------------------------------------------------
    # Listening loop
    # -----------------------------------------------------
    async def _listen(self) -> None:
        dispatcher = self.context.get("dispatcher")
        if not dispatcher:
            return
        while True:
            try:
                text = await recognizer.transcribe(timeout=3)
            except Exception:
                await asyncio.sleep(1)
                continue
            if not text:
                continue
            lowered = text.lower()
            if any(w.lower() in lowered for w in self.words):
                await dispatcher.dispatch("ping")

    def _start(self) -> str:
        if self.task and not self.task.done():
            return "[Lex] Wake word listener already running."
        self.task = asyncio.create_task(self._listen())
        return "[Lex] Wake word detection started."

    def _stop(self) -> str:
        if self.task:
            self.task.cancel()
            self.task = None
            return "[Lex] Wake word detection stopped."
        return "[Lex] Wake word listener not running."

    # -----------------------------------------------------
    # Command entry point
    # -----------------------------------------------------
    async def run(self, args: str) -> str:
        await asyncio.sleep(0)
        tokens = args.split(maxsplit=1)
        if not tokens:
            return (
                "[Lex] Use 'wakeword start', 'stop', 'list', 'add <word>' or 'remove <word>'."
            )

        cmd = tokens[0]

        if cmd == "start":
            return self._start()

        if cmd == "stop":
            return self._stop()

        if cmd == "list":
            return ", ".join(self.words)

        if cmd == "add" and len(tokens) == 2:
            word = tokens[1].strip().lower()
            if word in self.words:
                return "[Lex] Wake word already exists."
            self.words.append(word)
            self._save()
            return f"[Lex] Added wake word '{word}'."

        if cmd == "remove" and len(tokens) == 2:
            word = tokens[1].strip().lower()
            if word in self.words:
                self.words.remove(word)
                self._save()
                return f"[Lex] Removed wake word '{word}'."
            return "[Lex] Wake word not found."

        return (
            "[Lex] Use 'wakeword start', 'stop', 'list', 'add <word>' or 'remove <word>'."
        )

