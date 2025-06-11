"""Switch Lex's Textual UI theme.

Available themes live in the ``themes/`` folder and ship with ``lex`` and ``meme`` styles.
"""

from __future__ import annotations

import asyncio
from pathlib import Path
from typing import List

from core.settings import save_settings

THEMES_DIR = Path("themes")
SETTINGS_FILE = Path("settings.json")


class Command:
    """Change the active UI theme."""

    trigger = ["theme"]
    description = "Change the Textual UI theme. Usage: theme <name>"

    def __init__(self, context):
        self.context = context

    def _available(self) -> List[str]:
        return [p.stem for p in THEMES_DIR.glob("*.css")]

    async def run(self, args: str) -> str:
        await asyncio.sleep(0)
        name = args.strip()
        if not name:
            return f"[Lex] Usage: theme <name>. Available: {', '.join(self._available())}"
        if name not in self._available():
            return f"[Lex] Unknown theme. Available: {', '.join(self._available())}"
        settings = self.context.get("settings", {})
        settings["theme"] = name
        save_settings(settings, str(SETTINGS_FILE))
        app = self.context.get("app")
        if app and hasattr(app, "set_theme"):
            if app.set_theme(name):
                return f"[Lex] Theme switched to {name}."
        return "[Lex] Theme saved. Restart Lex to apply."
