from __future__ import annotations

import argparse
import sys
from pathlib import Path

from aiwf import __version__
from aiwf.install import install
from aiwf.paths import default_install_targets
from aiwf.render import build
from aiwf.validate import validate
from aiwf.workflows import load_catalog


def _root() -> Path:
    return Path(__file__).resolve().parents[2]


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="aiwf")
    parser.add_argument("--home", type=Path, default=None)
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("build")
    subparsers.add_parser("validate")
    subparsers.add_parser("list")
    subparsers.add_parser("doctor")

    install_parser = subparsers.add_parser("install")
    install_parser.add_argument("target", choices=["codex", "opencode", "claude", "all"])
    install_parser.add_argument("--dry-run", action="store_true")

    subparsers.add_parser("version")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    root = _root()
    home = args.home or Path.home()

    if args.command == "build":
        layout = build(root)
        print(layout.dist)
        return 0
    if args.command == "validate":
        issues = validate(root)
        if issues:
            for issue in issues:
                print(issue, file=sys.stderr)
            return 1
        print("ok")
        return 0
    if args.command == "list":
        for workflow in load_catalog(root).workflows:
            print(f"{workflow.name}: {workflow.description}")
        return 0
    if args.command == "doctor":
        targets = default_install_targets(home)
        print(f"codex_skills={targets.codex_skills}")
        print(f"opencode_commands={targets.opencode_commands}")
        print(f"opencode_skills={targets.opencode_skills}")
        print(f"claude_commands={targets.claude_commands}")
        return 0
    if args.command == "install":
        actions = install(root, args.target, home=home, dry_run=args.dry_run)
        for action in actions:
            print(f"{action.source} -> {action.destination}")
        return 0
    if args.command == "version":
        print(__version__)
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
