"""Create or confirm a git feature branch (never works on the default branch)."""
from __future__ import annotations

import subprocess
from typing import Dict


def _git(*args: str, cwd: str = ".") -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True)


def current_branch(cwd: str = ".") -> str:
    result = _git("rev-parse", "--abbrev-ref", "HEAD", cwd=cwd)
    return result.stdout.strip()


def create_branch(name: str, *, base: str = "main", cwd: str = ".", create: bool = True) -> Dict[str, object]:
    """Switch to `name`, creating it from `base` when create=True.

    Refuses to operate directly on the default branch name.
    """
    if name == base:
        raise ValueError(f"refusing to work directly on default branch '{base}'")
    existing = _git("rev-parse", "--verify", name, cwd=cwd).returncode == 0
    if existing:
        result = _git("checkout", name, cwd=cwd)
    elif create:
        result = _git("checkout", "-b", name, base, cwd=cwd)
    else:
        result = _git("checkout", name, cwd=cwd)
    return {
        "branch": name,
        "existed": existing,
        "ok": result.returncode == 0,
        "stderr": result.stderr.strip(),
    }
