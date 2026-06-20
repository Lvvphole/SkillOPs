"""Score performance and surface deterministic improvement targets.

Mirrors src/analysis/analyzePerformance.ts. Recommendations name failing metrics;
they are suggestions only and must pass verification before any update.
"""
from __future__ import annotations

from typing import Any, Dict, Sequence

from skillops import SkillRun, Thresholds
from skillops.metrics.calculate_metric_summary import calculate_metric_summary


def analyze_performance(
    runs: Sequence[SkillRun],
    thresholds: Thresholds,
    *,
    explicit_review: bool = False,
) -> Dict[str, Any]:
    summary = calculate_metric_summary(runs, thresholds)
    targets = list(summary.failures)
    if explicit_review and summary.passed:
        # An explicit review surfaces headroom even on a pass (maintenance mode).
        targets = ["maintenance_review"]
    return {"summary": summary, "improvement_targets": targets}
