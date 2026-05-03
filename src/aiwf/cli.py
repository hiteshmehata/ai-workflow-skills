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
    def add_home_flag(target: argparse.ArgumentParser) -> None:
        target.add_argument("--home", type=Path, default=None)

    def add_repo_flag(target: argparse.ArgumentParser) -> None:
        target.add_argument("--repo", type=Path, default=None)

    parser = argparse.ArgumentParser(prog="aiwf")
    add_home_flag(parser)
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_home_flag(subparsers.add_parser("build"))
    add_home_flag(subparsers.add_parser("validate"))
    add_home_flag(subparsers.add_parser("list"))
    add_home_flag(subparsers.add_parser("doctor"))

    install_parser = subparsers.add_parser("install")
    add_home_flag(install_parser)
    add_repo_flag(install_parser)
    install_parser.add_argument("target", choices=["codex", "copilot", "opencode", "claude", "all"])
    install_parser.add_argument("--dry-run", action="store_true")

    add_home_flag(subparsers.add_parser("version"))
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
        if getattr(args, "repo", None) is not None:
            print(f"copilot_prompts={args.repo / '.github' / 'prompts'}")
        else:
            print("copilot_prompts=<repo>/.github/prompts")
        print(f"opencode_commands={targets.opencode_commands}")
        print(f"opencode_skills={targets.opencode_skills}")
        print(f"claude_commands={targets.claude_commands}")
        return 0
    if args.command == "install":
        if args.target == "copilot" and args.repo is None:
            print("copilot install requires --repo", file=sys.stderr)
            return 2
        actions = install(root, args.target, home=home, dry_run=args.dry_run, repo=args.repo)
        for action in actions:
            print(f"{action.source} -> {action.destination}")
        return 0
    if args.command == "version":
        print(__version__)
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
