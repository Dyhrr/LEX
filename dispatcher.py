# Dispatches commands to plugins

import importlib
import os
import asyncio

class Dispatcher:
    def __init__(self):
        self.commands = {}
        self.load_commands()

    def load_commands(self):
        for filename in os.listdir("commands"):
            if filename.endswith(".py") and not filename.startswith("__"):
                mod_name = filename[:-3]
                mod = importlib.import_module(f"commands.{mod_name}")
                if hasattr(mod, "metadata"):
                    for trigger in mod.metadata["trigger"]:
                        self.commands[trigger.lower()] = mod

    async def dispatch(self, input_text):
        input_text = input_text.lower()
        for trigger, mod in self.commands.items():
            if trigger in input_text:
                return mod.run(input_text)
        return "[Lex] I don't know what you want, and I'm too tired to guess."