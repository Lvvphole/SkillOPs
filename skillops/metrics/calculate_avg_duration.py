"""Average duration metric. Mirrors src/metrics/calculateAvgDuration.ts."""
from __future__ import annotations

from typing import Sequence

from skillops import SkillRun
from skillops.utils.average import average


def calculate_avg_duration(runs: Sequence[SkillRun]) -> float:
    """Mean run duration in milliseconds (0.0 for an empty sample)."""
    return average([r.duration_ms for r in runs])
