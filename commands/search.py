"""Search files from a local index."""

import asyncio
import json
import os
from pathlib import Path

INDEX_FILE = Path("memory") / "file_index.json"


class Command:
    description = "Search files from a local index."
    """Search files from a simple local index."""

    trigger = ["search", "find", "locate"]

    def __init__(self, context):
        self.context = context
        self.file = INDEX_FILE
        self._index: list[str] | None = None

    def _create_index(self, start: Path) -> list[str]:
        paths: list[str] = []
        for root, _dirs, files in os.walk(start):
            for name in files:
                paths.append(str(Path(root) / name))
        return paths

    def _load_index(self) -> list[str]:
        if self._index is not None:
            return self._index
        if self.file.exists():
            try:
                with self.file.open("r", encoding="utf-8") as fh:
                    self._index = json.load(fh)
                    return self._index
            except Exception:
                pass
        self._index = []
        return self._index

    async def run(self, args: str) -> str:
        await asyncio.sleep(0)
        tokens = args.split()
        if tokens and tokens[0] == "index":
            start = Path.home()
            index = await asyncio.to_thread(self._create_index, start)
            self._index = index
            os.makedirs(self.file.parent, exist_ok=True)
            with self.file.open("w", encoding="utf-8") as fh:
                json.dump(index, fh)
            return f"[Lex] Indexed {len(index)} files."

        term = args.strip().lower()
        if not term:
            return "[Lex] Provide a search term or 'search index'."
        index = self._load_index()
        if not index:
            return "[Lex] No index found. Run 'search index' first."
        matches = [p for p in index if term in os.path.basename(p).lower()]
        if not matches:
            return "[Lex] No matches."
        return "\n".join(matches[:5])
