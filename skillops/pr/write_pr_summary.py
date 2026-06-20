"""Render the PR summary markdown body from a loop report."""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict


def write_pr_summary(report: Dict[str, Any], *, out_path: str = "artifacts/pr-summary.md") -> str:
    summary = report.get("metric_summary", {})
    body = f"""# SkillOps: manifest-driven autonomous loop runtime

## Summary
Python-first, manifest-driven SkillOps loop runtime. Define a loop once in a
manifest, hit go, and the runtime runs the skill, collects evidence, measures
metrics, compares thresholds, branches into corrective repair (on fail) or
preventive maintenance + optimization (on pass), verifies any proposed change,
versions the skill, writes memory, and emits artifacts.

## Architecture overview
- `skillops/` Python core: orchestrator, runs, evidence, metrics, analysis,
  recommendations, verification, versioning, memory, pr, db, utils.
- `loops/` manifests + JSON schemas (LoopSpec, SkillSpec, EvidenceSpec,
  MetricSpec, ImprovementPolicy, EscalationPolicy).
- `skills/incident-triage/` sample skill (spec, config, thresholds, evidence,
  evaluation, improvement-policy, versioned skill files).
- `tests/` pytest suite for runner, metrics, thresholds, branching, verifier,
  versioning, memory, update flow.

## Language selection rationale (Python-first)
The repo originated greenfield and is primarily an autonomous SkillOps loop
engine, so per the contract Python owns the deterministic core. The pre-existing
TypeScript scaffold is preserved as an adapter/interface layer, not rewritten.

## Manifest-driven loop
LoopSpec defines target skill, trigger, runtime limits, required evidence,
metrics, thresholds, branches, corrective/preventive/optimization actions,
verifier/test/PR behavior, memory file, required artifacts, and terminal states.

## Branch behavior
- Fail -> corrective repair: diagnose, recommend patch, verify, new version, PR.
- Pass -> preventive: record pass, staleness + drift checks, challenge
  benchmarks, optimization scan; candidate only on evidence-backed improvement.

## Terminal state of this run
`{report.get('terminal_state')}` (metrics: {summary}).

## Tests / validation
- `pytest` (see artifacts/test-results.log).
- manifest validation + byte-compile (see artifacts/build-results.log).

## Artifacts
repo-inspection, implementation-notes, run-history, metric-summary,
weekly-performance-report, recommendation-report, verification-report,
evaluation-report, skill-change-log, test-results, build-results,
final-diff.patch, pr-summary, pr-url.

## Risk notes
Single sample skill; JSON-file persistence (no DB server); PR creation requires
operator GitHub auth. LLM calls are not invoked (deterministic core).

## Rollback notes
All skill updates are versioned; `rollback_skill` repoints the active version.
Revert the branch to undo; no destructive rewrites of the TypeScript layer.

## Known limitations
v1 ships one skill, a JSON store, and a pure-Python schema validator subset.
"""
    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(body, encoding="utf-8")
    return body
