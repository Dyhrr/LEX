import importlib
import inspect
import pkgutil

import pytest


@pytest.mark.asyncio
@pytest.mark.parametrize("module_name", [name for _, name, _ in pkgutil.iter_modules(["commands"])])
async def test_command_structure(module_name):
    module = importlib.import_module(f"commands.{module_name}")
    assert hasattr(module, "Command"), f"{module_name} missing Command"
    cmd_cls = module.Command
    instance = cmd_cls({})
    assert hasattr(instance, "trigger")
    assert hasattr(instance, "run")
    assert inspect.iscoroutinefunction(instance.run)
