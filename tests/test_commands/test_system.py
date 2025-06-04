import pytest

from commands.system import Command


@pytest.mark.asyncio
async def test_system_info():
    cmd = Command({})
    resp = await cmd.run("")
    assert "System:" in resp
