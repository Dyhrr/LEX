import importlib
from core.logger import get_logger
import os
import pkgutil
import sys
from typing import List

import asyncio

from core.nlp import normalize_input
import json

USAGE_FILE = os.path.join("memory", "usage.json")

logger = get_logger()


class Dispatcher:
    def __init__(self, context: dict | None = None, package: str = "commands"):
        self.package = package
        self.context = context or {}
        self.context["dispatcher"] = self
        self.context.setdefault("history", [])
        settings = self.context.get("settings", {})
        self.timeout = float(settings.get("plugin_timeout", 5.0) or 5.0)
        self.commands: List[object] = []
        self.trigger_map: dict[str, object] = {}
        self.module_mtimes: dict[str, float] = {}
        self.package_path = importlib.import_module(self.package).__path__[0]

        # Track command usage counts for analytics
        self.usage_file = self.context.get("usage_file", USAGE_FILE)
        self.usage_counts = self._load_usage()
        self.context["usage_counts"] = self.usage_counts

        self.load_modules()

    def check_for_updates(self) -> bool:
        """Reload modules if any command file changed or added."""
        updated = False
        for _, name, _ in pkgutil.iter_modules([self.package_path]):
            module_name = f"{self.package}.{name}"
            path = os.path.join(self.package_path, f"{name}.py")
            try:
                mtime = os.path.getmtime(path)
            except OSError:
                continue
            if (
                module_name not in self.module_mtimes
                or mtime > self.module_mtimes[module_name]
            ):
                updated = True
                break
        if updated:
            self.load_modules()
            logger.info("Reloaded command modules")
        return updated

    async def watch_modules(self, interval: float = 1.0) -> None:
        """Continuously watch for plugin changes."""
        while True:
            await asyncio.sleep(interval)
            self.check_for_updates()

    def _load_usage(self) -> dict[str, int]:
        """Load usage counts from disk."""
        if os.path.exists(self.usage_file):
            try:
                with open(self.usage_file, "r", encoding="utf-8") as fh:
                    data = json.load(fh)
                if isinstance(data, dict):
                    return {k: int(v) for k, v in data.items()}
            except Exception:
                pass
        return {}

    def _save_usage(self) -> None:
        os.makedirs(os.path.dirname(self.usage_file), exist_ok=True)
        with open(self.usage_file, "w", encoding="utf-8") as fh:
            json.dump(self.usage_counts, fh)

    async def _safe_execute(self, cmd: object, args: str) -> str:
        """Execute a command with sandboxing and exception handling."""
        try:
            return await asyncio.wait_for(cmd.run(args), timeout=self.timeout)
        except asyncio.TimeoutError:
            logger.warning("%s timed out", cmd.__class__.__name__)
            return "[Lex] Command timed out."
        except Exception:
            logger.exception("Error in %s", cmd.__class__.__name__)
            return "[Lex] Something went wrong."

    def load_modules(self) -> None:
        self.commands.clear()
        self.trigger_map.clear()
        package = self.package
        for _, name, _ in pkgutil.iter_modules([self.package_path]):
            module_name = f"{package}.{name}"
            try:
                if module_name in sys.modules:
                    module = importlib.reload(sys.modules[module_name])
                else:
                    module = importlib.import_module(module_name)
                self.module_mtimes[module_name] = os.path.getmtime(
                    os.path.join(self.package_path, f"{name}.py")
                )
                if hasattr(module, "Command"):
                    instance = module.Command(self.context)
                    self.commands.append(instance)
                    self.context.setdefault("commands", {})[name] = instance
                    # Map triggers to command instance for quick lookup
                    for trig in getattr(instance, "trigger", []):
                        self.trigger_map[trig.lower()] = instance
                    logger.info("Loaded: %s", module_name)
                else:
                    logger.warning("%s missing Command class", module_name)
            except Exception as e:
                logger.error("ERROR loading %s: %s", module_name, e)

    async def dispatch(self, input_text: str):
        """Route the given text to the appropriate command."""
        # normalize_input uses difflib.get_close_matches under the hood for
        # fuzzy trigger substitution when the user mistypes a command
        settings = self.context.get("settings", {})
        cutoff = float(settings.get("fuzzy_threshold", 0.75) or 0)
        if cutoff <= 0 or cutoff > 1:
            cutoff = 1.0
        text = normalize_input(input_text, self.trigger_map.keys(), cutoff=cutoff)
        lowered = text.lower()

        for trig, cmd in self.trigger_map.items():
            if lowered.startswith(trig):
                args = text[len(trig):].strip()
                result = await self._safe_execute(cmd, args)
                self.context["last_command"] = trig
                self.context["last_result"] = result
                history = self.context.get("history")
                if isinstance(history, list):
                    history.append((input_text, result))
                    if len(history) > 20:
                        del history[:-20]
                self.usage_counts[trig] = self.usage_counts.get(trig, 0) + 1
                await asyncio.to_thread(self._save_usage)
                return result

        from difflib import get_close_matches
        parts = lowered.split()
        if parts:
            suggestions = get_close_matches(
                parts[0], self.trigger_map.keys(), n=1, cutoff=0.5
            )
            if suggestions:
                return f"[Lex] Unknown command. Did you mean: {suggestions[0]}?"

        return "[Lex] I don't know what you want, and I'm too tired to guess."

    async def run_command(self, command: str) -> str:
        """Public helper to execute a command string."""
        self.check_for_updates()
        return await self.dispatch(command)
