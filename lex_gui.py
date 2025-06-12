"""Simple Tkinter-based GUI for Lex."""

from __future__ import annotations

import argparse
import asyncio
import logging
import threading
import tkinter as tk
from tkinter.scrolledtext import ScrolledText

from core.settings import load_settings
from core.security import require_vault_key
from dispatcher import Dispatcher
from core.logger import set_log_level

LEX_VERSION = "0.1.0"


class LexGUI:
    """Basic text-based GUI using Tkinter."""

    def __init__(self, dispatcher: Dispatcher) -> None:
        self.dispatcher = dispatcher
        self.loop = asyncio.new_event_loop()
        self.thread = threading.Thread(target=self.loop.run_forever, daemon=True)
        self.thread.start()

        self.root = tk.Tk()
        self.root.title(f"Lex v{LEX_VERSION}")
        self.root.protocol("WM_DELETE_WINDOW", self.close)

        self.output = ScrolledText(self.root, state="disabled", height=20, width=60)
        self.output.pack(padx=5, pady=5, fill="both", expand=True)

        self.entry = tk.Entry(self.root)
        self.entry.pack(fill="x", padx=5, pady=5)
        self.entry.bind("<Return>", self.submit)
        self.entry.focus_set()

    # -----------------------------------------------------
    # GUI helpers
    # -----------------------------------------------------
    def log(self, text: str) -> None:
        self.output.configure(state="normal")
        self.output.insert(tk.END, text + "\n")
        self.output.see(tk.END)
        self.output.configure(state="disabled")

    def submit(self, _event=None) -> None:
        command = self.entry.get().strip()
        if not command:
            return
        self.entry.delete(0, tk.END)
        self.log(f"> {command}")
        future = asyncio.run_coroutine_threadsafe(
            self.dispatcher.run_command(command), self.loop
        )
        future.add_done_callback(lambda f: self.root.after(0, self.log, f.result()))

    def close(self) -> None:
        self.root.destroy()
        self.loop.call_soon_threadsafe(self.loop.stop)
        self.thread.join()

    def run(self) -> None:
        self.root.mainloop()


# ---------------------------------------------------------
# Entry point
# ---------------------------------------------------------

def main() -> None:
    settings = load_settings()
    key = require_vault_key()
    dispatcher = Dispatcher({"settings": settings, "vault_key": key})
    gui = LexGUI(dispatcher)
    dispatcher.context["app"] = gui
    gui.run()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Lex GUI")
    parser.add_argument("--verbose", action="store_true", help="Enable debug logging")
    parser.add_argument("--quiet", action="store_true", help="Only show warnings")
    args = parser.parse_args()

    if args.verbose:
        set_log_level(logging.DEBUG)
    elif args.quiet:
        set_log_level(logging.WARNING)

    main()
