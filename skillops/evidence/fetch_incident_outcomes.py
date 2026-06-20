"""Derive incident-outcome evidence from run history.

Outcomes describe, per run, whether the prediction matched ground truth. This is
the deterministic evidence the evaluator relies on -- not agent narration.
"""
from __future__ import annotations

from typing import Dict, List

from skillops import SkillRun


def fetch_incident_outcomes(runs: List[SkillRun]) -> List[Dict[str, object]]:
    outcomes: List[Dict[str, object]] = []
    for r in runs:
        outcomes.append({
            "run_id": r.id,
            "predicted_positive": r.predicted_positive,
            "actual_positive": r.actual_positive,
            "correct": r.success,
            "action_taken": r.action_taken,
            "false_positive": r.predicted_positive and not r.actual_positive,
            "false_negative": (not r.predicted_positive) and r.actual_positive,
        })
    return outcomes
