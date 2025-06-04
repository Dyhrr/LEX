import pytest
from commands import vault as vault_module


@pytest.mark.asyncio
async def test_vault_set_get_list(tmp_path):
    # redirect vault file to temporary directory
    vault_file = tmp_path / "vault.json"
    vault_module.VAULT_FILE = str(vault_file)
    cmd = vault_module.Command({})

    resp = await cmd.run("set foo bar")
    assert "Stored" in resp

    resp = await cmd.run("get foo")
    assert resp == "bar"

    resp = await cmd.run("list")
    assert "foo" in resp

    resp = await cmd.run("get missing")
    assert "Not found" in resp
