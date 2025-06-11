"""Register global hotkeys that trigger Lex commands."""

import asyncio
import json
import os
from pathlib import Path


HOTKEY_FILE = Path("memory") / "hotkeys.json"


class Command:
    description = "Register global hotkeys that trigger Lex commands."
    """Register and manage global hotkeys."""

    trigger = ["hotkey"]

    def __init__(self, context):
        self.context = context
        self.file = HOTKEY_FILE
        self.hotkeys: dict[str, str] = {}
        self.loop: asyncio.AbstractEventLoop | None = None
        self.keyboard = None
        self.active = False
        self._load()

    # ---------------------------------------------------------
    # Persistence helpers
    # ---------------------------------------------------------
    def _load(self) -> None:
        if self.file.exists():
            try:
                with self.file.open("r", encoding="utf-8") as fh:
                    self.hotkeys = json.load(fh)
            except Exception:
                self.hotkeys = {}

    def _save(self) -> None:
        os.makedirs(self.file.parent, exist_ok=True)
        with self.file.open("w", encoding="utf-8") as fh:
            json.dump(self.hotkeys, fh)

    # ---------------------------------------------------------
    # Hotkey handling helpers
    # ---------------------------------------------------------
    def _callback(self, command: str):
        def inner() -> None:
            if not self.active or not self.loop:
                return
            dispatcher = self.context.get("dispatcher")
            if not dispatcher:
                return
            asyncio.run_coroutine_threadsafe(
                dispatcher.dispatch(command), self.loop
            )

        return inner

    def _register_all(self) -> None:
        if not self.keyboard:
            return
        for combo, cmd in self.hotkeys.items():
            self.keyboard.add_hotkey(combo, self._callback(cmd))

    def start_listener(self, loop: asyncio.AbstractEventLoop) -> str:
        if self.active:
            return "[Lex] Hotkey listener already running."
        try:
            import keyboard

            self.keyboard = keyboard
        except Exception:
            return "[Lex] 'keyboard' package not installed."

        self.loop = loop
        self._register_all()
        self.active = True
        return "[Lex] Hotkey listener started."

    def stop_listener(self) -> str:
        if not self.active:
            return "[Lex] Hotkey listener not running."
        if self.keyboard:
            try:
                self.keyboard.clear_all_hotkeys()
            except Exception:
                pass
        self.active = False
        return "[Lex] Hotkey listener stopped."

    # ---------------------------------------------------------
    # Command entry point
    # ---------------------------------------------------------
    async def run(self, args: str) -> str:
        await asyncio.sleep(0)
        tokens = args.split()
        if not tokens:
            return (
                "[Lex] Use 'hotkey add <combo> <command>', 'remove <combo>', "
                "'list', 'start', or 'stop'."
            )

        cmd = tokens[0]

        if cmd == "list":
            if not self.hotkeys:
                return "[Lex] No hotkeys defined."
            return "\n".join(f"{k} -> {v}" for k, v in self.hotkeys.items())

        if cmd == "add" and len(tokens) >= 3:
            combo = tokens[1]
            command = " ".join(tokens[2:])
            self.hotkeys[combo] = command
            self._save()
            if self.active and self.keyboard:
                try:
                    self.keyboard.add_hotkey(combo, self._callback(command))
                except Exception:
                    pass
            return f"[Lex] Hotkey '{combo}' added."

        if cmd == "remove" and len(tokens) >= 2:
            combo = tokens[1]
            if combo in self.hotkeys:
                del self.hotkeys[combo]
                self._save()
                if self.active and self.keyboard:
                    try:
                        self.keyboard.remove_hotkey(combo)
                    except Exception:
                        pass
                return f"[Lex] Removed hotkey '{combo}'."
            return "[Lex] Hotkey not found."

        if cmd == "start":
            loop = asyncio.get_running_loop()
            return self.start_listener(loop)

        if cmd == "stop":
            return self.stop_listener()

        return "[Lex] Unknown hotkey command."
