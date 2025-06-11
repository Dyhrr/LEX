"""Simple linter to validate plugin metadata.

Checks each module in the ``commands`` package for a ``Command`` class and
ensures that the class exposes both ``trigger`` and ``description`` attributes.
Returns a non-zero exit code if any issues are found.
"""

from __future__ import annotations

import importlib
import pkgutil
import sys
from typing import List


def lint(package: str = "commands") -> List[str]:
    errors: List[str] = []
    mod = importlib.import_module(package)
    for _, name, _ in pkgutil.iter_modules(mod.__path__):
        module_name = f"{package}.{name}"
        try:
            module = importlib.import_module(module_name)
        except Exception as e:
            errors.append(f"{module_name}: failed to import ({e})")
            continue
        cmd_cls = getattr(module, "Command", None)
        if cmd_cls is None:
            continue
        if not getattr(cmd_cls, "trigger", None):
            errors.append(f"{module_name}: missing Command.trigger")
        if not getattr(cmd_cls, "description", None):
            errors.append(f"{module_name}: missing Command.description")
    return errors


def main() -> None:
    errors = lint()
    if errors:
        print("[Linter] Issues found:")
        for err in errors:
            print(" -", err)
        sys.exit(1)
    print("[Linter] All plugins have required metadata.")


if __name__ == "__main__":
    main()
