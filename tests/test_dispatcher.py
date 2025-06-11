import pytest
import asyncio

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


@pytest.mark.asyncio
async def test_nlp_remind_variation(tmp_path):
    settings = load_settings()
    dispatcher = Dispatcher({"settings": settings})
    for cmd in dispatcher.commands:
        if hasattr(cmd, "file"):
            cmd.file = tmp_path / "reminders2.json"
    resp = await dispatcher.dispatch("Can you remind me to stand up")
    assert "Reminder saved" in resp


@pytest.mark.asyncio
async def test_nlp_tools_uuid():
    dispatcher = Dispatcher({"settings": load_settings()})
    resp = await dispatcher.dispatch("I need a uuid")
    import uuid
    uuid.UUID(resp)


@pytest.mark.asyncio
async def test_nlp_weather():
    dispatcher = Dispatcher({"settings": load_settings()})
    resp = await dispatcher.dispatch("How's the weather in Tokyo")
    assert "Tokyo" in resp


@pytest.mark.asyncio
async def test_dispatcher_features(tmp_path, monkeypatch):
    import json
    from commands import features

    file = tmp_path / "feature_suggestions.json"
    file.write_text(json.dumps({"brew coffee": {"pattern": "^brew$"}}))
    dispatcher = Dispatcher({"settings": load_settings()})
    monkeypatch.setattr(features, "SUGGESTIONS_FILE", file)
    resp = await dispatcher.dispatch("what features are you missing")
    assert "brew coffee" in resp


@pytest.mark.asyncio
async def test_nlp_fuzzy_match(tmp_path):
    settings = load_settings()
    dispatcher = Dispatcher({"settings": settings})
    for cmd in dispatcher.commands:
        if hasattr(cmd, "file"):
            cmd.file = tmp_path / "reminders_fuzzy.json"
    # Intentionally misspelled command
    resp = await dispatcher.dispatch("remmind me to sleep")
    assert "Reminder saved" in resp


@pytest.mark.asyncio
async def test_command_timeout(monkeypatch):
    settings = load_settings()
    settings["plugin_timeout"] = 0.1
    dispatcher = Dispatcher({"settings": settings})

    class Dummy:
        trigger = ["hang"]

        async def run(self, _args):
            await asyncio.sleep(1)
            return "done"

    dummy = Dummy()
    dispatcher.commands.append(dummy)
    dispatcher.trigger_map["hang"] = dummy

    result = await dispatcher.dispatch("hang")
    assert "timed out" in result.lower()


@pytest.mark.asyncio
async def test_auto_suggest():
    settings = load_settings()
    settings["fuzzy_threshold"] = 1.0
    dispatcher = Dispatcher({"settings": settings})
    result = await dispatcher.dispatch("pimg")
    assert "did you mean" in result.lower()


def test_context_nested():
    dispatcher = Dispatcher({"settings": load_settings()})
    ctx = dispatcher.context
    assert "system" in ctx
    assert ctx["settings"] is ctx.system.get("settings")

