# AI Workflow Skills

Cross-agent workflow skills for Codex, OpenCode, and Claude Code.

## What ships

- Canonical workflow definitions under `skills-src/`
- Generated Agent Skills for Codex and OpenCode under `dist/`
- Generated slash commands for OpenCode and Claude Code under `dist/`
- `aiwf` CLI for build, validation, install, and environment checks

## Workflows

- `grill-me`
- `write-prd`
- `slice-planner`
- `ralph-loop`
- `ubiquitous-language`
- `harness-engineering`

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
aiwf build
aiwf validate
aiwf install all --dry-run
```

## Install targets

- Codex: Agent Skills under `~/.codex/skills/`
- OpenCode commands: `~/.config/opencode/commands/`
- OpenCode skills: `~/.config/opencode/skills/`
- Claude Code commands: `~/.claude/commands/`

## Repo artifacts created by the workflows

- `docs/ai/design_concept.md`
- `docs/ai/prd.md`
- `docs/ai/backlog.md`
- `docs/ai/research.md`
- `docs/ai/ubiquitous_language.md`
- `docs/ai/handoff.md`
