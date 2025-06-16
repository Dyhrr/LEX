import argparse
import asyncio
import atexit
import logging
import sys
import threading

from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QLineEdit

from core.settings import load_settings
from core.security import require_vault_key
from dispatcher import Dispatcher
from core.logger import set_log_level


# Create a persistent asyncio event loop running in a background thread.
event_loop = asyncio.new_event_loop()
asyncio.set_event_loop(event_loop)
threading.Thread(target=event_loop.run_forever, daemon=True).start()


def _shutdown_loop() -> None:
    """Stop the background event loop."""
    event_loop.call_soon_threadsafe(event_loop.stop)


atexit.register(_shutdown_loop)


class LexWindow(QWidget):
    """Simple PySide6 GUI for interacting with Lex."""

    result_ready = Signal(str)

    def __init__(self, dispatcher: Dispatcher) -> None:
        super().__init__()
        self.dispatcher = dispatcher
        self.setWindowTitle("Lex GUI")

        layout = QVBoxLayout(self)
        self.log = QTextEdit(self)
        self.log.setReadOnly(True)
        self.input = QLineEdit(self)

        layout.addWidget(self.log)
        layout.addWidget(self.input)

        self.input.returnPressed.connect(self.submit)
        self.result_ready.connect(self.append_log)

    @Slot(str)
    def append_log(self, message: str) -> None:
        """Append a line to the log and scroll to the end."""
        self.log.append(message.strip())
        bar = self.log.verticalScrollBar()
        bar.setValue(bar.maximum())

    @Slot()
    def submit(self) -> None:
        text = self.input.text().strip()
        if not text:
            return
        self.log.append(f"> {text}")
        self.input.clear()
        threading.Thread(target=self._execute, args=(text,), daemon=True).start()

    def _execute(self, text: str) -> None:
        future = asyncio.run_coroutine_threadsafe(
            self.dispatcher.run_command(text), event_loop
        )
        try:
            result = future.result()
        except Exception as e:
            result = f"[ERROR] {e}"
        self.result_ready.emit(result.strip())


def main() -> None:
    settings = load_settings()
    key = require_vault_key()
    dispatcher = Dispatcher({"settings": settings, "vault_key": key})

    app = QApplication(sys.argv)
    window = LexWindow(dispatcher)
    window.resize(600, 400)
    window.show()
    app.exec()
    event_loop.call_soon_threadsafe(event_loop.stop)


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
