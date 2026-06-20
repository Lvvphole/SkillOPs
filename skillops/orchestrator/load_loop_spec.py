"""Load a LoopSpec (or any manifest) from YAML."""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

import yaml


def load_yaml(path: str) -> Dict[str, Any]:
    text = Path(path).read_text(encoding="utf-8")
    data = yaml.safe_load(text)
    if not isinstance(data, dict):
        raise ValueError(f"manifest at {path} did not parse to a mapping")
    return data


def load_loop_spec(path: str) -> Dict[str, Any]:
    """Load a LoopSpec manifest. Schema validation is a separate, explicit step."""
    spec = load_yaml(path)
    spec["_path"] = path
    return spec
