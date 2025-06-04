import uuid
import pytest

from commands.tools import Command


@pytest.mark.asyncio
async def test_tools_uuid():
    cmd = Command({})
    result = await cmd.run("uuid")
    # ensure valid UUID
    uuid_obj = uuid.UUID(result)
    assert str(uuid_obj) == result


@pytest.mark.asyncio
async def test_tools_password_length():
    cmd = Command({})
    pwd = await cmd.run("password 16")
    assert len(pwd) == 16


@pytest.mark.asyncio
async def test_tools_help_message():
    cmd = Command({})
    msg = await cmd.run("")
    assert "tools uuid" in msg
