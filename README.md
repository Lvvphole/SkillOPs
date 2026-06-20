## Summary

Ports the SkillOps patch into `Lvvphole/SkillOPs` on branch `codex/skillops-patch`.

This change adds a deterministic TypeScript SkillOps implementation with role-separated verification artifacts, incident-triage skill logic, metric scoring, mocked Inngest-compatible workflow declarations, persistent memory artifacts, and project documentation.

## Changes

- Added project configuration:
  - `package.json`
  - `package-lock.json`
  - `tsconfig.json`
  - `.env.example`
  - `.gitignore`

- Added SkillOps agent rules:
  - `AGENTS.md`

- Added SkillOps documentation:
  - `docs/skillops.md`

- Added TypeScript source modules:
  - analysis
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
