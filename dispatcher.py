import importlib
from core.logger import get_logger
import os
import pkgutil
import sys
from typing import List

import asyncio

from core.nlp import normalize_input

logger = get_logger()


class Dispatcher:
    def __init__(self, context: dict | None = None, package: str = "commands"):
        self.package = package
        self.context = context or {}
        self.context["dispatcher"] = self
        self.context.setdefault("history", [])
        self.commands: List[object] = []
        self.trigger_map: dict[str, object] = {}
        self.module_mtimes: dict[str, float] = {}
        self.package_path = importlib.import_module(self.package).__path__[0]

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
        text = normalize_input(input_text, self.trigger_map.keys())
        lowered = text.lower()

        for trig, cmd in self.trigger_map.items():
            if lowered.startswith(trig):
                args = text[len(trig):].strip()
                try:
                    result = await cmd.run(args)
                    self.context["last_command"] = trig
                    self.context["last_result"] = result
                    history = self.context.get("history")
                    if isinstance(history, list):
                        history.append((input_text, result))
                        if len(history) > 20:
                            del history[:-20]
                    return result
                except Exception as e:
                    logger.exception("Error in %s", cmd.__class__.__name__)
                    return "[Lex] Something went wrong."

        return "[Lex] I don't know what you want, and I'm too tired to guess."
