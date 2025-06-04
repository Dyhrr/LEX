"""Basic Home Assistant integration."""

from __future__ import annotations

import asyncio
import requests


class Command:
    trigger = ["smarthome"]

    def __init__(self, context):
        self.context = context
        settings = context.get("settings", {})
        self.url: str = settings.get("ha_url", "http://localhost:8123")
        self.token: str | None = settings.get("ha_token")

    def _post(self, path: str, data: dict) -> str:
        url = f"{self.url}/api/services/{path}"
        headers = {"Authorization": f"Bearer {self.token}"} if self.token else {}
        try:
            resp = requests.post(url, headers=headers, json=data, timeout=5)
            if resp.status_code in (200, 201):
                return "ok"
            return f"HTTP {resp.status_code}"
        except Exception as e:
            return str(e)

    # -----------------------------------------------------
    # Command entry point
    # -----------------------------------------------------
    async def run(self, args: str) -> str:
        await asyncio.sleep(0)
        tokens = args.split()
        if not tokens:
            return (
                "[Lex] Use 'smarthome light on <id>', 'light off <id>', "
                "'thermostat <temp>' or 'scene <name>'."
            )

        cmd = tokens[0]

        if cmd == "light" and len(tokens) >= 3:
            action = tokens[1]
            entity = tokens[2]
            if action not in ("on", "off"):
                return "[Lex] Specify 'on' or 'off' for the light."
            path = f"light/turn_{action}"
            result = await asyncio.to_thread(self._post, path, {"entity_id": entity})
            if result == "ok":
                return f"[Lex] Light {entity} turned {action}."
            return f"[Lex] Failed: {result}"

        if cmd == "thermostat" and len(tokens) >= 2:
            try:
                temp = float(tokens[1])
            except ValueError:
                return "[Lex] Give me a temperature number."
            data = {"temperature": temp}
            result = await asyncio.to_thread(
                self._post, "climate/set_temperature", data
            )
            if result == "ok":
                return f"[Lex] Thermostat set to {temp}°C."
            return f"[Lex] Failed: {result}"

        if cmd == "scene" and len(tokens) >= 2:
            scene = tokens[1]
            data = {"entity_id": f"scene.{scene}"}
            result = await asyncio.to_thread(self._post, "scene/turn_on", data)
            if result == "ok":
                return f"[Lex] Scene '{scene}' activated."
            return f"[Lex] Failed: {result}"

        return (
            "[Lex] Use 'smarthome light on <id>', 'light off <id>', "
            "'thermostat <temp>' or 'scene <name>'."
        )

