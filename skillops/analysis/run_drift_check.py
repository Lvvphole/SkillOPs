"""Preventive drift check: has a metric moved beyond an allowed delta?"""
from __future__ import annotations

from typing import Any, Dict

from skillops import MetricSummary


def run_drift_check(
    current: MetricSummary,
    baseline: Dict[str, float],
    *,
    max_delta: float = 0.1,
) -> Dict[str, Any]:
    """Compare current metrics to a baseline snapshot; flag drifted metrics."""
    drifted = {}
    for metric in ("success_rate", "false_positive_rate", "action_rate"):
        if metric not in baseline:
            continue
        delta = getattr(current, metric) - baseline[metric]
        if abs(delta) > max_delta:
            drifted[metric] = round(delta, 4)
    return {"drift_detected": bool(drifted), "drifted_metrics": drifted}
