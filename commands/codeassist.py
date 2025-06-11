"""Offline code snippet helper."""

import asyncio


SNIPPETS: dict[str, str] = {
    "csv": (
        "import csv\n\n"
        "with open('file.csv', newline='') as fh:\n"
        "    reader = csv.DictReader(fh)\n"
        "    for row in reader:\n"
        "        print(row)"
    ),
    "http server": (
        "from http.server import HTTPServer, SimpleHTTPRequestHandler\n\n"
        "server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)\n"
        "server.serve_forever()"
    ),
}


class Command:
    description = "Return handy Python code snippets for common tasks."
    """Return small code snippets for common tasks."""

    trigger = ["codeassist"]

    def __init__(self, context):
        self.context = context

    async def run(self, args: str) -> str:
        await asyncio.sleep(0)
        query = args.strip().lower()
        if not query or query == "list":
            names = ", ".join(sorted(SNIPPETS))
            return f"[Lex] Available snippets: {names}"

        snippet = SNIPPETS.get(query)
        if snippet:
            return snippet

        return "[Lex] No snippet for that topic. Try 'codeassist list'."
