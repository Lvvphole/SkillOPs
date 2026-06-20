"""Validate that required evidence exists before analysis is permitted."""
from __future__ import annotations

from typing import Any, Dict, List


def validate_evidence(bundle: Dict[str, Any], required_sources: List[str]) -> Dict[str, Any]:
    """Confirm every required evidence source is present and non-empty.

    Returns {'valid': bool, 'missing': [...], 'sample_size': int}. Analysis must
    not proceed when valid is False -- this enforces "evidence before analysis".
    """
    present = set(bundle.get("sources", []))
    missing = [s for s in required_sources if s not in present]
    sample_size = int(bundle.get("sample_size", 0))
    if sample_size <= 0:
        if "run_history" not in missing:
            missing.append("run_history")
    return {
        "valid": len(missing) == 0 and sample_size > 0,
        "missing": missing,
        "sample_size": sample_size,
    }
