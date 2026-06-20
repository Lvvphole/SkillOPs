"""Verification: the Verifier authority.

The Verifier rejects unsupported recommendations, missing evidence, unsafe
updates, self-certification, and undocumented path substitutions. It consumes
files, logs, metrics, and diffs -- never agent explanations.
"""
from skillops.verification.verify_evidence import verify_evidence
from skillops.verification.verify_proposed_changes import verify_proposed_changes
from skillops.verification.verify_candidate import verify_candidate
from skillops.verification.verify_no_self_certification import verify_no_self_certification
from skillops.verification.approve_skill_update import approve_skill_update

__all__ = [
    "verify_evidence",
    "verify_proposed_changes",
    "verify_candidate",
    "verify_no_self_certification",
    "approve_skill_update",
]
