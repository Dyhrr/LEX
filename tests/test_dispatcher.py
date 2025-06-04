import pytest

from core.settings import load_settings
from dispatcher import Dispatcher


@pytest.mark.asyncio
async def test_dispatcher_ping():
    dispatcher = Dispatcher({"settings": load_settings()})
    assert "ping" in dispatcher.trigger_map
    resp = await dispatcher.dispatch("ping")
    assert "Pong" in resp


@pytest.mark.asyncio
async def test_dispatcher_alias():
    dispatcher = Dispatcher({"settings": load_settings()})
    resp = await dispatcher.dispatch("are you alive")
    assert "Pong" in resp


@pytest.mark.asyncio
async def test_nlp_remind(tmp_path):
    settings = load_settings()
    dispatcher = Dispatcher({"settings": settings})
    for cmd in dispatcher.commands:
        if hasattr(cmd, "file"):
            cmd.file = tmp_path / "reminders.json"
    resp = await dispatcher.dispatch("Remind me to drink water")
    assert "Reminder saved" in resp
