"""End-to-end update flow: recommend -> constrain -> verify -> version.

Covers both the corrective (fail) path producing a verified patch version and
the optimization (pass) path gating a candidate on measurable improvement.
"""
from skillops import SkillChange, Thresholds
from skillops.metrics.calculate_metric_summary import calculate_metric_summary
from skillops.analysis.run_optimization_scan import run_optimization_scan
from skillops.recommendations.recommend_patch import recommend_patch
from skillops.recommendations.recommend_candidate import recommend_candidate
from skillops.verification.approve_skill_update import approve_skill_update
from skillops.verification.verify_candidate import verify_candidate
from skillops.versioning.create_skill_version import create_skill_version

from tests.conftest import make_run

T = Thresholds(0.8, 1000, 0.2, 0.25)


def test_corrective_update_flow_versions_new_skill(tmp_path):
    # Failing sample -> patch recommendation -> approved update -> new version.
    runs = [make_run(success=False) for _ in range(4)]
    summary = calculate_metric_summary(runs, T)
    assert summary.passed is False

    evidence = tmp_path / "run-history.json"
    evidence.write_text("[{}]\n")
    patch = recommend_patch(summary, evidence_paths=[str(evidence)])
    assert patch["warranted"] is True
    assert patch["constrained_valid"] is True

    # seed v1 then create the verified patch as v2
    (tmp_path / "incident-triage" / "versions").mkdir(parents=True)
    (tmp_path / "incident-triage" / "versions" / "v1.skill.md").write_text("# v1\n")
    change = SkillChange("incident-triage", "v1", "v2", "# v2 patched\n", [str(evidence)], "corrective")
    assert approve_skill_update(change)["approved"] is True
    res = create_skill_version("incident-triage", "# v2 patched\n", reason="corrective",
                               skills_root=str(tmp_path), changelog_path=str(tmp_path / "c.md"))
    assert res["version"] == "v2"


def test_passing_skill_no_candidate_without_measured_improvement():
    summary = calculate_metric_summary([make_run() for _ in range(6)], T)
    scan = run_optimization_scan(summary, T)
    rec = recommend_candidate(scan, evidence_paths=["artifacts/run-history.json"], measured_improvement={})
    assert rec["warranted"] is False
    assert "no-change" in rec["reason"]


def test_passing_skill_candidate_requires_threshold_preservation():
    current = calculate_metric_summary(
        [make_run(predicted_positive=True, actual_positive=False)] + [make_run() for _ in range(9)], T)
    # candidate improves false positives to zero while preserving thresholds
    candidate = calculate_metric_summary([make_run() for _ in range(10)], T)
    verdict = verify_candidate(current, candidate, T, ["false_positive_rate"])
    assert verdict["approved"] is True
    assert verdict["preserves_thresholds"] is True
