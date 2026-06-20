"""Threshold comparison. Mirrors src/analysis/compareToThresholds.ts.

This is the single source of truth for pass/fail. It consumes only computed
metrics and the declared thresholds -- never agent text.
"""
from __future__ import annotations

from typing import Dict, List

from skillops import MetricSummary


def compare_thresholds(summary: MetricSummary) -> Dict[str, object]:
    """Return {'passed': bool, 'failures': [...]} derived purely from metrics."""
    failures: List[str] = list(summary.failures)
    return {"passed": summary.passed and not failures, "failures": failures}
