"""Evidence collection and validation.

Evidence must exist before analysis. These functions gather run history and
incident outcomes, then validate that every evidence source required by the
skill's EvidenceSpec is present and non-empty.
"""
from skillops.evidence.fetch_run_history import fetch_run_history
from skillops.evidence.fetch_incident_outcomes import fetch_incident_outcomes
from skillops.evidence.collect_evidence import collect_evidence
from skillops.evidence.validate_evidence import validate_evidence

__all__ = [
    "fetch_run_history",
    "fetch_incident_outcomes",
    "collect_evidence",
    "validate_evidence",
]
