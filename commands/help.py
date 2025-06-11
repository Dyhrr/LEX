import asyncio
import re
from pathlib import Path

DOCS_FILE = Path("documentation.md")


class Command:
    trigger = ["help"]

    def __init__(self, context):
        self.context = context

    def _load_docs(self) -> dict[str, str]:
        if not DOCS_FILE.exists():
            return {}
        info: dict[str, str] = {}
        with DOCS_FILE.open("r", encoding="utf-8") as fh:
            for line in fh:
                if not line.startswith("|") or line.startswith("|---"):
                    continue
                parts = [p.strip() for p in line.strip().strip("|").split("|")]
                if len(parts) < 3 or not parts[0].endswith(".py"):
                    continue
                triggers = [t.strip("` ") for t in parts[1].split(",")]
                desc = parts[2]
                for trig in triggers:
                    if trig:
                        info[trig] = desc
        return info

    async def run(self, args: str) -> str:
        """List all available command triggers with descriptions."""
        dispatcher = self.context.get("dispatcher")
        if not dispatcher:
            return "[Lex] Dispatcher not available."

        docs = await asyncio.to_thread(self._load_docs)
        lines = []
        for cmd in dispatcher.commands:
            triggers = getattr(cmd, "trigger", [])
            if not isinstance(triggers, (list, tuple)):
                continue
            desc = next((docs.get(t) for t in triggers if t in docs), "")
            trig_list = ", ".join(triggers)
            if desc:
                lines.append(f"{trig_list} - {desc}")
            else:
                lines.append(trig_list)

        if not lines:
            return "[Lex] No commands loaded."
        return "[Lex] Available commands:\n" + "\n".join(sorted(lines))

