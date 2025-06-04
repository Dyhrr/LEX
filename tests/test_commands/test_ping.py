import pytest
from commands.ping import Command


@pytest.mark.asyncio
async def test_ping_response():
    cmd = Command({})
    resp = await cmd.run("")
    assert "Pong" in resp
