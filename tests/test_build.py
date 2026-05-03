from __future__ import annotations

from pathlib import Path

from aiwf.render import build
from aiwf.validate import validate
from aiwf.workflows import ARTIFACTS, load_catalog


ROOT = Path(__file__).resolve().parents[1]


def test_build_generates_expected_outputs() -> None:
    layout = build(ROOT)
    catalog = load_catalog(ROOT)

    for workflow in catalog.workflows:
        assert (layout.codex_skills / workflow.name / "SKILL.md").exists()
        assert (layout.opencode_skills / workflow.name / "SKILL.md").exists()
        assert (layout.opencode_commands / f"{workflow.name}.md").exists()
        assert (layout.claude_commands / f"{workflow.name}.md").exists()

    assert (layout.bin_dir / "aiwf-workflow").exists()


def test_validate_after_build_is_clean() -> None:
    build(ROOT)
    assert validate(ROOT) == []


def test_shared_artifact_contract_is_stable() -> None:
    catalog = load_catalog(ROOT)
    assert catalog.workflows
    for workflow in catalog.workflows:
        assert workflow.outputs == ARTIFACTS
