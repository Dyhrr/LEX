import asyncio
import json
from pathlib import Path

SUGGESTIONS_FILE = Path("data") / "feature_suggestions.json"


class Command:
    """List potential new features from the suggestions file."""

    trigger = ["features", "missing features", "feature suggestions"]

    def __init__(self, context):
        self.context = context

    async def run(self, args: str) -> str:
        await asyncio.sleep(0)
        file = SUGGESTIONS_FILE
        if not file.exists():
            return "[Lex] I don't have any feature requests yet."
        try:
            with file.open("r", encoding="utf-8") as fh:
                data = json.load(fh)
        except Exception:
            return "[Lex] Couldn't read feature suggestions."
        if not data:
            return "[Lex] I don't have any feature requests right now."
        names = ", ".join(sorted(data.keys()))
        return f"[Lex] Potential features: {names}"
