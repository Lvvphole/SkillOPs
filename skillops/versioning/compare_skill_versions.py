"""Diff two skill versions (current vs candidate) for the version comparison gate."""
from __future__ import annotations

import difflib
from pathlib import Path
from typing import Any, Dict


def _read(skill_id: str, version: str, skills_root: str) -> str:
    path = Path(skills_root) / skill_id / "versions" / f"{version}.skill.md"
    if not path.exists():
        raise FileNotFoundError(str(path))
    return path.read_text(encoding="utf-8")


def compare_skill_versions(
    skill_id: str,
    from_version: str,
    to_version: str,
    *,
    skills_root: str = "skills",
) -> Dict[str, Any]:
    a = _read(skill_id, from_version, skills_root).splitlines()
    b = _read(skill_id, to_version, skills_root).splitlines()
    diff = list(difflib.unified_diff(a, b, fromfile=from_version, tofile=to_version, lineterm=""))
    added = sum(1 for line in diff if line.startswith("+") and not line.startswith("+++"))
    removed = sum(1 for line in diff if line.startswith("-") and not line.startswith("---"))
    return {
        "skill_id": skill_id,
        "from_version": from_version,
        "to_version": to_version,
        "changed": bool(diff),
        "lines_added": added,
        "lines_removed": removed,
        "diff": "\n".join(diff),
    }
