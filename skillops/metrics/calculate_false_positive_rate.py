"""False positive rate. Mirrors src/metrics/calculateFalsePositiveRate.ts."""
from __future__ import annotations

from typing import Sequence

from skillops import SkillRun


def calculate_false_positive_rate(runs: Sequence[SkillRun]) -> float:
    """Among predicted-positive runs, the fraction that were not actually positive."""
    predicted = [r for r in runs if r.predicted_positive]
    if not predicted:
        return 0.0
    return sum(1 for r in predicted if not r.actual_positive) / len(predicted)
