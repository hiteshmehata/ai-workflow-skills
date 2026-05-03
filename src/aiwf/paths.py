from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class InstallTargets:
    codex_skills: Path
    opencode_commands: Path
    opencode_skills: Path
    claude_commands: Path


@dataclass(frozen=True)
class ProjectLayout:
    root: Path
    dist: Path
    agent_skills: Path
    codex_skills: Path
    copilot_prompts: Path
    opencode_skills: Path
    opencode_commands: Path
    claude_commands: Path
    bin_dir: Path


def default_install_targets(home: Path) -> InstallTargets:
    return InstallTargets(
        codex_skills=home / ".codex" / "skills",
        opencode_commands=home / ".config" / "opencode" / "commands",
        opencode_skills=home / ".config" / "opencode" / "skills",
        claude_commands=home / ".claude" / "commands",
    )


def project_layout(root: Path) -> ProjectLayout:
    dist = root / "dist"
    return ProjectLayout(
        root=root,
        dist=dist,
        agent_skills=dist / "agent-skills",
        codex_skills=dist / "codex" / "skills",
        copilot_prompts=dist / "copilot" / "prompts",
        opencode_skills=dist / "opencode" / "skills",
        opencode_commands=dist / "opencode" / "commands",
        claude_commands=dist / "claude" / "commands",
        bin_dir=dist / "bin",
    )
