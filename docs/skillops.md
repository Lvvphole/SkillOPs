# SkillOps Control Loop

SkillOps is a deterministic control-loop reference implementation for operating AI skills. The loop runs a skill, records run evidence, calculates metrics, compares those metrics to fixed thresholds, recommends improvements only when review is requested or thresholds fail, verifies evidence and proposed changes, writes new versioned skill files, and repeats on a weekly cadence.

## Generated patch policy

Root `README.md` is not used as the generated documentation patch target for PR
repair or evidence-only changes. Expanded operator documentation belongs in this
dedicated docs file, and README-specific edits require an explicit task that
names `README.md`.

For PR repair/evidence-only changes, the verifier records a README diff check in
`artifacts/readme-diff-verification.md`. The branch must not contain a
`diff --git a/README.md b/README.md` file header in the aggregate PR diff.

## Install

```bash
npm install
```

The project uses Node.js and TypeScript for the local v1 workflow. No paid service is required to run tests.

## Configuration

Copy `.env.example` to `.env` if you want local environment overrides:

```bash
cp .env.example .env
```

No secrets are required for local tests. Optional Inngest keys are documented in `.env.example` for hosted execution.

## Run and test

```bash
npm test
npm run build
npm run typecheck
```

- `npm test` builds TypeScript and runs compiled Node test suites.
- `npm run build` compiles TypeScript into `dist/`.
- `npm run typecheck` verifies TypeScript without emitting files.

## Architecture

- `src/inngest/` contains scheduled and event workflow declarations.
- `src/runs/` executes skills and stores run history.
- `src/metrics/` computes success rate, average duration, false positive rate, action rate, and deterministic threshold pass/fail.
- `src/analysis/` separates deterministic scoring from recommendation text.
- `src/verification/` approves evidence-backed, versioned updates before writes.
- `src/skills/incident-triage/` is the sample skill with classifier, evaluator, verifier, thresholds, and versioned skill files.
- `src/memory/` stores skill memory, update history, and failure patterns.
- `src/db/` provides the schema and query abstraction used by run logging/history.
- `src/utils/` contains shared date, average, and logging utilities.

## Loop behavior

1. `run-skill` executes the configured skill and logs a run result.
2. `review-skill-performance` loads run history and computes deterministic metrics.
3. `scoreSkillPerformance` compares metrics to thresholds and returns pass/fail mechanically.
4. `recommendImprovements` emits recommendations only after threshold failure or explicit review.
5. `approveSkillUpdate` verifies evidence and proposed changes before update writes.
6. `update-skill` writes a new versioned skill file instead of overwriting prior versions.
7. `weekly-skill-loop` repeats the review cadence for `incident-triage`.

LLMs may assist with recommendation wording, but they do not decide whether a skill passes or fails.

## Evidence artifacts

Evidence is stored under `artifacts/`, including repo inspection, implementation notes, weekly performance report, metric summary, recommendation report, verification report, evaluation report, skill changelog, test results, build results, and final diff.

## PR verification process

Before creating or updating a PR, verify:

1. Required files exist at the documented exact paths.
2. `npm test` passes and output is saved in `artifacts/test-results.log`.
3. `npm run build` passes and output is saved in `artifacts/build-results.log`.
4. `git diff --name-status origin/main...HEAD -- README.md` produces no output
   unless the task explicitly names `README.md`.
5. `artifacts/final-diff.patch` is regenerated from the current branch diff and
   contains no root README file header for PR repair/evidence-only changes.
6. Branch name, commit hash, test command, build command, and PR evidence are documented.
