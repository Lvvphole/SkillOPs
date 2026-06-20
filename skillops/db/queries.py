"""JSON-file persistence mirroring src/db/queries.ts.

Storage location is controlled by SKILLOPS_DATA_DIR (default: .skillops-data),
which is gitignored so committed artifacts stay deterministic. The loop writes a
committed evidence snapshot separately (artifacts/run-history.json).
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict, List

from skillops import SkillRun


def data_dir() -> Path:
    return Path(os.environ.get("SKILLOPS_DATA_DIR", ".skillops-data"))


def _store(name: str) -> Path:
    return data_dir() / name


def _read(name: str) -> List[Dict[str, Any]]:
    path = _store(name)
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8").strip()
    return json.loads(text) if text else []


def _write(name: str, rows: List[Dict[str, Any]]) -> None:
    path = _store(name)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(rows, indent=2), encoding="utf-8")


# --- runs ---------------------------------------------------------------

def insert_run(run: SkillRun) -> SkillRun:
    rows = _read("runs.json")
    rows.append(run.to_dict())
    _write("runs.json", rows)
    return run


def select_runs(skill_id: str) -> List[SkillRun]:
    return [SkillRun.from_dict(r) for r in _read("runs.json") if r.get("skill_id") == skill_id]


# --- versions -----------------------------------------------------------

def record_version(skill_id: str, version: str, path: str, created_at: str, reason: str) -> None:
    rows = _read("versions.json")
    rows = [r for r in rows if not (r["skill_id"] == skill_id and r["version"] == version)]
    rows.append({
        "skill_id": skill_id,
        "version": version,
        "path": path,
        "created_at": created_at,
        "reason": reason,
    })
    _write("versions.json", rows)


def select_versions(skill_id: str) -> List[Dict[str, Any]]:
    return [r for r in _read("versions.json") if r.get("skill_id") == skill_id]


# --- updates ------------------------------------------------------------

def record_update(update: Dict[str, Any]) -> None:
    rows = _read("updates.json")
    rows.append(update)
    _write("updates.json", rows)


def select_updates(skill_id: str) -> List[Dict[str, Any]]:
    return [r for r in _read("updates.json") if r.get("skill_id") == skill_id]
