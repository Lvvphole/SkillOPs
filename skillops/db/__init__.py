"""JSON-file-backed persistence for runs, versions, and updates.

The relational shape is documented in schema.sql; the default v1 store is a
JSON file under SKILLOPS_DATA_DIR so tests and the loop need no database server.
"""
from skillops.db.queries import (
    insert_run,
    select_runs,
    record_version,
    select_versions,
    record_update,
    select_updates,
    data_dir,
)

__all__ = [
    "insert_run",
    "select_runs",
    "record_version",
    "select_versions",
    "record_update",
    "select_updates",
    "data_dir",
]
