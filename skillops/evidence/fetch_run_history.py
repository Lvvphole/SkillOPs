"""Fetch run-history evidence for a skill."""
from __future__ import annotations

from typing import List

from skillops import SkillRun
from skillops.runs.get_run_history import get_run_history


def fetch_run_history(skill_id: str) -> List[SkillRun]:
    """Return all recorded runs for the skill (the primary evidence source)."""
    return get_run_history(skill_id)
