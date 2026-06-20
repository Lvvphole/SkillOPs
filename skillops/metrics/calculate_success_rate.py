"""Success rate metric. Mirrors src/metrics/calculateSuccessRate.ts."""
from __future__ import annotations

from typing import Sequence

from skillops import SkillRun


def calculate_success_rate(runs: Sequence[SkillRun]) -> float:
    """Fraction of runs whose deterministic evaluation succeeded."""
    if not runs:
        return 0.0
    return sum(1 for r in runs if r.success) / len(runs)
