"""Preventive challenge benchmarks: run the skill against harder edge cases.

This stresses a passing skill with adversarial/ambiguous incidents to confirm it
is still robust. Results feed maintenance decisions; they never override the
metric-based pass/fail of the primary sample.
"""
from __future__ import annotations

from typing import Any, Dict, List

from skillops.runs.run_skill import classify_incident, evaluate_incident

_DEFAULT_CHALLENGES: List[Dict[str, Any]] = [
    {"id": "chal-1", "description": "low sev but customer impacting", "severity": "low", "customer_impact": True},
    {"id": "chal-2", "description": "high sev no customer impact", "severity": "high", "customer_impact": False},
    {"id": "chal-3", "description": "medium sev, no impact", "severity": "medium", "customer_impact": False},
    {"id": "chal-4", "description": "low sev, no impact", "severity": "low", "customer_impact": False},
]


def run_challenge_benchmarks(challenges: List[Dict[str, Any]] | None = None) -> Dict[str, Any]:
    challenges = challenges if challenges is not None else _DEFAULT_CHALLENGES
    results = []
    passed = 0
    for incident in challenges:
        classification = classify_incident(incident)
        evaluation = evaluate_incident(incident, classification["label"])
        if evaluation["success"]:
            passed += 1
        results.append({
            "id": incident["id"],
            "label": classification["label"],
            "correct": evaluation["success"],
        })
    total = len(challenges)
    return {
        "total": total,
        "passed": passed,
        "pass_rate": round(passed / total, 4) if total else 0.0,
        "all_passed": passed == total,
        "results": results,
    }
