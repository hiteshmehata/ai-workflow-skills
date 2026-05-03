from __future__ import annotations

import shutil
from pathlib import Path

from aiwf.paths import ProjectLayout, project_layout
from aiwf.workflows import ARTIFACTS, Workflow, WorkflowCatalog, load_catalog


def _skill_markdown(workflow: Workflow) -> str:
    outputs = "\n".join(f"- `{output}`" for output in workflow.outputs)
    return f"""---
name: {workflow.name}
description: {workflow.description}
---

# {workflow.title}

Use this skill when the user wants the `{workflow.name}` workflow.

## Operating rules

- Work from repository truth before guessing.
- Keep context compact and externalize durable state into markdown artifacts.
- Use the project artifact contract consistently.
- Prefer explicit assumptions and validation criteria.

## Workflow

{workflow.prompt}

## Standard artifacts

{outputs}
"""


def _openai_yaml(workflow: Workflow) -> str:
    default_prompt = workflow.prompt.splitlines()[0].strip()
    return (
        "display_name: \"%s\"\n"
        "short_description: \"%s\"\n"
        "default_prompt: \"%s\"\n"
    ) % (workflow.title, workflow.description, default_prompt.replace('"', "'"))


def _command_markdown(workflow: Workflow, tool_name: str) -> str:
    outputs = "\n".join(f"- `{output}`" for output in workflow.outputs)
    return f"""---
description: {workflow.command_description}
argument-hint: ""
---

# /{workflow.name}

You are running the `{workflow.name}` workflow in {tool_name}.

{workflow.prompt}

Standard project artifacts:
{outputs}
"""


def _copilot_prompt_markdown(workflow: Workflow) -> str:
    outputs = "\n".join(f"- `{output}`" for output in workflow.outputs)
    return f"""---
agent: 'agent'
description: '{workflow.command_description}'
---

You are running the `{workflow.name}` workflow in GitHub Copilot.

{workflow.prompt}

Standard project artifacts:
{outputs}
"""


def _launcher_script(catalog: WorkflowCatalog) -> str:
    names = " ".join(sorted(workflow.name for workflow in catalog.workflows))
    return f"""#!/usr/bin/env sh
set -eu

if [ "$#" -lt 1 ]; then
  echo "usage: aiwf-workflow <workflow-name>"
  echo "available: {names}"
  exit 1
fi

case "$1" in
"""


def _launcher_cases(catalog: WorkflowCatalog) -> str:
    blocks: list[str] = []
    for workflow in sorted(catalog.workflows, key=lambda item: item.name):
        prompt = workflow.prompt.replace('"', '\\"')
        blocks.append(f"  {workflow.name})\n    printf '%s\\n' \"{prompt}\"\n    ;;")
    blocks.append("  *)\n    echo \"unknown workflow: $1\"\n    exit 1\n    ;;")
    return "\n".join(blocks) + "\nesac\n"


def build(root: Path) -> ProjectLayout:
    layout = project_layout(root)
    if layout.dist.exists():
        shutil.rmtree(layout.dist)
    for directory in (
        layout.agent_skills,
        layout.codex_skills,
        layout.copilot_prompts,
        layout.opencode_skills,
        layout.opencode_commands,
        layout.claude_commands,
        layout.bin_dir,
    ):
        directory.mkdir(parents=True, exist_ok=True)

    catalog = load_catalog(root)
    for workflow in catalog.workflows:
        _write_skill_bundle(layout.agent_skills / workflow.name, workflow)
        _write_skill_bundle(layout.codex_skills / workflow.name, workflow)
        (layout.copilot_prompts / f"{workflow.name}.prompt.md").write_text(
            _copilot_prompt_markdown(workflow)
        )
        _write_skill_bundle(layout.opencode_skills / workflow.name, workflow)
        (layout.opencode_commands / f"{workflow.name}.md").write_text(
            _command_markdown(workflow, "OpenCode")
        )
        (layout.claude_commands / f"{workflow.name}.md").write_text(
            _command_markdown(workflow, "Claude Code")
        )

    launcher = layout.bin_dir / "aiwf-workflow"
    launcher.write_text(_launcher_script(catalog) + _launcher_cases(catalog))
    launcher.chmod(0o755)

    _write_example_docs(root)
    return layout


def _write_skill_bundle(directory: Path, workflow: Workflow) -> None:
    (directory / "agents").mkdir(parents=True, exist_ok=True)
    (directory / "references").mkdir(parents=True, exist_ok=True)
    (directory / "SKILL.md").write_text(_skill_markdown(workflow))
    (directory / "agents" / "openai.yaml").write_text(_openai_yaml(workflow))
    (directory / "references" / "artifact-contract.md").write_text(
        "\n".join(["# Artifact Contract", ""] + [f"- `{item}`" for item in ARTIFACTS]) + "\n"
    )


def _write_example_docs(root: Path) -> None:
    docs_root = root / "examples" / "project" / "docs" / "ai"
    docs_root.mkdir(parents=True, exist_ok=True)
    for artifact in ARTIFACTS:
        path = docs_root / Path(artifact).name
        if not path.exists():
            path.write_text(f"# {path.name}\n")
