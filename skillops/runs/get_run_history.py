"""Read run history for a skill. Mirrors src/runs/getRunHistory.ts."""
from __future__ import annotations

from typing import List

from skillops import SkillRun
from skillops.db.queries import select_runs


def get_run_history(skill_id: str) -> List[SkillRun]:
    return select_runs(skill_id)
