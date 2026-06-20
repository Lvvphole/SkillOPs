"""Reject self-certification: the executor/LLM may not declare its own pass.

A pass/fail decision is only valid when it carries a metric_summary whose
`passed` flag was computed from metrics. If a record claims completion from text
(no metric evidence, or a verdict asserted by the author), it is rejected.
"""
from __future__ import annotations

from typing import Any, Dict

from skillops import MetricSummary

_BANNED_PHRASES = ("looks good", "probably fixed", "done", "complete", "trust me")


def verify_no_self_certification(record: Dict[str, Any]) -> Dict[str, Any]:
    errors = []

    summary = record.get("metric_summary")
    if not isinstance(summary, (MetricSummary, dict)):
        errors.append("pass/fail must be backed by a metric_summary")
    else:
        passed = summary.passed if isinstance(summary, MetricSummary) else summary.get("passed")
        if passed is None:
            errors.append("metric_summary missing computed pass/fail")

    if record.get("self_certified"):
        errors.append("executor cannot self-certify completion")

    asserted = str(record.get("author_verdict", "")).lower()
    for phrase in _BANNED_PHRASES:
        if phrase in asserted:
            errors.append(f"author verdict is not evidence: '{phrase}'")
            break

    return {"approved": len(errors) == 0, "errors": errors}
