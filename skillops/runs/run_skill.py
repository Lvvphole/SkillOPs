"""Execute a skill against one input and log the result.

The deterministic incident-triage logic is implemented here in the Python core
(mirroring the TS classifier/evaluator/verifier). Skills are registered in
_SKILLS so additional skills can be added without changing the runner.
"""
from __future__ import annotations

import time
from typing import Any, Callable, Dict, Tuple

from skillops import SkillRun
from skillops.runs.log_run_result import log_run_result
from skillops.utils.dates import now_iso

_VALID_SEVERITIES = ("low", "medium", "high")


def verify_incident_input(incident: Dict[str, Any]) -> bool:
    """Input guard mirroring src/skills/incident-triage/verifier.ts."""
    return (
        isinstance(incident, dict)
        and isinstance(incident.get("id"), str)
        and isinstance(incident.get("description"), str)
        and incident.get("severity") in _VALID_SEVERITIES
        and isinstance(incident.get("customer_impact"), bool)
    )


def classify_incident(incident: Dict[str, Any]) -> Dict[str, Any]:
    """Classify an incident as urgent or standard (deterministic policy)."""
    urgent = incident["severity"] == "high" or incident["customer_impact"]
    return {"label": "urgent" if urgent else "standard", "predicted_positive": urgent}


def evaluate_incident(incident: Dict[str, Any], label: str) -> Dict[str, Any]:
    """Deterministic evaluator: ground truth is severity high or customer impact."""
    actual_positive = incident["severity"] == "high" or incident["customer_impact"]
    success = (actual_positive and label == "urgent") or (
        not actual_positive and label == "standard"
    )
    return {
        "success": success,
        "actual_positive": actual_positive,
        "action_taken": label == "urgent",
    }


def _run_incident_triage(incident: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    if not verify_incident_input(incident):
        raise ValueError("Invalid incident input")
    classification = classify_incident(incident)
    evaluation = evaluate_incident(incident, classification["label"])
    return classification, evaluation


_SKILLS: Dict[str, Callable[[Dict[str, Any]], Tuple[Dict[str, Any], Dict[str, Any]]]] = {
    "incident-triage": _run_incident_triage,
}


def run_skill(skill_id: str, input_payload: Dict[str, Any], *, duration_ms: int | None = None) -> SkillRun:
    """Run a registered skill and log the resulting SkillRun.

    `duration_ms` may be supplied for deterministic tests/artifacts; otherwise it
    is measured from a monotonic clock (floored at 1ms).
    """
    handler = _SKILLS.get(skill_id)
    if handler is None:
        raise ValueError(f"Unknown skill: {skill_id}")

    started = now_iso()
    start = time.monotonic()
    classification, evaluation = handler(input_payload)
    measured = duration_ms if duration_ms is not None else max(1, round((time.monotonic() - start) * 1000))
    ended = now_iso()

    run = SkillRun(
        id=f"{skill_id}-{input_payload['id']}-{round(start * 1000)}",
        skill_id=skill_id,
        started_at=started,
        ended_at=ended,
        duration_ms=measured,
        success=evaluation["success"],
        predicted_positive=classification["predicted_positive"],
        actual_positive=evaluation["actual_positive"],
        action_taken=evaluation["action_taken"],
        notes=classification["label"],
    )
    return log_run_result(run)
