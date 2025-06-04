import os
import pytest
from commands.vault import Command

@pytest.mark.asyncio
async def test_vault_basic(tmp_path):
    cmd = Command({})
    cmd.file = tmp_path / "vault.json"

    resp = await cmd.run("list")
    assert "empty" in resp

    await cmd.run("set foo bar")
    assert os.path.exists(cmd.file)

    value = await cmd.run("get foo")
    assert value == "bar"

    resp = await cmd.run("list")
    assert "foo" in resp

