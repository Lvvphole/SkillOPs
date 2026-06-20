"""Preventive staleness check: has the skill gone too long without review?"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from skillops import SkillRun
from skillops.utils.dates import days_between, now_iso


def run_staleness_check(
    runs: List[SkillRun],
    *,
    last_updated_iso: Optional[str],
    max_age_days: float = 30.0,
    now: Optional[str] = None,
) -> Dict[str, Any]:
    now = now or now_iso()
    if last_updated_iso is None:
        return {"stale": True, "age_days": None, "reason": "no recorded update"}
    age = days_between(last_updated_iso, now)
    return {
        "stale": age > max_age_days,
        "age_days": round(age, 3),
        "reason": f"last update {round(age, 1)}d ago (max {max_age_days}d)",
    }
