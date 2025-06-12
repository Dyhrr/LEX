import argparse
import asyncio
import logging
import sys
import threading

from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QLineEdit

from core.settings import load_settings
from core.security import require_vault_key
from dispatcher import Dispatcher
from core.logger import set_log_level


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
        self.result_ready.connect(self.log.append)

    @Slot()
    def submit(self) -> None:
        text = self.input.text().strip()
        if not text:
            return
        self.log.append(f"> {text}")
        self.input.clear()
        threading.Thread(target=self._execute, args=(text,), daemon=True).start()

    def _execute(self, text: str) -> None:
        try:
            result = asyncio.run(self.dispatcher.run_command(text))
        except Exception as e:
            result = f"[ERROR] {e}"
        self.result_ready.emit(result)


def main() -> None:
    settings = load_settings()
    key = require_vault_key()
    dispatcher = Dispatcher({"settings": settings, "vault_key": key})

    app = QApplication(sys.argv)
    window = LexWindow(dispatcher)
    window.resize(600, 400)
    window.show()
    app.exec()


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
