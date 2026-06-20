"""Read a memory JSON file, returning a default when absent or empty."""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

_MEMORY_DIR = Path(__file__).resolve().parent


def memory_path(name: str) -> Path:
    """Resolve a memory file, honoring SKILLOPS_MEMORY_DIR for test isolation."""
    override = os.environ.get("SKILLOPS_MEMORY_DIR")
    base = Path(override) if override else _MEMORY_DIR
    base.mkdir(parents=True, exist_ok=True)
    return base / name


def read_memory(name: str, default: Any = None) -> Any:
    path = memory_path(name)
    if not path.exists():
        return default if default is not None else {}
    text = path.read_text(encoding="utf-8").strip()
    if not text:
        return default if default is not None else {}
    return json.loads(text)
