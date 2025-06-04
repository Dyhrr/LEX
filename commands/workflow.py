import asyncio
import json
import os
from pathlib import Path


WORKFLOW_FILE = Path("memory") / "workflows.json"


class Command:
    """Create and run simple multi-step workflows."""

    trigger = ["workflow"]

    def __init__(self, context):
        self.context = context
        self.file = WORKFLOW_FILE

    # ---------------------------------------------------------
    # Persistence helpers
    # ---------------------------------------------------------
    def _load(self) -> dict[str, list[str]]:
        if self.file.exists():
            try:
                with self.file.open("r", encoding="utf-8") as fh:
                    return json.load(fh)
            except Exception:
                pass
        return {}

    def _save(self, data: dict[str, list[str]]) -> None:
        os.makedirs(self.file.parent, exist_ok=True)
        with self.file.open("w", encoding="utf-8") as fh:
            json.dump(data, fh)

    # ---------------------------------------------------------
    # Command entry point
    # ---------------------------------------------------------
    async def run(self, args: str) -> str:
        await asyncio.sleep(0)
        tokens = args.split(maxsplit=2)
        if not tokens or tokens[0] == "list":
            workflows = self._load()
            if not workflows:
                return "[Lex] No workflows defined."
            lines = [f"{name}: {'; '.join(steps)}" for name, steps in workflows.items()]
            return "\n".join(lines)

        cmd = tokens[0]

        if cmd == "create" and len(tokens) == 3:
            name = tokens[1]
            steps = [s.strip() for s in tokens[2].split(";") if s.strip()]
            data = self._load()
            data[name] = steps
            self._save(data)
            return f"[Lex] Workflow '{name}' saved."

        if cmd == "run" and len(tokens) >= 2:
            name = tokens[1]
            data = self._load()
            steps = data.get(name)
            if not steps:
                return f"[Lex] No workflow named '{name}'."
            dispatcher = self.context.get("dispatcher")
            if not dispatcher:
                return "[Lex] Dispatcher not available."
            for step in steps:
                await dispatcher.dispatch(step)
            return f"[Lex] Workflow '{name}' executed."

        if cmd == "delete" and len(tokens) >= 2:
            name = tokens[1]
            data = self._load()
            if name in data:
                del data[name]
                self._save(data)
                return f"[Lex] Workflow '{name}' deleted."
            return f"[Lex] No workflow named '{name}'."

        return (
            "[Lex] Use 'workflow create <name> cmd1; cmd2', 'run <name>', "
            "'delete <name>' or 'list'."
        )
