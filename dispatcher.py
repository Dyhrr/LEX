import importlib

class Dispatcher:
    def __init__(self):
        self.modules = [
            "commands.system",
            "commands.gaming",
            "commands.info",
            "commands.personality",
            "commands.tools",
            "commands.vault"
        ]
        self.handlers = []
        self.load_modules()

    def load_modules(self):
        for module_name in self.modules:
            try:
                module = importlib.import_module(module_name)
                if hasattr(module, "handle"):
                    self.handlers.append(module.handle)
                    print(f"[Lex] Loaded: {module_name}")
                else:
                    print(f"[Lex] WARNING: {module_name} has no handle()")
            except Exception as e:
                print(f"[Lex] ERROR loading {module_name}: {e}")

    async def dispatch(self, input_text: str):
        input_text = input_text.lower()
        for handler in self.handlers:
            try:
                result = handler(input_text)
                if result:
                    return result
            except Exception as e:
                print(f"[Lex] ERROR in handler: {e}")
        return "[Lex] I don't know what you want, and I'm too tired to guess."
