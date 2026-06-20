"""Route a blocker to an escalation record (terminal: ESCALATED_WITH_BLOCKER)."""
from __future__ import annotations

from typing import Any, Dict

from skillops.utils.dates import now_iso

_KNOWN_REASONS = {
    "path_missing", "not_git_repo", "remote_mismatch", "default_branch_unknown",
    "uncommitted_user_changes", "new_path_needed", "language_ambiguous",
    "package_manager_unknown", "install_failed_twice", "build_failed_twice",
    "tests_failed_twice", "push_failed_twice", "pr_failed_twice",
    "architecture_conflict", "missing_evidence_artifact", "unsafe_update",
    "verifier_rejected_twice",
}


def route_escalation(reason: str, context: Dict[str, Any] | None = None) -> Dict[str, Any]:
    return {
        "terminal_state": "ESCALATED_WITH_BLOCKER",
        "reason": reason,
        "known_reason": reason in _KNOWN_REASONS,
        "context": context or {},
        "raised_at": now_iso(),
        "next_action": "human approval / input required",
    }
