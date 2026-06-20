"""Test isolation: redirect the run store and memory to a temp dir per test."""
import os
import pytest


@pytest.fixture(autouse=True)
def isolated_state(tmp_path, monkeypatch):
    monkeypatch.setenv("SKILLOPS_DATA_DIR", str(tmp_path / "data"))
    monkeypatch.setenv("SKILLOPS_MEMORY_DIR", str(tmp_path / "memory"))
    monkeypatch.setenv("SKILLOPS_LOG_LEVEL", "error")
    yield


def make_run(**kw):
    from skillops import SkillRun
    base = dict(
        id="r", skill_id="incident-triage", started_at="2026-06-20T00:00:00.000Z",
        ended_at="2026-06-20T00:00:00.005Z", duration_ms=5, success=True,
        predicted_positive=True, actual_positive=True, action_taken=True, notes="urgent",
    )
    base.update(kw)
    return SkillRun(**base)
