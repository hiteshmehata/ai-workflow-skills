from __future__ import annotations

from aiwf.cli import main


def test_list_command(capsys) -> None:
    assert main(["list"]) == 0
    output = capsys.readouterr().out
    assert "grill-me" in output
    assert "harness-engineering" in output


def test_doctor_command(capsys, tmp_path) -> None:
    assert main(["doctor", "--home", str(tmp_path)]) == 0
    output = capsys.readouterr().out
    assert ".codex/skills" in output
    assert ".claude/commands" in output
