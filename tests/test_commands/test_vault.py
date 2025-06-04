import pytest

from commands.vault import Command


@pytest.mark.asyncio
async def test_vault_set_and_get(tmp_path):
    cmd = Command({})
    cmd.file = tmp_path / "vault.json"

    resp = await cmd.run("set foo bar")
    assert "Stored" in resp

    result = await cmd.run("get foo")
    assert result == "bar"


@pytest.mark.asyncio
async def test_vault_list(tmp_path):
    cmd = Command({})
    cmd.file = tmp_path / "vault.json"

    await cmd.run("set alpha beta")
    listing = await cmd.run("list")
    assert "alpha" in listing

