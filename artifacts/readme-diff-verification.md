# README Diff Verification

Purpose: prove that the PR repair/evidence-only branch does not target root
`README.md`.

## Commands

```text
git diff --name-status origin/main -- README.md
git diff --name-only origin/main
git rev-parse origin/main:README.md
git rev-parse HEAD:README.md
```

## Results

- `git diff --name-status origin/main -- README.md`: no output
- Aggregate PR diff file headers: no `diff --git a/README.md b/README.md`
- `origin/main:README.md` blob: `83af4be9434fc3210b27e604134ae11ea5319b7d`
- `HEAD:README.md` blob: `83af4be9434fc3210b27e604134ae11ea5319b7d`
- Blob comparison: identical

## Verdict

PASS: root `README.md` is not changed by this branch.
