"""Minimal Textual-based TUI for Lex."""

import asyncio
import argparse

from textual.app import App, ComposeResult
from textual.containers import Container
from textual.reactive import reactive
from textual.widgets import Input, Log, Static

from core.settings import load_settings
from core.security import require_vault_key
from dispatcher import Dispatcher


class LexApp(App):
    """Textual TUI that interacts with Lex's dispatcher."""

    CSS = """
    Screen { layout: vertical; }
    #log { height: 1fr; }
    #input { height:3; }
    #sidebar { width:25; border:heavy $secondary; }
    """

    BINDINGS = [("enter", "submit", "Run command")]

    show_sidebar = reactive(False)

    def __init__(self, dispatcher: Dispatcher, *, sidebar: bool = False) -> None:
        super().__init__()
        self.dispatcher = dispatcher
        self.show_sidebar = sidebar

    def compose(self) -> ComposeResult:
        if self.show_sidebar:
            with Container(id="sidebar"):
                yield Static(self._sidebar_text(), id="triggers")
        yield Log(id="log")
        yield Input(placeholder="Enter command", id="input")

    def on_mount(self) -> None:
        self.query_one(Input).focus()

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
        field.value = ""
        response = await self.dispatcher.run_command(text)
        if response:
            log.write_line(response)
        if self.show_sidebar:
            # reload sidebar in case commands changed
            self.query_one("#triggers", Static).update(self._sidebar_text())


async def main(sidebar: bool = False) -> None:
    """Entry point to start the TUI."""

    settings = load_settings()
    key = require_vault_key()
    dispatcher = Dispatcher({"settings": settings, "vault_key": key})
    app = LexApp(dispatcher, sidebar=sidebar)
    await app.run_async()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Lex Textual UI")
    parser.add_argument(
        "--sidebar",
        action="store_true",
        help="Show available command triggers",
    )
    args = parser.parse_args()
    asyncio.run(main(sidebar=args.sidebar))
