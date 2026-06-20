"""Aggregate metric summary + deterministic pass/fail.

Mirrors src/metrics/scoreSkillPerformance.ts. The `failures` list names every
threshold that was violated; `passed` is True only when that list is empty.
"""
from __future__ import annotations

from typing import Sequence

from skillops import SkillRun, Thresholds, MetricSummary
from skillops.metrics.calculate_success_rate import calculate_success_rate
from skillops.metrics.calculate_avg_duration import calculate_avg_duration
from skillops.metrics.calculate_false_positive_rate import calculate_false_positive_rate
from skillops.metrics.calculate_action_rate import calculate_action_rate


def calculate_metric_summary(runs: Sequence[SkillRun], thresholds: Thresholds) -> MetricSummary:
    success_rate = calculate_success_rate(runs)
    avg_duration_ms = calculate_avg_duration(runs)
    false_positive_rate = calculate_false_positive_rate(runs)
    action_rate = calculate_action_rate(runs)

    failures = []
    if success_rate < thresholds.min_success_rate:
        failures.append("success_rate")
    if avg_duration_ms > thresholds.max_avg_duration_ms:
        failures.append("avg_duration_ms")
    if false_positive_rate > thresholds.max_false_positive_rate:
        failures.append("false_positive_rate")
    if action_rate < thresholds.min_action_rate:
        failures.append("action_rate")

    return MetricSummary(
        success_rate=success_rate,
        avg_duration_ms=avg_duration_ms,
        false_positive_rate=false_positive_rate,
        action_rate=action_rate,
        passed=len(failures) == 0,
        failures=failures,
        sample_size=len(runs),
    )
