# SkillOps Agent Rules

SkillOps is an autonomous loop runtime, not an open-ended agent. The user stays
outside the loop except to approve escalations. Roles are separated and the
executor can never grade its own work or declare completion.

## Role separation
- **Planner** inspects the repo, validates preflight safety, applies the language
  selection rule, maps structure, and sequences milestones. Does not claim completion.
- **Executor** edits files, writes code/tests, runs commands, commits, pushes, and
  opens PRs. Cannot grade its own work; never determines completion.
- **Verifier** checks files, approved path mappings, logs, test/build output,
  artifacts, git status, diff, commit hash, pushed branch, and PR URL.
- **Evaluator** scores the implementation against the contract and can require
  correction; triggers escalation after repeated failure.
- **Memory Manager** records state, decisions, mappings, commands, artifacts,
  branch/commit/push/PR, blockers, and next actions.
- **Escalation Manager** handles blocked path, repo mismatch, uncommitted work,
  language ambiguity, failed install/build/test/push/PR, and unsafe architecture.

## Evidence rules
- Evidence must exist **before** analysis.
- Agent explanations are **not** evidence. Completion requires files, logs,
  tests, build output, diffs, artifacts, branch/push state, and a PR URL.
- Metrics decide pass/fail. LLM output **cannot** decide pass/fail; it may only
  suggest a patch or candidate, which must be verified before use.

## No self-certification
- The executor cannot self-certify completion. Completion is determined only by
  mechanical stop conditions checked by the Verifier and Evaluator.
- Invalid terminal states: "done", "complete", "looks good", "probably fixed".
- Valid terminal states: `PASS_NO_CHANGE_RECORDED`,
  `PASS_CANDIDATE_REJECTED_RECORDED`, `PASS_CANDIDATE_PR_CREATED`,
  `FAIL_PATCH_PR_CREATED`, `ESCALATED_WITH_BLOCKER`.

## Verifier authority
The Verifier rejects unsupported recommendations, missing evidence, unsafe
updates, self-certification, and undocumented path substitutions. Path
substitutions are only valid when mapped in `artifacts/repo-inspection.md`.

## Evaluator authority
The Evaluator scores only against contract success criteria and may require
correction. It confirms no unresolved correction or escalation remains.

## Branch safety
- Never work directly on the default branch.
- Pull the latest default branch before creating the feature branch.
- Push only the feature branch.

## PR rules
- Create the PR against the default branch.
- The PR body documents summary, architecture, language rationale, loop behavior
  (corrective + preventive/optimization), tests, validation, artifacts, changed
  files, risk notes, rollback notes, and known limitations.
- The PR URL is written to `artifacts/pr-url.txt`, referenced in
  `artifacts/evaluation-report.md`, and printed in the final handoff.

## Update safety
All skill updates are versioned or reversible. A new version never overwrites a
prior version without a changelog entry. No secrets or hardcoded credentials are
committed.

## Mechanical completion
Stop only when: required structure exists (or an approved mapping does), required
artifacts exist, tests pass, validation passes, no secrets are committed, the
final diff is saved, changes are committed, the branch is pushed, the PR URL
exists, the Verifier approves, and the Evaluator confirms no open correction.
