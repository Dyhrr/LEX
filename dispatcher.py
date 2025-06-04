import importlib
import pkgutil
from typing import List


class Dispatcher:
    def __init__(self, context: dict | None = None):
        self.context = context or {}
        self.context["dispatcher"] = self
        self.commands: List[object] = []
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
                    print(f"[Lex] Loaded: {module_name}")
                else:
                    print(f"[Lex] WARNING: {module_name} missing Command class")
            except Exception as e:
                print(f"[Lex] ERROR loading {module_name}: {e}")

    async def dispatch(self, input_text: str):
        lowered = input_text.lower()
        for cmd in self.commands:
            triggers = getattr(cmd, "trigger", [])
            for trig in triggers:
                if lowered.startswith(trig):
                    args = input_text[len(trig):].strip()
                    try:
                        return await cmd.run(args)
                    except Exception as e:
                        print(f"[Lex] ERROR in {cmd.__class__.__name__}: {e}")
                        return "[Lex] Something went wrong."
        return "[Lex] I don't know what you want, and I'm too tired to guess."
