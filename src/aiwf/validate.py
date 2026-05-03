from __future__ import annotations

from pathlib import Path

from aiwf.paths import project_layout
from aiwf.workflows import ARTIFACTS, load_catalog


class ValidationError(RuntimeError):
    pass


def validate(root: Path) -> list[str]:
    issues: list[str] = []
    catalog = load_catalog(root)
    if not catalog.workflows:
        issues.append("no workflows defined")

    seen_names: set[str] = set()
    for workflow in catalog.workflows:
        if workflow.name in seen_names:
            issues.append(f"duplicate workflow: {workflow.name}")
        seen_names.add(workflow.name)
        if tuple(workflow.outputs) != ARTIFACTS:
            issues.append(f"workflow {workflow.name} changed the shared artifact contract")

    layout = project_layout(root)
    expected = [layout.codex_skills, layout.opencode_commands, layout.opencode_skills, layout.claude_commands]
    missing = [str(path) for path in expected if not path.exists()]
    if missing:
        issues.append("missing build outputs: " + ", ".join(missing))
    return issues
