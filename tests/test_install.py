from __future__ import annotations

from pathlib import Path

from aiwf.install import install
from aiwf.render import build


ROOT = Path(__file__).resolve().parents[1]


def test_dry_run_install_reports_expected_targets(tmp_path: Path) -> None:
    build(ROOT)
    actions = install(ROOT, "all", home=tmp_path, dry_run=True)
    assert actions
    destinations = {action.destination for action in actions}
    assert tmp_path / ".codex" / "skills" / "grill-me" in destinations
    assert tmp_path / ".config" / "opencode" / "commands" / "grill-me.md" in destinations
    assert tmp_path / ".claude" / "commands" / "grill-me.md" in destinations


def test_real_install_copies_outputs(tmp_path: Path) -> None:
    build(ROOT)
    install(ROOT, "opencode", home=tmp_path, dry_run=False)
    assert (tmp_path / ".config" / "opencode" / "skills" / "grill-me" / "SKILL.md").exists()
    assert (tmp_path / ".config" / "opencode" / "commands" / "grill-me.md").exists()
