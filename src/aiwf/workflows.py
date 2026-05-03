from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Final

ARTIFACTS: Final[tuple[str, ...]] = (
    "docs/ai/design_concept.md",
    "docs/ai/prd.md",
    "docs/ai/backlog.md",
    "docs/ai/research.md",
    "docs/ai/ubiquitous_language.md",
    "docs/ai/handoff.md",
)


@dataclass(frozen=True)
class Workflow:
    name: str
    title: str
    description: str
    command_description: str
    prompt: str
    outputs: tuple[str, ...]


@dataclass(frozen=True)
class WorkflowCatalog:
    workflows: tuple[Workflow, ...]

    def by_name(self, name: str) -> Workflow:
        for workflow in self.workflows:
            if workflow.name == name:
                return workflow
        raise KeyError(name)


def load_catalog(root: Path) -> WorkflowCatalog:
    skills_dir = root / "skills-src"
    workflows: list[Workflow] = []
    for path in sorted(skills_dir.glob("*.json")):
        payload = json.loads(path.read_text())
        workflows.append(
            Workflow(
                name=payload["name"],
                title=payload["title"],
                description=payload["description"],
                command_description=payload["command_description"],
                prompt=payload["prompt"],
                outputs=tuple(payload.get("outputs", ARTIFACTS)),
            )
        )
    return WorkflowCatalog(workflows=tuple(workflows))
