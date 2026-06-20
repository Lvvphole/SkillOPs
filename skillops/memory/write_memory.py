"""Write/update memory JSON files deterministically."""
from __future__ import annotations

import json
from typing import Any, Dict, List

from skillops.memory.read_memory import memory_path, read_memory
from skillops.utils.dates import now_iso


def _dump(name: str, data: Any) -> None:
    memory_path(name).write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_memory(skill_id: str, entry: Dict[str, Any], *, name: str = "skill-memory.json") -> Dict[str, Any]:
    memory: Dict[str, Any] = read_memory(name, default={})
    record = dict(entry)
    record.setdefault("updated_at", now_iso())
    memory[skill_id] = record
    _dump(name, memory)
    return memory


def append_update_history(update: Dict[str, Any], *, name: str = "update-history.json") -> List[Dict[str, Any]]:
    history: List[Dict[str, Any]] = read_memory(name, default=[])
    record = dict(update)
    record.setdefault("recorded_at", now_iso())
    history.append(record)
    _dump(name, history)
    return history


def record_failure_pattern(pattern: Dict[str, Any], *, name: str = "failure-patterns.json") -> List[Dict[str, Any]]:
    patterns: List[Dict[str, Any]] = read_memory(name, default=[])
    signature = pattern.get("signature")
    for existing in patterns:
        if existing.get("signature") == signature:
            existing["count"] = existing.get("count", 1) + 1
            existing["last_seen"] = now_iso()
            _dump(name, patterns)
            return patterns
    record = dict(pattern)
    record.setdefault("count", 1)
    record.setdefault("last_seen", now_iso())
    patterns.append(record)
    _dump(name, patterns)
    return patterns
