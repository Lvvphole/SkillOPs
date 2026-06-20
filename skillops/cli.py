"""SkillOps CLI: arrange once, hit go.

    python -m skillops run --loop loops/weekly-skill-review.yaml
    python -m skillops validate           # validate all loop manifests
    python -m skillops version
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from skillops import __version__
from skillops.orchestrator.load_loop_spec import load_loop_spec
from skillops.orchestrator.validate_loop_spec import validate_loop_spec
from skillops.orchestrator.run_loop import run_loop


def _cmd_run(args: argparse.Namespace) -> int:
    report = run_loop(args.loop, write_artifacts=not args.no_artifacts)
    print(json.dumps(report, indent=2, default=str))
    terminal = report.get("terminal_state", "")
    return 1 if terminal == "ESCALATED_WITH_BLOCKER" else 0


def _cmd_validate(args: argparse.Namespace) -> int:
    loops_dir = Path(args.loops_dir)
    manifests = sorted(
        p for p in loops_dir.glob("*.yaml")
    ) + sorted(loops_dir.glob("*.loop.yaml"))
    seen = set()
    ok = True
    for manifest in manifests:
        if manifest in seen:
            continue
        seen.add(manifest)
        spec = load_loop_spec(str(manifest))
        result = validate_loop_spec(spec, schemas_root=str(loops_dir / "schemas"))
        status = "VALID" if result["valid"] else "INVALID"
        print(f"{status}: {manifest}")
        if not result["valid"]:
            ok = False
            for err in result["errors"]:
                print(f"    - {err}")
    return 0 if ok else 1


def _cmd_version(_: argparse.Namespace) -> int:
    print(__version__)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="skillops", description="Manifest-driven SkillOps loop runtime")
    sub = parser.add_subparsers(dest="command", required=True)

    run_p = sub.add_parser("run", help="run a loop once")
    run_p.add_argument("--loop", required=True, help="path to a LoopSpec YAML manifest")
    run_p.add_argument("--no-artifacts", action="store_true", help="do not write loop artifacts")
    run_p.set_defaults(func=_cmd_run)

    val_p = sub.add_parser("validate", help="validate loop manifests against schemas")
    val_p.add_argument("--loops-dir", default="loops", help="directory of loop manifests")
    val_p.set_defaults(func=_cmd_validate)

    ver_p = sub.add_parser("version", help="print the runtime version")
    ver_p.set_defaults(func=_cmd_version)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
