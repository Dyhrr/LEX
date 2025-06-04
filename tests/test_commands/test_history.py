import pytest

from dispatcher import Dispatcher


@pytest.mark.asyncio
async def test_history_tracks_commands():
    dispatcher = Dispatcher({})
    await dispatcher.dispatch("ping")
    resp = await dispatcher.dispatch("history")
    assert "ping" in resp
