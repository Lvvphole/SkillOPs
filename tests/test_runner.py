import pytest

from skillops.runs.run_skill import (
    run_skill,
    classify_incident,
    evaluate_incident,
    verify_incident_input,
)
from skillops.runs.get_run_history import get_run_history


URGENT = {"id": "a", "description": "db outage", "severity": "high", "customer_impact": True}
STANDARD = {"id": "b", "description": "typo", "severity": "low", "customer_impact": False}


def test_classify_urgent_and_standard():
    assert classify_incident(URGENT) == {"label": "urgent", "predicted_positive": True}
    assert classify_incident(STANDARD) == {"label": "standard", "predicted_positive": False}


def test_evaluate_matches_ground_truth():
    assert evaluate_incident(URGENT, "urgent")["success"] is True
    assert evaluate_incident(STANDARD, "standard")["success"] is True
    assert evaluate_incident(URGENT, "standard")["success"] is False


def test_verify_input_guard():
    assert verify_incident_input(URGENT) is True
    assert verify_incident_input({"id": "x"}) is False
    assert verify_incident_input({"id": "x", "description": "d", "severity": "bad", "customer_impact": True}) is False


def test_run_skill_logs_run_and_sets_action():
    run = run_skill("incident-triage", URGENT, duration_ms=3)
    assert run.success is True
    assert run.action_taken is True
    assert run.duration_ms == 3
    history = get_run_history("incident-triage")
    assert len(history) == 1
    assert history[0].id == run.id


def test_run_skill_standard_no_action():
    run = run_skill("incident-triage", STANDARD, duration_ms=2)
    assert run.action_taken is False
    assert run.success is True


def test_unknown_skill_and_bad_input_raise():
    with pytest.raises(ValueError):
        run_skill("nope", URGENT)
    with pytest.raises(ValueError):
        run_skill("incident-triage", {"id": "x"})
