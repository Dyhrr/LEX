"""Textual-based frontend for Lex with theme support."""

import asyncio
import argparse
import logging
from pathlib import Path

from textual.app import App, ComposeResult
from textual.containers import Container
from textual.reactive import reactive
from textual.widgets import Input, Log, Static, Header, Footer

from core.settings import load_settings
from core.security import require_vault_key
from dispatcher import Dispatcher
from core.logger import set_log_level

LEX_VERSION = "0.1.0"
THEMES_DIR = Path("themes")


class LexApp(App):
    """Textual TUI that interacts with Lex's dispatcher."""

    BINDINGS = [("enter", "submit", "Run command")]
    show_sidebar = reactive(False)

    def __init__(self, dispatcher: Dispatcher, *, sidebar: bool = False, theme: str = "lex") -> None:
        theme_path = THEMES_DIR / f"{theme}.css"
        super().__init__(css_path=str(theme_path))
        self.dispatcher = dispatcher
        self.show_sidebar = sidebar
        self.history: list[str] = []
        self.history_index: int = 0

    # -----------------------------------------------------
    # Theme handling
    # -----------------------------------------------------
    def set_theme(self, name: str) -> bool:
        """Attempt to reload the UI with the given theme."""
        path = THEMES_DIR / f"{name}.css"
        if not path.exists():
            return False
        self.css_path = [path]
        self.stylesheet.read_all(self.css_path)
        self.stylesheet.parse()
        self.refresh_css()
        return True

    # -----------------------------------------------------
    # Layout
    # -----------------------------------------------------
    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        if self.show_sidebar:
            with Container(id="sidebar"):
                yield Static(self._sidebar_text(), id="triggers")
        yield Log(id="log")
        yield Input(placeholder="Enter command", id="input")
        yield Footer()
        yield Static(f"Lex v{LEX_VERSION} by Dyhrrr", id="version")

    def on_mount(self) -> None:
        self.query_one(Input).focus()
        settings = self.dispatcher.context.get("settings", {})
        cloud = "ON" if settings.get("use_cloud") else "OFF"
        sarcasm = settings.get("sarcasm_level", 0)
        plugins = len(self.dispatcher.commands)
        self.sub_title = f"Cloud: {cloud} | Sarcasm: {sarcasm} | Plugins: {plugins}"

    def _sidebar_text(self) -> str:
        trigs = sorted(self.dispatcher.trigger_map.keys())
        return "\n".join(trigs)

    async def action_submit(self) -> None:
        field = self.query_one(Input)
        text = field.value.strip()
        if not text:
            return
        log = self.query_one(Log)
        log.write_line(f"> {text}")
        log.scroll_end(animate=False)
        field.value = ""
        self.history.append(text)
        self.history_index = len(self.history)
        try:
            response = await self.dispatcher.run_command(text)
        except Exception as e:
            response = f"[ERROR] {e}"
        if response:
            log.write_line(response)
            log.scroll_end(animate=False)
        if self.show_sidebar:
            # reload sidebar in case commands changed
            self.query_one("#triggers", Static).update(self._sidebar_text())

    def on_key(self, event) -> None:
        input_widget = self.query_one(Input)
        if not input_widget.has_focus:
            return
        if event.key == "up":
            if self.history:
                self.history_index = max(0, self.history_index - 1)
                input_widget.value = self.history[self.history_index]
                input_widget.cursor_position = len(input_widget.value)
                event.prevent_default()
        elif event.key == "down":
            if self.history:
                self.history_index = min(len(self.history), self.history_index + 1)
                if self.history_index < len(self.history):
                    input_widget.value = self.history[self.history_index]
                else:
                    input_widget.value = ""
                input_widget.cursor_position = len(input_widget.value)
                event.prevent_default()


async def main(sidebar: bool = False) -> None:
    """Entry point to start the TUI."""

    settings = load_settings()
    key = require_vault_key()
    dispatcher = Dispatcher({"settings": settings, "vault_key": key})
    theme = settings.get("theme", "lex")
    app = LexApp(dispatcher, sidebar=sidebar, theme=theme)
    dispatcher.context["app"] = app
    await app.run_async()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Lex Textual UI")
    parser.add_argument(
        "--sidebar",
        action="store_true",
        help="Show available command triggers",
    )
    parser.add_argument("--verbose", action="store_true", help="Enable debug logging")
    parser.add_argument("--quiet", action="store_true", help="Only show warnings")
    args = parser.parse_args()

    if args.verbose:
        set_log_level(logging.DEBUG)
    elif args.quiet:
        set_log_level(logging.WARNING)

    asyncio.run(main(sidebar=args.sidebar))
