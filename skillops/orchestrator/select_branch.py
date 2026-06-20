"""Select the loop branch from the metric decision (deterministic).

Fail -> corrective. Pass -> preventive (maintenance + optimization). The branch
is chosen only from the metric summary's pass/fail; agent text has no influence.
"""
from __future__ import annotations

from skillops import MetricSummary

CORRECTIVE = "corrective"
PREVENTIVE = "preventive"


def select_branch(summary: MetricSummary) -> str:
    return PREVENTIVE if summary.passed else CORRECTIVE
