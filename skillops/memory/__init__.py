"""Memory: durable loop state across cycles.

skill-memory.json    -> per-skill last decision, metrics, terminal state.
update-history.json  -> every version/update the loop produced.
failure-patterns.json-> recurring failure signatures to avoid repeating.
"""
from skillops.memory.read_memory import read_memory
from skillops.memory.write_memory import (
    write_memory,
    append_update_history,
    record_failure_pattern,
)

__all__ = [
    "read_memory",
    "write_memory",
    "append_update_history",
    "record_failure_pattern",
]
