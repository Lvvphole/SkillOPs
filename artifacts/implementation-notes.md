# Implementation Notes

## What was built
A Python-first, manifest-driven SkillOps **autonomous loop runtime** (v1) added
alongside the preserved TypeScript adapter layer.

Arrange once, hit go:
```bash
python -m skillops run --loop loops/weekly-skill-review.yaml
```

## Loop pattern (deterministic)
`Run → Measure → Compare → (fail: Repair) | (pass: Maintain, Challenge, Optimize)
→ Recommend → Verify → Test → Version → Remember → Repeat.`

Implemented as a whitelisted state machine
(`skillops/orchestrator/state_machine.py`) that can only reach declared terminal
states, preventing open-ended agent behavior.

## Key design decisions
- **Metrics decide pass/fail.** `calculate_metric_summary` + `compare_thresholds`
  are the only pass/fail authority. LLM output never decides pass/fail; the
  `recommendations/` package may suggest a patch/candidate only, and
  `constrain_recommendation` rejects any recommendation that asserts a verdict.
- **Evidence before analysis.** `collect_evidence` seeds runs from the skill's
  sample inputs when history is empty; `validate_evidence` blocks analysis until
  required sources exist and are non-empty.
- **Pass ≠ stop.** The preventive branch runs staleness, drift, challenge
  benchmarks, and an optimization scan even when thresholds pass. A candidate is
  created only on evidence-backed measurable improvement that preserves every
  required threshold (`verify_candidate`), satisfying criteria 19/23/24.
- **All updates versioned/reversible.** `create_skill_version` refuses to
  overwrite a prior version without a changelog; `rollback_skill` repoints
  `ACTIVE_VERSION`; `write_changelog` records every event.
- **Dependency-light.** Runtime depends only on PyYAML. JSON-Schema validation
  uses a dependency-free internal validator
  (`orchestrator/validate_loop_spec.py`) supporting the manifest schema subset.
- **No secrets / no paid services.** The deterministic core invokes no external
  LLM, Inngest, Slack, or GitHub provider; those are mocked/omitted in tests.

## Domain logic parity with the preserved TypeScript layer
The Python core mirrors the established TS domain logic exactly: thresholds
(`min_success_rate=0.8`, `max_avg_duration_ms=1000`, `max_false_positive_rate=0.2`,
`min_action_rate=0.25`); incident classifier (`urgent` iff `severity==high` or
`customer_impact`); and the evaluator's success/action definitions.

## Non-destructive rewrite statement
No TypeScript file was deleted or rewritten. The only modified pre-existing files
are additive/documentation: `AGENTS.md` (expanded role/branch/PR rules),
`.env.example` (added optional LLM/GitHub placeholders), `.gitignore` (added
Python ignores), `README.md` (added Python-first operator docs), and the
`artifacts/` reports. This is recorded here per the "no destructive rewrite
unless documented" constraint.

## Live run outcome
`python -m skillops run --loop loops/weekly-skill-review.yaml` →
**PASS_NO_CHANGE_RECORDED** (branch=preventive). Metrics: success_rate=1.0,
avg_duration_ms=5.0, false_positive_rate=0.0, action_rate=0.5, sample_size=6.
Maintenance + optimization scans ran; no evidence-backed candidate → no-change,
recorded to memory. The corrective, candidate-rejected, candidate-PR, and
escalation paths are exercised by the test suite.

## Repair attempts log
- pytest ran under an isolated uv interpreter lacking PyYAML → installed pytest
  into the system interpreter (which has PyYAML) and ran `python3 -m pytest`
  (1 fix, within the two-attempt limit).
- `compileall` produced `__pycache__` that staged accidentally → added Python
  ignores to `.gitignore` and unstaged them (1 fix).
- `skillops run` stdout was polluted by a log line → routed all logger output to
  stderr so stdout is clean JSON (1 fix).
