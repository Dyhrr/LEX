import os
import pytest

from commands import vault


@pytest.mark.asyncio
async def test_vault_set_get_and_list(tmp_path, monkeypatch):
    test_file = tmp_path / "vault.json"
    monkeypatch.setattr(vault, "VAULT_FILE", str(test_file))

    cmd = vault.Command({})
    assert cmd.file == str(test_file)

    resp = await cmd.run("set foo bar")
    assert "Stored" in resp

    value = await cmd.run("get foo")
    assert value == "bar"

    keys = await cmd.run("list")
    assert "foo" in keys
