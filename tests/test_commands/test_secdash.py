import pytest
from commands.secdash import Command


@pytest.mark.asyncio
async def test_kill_disabled():
    cmd = Command({"settings": {"allow_process_terminate": False}})
    result = await cmd.run("kill 123")
    assert "disabled" in result.lower()
