"""Constrain a recommendation so it can never decide pass/fail.

A valid recommendation has kind in {patch, candidate}, names a target metric or
failure, carries evidence paths, and contains no pass/fail verdict. Any
recommendation that tries to assert completion or a verdict is rejected.
"""
from __future__ import annotations

from typing import Any, Dict

_FORBIDDEN_VERDICTS = (
    "passed", "failed", "pass/fail", "this is complete", "looks good",
    "done", "approved", "certify", "self-certif",
)
_ALLOWED_KINDS = ("patch", "candidate")


def constrain_recommendation(recommendation: Dict[str, Any]) -> Dict[str, Any]:
    errors = []
    kind = recommendation.get("kind")
    if kind not in _ALLOWED_KINDS:
        errors.append(f"kind must be one of {_ALLOWED_KINDS}")
    if not recommendation.get("rationale"):
        errors.append("rationale required")
    if not recommendation.get("evidence_paths"):
        errors.append("evidence_paths required")
    if recommendation.get("decides_pass_fail"):
        errors.append("recommendation may not decide pass/fail")

    blob = " ".join(
        str(recommendation.get(k, "")) for k in ("rationale", "summary", "verdict")
    ).lower()
    for verdict in _FORBIDDEN_VERDICTS:
        if verdict in blob:
            errors.append(f"recommendation contains forbidden verdict language: '{verdict}'")
            break

    return {"valid": len(errors) == 0, "errors": errors, "recommendation": recommendation}
