# SkillOps Agent Rules

- Separate roles: Planner maps work, Executor edits, Verifier checks evidence, Evaluator scores criteria, Memory Manager records state.
- No self-certification: explanations are not evidence; completion requires files, logs, tests, build output, diffs, and PR evidence.
- Verifier authority: verifier checks required file structure, evidence artifacts, test/build logs, update safety, and rejects missing or unsafe updates.
- Evaluator authority: evaluator scores only against contract criteria and can require correction.
- Mechanical completion: thresholds and deterministic checks decide pass/fail; LLMs may recommend improvements but never decide pass/fail.
- Skill updates must be versioned or reversible and must not overwrite prior versions without history.
- Do not commit secrets or hardcoded private credentials.
