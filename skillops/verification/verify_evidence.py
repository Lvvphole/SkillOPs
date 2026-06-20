"""Verify evidence files exist and are non-empty. Mirrors verifyEvidence.ts."""
from __future__ import annotations

from pathlib import Path
from typing import Dict, List


def verify_evidence(paths: List[str]) -> Dict[str, object]:
    """Approve only when every path exists and is non-empty."""
    missing: List[str] = []
    for p in paths:
        path = Path(p)
        if not path.exists() or path.stat().st_size == 0:
            missing.append(p)
    return {"approved": len(missing) == 0, "missing": missing}
