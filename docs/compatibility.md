# Compatibility

This project ships one canonical workflow suite and renders target-specific outputs.

- Codex: Agent Skills under `~/.codex/skills/`
- OpenCode: slash commands under `~/.config/opencode/commands/` and skills under `~/.config/opencode/skills/`
- Claude Code: slash commands under `~/.claude/commands/`

Codex support remains skill-based in v1. The generated `dist/bin/aiwf-workflow` helper prints canonical workflow prompts for command-like launch outside Codex chat.
