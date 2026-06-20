import pytest

from skillops import Thresholds
from skillops.metrics.calculate_metric_summary import calculate_metric_summary
from skillops.orchestrator.select_branch import select_branch, CORRECTIVE, PREVENTIVE
from skillops.orchestrator.route_escalation import route_escalation
from skillops.orchestrator.state_machine import LoopState, StateMachine, TERMINAL_STATES, InvalidTransition
from skillops.orchestrator.run_loop import run_loop

from tests.conftest import make_run

T = Thresholds(0.8, 1000, 0.2, 0.25)


def test_select_branch_pass_is_preventive():
    summary = calculate_metric_summary([make_run() for _ in range(4)], T)
    assert select_branch(summary) == PREVENTIVE


def test_select_branch_fail_is_corrective():
    summary = calculate_metric_summary([make_run(success=False) for _ in range(4)], T)
    assert select_branch(summary) == CORRECTIVE


def test_state_machine_happy_path():
    sm = StateMachine()
    for state in [
        LoopState.LOAD_SPEC, LoopState.VALIDATE_SPEC, LoopState.COLLECT_EVIDENCE,
        LoopState.VALIDATE_EVIDENCE, LoopState.MEASURE, LoopState.COMPARE,
        LoopState.BRANCH, LoopState.PREVENTIVE, LoopState.WRITE_ARTIFACTS,
        LoopState.UPDATE_MEMORY, LoopState.PASS_NO_CHANGE_RECORDED,
    ]:
        sm.to(state)
    assert sm.is_terminal()


def test_illegal_transition_rejected():
    sm = StateMachine()
    with pytest.raises(InvalidTransition):
        sm.to(LoopState.PASS_CANDIDATE_PR_CREATED)


def test_escalation_allowed_from_any_state():
    sm = StateMachine()
    sm.to(LoopState.LOAD_SPEC)
    sm.to(LoopState.ESCALATED_WITH_BLOCKER)
    assert sm.state in TERMINAL_STATES


def test_route_escalation_record():
    esc = route_escalation("tests_failed_twice", {"x": 1})
    assert esc["terminal_state"] == "ESCALATED_WITH_BLOCKER"
    assert esc["known_reason"] is True


def test_run_loop_pass_no_change_integration(tmp_path):
    report = run_loop(
        "loops/weekly-skill-review.yaml",
        artifacts_dir=str(tmp_path / "artifacts"),
        schemas_root="loops/schemas",
    )
    assert report["terminal_state"] == "PASS_NO_CHANGE_RECORDED"
    assert report["branch"] == PREVENTIVE
    assert report["metric_summary"]["passed"] is True
    # pass branch still runs maintenance/optimization scans
    assert "optimization" in report["analysis"]
    assert "staleness" in report["analysis"]
