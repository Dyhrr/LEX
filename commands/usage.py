import asyncio
import json
from pathlib import Path

USAGE_FILE = Path("memory") / "usage.json"

class Command:
    """Display command usage statistics."""

    trigger = ["usage"]

    def __init__(self, context):
        self.context = context
        self.file = Path(context.get("usage_file", USAGE_FILE))

    def _load(self) -> dict[str, int]:
        if self.file.exists():
            try:
                with self.file.open("r", encoding="utf-8") as fh:
                    data = json.load(fh)
                if isinstance(data, dict):
                    return {k: int(v) for k, v in data.items()}
            except Exception:
                pass
        return {}

    async def run(self, args: str) -> str:
        await asyncio.sleep(0)
        arg = args.strip().lower()
        if arg == "reset":
            if self.file.exists():
                self.file.unlink()
            return "[Lex] Usage stats cleared."

        data = await asyncio.to_thread(self._load)
        if not data:
            return "[Lex] No usage data."
        top = sorted(data.items(), key=lambda x: x[1], reverse=True)[:5]
        return "\n".join(f"{k}: {v}" for k, v in top)
