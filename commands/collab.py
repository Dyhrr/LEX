"""Simple collaboration utilities like file sharing or chat."""

from __future__ import annotations

import asyncio
import functools
import os
import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler


class Command:
    trigger = ["collab"]

    def __init__(self, context):
        self.context = context
        self.http_thread: threading.Thread | None = None
        self.httpd: HTTPServer | None = None

    # ---------------------------------------------------------
    # HTTP file share helpers
    # ---------------------------------------------------------
    def _start_share(self, path: str, port: int) -> str:
        if self.http_thread and self.http_thread.is_alive():
            return "[Lex] Share server already running."

        if not os.path.isdir(path):
            return "[Lex] Directory does not exist."

        def serve() -> None:
            handler = functools.partial(SimpleHTTPRequestHandler, directory=path)
            with HTTPServer(("0.0.0.0", port), handler) as self.httpd:
                self.httpd.serve_forever()

        self.http_thread = threading.Thread(target=serve, daemon=True)
        self.http_thread.start()
        return f"[Lex] Sharing {path} on port {port}."

    def _stop_share(self) -> str:
        if not self.httpd:
            return "[Lex] Share server not running."
        try:
            self.httpd.shutdown()
        except Exception:
            pass
        self.httpd = None
        return "[Lex] Share server stopped."

    # ---------------------------------------------------------
    # Command entry point
    # ---------------------------------------------------------
    async def run(self, args: str) -> str:
        await asyncio.sleep(0)
        tokens = args.split()
        if not tokens:
            return "[Lex] Use 'collab share <path> [port]' or 'collab stop'."

        cmd = tokens[0]

        if cmd == "share" and len(tokens) >= 2:
            path = tokens[1]
            port = int(tokens[2]) if len(tokens) >= 3 else 8000
            return self._start_share(path, port)

        if cmd == "stop":
            return self._stop_share()

        return "[Lex] Unknown collab command."
