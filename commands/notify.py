"""Simple desktop notification aggregator."""

from __future__ import annotations

import asyncio
import json
import os
import platform
import subprocess
from datetime import datetime
from pathlib import Path


NOTIFY_FILE = Path("memory") / "notifications.json"


class Command:
    description = "Send desktop notifications and list recent ones."
    trigger = ["notify"]

    def __init__(self, context):
        self.context = context
        self.file = NOTIFY_FILE
        self._cache: list[dict] | None = None
        self.lock = asyncio.Lock()

    # ---------------------------------------------------------
    # Persistence helpers
    # ---------------------------------------------------------
    def _load(self) -> list[dict]:
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

    def _save(self) -> None:
        data = self._cache or []
        os.makedirs(self.file.parent, exist_ok=True)
        with self.file.open("w", encoding="utf-8") as fh:
            json.dump(data, fh)

    def _send_os_notification(self, message: str) -> None:
        system = platform.system().lower()
        try:
            if system == "linux":
                subprocess.Popen(["notify-send", message])
            elif system == "darwin":
                subprocess.Popen([
                    "osascript",
                    "-e",
                    f'display notification "{message}" with title "Lex"',
                ])
            elif system == "windows":
                try:
                    from win10toast import ToastNotifier

                    ToastNotifier().show_toast("Lex", message, duration=5)
                except Exception:
                    pass
        except Exception:
            pass

    # ---------------------------------------------------------
    # Command entry point
    # ---------------------------------------------------------
    async def run(self, args: str) -> str:
        await asyncio.sleep(0)
        tokens = args.split()
        async with self.lock:
            history = await asyncio.to_thread(self._load)
        if not tokens:
            return "[Lex] Use 'notify <message>', 'list', or 'clear'."

        cmd = tokens[0]

        if cmd == "list":
            if not history:
                return "[Lex] No notifications."
            return "\n".join(
                f"{n['time']} - {n['msg']}" for n in history[-5:]
            )

        if cmd == "clear":
            history.clear()
            async with self.lock:
                await asyncio.to_thread(self._save)
            return "[Lex] Cleared notifications."

        message = args.strip()
        if not message:
            return "[Lex] Notification text required."
        self._send_os_notification(message)
        history.append(
            {"time": datetime.now().isoformat(timespec="seconds"), "msg": message}
        )
        history[:] = history[-50:]
        async with self.lock:
            await asyncio.to_thread(self._save)
        return f"[Lex] Notified: {message}"
