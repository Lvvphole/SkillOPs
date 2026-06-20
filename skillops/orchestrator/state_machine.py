"""Deterministic loop state machine.

The state machine enforces a bounded, predefined flow so the runtime can never
drift into open-ended agent behavior. Transitions are whitelisted; any state may
move to ESCALATED_WITH_BLOCKER, and terminal states have no outgoing edges.
"""
from __future__ import annotations

from enum import Enum
from typing import Dict, List, Set


class LoopState(str, Enum):
    INIT = "INIT"
    LOAD_SPEC = "LOAD_SPEC"
    VALIDATE_SPEC = "VALIDATE_SPEC"
    COLLECT_EVIDENCE = "COLLECT_EVIDENCE"
    VALIDATE_EVIDENCE = "VALIDATE_EVIDENCE"
    MEASURE = "MEASURE"
    COMPARE = "COMPARE"
    BRANCH = "BRANCH"
    CORRECTIVE = "CORRECTIVE"
    PREVENTIVE = "PREVENTIVE"
    RECOMMEND = "RECOMMEND"
    VERIFY = "VERIFY"
    VERSION = "VERSION"
    TEST = "TEST"
    COMPARE_VERSIONS = "COMPARE_VERSIONS"
    DECIDE_PR = "DECIDE_PR"
    WRITE_ARTIFACTS = "WRITE_ARTIFACTS"
    UPDATE_MEMORY = "UPDATE_MEMORY"
    # Terminal states
    PASS_NO_CHANGE_RECORDED = "PASS_NO_CHANGE_RECORDED"
    PASS_CANDIDATE_REJECTED_RECORDED = "PASS_CANDIDATE_REJECTED_RECORDED"
    PASS_CANDIDATE_PR_CREATED = "PASS_CANDIDATE_PR_CREATED"
    FAIL_PATCH_PR_CREATED = "FAIL_PATCH_PR_CREATED"
    ESCALATED_WITH_BLOCKER = "ESCALATED_WITH_BLOCKER"


TERMINAL_STATES: Set[LoopState] = {
    LoopState.PASS_NO_CHANGE_RECORDED,
    LoopState.PASS_CANDIDATE_REJECTED_RECORDED,
    LoopState.PASS_CANDIDATE_PR_CREATED,
    LoopState.FAIL_PATCH_PR_CREATED,
    LoopState.ESCALATED_WITH_BLOCKER,
}

_TRANSITIONS: Dict[LoopState, Set[LoopState]] = {
    LoopState.INIT: {LoopState.LOAD_SPEC},
    LoopState.LOAD_SPEC: {LoopState.VALIDATE_SPEC},
    LoopState.VALIDATE_SPEC: {LoopState.COLLECT_EVIDENCE},
    LoopState.COLLECT_EVIDENCE: {LoopState.VALIDATE_EVIDENCE},
    LoopState.VALIDATE_EVIDENCE: {LoopState.MEASURE},
    LoopState.MEASURE: {LoopState.COMPARE},
    LoopState.COMPARE: {LoopState.BRANCH},
    LoopState.BRANCH: {LoopState.CORRECTIVE, LoopState.PREVENTIVE},
    LoopState.CORRECTIVE: {LoopState.RECOMMEND},
    LoopState.PREVENTIVE: {LoopState.RECOMMEND, LoopState.WRITE_ARTIFACTS},
    LoopState.RECOMMEND: {LoopState.VERIFY, LoopState.WRITE_ARTIFACTS},
    LoopState.VERIFY: {LoopState.VERSION, LoopState.WRITE_ARTIFACTS},
    LoopState.VERSION: {LoopState.TEST},
    LoopState.TEST: {LoopState.COMPARE_VERSIONS},
    LoopState.COMPARE_VERSIONS: {LoopState.DECIDE_PR},
    LoopState.DECIDE_PR: {LoopState.WRITE_ARTIFACTS},
    LoopState.WRITE_ARTIFACTS: {LoopState.UPDATE_MEMORY},
    LoopState.UPDATE_MEMORY: set(TERMINAL_STATES),
}


class InvalidTransition(RuntimeError):
    pass


class StateMachine:
    def __init__(self, start: LoopState = LoopState.INIT):
        self.state = start
        self.history: List[LoopState] = [start]

    def is_terminal(self) -> bool:
        return self.state in TERMINAL_STATES

    def can(self, to: LoopState) -> bool:
        if to == LoopState.ESCALATED_WITH_BLOCKER and self.state not in TERMINAL_STATES:
            return True
        return to in _TRANSITIONS.get(self.state, set())

    def to(self, to: LoopState) -> LoopState:
        if self.is_terminal():
            raise InvalidTransition(f"{self.state} is terminal; cannot transition")
        if not self.can(to):
            raise InvalidTransition(f"illegal transition {self.state} -> {to}")
        self.state = to
        self.history.append(to)
        return to
