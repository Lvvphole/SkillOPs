"""Capture the working/committed diff to a patch file for verifier evidence."""
from __future__ import annotations

import subprocess
from pathlib import Path


def capture_diff(
    out_path: str = "artifacts/final-diff.patch",
    *,
    base: str = "main",
    cwd: str = ".",
) -> str:
    """Write `git diff <base>...HEAD` (plus uncommitted changes) to out_path."""
    committed = subprocess.run(
        ["git", "diff", f"{base}...HEAD"], cwd=cwd, capture_output=True, text=True
    ).stdout
    working = subprocess.run(
        ["git", "diff"], cwd=cwd, capture_output=True, text=True
    ).stdout
    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(committed + working, encoding="utf-8")
    return str(out)
