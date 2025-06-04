import asyncio
import os
import sys

import pytest

# Ensure pytest-asyncio plugin is active so async tests run
pytest_plugins = ("pytest_asyncio",)

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


@pytest.fixture
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()
