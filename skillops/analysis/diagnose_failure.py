"""Map failing metrics to deterministic diagnoses for the corrective branch."""
from __future__ import annotations

from typing import Dict, List

from skillops import MetricSummary

_DIAGNOSES = {
    "success_rate": "Classifier mislabels incidents; review decision boundary and add cases.",
    "avg_duration_ms": "Skill is too slow; reduce work per run or cache lookups.",
    "false_positive_rate": "Over-escalation; tighten the urgent criteria to cut false positives.",
    "action_rate": "Under-action; the skill rarely acts when it should escalate.",
}


def diagnose_failure(summary: MetricSummary) -> List[Dict[str, str]]:
    """Return a diagnosis per failing metric. Empty when the summary passed."""
    diagnoses: List[Dict[str, str]] = []
    for metric in summary.failures:
        diagnoses.append({
            "metric": metric,
            "diagnosis": _DIAGNOSES.get(metric, f"Investigate {metric} regression."),
        })
    return diagnoses
