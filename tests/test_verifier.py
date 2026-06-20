from skillops import SkillChange, Thresholds
from skillops.metrics.calculate_metric_summary import calculate_metric_summary
from skillops.verification.verify_evidence import verify_evidence
from skillops.verification.verify_proposed_changes import verify_proposed_changes
from skillops.verification.verify_candidate import verify_candidate
from skillops.verification.verify_no_self_certification import verify_no_self_certification
from skillops.verification.approve_skill_update import approve_skill_update
from skillops.recommendations.constrain_recommendation import constrain_recommendation

from tests.conftest import make_run

T = Thresholds(0.8, 1000, 0.2, 0.25)


def test_verify_evidence_missing(tmp_path):
    good = tmp_path / "ok.json"
    good.write_text("[]\n")  # non-empty
    empty = tmp_path / "empty.json"
    empty.write_text("")
    res = verify_evidence([str(good), str(empty), str(tmp_path / "nope.json")])
    assert res["approved"] is False
    assert str(empty) in res["missing"]


def test_verify_proposed_changes_rules():
    ok = SkillChange("incident-triage", "v1", "v2", "new content", [], "reason")
    assert verify_proposed_changes(ok)["approved"] is True

    not_versioned = SkillChange("incident-triage", "v1", "2.0", "c", [], "r")
    assert verify_proposed_changes(not_versioned)["approved"] is False

    same = SkillChange("incident-triage", "v2", "v2", "c", [], "r")
    assert "new version required" in verify_proposed_changes(same)["errors"]

    secret = SkillChange("incident-triage", "v1", "v2", "API_KEY=sk-abcdef0123456789abcd", [], "r")
    assert verify_proposed_changes(secret)["approved"] is False


def test_verify_candidate_requires_preserve_and_improve():
    current = calculate_metric_summary(
        [make_run(predicted_positive=True, actual_positive=False) for _ in range(1)]
        + [make_run() for _ in range(9)], T)
    candidate = calculate_metric_summary([make_run() for _ in range(10)], T)
    res = verify_candidate(current, candidate, T, ["false_positive_rate"])
    assert res["approved"] is True
    assert "false_positive_rate" in res["improvements"]


def test_verify_candidate_rejects_no_improvement():
    current = calculate_metric_summary([make_run() for _ in range(10)], T)
    candidate = calculate_metric_summary([make_run() for _ in range(10)], T)
    res = verify_candidate(current, candidate, T, ["false_positive_rate"])
    assert res["approved"] is False


def test_verify_no_self_certification():
    summary = calculate_metric_summary([make_run() for _ in range(4)], T)
    assert verify_no_self_certification({"metric_summary": summary})["approved"] is True
    assert verify_no_self_certification({"author_verdict": "looks good"})["approved"] is False
    assert verify_no_self_certification({"metric_summary": summary, "self_certified": True})["approved"] is False


def test_constrain_recommendation_blocks_verdicts():
    bad = {"kind": "patch", "rationale": "this is complete", "evidence_paths": ["x"]}
    assert constrain_recommendation(bad)["valid"] is False
    good = {"kind": "candidate", "rationale": "lower fp", "evidence_paths": ["x"]}
    assert constrain_recommendation(good)["valid"] is True


def test_approve_skill_update_combines(tmp_path):
    ev = tmp_path / "e.json"
    ev.write_text("[1]\n")
    change = SkillChange("incident-triage", "v1", "v2", "content", [str(ev)], "reason")
    assert approve_skill_update(change)["approved"] is True
