"""Verify an optimization candidate before it may open a PR.

A candidate is approved only when it (1) preserves EVERY required threshold and
(2) improves at least one approved optimization metric. This is the gate behind
success criterion 24.
"""
from __future__ import annotations

from typing import Any, Dict, List

from skillops import MetricSummary, Thresholds
from skillops.metrics.compare_thresholds import compare_thresholds


def _improves(metric: str, current: float, candidate: float) -> bool:
    # success_rate / action_rate: higher is better; durations / fp: lower is better.
    if metric in ("success_rate", "action_rate"):
        return candidate > current
    return candidate < current


def verify_candidate(
    current: MetricSummary,
    candidate: MetricSummary,
    thresholds: Thresholds,
    approved_optimization_metrics: List[str],
) -> Dict[str, Any]:
    candidate_check = compare_thresholds(candidate)
    preserves_thresholds = bool(candidate_check["passed"])

    improvements: Dict[str, Dict[str, float]] = {}
    for metric in approved_optimization_metrics:
        cur = getattr(current, metric, None)
        cand = getattr(candidate, metric, None)
        if cur is None or cand is None:
            continue
        if _improves(metric, cur, cand):
            improvements[metric] = {"from": cur, "to": cand}

    errors: List[str] = []
    if not preserves_thresholds:
        errors.append(f"candidate violates thresholds: {candidate_check['failures']}")
    if not improvements:
        errors.append("candidate improves no approved optimization metric")

    return {
        "approved": len(errors) == 0,
        "errors": errors,
        "preserves_thresholds": preserves_thresholds,
        "improvements": improvements,
    }
