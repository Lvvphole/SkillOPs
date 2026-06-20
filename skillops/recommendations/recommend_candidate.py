"""Recommend an optimization candidate for a passing skill (suggestion only).

A candidate is recommended only when the optimization scan found headroom AND
that headroom is backed by measurable evidence. Without evidence-backed
improvement, no candidate is recommended and the loop records a no-change.
"""
from __future__ import annotations

from typing import Any, Dict, List

from skillops.recommendations.constrain_recommendation import constrain_recommendation


def recommend_candidate(
    optimization_scan: Dict[str, Any],
    *,
    evidence_paths: List[str],
    measured_improvement: Dict[str, float] | None = None,
) -> Dict[str, Any]:
    measured_improvement = measured_improvement or {}
    has_evidence_backed_gain = any(v > 0 for v in measured_improvement.values())

    if not optimization_scan.get("has_opportunities") or not has_evidence_backed_gain:
        return {
            "recommendation": None,
            "warranted": False,
            "constrained_valid": True,
            "constraint_errors": [],
            "reason": "no evidence-backed improvement; record no-change",
        }

    targets = [o["metric"] for o in optimization_scan.get("opportunities", [])]
    recommendation = {
        "kind": "candidate",
        "targets": targets,
        "rationale": "Optimization headroom with measured improvement: "
                     + ", ".join(f"{k}+{v}" for k, v in measured_improvement.items()),
        "evidence_paths": evidence_paths,
        "measured_improvement": measured_improvement,
        "decides_pass_fail": False,
    }
    constrained = constrain_recommendation(recommendation)
    return {
        "recommendation": recommendation,
        "warranted": True,
        "constrained_valid": constrained["valid"],
        "constraint_errors": constrained["errors"],
        "reason": "evidence-backed candidate",
    }
