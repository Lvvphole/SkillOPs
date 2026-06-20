"""Verify a proposed change is versioned, non-empty, and secret-free.

Mirrors src/verification/verifyProposedChanges.ts with added secret patterns.
"""
from __future__ import annotations

import re
from typing import Dict, List

from skillops import SkillChange

_VERSION_RE = re.compile(r"^v\d+$")
_SECRET_RES = [
    re.compile(r"API_KEY\s*="),
    re.compile(r"SECRET\s*="),
    re.compile(r"sk-[A-Za-z0-9]{16,}"),
    re.compile(r"ghp_[A-Za-z0-9]{20,}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
]


def verify_proposed_changes(change: SkillChange) -> Dict[str, object]:
    errors: List[str] = []
    if not _VERSION_RE.match(change.to_version):
        errors.append("to_version must be versioned (vN)")
    if change.to_version == change.from_version:
        errors.append("new version required")
    if not change.proposed_content.strip():
        errors.append("empty proposed content")
    for pattern in _SECRET_RES:
        if pattern.search(change.proposed_content):
            errors.append("possible secret in proposed content")
            break
    return {"approved": len(errors) == 0, "errors": errors}
