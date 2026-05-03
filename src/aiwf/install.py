from __future__ import annotations

import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from aiwf.paths import InstallTargets, default_install_targets, project_layout


@dataclass(frozen=True)
class InstallAction:
    source: Path
    destination: Path


def _copy_tree(source: Path, destination: Path) -> None:
    if destination.exists():
        shutil.rmtree(destination)
    shutil.copytree(source, destination)


def _copy_file(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)


def install(
    root: Path,
    target: str,
    home: Path,
    dry_run: bool = False,
    repo: Path | None = None,
) -> list[InstallAction]:
    layout = project_layout(root)
    paths = default_install_targets(home)
    if target == "codex":
        return _install_skills(layout.codex_skills, paths.codex_skills, dry_run)
    if target == "copilot":
        if repo is None:
            raise ValueError("copilot install requires a repository path")
        return _install_prompt_files(layout.copilot_prompts, repo / ".github" / "prompts", dry_run)
    if target == "opencode":
        actions = _install_skills(layout.opencode_skills, paths.opencode_skills, dry_run)
        actions.extend(_install_commands(layout.opencode_commands, paths.opencode_commands, dry_run))
        return actions
    if target == "claude":
        return _install_commands(layout.claude_commands, paths.claude_commands, dry_run)
    if target == "all":
        actions: list[InstallAction] = []
        for item in ("codex", "opencode", "claude"):
            actions.extend(install(root, item, home=home, dry_run=dry_run, repo=repo))
        if repo is not None:
            actions.extend(install(root, "copilot", home=home, dry_run=dry_run, repo=repo))
        return actions
    raise ValueError(f"unknown install target: {target}")


def _install_skills(source_root: Path, destination_root: Path, dry_run: bool) -> list[InstallAction]:
    actions: list[InstallAction] = []
    destination_root.mkdir(parents=True, exist_ok=True)
    for source in sorted(source_root.iterdir()):
        destination = destination_root / source.name
        actions.append(InstallAction(source=source, destination=destination))
        if not dry_run:
            _copy_tree(source, destination)
    return actions


def _install_commands(source_root: Path, destination_root: Path, dry_run: bool) -> list[InstallAction]:
    actions: list[InstallAction] = []
    destination_root.mkdir(parents=True, exist_ok=True)
    for source in sorted(source_root.glob("*.md")):
        destination = destination_root / source.name
        actions.append(InstallAction(source=source, destination=destination))
        if not dry_run:
            _copy_file(source, destination)
    return actions


def _install_prompt_files(source_root: Path, destination_root: Path, dry_run: bool) -> list[InstallAction]:
    actions: list[InstallAction] = []
    destination_root.mkdir(parents=True, exist_ok=True)
    for source in sorted(source_root.glob("*.prompt.md")):
        destination = destination_root / source.name
        actions.append(InstallAction(source=source, destination=destination))
        if not dry_run:
            _copy_file(source, destination)
    return actions
