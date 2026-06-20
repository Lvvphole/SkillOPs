# SkillOps

SkillOps is a TypeScript control-loop system for building operational skills that can be run, measured, verified, improved, and versioned over time.

It is not currently a web app, dashboard, API service, database-backed platform, or CLI tool. It is the core runtime structure for managing looped skills with evidence-based updates.

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
