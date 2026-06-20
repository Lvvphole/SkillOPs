# SkillOps

SkillOps is a **Python-first, manifest-driven autonomous loop runtime** for AI
skills. You arrange a loop once in a manifest and hit go; the runtime then runs
the skill, collects evidence, measures performance, compares thresholds, branches
into corrective repair (on fail) or preventive maintenance + optimization (on
pass), verifies any proposed change, versions the skill, writes memory, and emits
artifacts — deterministically, without an open-ended agent.

> **Architecture:** the Python package `skillops/` owns the deterministic core
> (loop runtime, CLI, manifest loading, schema validation, evidence, metrics,
> thresholds, branching, verification, versioning, memory, artifacts, PR
> automation, tests). The pre-existing **TypeScript** code under `src/`
> (Inngest workflows, run/update functions) is **preserved as an adapter /
> interface layer** — see `artifacts/repo-inspection.md` for the language
> decision. The legacy TS documentation is retained further down this file.

## Arrange once, hit go

```bash
# Run a loop once
python -m skillops run --loop loops/weekly-skill-review.yaml

# Or via the installed console script (after `pip install -e .`)
skillops run --loop loops/weekly-skill-review.yaml

# Validate every loop manifest against its schema
python -m skillops validate

# Run the test suite
python -m pytest
```

`run` prints a JSON loop report to stdout (logs go to stderr) and ends in a
**declared terminal state** — never "done" or "looks good":
`PASS_NO_CHANGE_RECORDED`, `PASS_CANDIDATE_REJECTED_RECORDED`,
`PASS_CANDIDATE_PR_CREATED`, `FAIL_PATCH_PR_CREATED`, or
`ESCALATED_WITH_BLOCKER`.

## The loop

```text
Run → Measure → Compare
   → if fail: Repair (corrective)
   → if pass: Maintain, Challenge, Optimize (preventive)
→ Recommend → Verify → Test → Version → Remember → Repeat
```

- **How manifests control behavior.** A `LoopSpec` (`loops/*.yaml`) declares the
  target skill, trigger, runtime limits, required evidence, metrics, thresholds,
  branches, corrective/preventive/optimization actions, verifier/test/PR
  behavior, memory file, required artifacts, and terminal states. Skills are
  described by manifests under `skills/<skill>/` (spec, config, thresholds,
  evidence, evaluation, improvement-policy, versioned skill files). The runtime
  loads and schema-validates these before doing anything.
- **Why Python owns the core.** The repo originated greenfield and is primarily
  an autonomous loop engine, so the deterministic control system is implemented
  in Python. TypeScript is used only as an adapter/interface layer.
- **Pass does not stop improvement.** When thresholds pass, the loop still runs
  staleness, drift, challenge-benchmark, and optimization scans. It creates a
  candidate version **only** when there is evidence-backed measurable
  improvement that preserves every required threshold; otherwise it records a
  no-change decision and waits for the next trigger.
- **Fail triggers corrective repair.** Failing thresholds diagnose the failure,
  recommend a patch (suggestion only), verify it, create a **new** skill version
  (never overwriting history), run regression, and open a PR.
- **Metrics decide pass/fail — never the LLM.** `compare_thresholds` is the only
  authority. LLM-style output may suggest a patch/candidate, and even that is
  constrained (`constrain_recommendation`) and verified before use.
- **Verification blocks unsafe updates.** The Verifier rejects missing evidence,
  unversioned/secret-bearing changes, self-certification, and candidates that
  fail to preserve thresholds or show no measured improvement.
- **Versioning and rollback.** Every update is versioned; `create_skill_version`
  refuses to overwrite without a changelog and `rollback_skill` repoints the
  active version — updates are always reversible.
- **Artifacts prove completion.** Completion is mechanical: tests, build/
  validation logs, metric summaries, reports, the final diff, the commit, the
  pushed branch, and the PR URL in `artifacts/` — not an agent's say-so.

## Python package layout

```text
loops/
  schemas/         loop, skill, evidence, metric, improvement, escalation schemas
  *.yaml           weekly-skill-review, incident-triage.loop, meta-loop
skillops/
  cli.py           arrange-once entrypoint (run / validate / version)
  orchestrator/    load + validate spec, state machine, branch, escalation, run_loop
  runs/ evidence/ metrics/ analysis/ recommendations/
  verification/ versioning/ memory/ pr/ db/ utils/
skills/incident-triage/   sample skill (manifests + versioned skill files)
tests/                     pytest suite (runner, metrics, thresholds, branching,
                           verifier, versioning, memory, update flow)
artifacts/                 evidence: reports, logs, diff, PR url
```

---

## Legacy TypeScript adapter (preserved)

The original TypeScript control-loop core is retained as the adapter/interface
layer. It is not a web app, dashboard, API service, database-backed platform, or
CLI tool — it is the runtime structure for looped skills with evidence-based
updates, now driven by the Python core above.

## What Problem SkillOps Solves

Most automation systems can run a task, but they do not reliably answer:

- Did the skill work?
- Did it improve over time?
- What evidence proves the update should be accepted?
- What changed between versions?
- Which failures keep repeating?
- Who verifies completion?
- What should happen next when a skill underperforms?

SkillOps solves this by treating each skill as a loop:

```text
run -> log -> measure -> evaluate -> verify -> update -> remember -> repeat
```

The goal is to prevent untracked, unverified, or subjective skill changes. SkillOps makes skill behavior measurable and skill updates evidence-backed.

## Mental Model

A SkillOps skill is not just a prompt, function, or script.

A skill has:

- an input contract
- execution logic
- validation rules
- evaluation logic
- performance thresholds
- versioned skill documentation
- run history
- memory
- evidence requirements
- update verification

The system separates responsibilities:

```text
Skill logic decides what to do.
Run logging records what happened.
Metrics measure performance.
Analysis compares results to thresholds.
Verification checks evidence.
Memory stores history and failure patterns.
Version files preserve change history.
```

Completion is not based on an agent saying the work is done. Completion depends on external artifacts such as tests, logs, metrics, reports, and committed files.

## How A Skill Loop Works

A looped skill follows this lifecycle:

1. An input is received.
2. The skill verifies the input shape.
3. The skill runs deterministic decision logic.
4. The result is evaluated.
5. The run result is logged.
6. Metrics are calculated across run history.
7. Performance is compared against thresholds.
8. If performance fails, recommendations can be generated.
9. Proposed updates must include evidence.
10. Approved updates are versioned instead of overwriting history.
11. Memory records known failures, updates, and next actions.

Example skill loop:

```text
incident input
  -> incident-triage verifier
  -> classifier
  -> evaluator
  -> run log
  -> metric scoring
  -> threshold analysis
  -> recommendation or update review
```

## Repository Structure

```text
src/
  analysis/
  db/
  inngest/
  memory/
  metrics/
  runs/
  skills/
  utils/
  verification/

tests/
docs/
artifacts/
```

## Runtime Folder Map

### `src/skills/`

Contains individual looped skills.

The current sample skill is:

```text
src/skills/incident-triage/
```

It includes:

```text
classifier.ts
evaluator.ts
verifier.ts
config.json
thresholds.json
skill.md
versions/
```

This folder is where skill-specific behavior lives.

### `src/runs/`

Runs a skill and records the result.

The main runtime entry is:

```text
src/runs/runSkill.ts
```

This is currently called from tests or internal modules. In a larger system, this would be called by an API route, queue worker, scheduled job, webhook, or CLI.

### `src/metrics/`

Calculates measurable performance values such as:

```text
successRate
avgDurationMs
falsePositiveRate
actionRate
```

These metrics make skill behavior externally checkable.

### `src/analysis/`

Compares metrics against thresholds and produces pass/fail analysis.

This is where the system decides whether a skill is meeting its operating requirements.

### `src/verification/`

Checks whether proposed skill updates are allowed.

Verification currently checks things like:

- required evidence exists
- evidence files are non-empty
- proposed updates are versioned
- proposed content is not empty
- obvious secret-like strings are rejected

### `src/memory/`

Stores lightweight memory artifacts for the loop.

Current memory files include:

```text
failure-patterns.json
skill-memory.json
update-history.json
```

In a production system, these would likely move to a real database.

### `src/inngest/`

Contains mocked Inngest-compatible workflow declarations.

These model how the system could eventually run event-driven and scheduled loops, such as:

```text
skill/run
skill/update
weekly-skill-loop
review-skill-performance
```

They are not connected to a live Inngest deployment yet.

### `src/db/`

Contains lightweight persistence helpers and schema placeholders.

This is not currently a production database layer.

### `tests/`

Contains project verification tests.

The tests verify metrics, skill execution, update approval, and verifier behavior.

### `artifacts/`

Contains evidence files such as logs, reports, metric summaries, verification notes, and PR evidence.

These files are useful for auditability, but they are not the runtime database.

## Adding Another Looped Skill

Create a new folder under `src/skills/`:

```text
src/skills/<skill-id>/
```

Recommended structure:

```text
src/skills/<skill-id>/
  classifier.ts
  evaluator.ts
  verifier.ts
  config.json
  thresholds.json
  skill.md
  versions/
    v1.skill.md
```

A new skill should define:

- the input shape it accepts
- how inputs are verified
- how the skill makes a decision
- how the outcome is evaluated
- what metrics matter
- what thresholds define pass/fail behavior
- what version of the skill is active
- what evidence is required before updates are approved

Then update the shared runtime as needed:

```text
src/runs/runSkill.ts
src/analysis/
src/metrics/
src/memory/
tests/
```

At minimum, add tests that prove:

- valid input runs successfully
- invalid input is rejected
- metrics can be calculated
- threshold analysis works
- updates require evidence and version changes

## Running The Project

Install dependencies:

```bash
npm install
```

Build:

```bash
npm run build
```

Typecheck:

```bash
npm run typecheck
```

Run tests:

```bash
npm test
```

Expected result:

```text
tests 4
pass 4
fail 0
```

## Current Limitations

SkillOps currently does not include:

- no web API
- no dashboard
- no production database
- no queue worker
- no deployed Inngest integration
- no application CLI
- no authentication
- no multi-tenant model
- no hosted service
- no UI for approving updates
- no external observability integration

The current repo is the control-loop core. Its job is to prove the SkillOps operating model before adding platform layers around it.
  - metrics
  - runs
  - verification
  - memory
  - mocked Inngest function declarations
  - incident-triage sample skill

- Added tests:
  - metric scoring
  - skill execution
  - skill update validation
  - evidence-backed verifier approval

- Added evidence artifacts:
  - build results
  - test results
  - repo inspection
  - implementation notes
  - verification report
  - evaluation report
  - recommendation report
  - metric summary
  - weekly performance report
  - skill change log
  - PR evidence

- Added missing `typescript` dev dependency required for `tsc`.

- Updated verifier test evidence path to use an existing committed artifact:
  - `artifacts/verification-report.md`

## CLI Smoke Test

N/A, no CLI is defined in `package.json`, no `bin` entry exists, and no `src/cli.ts` exists.

## Verification

The following commands passed:

```bash
npm run build
npm run typecheck
npm test
