"""Collect the full evidence bundle required by a skill's EvidenceSpec.

If no run history exists yet, the collector executes the skill against the
sample incidents declared in the skill config so that evidence exists before any
analysis runs. Returns a structured bundle plus the sources actually produced.
"""
from __future__ import annotations

from typing import Any, Dict, List

from skillops import SkillRun
from skillops.evidence.fetch_run_history import fetch_run_history
from skillops.evidence.fetch_incident_outcomes import fetch_incident_outcomes
from skillops.runs.run_skill import run_skill


def collect_evidence(
    skill_id: str,
    *,
    sample_inputs: List[Dict[str, Any]] | None = None,
    seed_if_empty: bool = True,
) -> Dict[str, Any]:
    runs = fetch_run_history(skill_id)

    if not runs and seed_if_empty and sample_inputs:
        for incident in sample_inputs:
            run_skill(skill_id, incident, duration_ms=incident.get("_duration_ms", 5))
        runs = fetch_run_history(skill_id)

    outcomes = fetch_incident_outcomes(runs)
    sources = []
    if runs:
        sources.append("run_history")
    if outcomes:
        sources.append("incident_outcomes")

    return {
        "skill_id": skill_id,
        "runs": runs,
        "outcomes": outcomes,
        "sources": sources,
        "sample_size": len(runs),
    }


def runs_from_bundle(bundle: Dict[str, Any]) -> List[SkillRun]:
    return list(bundle.get("runs", []))
