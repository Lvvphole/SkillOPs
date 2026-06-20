"""Action rate metric. Mirrors src/metrics/calculateActionRate.ts."""
from __future__ import annotations

from typing import Sequence

from skillops import SkillRun


def calculate_action_rate(runs: Sequence[SkillRun]) -> float:
    """Fraction of runs in which the skill took an action."""
    if not runs:
        return 0.0
    return sum(1 for r in runs if r.action_taken) / len(runs)
