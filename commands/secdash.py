"""Basic security dashboard utilities."""

from __future__ import annotations

import asyncio
import psutil


class Command:
    trigger = ["secdash"]

    def __init__(self, context):
        self.context = context

    def _format_conn(self, conn: psutil._common.sconn) -> str:
        laddr = f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else "?"
        raddr = f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "?"
        return f"PID {conn.pid} {laddr} -> {raddr}"

    # ---------------------------------------------------------
    # Command entry point
    # ---------------------------------------------------------
    async def run(self, args: str) -> str:
        await asyncio.sleep(0)
        tokens = args.split()
        if tokens and tokens[0] == "kill" and len(tokens) > 1:
            settings = self.context.get("settings", {})
            if not settings.get("allow_process_terminate", False):
                return "[Lex] Process termination disabled in settings."
            try:
                pid = int(tokens[1])
                psutil.Process(pid).terminate()
                return f"[Lex] Terminated PID {pid}."
            except Exception as e:
                return f"[Lex] Failed to terminate: {e}"

        conns = [
            c
            for c in psutil.net_connections(kind="inet")
            if c.raddr
            and c.raddr.ip
            and not c.raddr.ip.startswith("127.")
            and c.pid
        ]
        if not conns:
            return "[Lex] No external connections detected."
        lines = [self._format_conn(c) for c in conns[:5]]
        if len(conns) > 5:
            lines.append(f"...and {len(conns) - 5} more")
        return "\n".join(lines)
