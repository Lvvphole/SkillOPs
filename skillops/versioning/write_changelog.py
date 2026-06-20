"""Append a changelog entry. Required whenever a version is created or replaced."""
from __future__ import annotations

from pathlib import Path

from skillops.utils.dates import now_iso


def write_changelog(
    skill_id: str,
    *,
    from_version: str,
    to_version: str,
    reason: str,
    changelog_path: str = "artifacts/skill-change-log.md",
    metrics_note: str = "",
) -> str:
    path = Path(changelog_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text("# Skill Change Log\n\n", encoding="utf-8")
    entry = (
        f"- {now_iso()} | `{skill_id}` | {from_version} -> {to_version} | {reason}"
        + (f" | {metrics_note}" if metrics_note else "")
        + "\n"
    )
    with path.open("a", encoding="utf-8") as fh:
        fh.write(entry)
    return entry
