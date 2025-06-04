"""Proactively monitor battery and run scheduled commands."""

from __future__ import annotations

import asyncio
import json
import os
from datetime import datetime
from pathlib import Path

import psutil


TASK_FILE = Path("memory") / "proactive.json"


class Command:
    trigger = ["proactive"]

    def __init__(self, context):
        self.context = context
        self.file = TASK_FILE
        self.tasks: list[dict] = self._load()
        self.loop_task: asyncio.Task | None = None

    # -----------------------------------------------------
    # Persistence helpers
    # -----------------------------------------------------
    def _load(self) -> list[dict]:
        if self.file.exists():
            try:
                with self.file.open("r", encoding="utf-8") as fh:
                    return json.load(fh)
            except Exception:
                pass
        return []

    def _save(self) -> None:
        os.makedirs(self.file.parent, exist_ok=True)
        with self.file.open("w", encoding="utf-8") as fh:
            json.dump(self.tasks, fh)

    # -----------------------------------------------------
    # Background loop
    # -----------------------------------------------------
    async def _check_battery(self) -> None:
        batt = psutil.sensors_battery()
        if batt and batt.power_plugged is False and batt.percent <= 20:
            dispatcher = self.context.get("dispatcher")
            cmd = dispatcher.trigger_map.get("notify") if dispatcher else None
            if cmd:
                await cmd.run(f"Battery low ({batt.percent}%)")

    async def _run_tasks(self) -> None:
        dispatcher = self.context.get("dispatcher")
        if not dispatcher:
            return
        now = datetime.now().strftime("%H:%M")
        for task in self.tasks:
            if task.get("time") == now:
                last = task.get("last")
                today = datetime.now().date().isoformat()
                if last == today:
                    continue
                await dispatcher.dispatch(task["command"])
                task["last"] = today
                self._save()

    async def _loop(self) -> None:
        while True:
            await asyncio.sleep(60)
            await self._check_battery()
            await self._run_tasks()

    def _start_loop(self) -> str:
        if self.loop_task and not self.loop_task.done():
            return "[Lex] Proactive mode already running."
        self.loop_task = asyncio.create_task(self._loop())
        return "[Lex] Proactive mode activated."

    def _stop_loop(self) -> str:
        if self.loop_task:
            self.loop_task.cancel()
            self.loop_task = None
            return "[Lex] Proactive mode stopped."
        return "[Lex] Proactive mode not running."

    # -----------------------------------------------------
    # Command entry point
    # -----------------------------------------------------
    async def run(self, args: str) -> str:
        await asyncio.sleep(0)
        tokens = args.split(maxsplit=2)
        if not tokens:
            return (
                "[Lex] Use 'proactive start', 'stop', 'list', "
                "'add HH:MM <command>' or 'remove <num>'."
            )

        cmd = tokens[0]

        if cmd == "start":
            return self._start_loop()

        if cmd == "stop":
            return self._stop_loop()

        if cmd == "list":
            if not self.tasks:
                return "[Lex] No proactive tasks defined."
            return "\n".join(
                f"{i+1}. {t['time']} -> {t['command']}" for i, t in enumerate(self.tasks)
            )

        if cmd == "add" and len(tokens) == 3:
            time_str = tokens[1]
            try:
                datetime.strptime(time_str, "%H:%M")
            except ValueError:
                return "[Lex] Time format should be HH:MM."
            command = tokens[2]
            self.tasks.append({"time": time_str, "command": command, "last": ""})
            self._save()
            return f"[Lex] Proactive task added for {time_str}."

        if cmd == "remove" and len(tokens) >= 2:
            try:
                idx = int(tokens[1]) - 1
            except ValueError:
                return "[Lex] Provide a task number to remove."
            if 0 <= idx < len(self.tasks):
                removed = self.tasks.pop(idx)
                self._save()
                return f"[Lex] Removed task '{removed['command']}'."
            return "[Lex] No task with that number."

        return (
            "[Lex] Use 'proactive start', 'stop', 'list', "
            "'add HH:MM <command>' or 'remove <num>'."
        )

