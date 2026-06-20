# Repo Inspection

## Preflight (HARD GIT AND PR RULES)

| Check | Result |
| --- | --- |
| Contract target path | `C:\Users\Emory Harris\projects\skill-ops` (operator's local Windows path) |
| Actual execution path | `/home/user/SkillOPs` (Claude Code on the web; fresh clone of the same GitHub repo) |
| Git root | `/home/user/SkillOPs` (confirmed `git rev-parse --show-toplevel`) |
| Remote `origin` | proxied `…/git/Lvvphole/SkillOPs` → `https://github.com/Lvvphole/SkillOPs` ✅ matches required remote |
| Default branch | `main` (origin/main present; current branch == origin/main, 0/0 divergence) |
| Current / feature branch | `claude/zealous-hopper-hrc9n6` (see path/branch mapping below) |
| Working tree at start | clean (`git status --short` empty) — no uncommitted user work to overwrite |
| Existing language stack | TypeScript ESM on Node.js (Inngest), `tsc`, `node:test`; scaffolded by a prior run |
| Package manager | npm (existing TS) + pip/`pyproject.toml` (new Python core) |
| Existing scripts | `npm test` / `npm run build` / `npm run typecheck` |
| Python available | Python 3.11.15, pytest 9.0.2, PyYAML 6.0.1 |

No new repo, clone, worktree, or alternate path was created. Work proceeded on the
existing clone and the harness-designated branch.

## Language selection decision — **Python-first (additive hybrid)**

Per `LANGUAGE_SELECTION_RULE` and success criteria 6–8:

- The repo **originated greenfield** (the pre-existing `artifacts/repo-inspection.md`
  recorded only `README.md` + `LICENSE` initially) and is **primarily an autonomous
  SkillOps loop engine** → criterion 7 selects **Python** as the core runtime.
- A prior run scaffolded a **TypeScript** implementation of the same goal. Per
  criterion 8 and the "do not rewrite a working TypeScript app into Python without
  user approval" constraint, that TypeScript layer is **preserved, not rewritten**.
- Resolution for "both exist": **Python owns the deterministic core**
  (loop runtime, CLI, manifests, schema validation, evidence, metrics, thresholds,
  branching, verification, versioning, memory, artifacts, PR automation, tests);
  the existing TypeScript (`src/**`, `package.json`, `tsconfig.json`,
  `tests/*.test.ts`) remains as the **adapter / interface layer** (Inngest
  workflows, run/update functions). No TypeScript file was deleted or rewritten.

This is an **additive** change (new `skillops/` core alongside existing `src/`), so
it is non-destructive and reversible. No user approval gate was triggered because
the change does not rewrite the working TypeScript app.

## Path / branch mappings (approved equivalents)

The contract's exact required paths are implemented verbatim except for two
documented, intentional mappings:

| Contract specifies | Implemented as | Reason |
| --- | --- | --- |
| feature branch `feat/manifest-skillops-loop-runtime` | `claude/zealous-hopper-hrc9n6` | The web harness pins this session to its own branch and forbids pushing elsewhere. The PR is opened from this branch into `main`. |
| `C:\Users\Emory Harris\projects\skill-ops` | `/home/user/SkillOPs` | Cloud execution environment is a fresh clone of the same GitHub repo; same git root, same `origin`. |

Additional files beyond the required list (all additive, non-conflicting):
`skillops/__main__.py` (enables `python -m skillops`), and
`skills/incident-triage/ACTIVE_VERSION` (rollback pointer for reversible updates).

All other required paths (`loops/schemas/*`, `loops/*.yaml`, `skillops/**`,
`skills/incident-triage/**`, `tests/test_*.py`, `artifacts/*`, root `AGENTS.md`,
`README.md`, `pyproject.toml`, `.env.example`) are implemented exactly.

## Existing structure preserved

`src/` (TypeScript), `package.json`, `package-lock.json`, `tsconfig.json`,
`docs/skillops.md`, `LICENSE`, and `tests/*.test.ts` are unchanged. `package.json`
and `tsconfig.json` are retained as the optional Node/TS compatibility files.
