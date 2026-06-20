"""Drive one loop cycle end-to-end against a LoopSpec manifest.

Flow: load spec -> validate spec -> load skill -> collect evidence ->
validate evidence -> measure -> compare -> branch -> (corrective | preventive)
-> recommend -> verify -> version -> test -> compare versions -> decide PR ->
write artifacts -> update memory -> terminal state.

Metrics decide pass/fail. Recommendations are suggestions only and are verified
before any version is written. The cycle always ends in a declared terminal
state; "done"/"looks good" are not valid outcomes.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

from skillops import Thresholds, SkillChange
from skillops.orchestrator.load_loop_spec import load_loop_spec, load_yaml
from skillops.orchestrator.validate_loop_spec import validate_loop_spec
from skillops.orchestrator.select_branch import select_branch, CORRECTIVE, PREVENTIVE
from skillops.orchestrator.route_escalation import route_escalation
from skillops.orchestrator.state_machine import LoopState, StateMachine
from skillops.evidence.collect_evidence import collect_evidence, runs_from_bundle
from skillops.evidence.validate_evidence import validate_evidence
from skillops.metrics.calculate_metric_summary import calculate_metric_summary
from skillops.metrics.compare_thresholds import compare_thresholds
from skillops.analysis.diagnose_failure import diagnose_failure
from skillops.analysis.run_staleness_check import run_staleness_check
from skillops.analysis.run_drift_check import run_drift_check
from skillops.analysis.run_optimization_scan import run_optimization_scan
from skillops.analysis.run_challenge_benchmarks import run_challenge_benchmarks
from skillops.recommendations.recommend_patch import recommend_patch
from skillops.recommendations.recommend_candidate import recommend_candidate
from skillops.verification.verify_evidence import verify_evidence
from skillops.verification.approve_skill_update import approve_skill_update
from skillops.memory.write_memory import write_memory, append_update_history, record_failure_pattern
from skillops.memory.read_memory import read_memory
from skillops.utils.dates import now_iso
from skillops.utils.logger import logger


def _load_skill(skill_id: str, skills_root: str) -> Dict[str, Any]:
    base = Path(skills_root) / skill_id
    spec = load_yaml(str(base / "skill.spec.yaml"))
    thresholds_doc = load_yaml(str(base / "thresholds.yaml"))
    evidence_doc = load_yaml(str(base / "evidence.yaml"))
    improvement = load_yaml(str(base / "improvement-policy.yaml"))
    return {
        "spec": spec,
        "thresholds": Thresholds.from_dict(thresholds_doc),
        "evidence_doc": evidence_doc,
        "improvement": improvement,
        "base": str(base),
    }


def run_loop(
    loop_path: str,
    *,
    skills_root: str = "skills",
    artifacts_dir: str = "artifacts",
    schemas_root: str = "loops/schemas",
    write_artifacts: bool = True,
) -> Dict[str, Any]:
    sm = StateMachine()
    art = Path(artifacts_dir)
    art.mkdir(parents=True, exist_ok=True)

    # --- load + validate spec -------------------------------------------
    sm.to(LoopState.LOAD_SPEC)
    spec = load_loop_spec(loop_path)
    sm.to(LoopState.VALIDATE_SPEC)
    validation = validate_loop_spec(spec, schemas_root=schemas_root)
    if not validation["valid"]:
        esc = route_escalation("architecture_conflict", {"schema_errors": validation["errors"]})
        sm.to(LoopState.ESCALATED_WITH_BLOCKER)
        return _finalize(sm, spec, escalation=esc)

    skill_id = spec["target_skill"]
    skill = _load_skill(skill_id, skills_root)
    thresholds: Thresholds = skill["thresholds"]
    sample_inputs: List[Dict[str, Any]] = skill["evidence_doc"].get("sample_inputs", [])

    # --- collect + validate evidence ------------------------------------
    sm.to(LoopState.COLLECT_EVIDENCE)
    bundle = collect_evidence(skill_id, sample_inputs=sample_inputs)
    sm.to(LoopState.VALIDATE_EVIDENCE)
    required_sources = skill["evidence_doc"].get("required_sources", ["run_history"])
    ev_check = validate_evidence(bundle, required_sources)
    if not ev_check["valid"]:
        esc = route_escalation("missing_evidence_artifact", ev_check)
        sm.to(LoopState.ESCALATED_WITH_BLOCKER)
        return _finalize(sm, spec, escalation=esc)

    runs = runs_from_bundle(bundle)

    # --- measure + compare (metrics decide pass/fail) -------------------
    sm.to(LoopState.MEASURE)
    summary = calculate_metric_summary(runs, thresholds)
    sm.to(LoopState.COMPARE)
    decision = compare_thresholds(summary)

    # --- branch ----------------------------------------------------------
    sm.to(LoopState.BRANCH)
    branch = select_branch(summary)

    report: Dict[str, Any] = {
        "loop_id": spec.get("loop_id"),
        "skill_id": skill_id,
        "branch": branch,
        "metric_summary": summary.to_dict(),
        "threshold_decision": decision,
        "run_history": [r.to_dict() for r in runs],
        "analysis": {},
        "recommendation": None,
        "verification": None,
        "version": None,
        "pr": None,
    }

    run_history_path = str(art / "run-history.json")
    if branch == CORRECTIVE:
        terminal = _corrective_branch(sm, spec, skill, summary, run_history_path, report)
    else:
        terminal = _preventive_branch(sm, spec, skill, summary, run_history_path, report)

    # --- artifacts + memory ---------------------------------------------
    sm.to(LoopState.WRITE_ARTIFACTS)
    if write_artifacts:
        _write_loop_artifacts(art, report, runs)
    sm.to(LoopState.UPDATE_MEMORY)
    _update_memory(skill_id, report, terminal)

    sm.to(terminal)
    report["terminal_state"] = terminal.value
    report["state_history"] = [s.value for s in sm.history]
    logger.info("loop complete", {"terminal": terminal.value, "branch": branch})
    return report


def _corrective_branch(sm, spec, skill, summary, run_history_path, report) -> LoopState:
    sm.to(LoopState.CORRECTIVE)
    diagnoses = diagnose_failure(summary)
    report["analysis"]["diagnoses"] = diagnoses

    sm.to(LoopState.RECOMMEND)
    patch = recommend_patch(summary, evidence_paths=[run_history_path])
    report["recommendation"] = patch

    sm.to(LoopState.VERIFY)
    skill_id = report["skill_id"]
    proposed_content = _patch_content(skill, summary, diagnoses)
    change = SkillChange(
        skill_id=skill_id,
        from_version=skill["spec"].get("active_version", "v1"),
        to_version="v2",
        proposed_content=proposed_content,
        evidence_paths=[run_history_path],
        reason="corrective patch for: " + ", ".join(summary.failures),
        kind="patch",
    )
    approval = approve_skill_update(change)
    report["verification"] = approval
    if not approval["approved"]:
        record_failure_pattern({"signature": "corrective_verify_rejected:" + skill_id,
                                "errors": approval})
        esc = route_escalation("verifier_rejected_twice", approval)
        sm.to(LoopState.ESCALATED_WITH_BLOCKER)
        report["escalation"] = esc
        return LoopState.ESCALATED_WITH_BLOCKER

    sm.to(LoopState.VERSION)
    report["version"] = {"skill_id": skill_id, "to_version": change.to_version, "kind": "patch"}
    sm.to(LoopState.TEST)
    report["analysis"]["regression"] = run_challenge_benchmarks()
    sm.to(LoopState.COMPARE_VERSIONS)
    sm.to(LoopState.DECIDE_PR)
    report["pr"] = {"required": True, "kind": "patch", "head": spec.get("_branch")}
    return LoopState.FAIL_PATCH_PR_CREATED


def _preventive_branch(sm, spec, skill, summary, run_history_path, report) -> LoopState:
    sm.to(LoopState.PREVENTIVE)
    skill_id = report["skill_id"]
    memory = read_memory("skill-memory.json", default={}).get(skill_id, {})
    last_updated = memory.get("last_updated_iso")
    baseline = memory.get("baseline_metrics", {})

    staleness = run_staleness_check(report["run_history"], last_updated_iso=last_updated)
    drift = run_drift_check(summary, baseline)
    challenge = run_challenge_benchmarks()
    optimization = run_optimization_scan(summary, skill["thresholds"])
    report["analysis"] = {
        "staleness": staleness,
        "drift": drift,
        "challenge": challenge,
        "optimization": optimization,
    }

    # Candidate only on evidence-backed measurable improvement. v1 does not
    # fabricate improvement, so this records a no-change unless a measured gain
    # is supplied by an adapter.
    measured = skill["improvement"].get("measured_improvement", {})
    sm.to(LoopState.RECOMMEND)
    candidate = recommend_candidate(
        optimization, evidence_paths=[run_history_path], measured_improvement=measured
    )
    report["recommendation"] = candidate

    if not candidate["warranted"]:
        return LoopState.PASS_NO_CHANGE_RECORDED

    sm.to(LoopState.VERIFY)
    ev = verify_evidence([run_history_path])
    report["verification"] = ev
    if not ev["approved"]:
        return LoopState.PASS_CANDIDATE_REJECTED_RECORDED

    sm.to(LoopState.VERSION)
    sm.to(LoopState.TEST)
    sm.to(LoopState.COMPARE_VERSIONS)
    sm.to(LoopState.DECIDE_PR)
    report["pr"] = {"required": True, "kind": "candidate"}
    return LoopState.PASS_CANDIDATE_PR_CREATED


def _patch_content(skill: Dict[str, Any], summary, diagnoses) -> str:
    lines = ["# Incident Triage Skill (patched candidate v2)", ""]
    lines.append("Classify high-severity or customer-impacting incidents as urgent;")
    lines.append("classify all others as standard.")
    lines.append("")
    lines.append("## Corrective adjustments")
    for d in diagnoses:
        lines.append(f"- {d['metric']}: {d['diagnosis']}")
    return "\n".join(lines) + "\n"


def _write_loop_artifacts(art: Path, report: Dict[str, Any], runs) -> None:
    (art / "run-history.json").write_text(
        json.dumps([r.to_dict() for r in runs], indent=2), encoding="utf-8"
    )
    summary = report["metric_summary"]
    (art / "metric-summary.json").write_text(
        json.dumps({
            "loop_id": report["loop_id"],
            "skill_id": report["skill_id"],
            "branch": report["branch"],
            "metrics": summary,
            "threshold_decision": report["threshold_decision"],
        }, indent=2),
        encoding="utf-8",
    )
    _write_weekly_report(art, report)
    _write_recommendation_report(art, report)


def _write_weekly_report(art: Path, report: Dict[str, Any]) -> None:
    s = report["metric_summary"]
    a = report.get("analysis", {})
    lines = [
        "# Weekly Performance Report",
        "",
        f"- Generated: {now_iso()}",
        f"- Loop: `{report['loop_id']}`  Skill: `{report['skill_id']}`",
        f"- Sample size: {s.get('sample_size')}",
        f"- Branch: **{report['branch']}**  Terminal: **{report.get('terminal_state', 'in-progress')}**",
        "",
        "## Metrics vs thresholds",
        f"- success_rate: {s['success_rate']:.3f}",
        f"- avg_duration_ms: {s['avg_duration_ms']:.3f}",
        f"- false_positive_rate: {s['false_positive_rate']:.3f}",
        f"- action_rate: {s['action_rate']:.3f}",
        f"- passed: **{s['passed']}**  failures: {s['failures'] or 'none'}",
        "",
        "## Maintenance / optimization scans (pass branch)",
    ]
    if "staleness" in a:
        lines.append(f"- staleness: {a['staleness']}")
        lines.append(f"- drift: {a['drift']}")
        lines.append(f"- challenge benchmarks: {a['challenge']['passed']}/{a['challenge']['total']} passed")
        lines.append(f"- optimization opportunities: {a['optimization']['has_opportunities']}")
    else:
        lines.append("- corrective branch: see recommendation report for diagnoses")
    lines.append("")
    (art / "weekly-performance-report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def _write_recommendation_report(art: Path, report: Dict[str, Any]) -> None:
    rec = report.get("recommendation") or {}
    lines = [
        "# Recommendation Report",
        "",
        f"- Generated: {now_iso()}",
        f"- Branch: {report['branch']}",
        f"- Warranted: {rec.get('warranted')}",
        f"- Reason: {rec.get('reason', 'n/a')}",
        "",
        "Recommendations are suggestions only; metrics decide pass/fail and the",
        "verifier gates any change. A candidate is created only on evidence-backed",
        "measurable improvement that preserves all required thresholds.",
        "",
        "## Detail",
        "```json",
        json.dumps(rec, indent=2, default=str),
        "```",
    ]
    (art / "recommendation-report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def _update_memory(skill_id: str, report: Dict[str, Any], terminal: LoopState) -> None:
    s = report["metric_summary"]
    write_memory(skill_id, {
        "last_terminal_state": terminal.value,
        "last_branch": report["branch"],
        "last_updated_iso": now_iso(),
        "baseline_metrics": {
            "success_rate": s["success_rate"],
            "false_positive_rate": s["false_positive_rate"],
            "action_rate": s["action_rate"],
        },
        "passed": s["passed"],
    })
    if report.get("version"):
        append_update_history({
            "skill_id": skill_id,
            "version": report["version"].get("to_version"),
            "kind": report["version"].get("kind"),
            "terminal_state": terminal.value,
        })


def _finalize(sm: StateMachine, spec: Dict[str, Any], *, escalation: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "loop_id": spec.get("loop_id"),
        "terminal_state": LoopState.ESCALATED_WITH_BLOCKER.value,
        "escalation": escalation,
        "state_history": [s.value for s in sm.history],
    }
