import sys
import time

import pytest

from dispatcher import Dispatcher


@pytest.mark.asyncio
async def test_dispatcher_hot_reload(tmp_path, monkeypatch):
    pkg = tmp_path / "temp_cmds"
    pkg.mkdir()
    (pkg / "__init__.py").write_text("")

    monkeypatch.syspath_prepend(str(tmp_path))

    dispatcher = Dispatcher(package="temp_cmds")
    # no plugin yet
    resp = await dispatcher.dispatch("hot")
    assert "don't know" in resp

    plugin = pkg / "hot.py"
    plugin.write_text(
        """
class Command:
    trigger = ["hot"]

    def __init__(self, context):
        pass

    async def run(self, args: str) -> str:
        return "first"
"""
    )
    time.sleep(0.05)

    dispatcher.check_for_updates()
    resp = await dispatcher.dispatch("hot")
    assert resp == "first"

    plugin.write_text(
        """
class Command:
    trigger = ["hot"]

    def __init__(self, context):
        pass

    async def run(self, args: str) -> str:
        return "second"
"""
    )
    time.sleep(0.05)

    dispatcher.check_for_updates()
    resp = await dispatcher.dispatch("hot")
    assert resp == "second"
