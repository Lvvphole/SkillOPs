"""Preventive optimization scan: find headroom to optimize on a passing skill.

Headroom is purely informational -- it names metrics that *could* improve. A
candidate is only created later if measurable improvement evidence exists.
"""
from __future__ import annotations

from typing import Any, Dict, List

from skillops import MetricSummary, Thresholds


def run_optimization_scan(summary: MetricSummary, thresholds: Thresholds) -> Dict[str, Any]:
    opportunities: List[Dict[str, Any]] = []

    # Duration headroom: how far below the ceiling are we (room to add capability)?
    if summary.avg_duration_ms < thresholds.max_avg_duration_ms:
        opportunities.append({
            "metric": "avg_duration_ms",
            "headroom": round(thresholds.max_avg_duration_ms - summary.avg_duration_ms, 3),
            "direction": "lower_is_better",
        })
    # False-positive headroom.
    if summary.false_positive_rate < thresholds.max_false_positive_rate:
        opportunities.append({
            "metric": "false_positive_rate",
            "headroom": round(thresholds.max_false_positive_rate - summary.false_positive_rate, 4),
            "direction": "lower_is_better",
        })
    # Success-rate headroom toward 1.0.
    if summary.success_rate < 1.0:
        opportunities.append({
            "metric": "success_rate",
            "headroom": round(1.0 - summary.success_rate, 4),
            "direction": "higher_is_better",
        })

    return {"has_opportunities": bool(opportunities), "opportunities": opportunities}
