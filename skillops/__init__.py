"""SkillOps: a Python-first, manifest-driven autonomous loop runtime for AI skills.

This package owns the deterministic core: loop runtime, CLI, manifest loading,
schema validation, evidence collection, metrics, threshold comparison, branching,
verification, versioning, memory, artifact generation, PR automation, and tests.

The loop pattern is:
    Run -> Measure -> Compare
        -> if fail:  Repair (corrective)
        -> if pass:  Maintain, Challenge, Optimize (preventive)
    -> Recommend -> Verify -> Test -> Version -> Remember -> Repeat.

Metrics decide pass/fail. LLM output never decides pass/fail; it may only
suggest patches or candidates, which must be verified before use.
"""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import List

__version__ = "1.0.0"


@dataclass
class SkillRun:
    """A single execution record of a skill."""

    id: str
    skill_id: str
    started_at: str
    ended_at: str
    duration_ms: int
    success: bool
    predicted_positive: bool
    actual_positive: bool
    action_taken: bool
    notes: str = ""

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "SkillRun":
        return cls(
            id=d["id"],
            skill_id=d["skill_id"],
            started_at=d["started_at"],
            ended_at=d["ended_at"],
            duration_ms=int(d["duration_ms"]),
            success=bool(d["success"]),
            predicted_positive=bool(d["predicted_positive"]),
            actual_positive=bool(d["actual_positive"]),
            action_taken=bool(d["action_taken"]),
            notes=d.get("notes", ""),
        )


@dataclass
class Thresholds:
    """Deterministic pass/fail bounds for a skill."""

    min_success_rate: float
    max_avg_duration_ms: float
    max_false_positive_rate: float
    min_action_rate: float

    @classmethod
    def from_dict(cls, d: dict) -> "Thresholds":
        return cls(
            min_success_rate=float(d["min_success_rate"]),
            max_avg_duration_ms=float(d["max_avg_duration_ms"]),
            max_false_positive_rate=float(d["max_false_positive_rate"]),
            min_action_rate=float(d["min_action_rate"]),
        )


@dataclass
class MetricSummary:
    """Computed metrics plus the deterministic pass/fail decision."""

    success_rate: float
    avg_duration_ms: float
    false_positive_rate: float
    action_rate: float
    passed: bool
    failures: List[str] = field(default_factory=list)
    sample_size: int = 0

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class SkillChange:
    """A proposed change to a skill (patch or candidate)."""

    skill_id: str
    from_version: str
    to_version: str
    proposed_content: str
    evidence_paths: List[str] = field(default_factory=list)
    reason: str = ""
    kind: str = "patch"  # "patch" (corrective) or "candidate" (optimization)

    def to_dict(self) -> dict:
        return asdict(self)


__all__ = [
    "SkillRun",
    "Thresholds",
    "MetricSummary",
    "SkillChange",
    "__version__",
]
