"""Combine evidence + change checks into one approval. Mirrors approveSkillUpdate.ts."""
from __future__ import annotations

from typing import Any, Dict

from skillops import SkillChange
from skillops.verification.verify_evidence import verify_evidence
from skillops.verification.verify_proposed_changes import verify_proposed_changes


def approve_skill_update(change: SkillChange) -> Dict[str, Any]:
    evidence = verify_evidence(change.evidence_paths)
    changes = verify_proposed_changes(change)
    return {
        "approved": bool(evidence["approved"]) and bool(changes["approved"]),
        "evidence": evidence,
        "changes": changes,
    }
