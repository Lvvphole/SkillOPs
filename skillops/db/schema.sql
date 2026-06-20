-- SkillOps relational schema (reference shape).
-- The v1 runtime persists these as JSON under SKILLOPS_DATA_DIR (see queries.py),
-- so no database server is required for tests or the loop. The SQL below documents
-- the canonical schema for adapters that want a real database.

CREATE TABLE IF NOT EXISTS skill_runs (
  id               TEXT PRIMARY KEY,
  skill_id         TEXT NOT NULL,
  started_at       TEXT NOT NULL,
  ended_at         TEXT NOT NULL,
  duration_ms      INTEGER NOT NULL,
  success          INTEGER NOT NULL,
  predicted_positive INTEGER NOT NULL,
  actual_positive  INTEGER NOT NULL,
  action_taken     INTEGER NOT NULL,
  notes            TEXT
);

CREATE TABLE IF NOT EXISTS skill_versions (
  skill_id    TEXT NOT NULL,
  version     TEXT NOT NULL,
  path        TEXT NOT NULL,
  created_at  TEXT NOT NULL,
  reason      TEXT NOT NULL,
  PRIMARY KEY (skill_id, version)
);

CREATE TABLE IF NOT EXISTS skill_updates (
  id            TEXT PRIMARY KEY,
  skill_id      TEXT NOT NULL,
  from_version  TEXT NOT NULL,
  to_version    TEXT NOT NULL,
  kind          TEXT NOT NULL,
  evidence_json TEXT NOT NULL,
  approved      INTEGER NOT NULL,
  created_at    TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_skill_runs_skill ON skill_runs (skill_id);
CREATE INDEX IF NOT EXISTS idx_skill_updates_skill ON skill_updates (skill_id);
