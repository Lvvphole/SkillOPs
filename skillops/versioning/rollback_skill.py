"""Roll back the active skill version to a prior version (reversible updates).

Rollback never deletes versions; it repoints the active pointer file
(skills/<skill>/ACTIVE_VERSION) to an existing prior version and logs the change.
"""
from __future__ import annotations

from pathlib import Path
from typing import Dict

from skillops.versioning.write_changelog import write_changelog

_POINTER = "ACTIVE_VERSION"


def active_version(skill_id: str, skills_root: str = "skills") -> str | None:
    pointer = Path(skills_root) / skill_id / _POINTER
    return pointer.read_text(encoding="utf-8").strip() if pointer.exists() else None


def set_active_version(skill_id: str, version: str, skills_root: str = "skills") -> None:
    base = Path(skills_root) / skill_id
    base.mkdir(parents=True, exist_ok=True)
    (base / _POINTER).write_text(version + "\n", encoding="utf-8")


def rollback_skill(
    skill_id: str,
    to_version: str,
    *,
    skills_root: str = "skills",
    changelog_path: str = "artifacts/skill-change-log.md",
) -> Dict[str, str]:
    target = Path(skills_root) / skill_id / "versions" / f"{to_version}.skill.md"
    if not target.exists():
        raise FileNotFoundError(f"cannot roll back to missing version: {target}")
    previous = active_version(skill_id, skills_root) or "(unset)"
    set_active_version(skill_id, to_version, skills_root)
    write_changelog(
        skill_id,
        from_version=previous,
        to_version=to_version,
        reason="rollback",
        changelog_path=changelog_path,
    )
    return {"skill_id": skill_id, "rolled_back_from": previous, "active_version": to_version}
