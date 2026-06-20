from skillops.memory.read_memory import read_memory
from skillops.memory.write_memory import write_memory, append_update_history, record_failure_pattern


def test_write_and_read_skill_memory():
    write_memory("incident-triage", {"passed": True, "last_branch": "preventive"})
    mem = read_memory("skill-memory.json")
    assert mem["incident-triage"]["passed"] is True
    assert "updated_at" in mem["incident-triage"]


def test_update_history_appends():
    append_update_history({"skill_id": "incident-triage", "version": "v2", "kind": "patch"})
    append_update_history({"skill_id": "incident-triage", "version": "v3", "kind": "candidate"})
    history = read_memory("update-history.json", default=[])
    assert len(history) == 2
    assert history[0]["version"] == "v2"


def test_failure_pattern_dedupes_and_counts():
    record_failure_pattern({"signature": "verify_rejected:incident-triage"})
    record_failure_pattern({"signature": "verify_rejected:incident-triage"})
    patterns = read_memory("failure-patterns.json", default=[])
    assert len(patterns) == 1
    assert patterns[0]["count"] == 2


def test_read_missing_returns_default():
    assert read_memory("does-not-exist.json", default={"a": 1}) == {"a": 1}
