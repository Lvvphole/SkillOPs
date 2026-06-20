"""Persist a run result. Mirrors src/runs/logRunResult.ts."""
from __future__ import annotations

from skillops import SkillRun
from skillops.db.queries import insert_run


def log_run_result(run: SkillRun) -> SkillRun:
    insert_run(run)
    return run
