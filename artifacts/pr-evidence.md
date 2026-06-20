# PR Evidence

Branch: `codex/readme-verification-fix`
Commit hash: pending until commit
PR URL or creation log: pending until push/PR creation
Install commands:
- `npm.cmd install`
- `.venv\Scripts\python.exe -m pip install -e .[dev] --cache-dir .venv\pip-cache`
Test commands:
- `npm.cmd test`
- `.venv\Scripts\python.exe -m pytest` with `TMP`/`TEMP` set to `.venv\tmp`
Build/typecheck commands:
- `npm.cmd run build`
- `npm.cmd run typecheck`
Verification commands:
- `.venv\Scripts\python.exe -m skillops validate`
- `.venv\Scripts\python.exe -m compileall skillops`
- `git diff --name-status origin/main -- README.md`
- `rg -n "^diff --git a/README.md b/README.md" artifacts\final-diff.patch`
