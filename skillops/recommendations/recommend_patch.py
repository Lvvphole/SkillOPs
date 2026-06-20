"""Recommend a corrective patch for failing metrics (suggestion only)."""
from __future__ import annotations

from typing import Any, Dict, List

from skillops import MetricSummary
from skillops.analysis.diagnose_failure import diagnose_failure
from skillops.recommendations.constrain_recommendation import constrain_recommendation


def recommend_patch(
    summary: MetricSummary,
    *,
    evidence_paths: List[str],
) -> Dict[str, Any]:
    """Produce a constrained patch recommendation targeting the failing metrics."""
    diagnoses = diagnose_failure(summary)
    targets = [d["metric"] for d in diagnoses]
    rationale = "; ".join(f"{d['metric']}: {d['diagnosis']}" for d in diagnoses) or \
        "No failing metric; patch not warranted."
    recommendation = {
        "kind": "patch",
        "targets": targets,
        "rationale": rationale,
        "evidence_paths": evidence_paths,
        "decides_pass_fail": False,
    }
    constrained = constrain_recommendation(recommendation)
    return {
        "recommendation": recommendation,
        "constrained_valid": constrained["valid"],
        "constraint_errors": constrained["errors"],
        "warranted": bool(targets),
    }
