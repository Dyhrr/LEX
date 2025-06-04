import importlib
import pkgutil
from typing import List

from core.nlp import normalize_input


class Dispatcher:
    def __init__(self, context: dict | None = None):
        self.context = context or {}
        self.context["dispatcher"] = self
        self.commands: List[object] = []
        # expose dispatcher in shared context for plugins
        self.context["dispatcher"] = self
        self.load_modules()

    def load_modules(self):
        package = "commands"
        for _, name, _ in pkgutil.iter_modules([package]):
            module_name = f"{package}.{name}"
            try:
                module = importlib.import_module(module_name)
                if hasattr(module, "Command"):
                    instance = module.Command(self.context)
                    self.commands.append(instance)
                    # keep track of loaded command instances
                    self.context.setdefault("commands", {})[name] = instance
                    print(f"[Lex] Loaded: {module_name}")
                else:
                    print(f"[Lex] WARNING: {module_name} missing Command class")
            except Exception as e:
                print(f"[Lex] ERROR loading {module_name}: {e}")

    async def dispatch(self, input_text: str):
        """Route the given text to the appropriate command."""
        text = normalize_input(input_text)
        lowered = text.lower()
        for cmd in self.commands:
            triggers = getattr(cmd, "trigger", [])
            for trig in triggers:
                if lowered.startswith(trig):
                    args = text[len(trig):].strip()
                    try:
                        result = await cmd.run(args)
                        self.context["last_command"] = trig
                        self.context["last_result"] = result
                        return result
                    except Exception as e:
                        print(f"[Lex] ERROR in {cmd.__class__.__name__}: {e}")
                        return "[Lex] Something went wrong."
        return "[Lex] I don't know what you want, and I'm too tired to guess."
