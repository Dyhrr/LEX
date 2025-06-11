from __future__ import annotations

from collections.abc import MutableMapping
from typing import Any, Iterator


class LexContext(MutableMapping):
    """Context container separating system, user and plugin data."""

    def __init__(self, data: dict | None = None) -> None:
        data = data or {}
        self.system: dict = data.get("system", {})
        self.user: dict = data.get("user", {})
        self.plugin: dict = data.get("plugin", {})
        self.system.update(
            {k: v for k, v in data.items() if k not in {"system", "user", "plugin"}}
        )

    # Mapping protocol -------------------------------------------------
    def __getitem__(self, key: str) -> Any:
        if key in {"system", "user", "plugin"}:
            return getattr(self, key)
        for space in (self.system, self.user, self.plugin):
            if key in space:
                return space[key]
        raise KeyError(key)

    def __setitem__(self, key: str, value: Any) -> None:
        if key in {"system", "user", "plugin"}:
            setattr(self, key, value)
        else:
            self.system[key] = value

    def __delitem__(self, key: str) -> None:
        for space in (self.system, self.user, self.plugin):
            if key in space:
                del space[key]
                return
        raise KeyError(key)

    def __iter__(self) -> Iterator[str]:
        yield from {"system", "user", "plugin"}
        for space in (self.system, self.user, self.plugin):
            yield from space.keys()

    def __len__(self) -> int:
        return sum(len(s) for s in (self.system, self.user, self.plugin)) + 3

    # Convenience helpers ---------------------------------------------
    def get(self, key: str, default: Any = None) -> Any:  # type: ignore[override]
        try:
            return self[key]
        except KeyError:
            return default

    def setdefault(self, key: str, default: Any) -> Any:  # type: ignore[override]
        if key in self:
            return self[key]
        self[key] = default
        return default

