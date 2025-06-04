import pytest

from commands.learn import Command
from dispatcher import Dispatcher
from core.settings import load_settings
from core import nlp


@pytest.mark.asyncio
async def test_learn_custom_phrase(tmp_path, monkeypatch):
    custom_file = tmp_path / "custom.json"
    monkeypatch.setattr(nlp, "CUSTOM_INTENTS_FILE", str(custom_file))
    # reset caches and registry
    nlp._custom_cache = None
    nlp._refresh_custom_registry()

    cmd = Command({})
    resp = await cmd.run("hello there as ping")
    assert "Learned" in resp

    dispatcher = Dispatcher({"settings": load_settings()})
    result = await dispatcher.dispatch("hello there")
    assert "Pong" in result

