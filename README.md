# AI Workflow Skills

Cross-agent workflow skills for Codex, OpenCode, and Claude Code.

Some skills in this repo are general-purpose thinking and planning tools, and some are specifically part of the AI coding workflow. In particular, `grill-me` and `ubiquitous-language` are general skills that the coding workflow reuses.

## What ships

- Canonical workflow definitions under `skills-src/`
- Generated Agent Skills for Codex and OpenCode under `dist/`
- Generated GitHub Copilot prompt files under `dist/`
- Generated slash commands for OpenCode and Claude Code under `dist/`
- `aiwf` CLI for build, validation, install, and environment checks

## Workflows

- `grill-me`
- `research`
- `write-prd`
- `slice-planner`
- `ralph-loop`
- `ubiquitous-language`
- `improve-architecture`
- `review-security`
- `review-reliability`
- `review-ux-consistency`
- `review-architecture`
- `review-test-quality`
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
- GitHub Copilot: prompt files under `.github/prompts/` in a target repository
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
