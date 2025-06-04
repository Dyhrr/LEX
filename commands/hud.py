import asyncio
import threading
import tkinter as tk
import psutil


class Command:
    """Toggle a simple system stats heads-up display."""

    trigger = ["hud"]

    def __init__(self, context):
        self.context = context
        self.root: tk.Tk | None = None
        self.thread: threading.Thread | None = None
        self.running = False

    # ---------------------------------------------------------
    # GUI helpers
    # ---------------------------------------------------------
    def _update_label(self, label: tk.Label) -> None:
        if not self.running:
            return
        cpu = psutil.cpu_percent(interval=None)
        mem = psutil.virtual_memory().percent
        label.config(text=f"CPU {cpu}% | MEM {mem}%")
        if self.root:
            self.root.after(1000, self._update_label, label)

    def _run_gui(self) -> None:
        self.root = tk.Tk()
        self.root.title("Lex HUD")
        self.root.attributes("-topmost", True)
        self.root.resizable(False, False)
        label = tk.Label(self.root, text="", font=("Arial", 10))
        label.pack(padx=10, pady=5)
        self.running = True
        self._update_label(label)
        self.root.mainloop()
        self.running = False

    def _start_gui(self) -> None:
        if self.thread and self.thread.is_alive():
            return
        self.thread = threading.Thread(target=self._run_gui, daemon=True)
        self.thread.start()

    def _stop_gui(self) -> None:
        if self.root:
            try:
                self.running = False
                self.root.after(0, self.root.destroy)
            except Exception:
                pass

    # ---------------------------------------------------------
    # Command entry point
    # ---------------------------------------------------------
    async def run(self, args: str) -> str:
        await asyncio.sleep(0)
        arg = args.strip().lower()
        if arg in ("", "on", "start"):
            if self.running:
                return "[Lex] HUD already running."
            self._start_gui()
            return "[Lex] HUD started."
        if arg in ("off", "stop"):
            if not self.running:
                return "[Lex] HUD not running."
            self._stop_gui()
            return "[Lex] HUD closed."
        return "[Lex] Use 'hud on' or 'hud off'."
