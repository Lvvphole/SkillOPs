"""Create a new skill version without overwriting prior versions.

Versions live in skills/<skill>/versions/vN.skill.md. Creating a version that
already exists requires allow_overwrite=True AND a changelog reason; otherwise it
raises, protecting prior versions.
"""
from __future__ import annotations

from pathlib import Path
from typing import Optional

from skillops.utils.dates import now_iso
from skillops.versioning.write_changelog import write_changelog


def _skill_dir(skill_id: str, skills_root: str) -> Path:
    return Path(skills_root) / skill_id / "versions"


def next_version(skill_id: str, skills_root: str = "skills") -> str:
    versions_dir = _skill_dir(skill_id, skills_root)
    existing = sorted(
        int(p.stem.split(".")[0][1:])
        for p in versions_dir.glob("v*.skill.md")
        if p.stem.split(".")[0][1:].isdigit()
    ) if versions_dir.exists() else []
    return f"v{(existing[-1] + 1) if existing else 1}"


def create_skill_version(
    skill_id: str,
    content: str,
    *,
    version: Optional[str] = None,
    reason: str = "",
    skills_root: str = "skills",
    changelog_path: str = "artifacts/skill-change-log.md",
    allow_overwrite: bool = False,
) -> dict:
    versions_dir = _skill_dir(skill_id, skills_root)
    versions_dir.mkdir(parents=True, exist_ok=True)
    version = version or next_version(skill_id, skills_root)
    target = versions_dir / f"{version}.skill.md"

    if target.exists() and not allow_overwrite:
        raise FileExistsError(
            f"{target} exists; refusing to overwrite {version} without allow_overwrite + changelog"
        )
    if target.exists() and not reason:
        raise ValueError("overwriting an existing version requires a changelog reason")

    target.write_text(content, encoding="utf-8")
    write_changelog(
        skill_id,
        from_version="(new)",
        to_version=version,
        reason=reason or "version created",
        changelog_path=changelog_path,
    )
    return {"skill_id": skill_id, "version": version, "path": str(target), "created_at": now_iso()}
