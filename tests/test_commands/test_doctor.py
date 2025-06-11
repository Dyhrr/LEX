import pytest
from commands.doctor import Command


@pytest.mark.asyncio
async def test_doctor_runs():
    cmd = Command({"settings": {}})
    result = await cmd.run("")
    assert result.startswith("[Lex]")
