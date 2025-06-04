import asyncio
import os
import shutil
from pathlib import Path


class Command:
    """Simple disk cleanup utilities."""

    trigger = ["cleanup"]

    def __init__(self, context):
        self.context = context

    def _remove_tmp(self, root: Path) -> int:
        count = 0
        for path in root.rglob("*.tmp"):
            try:
                path.unlink()
                count += 1
            except Exception:
                pass
        return count

    def _remove_pycache(self, root: Path) -> int:
        count = 0
        for cache in root.rglob("__pycache__"):
            shutil.rmtree(cache, ignore_errors=True)
            count += 1
        for pyc in root.rglob("*.pyc"):
            try:
                pyc.unlink()
                count += 1
            except Exception:
                pass
        return count

    async def run(self, args: str) -> str:
        await asyncio.sleep(0)
        option = args.strip().lower()
        root = Path(".")
        if option == "pycache":
            removed = await asyncio.to_thread(self._remove_pycache, root)
            return f"[Lex] Removed {removed} pycache items."

        removed = await asyncio.to_thread(self._remove_tmp, root)
        return f"[Lex] Removed {removed} .tmp files."
