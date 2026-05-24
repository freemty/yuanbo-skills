# yuanbo-skills

This repository is a monorepo of personal agent skills, plugins, and projects.

## Repository Structure

```
skills/          Single-skill directories
plugins/         Multi-skill plugins; may include nested skills, agents, hooks
projects/        Standalone projects
docs/            Plugin notes, knowhow, conventions
scripts/         Build and validation scripts
```

## Platform Support

This repo supports three AI agent platforms from the same SKILL.md sources (Agent Skills open standard):

| Platform | Skill directory | Install command |
|----------|-----------------|-----------------|
| Claude Code | `~/.claude/skills/` | `./install.sh --target claude` (default) |
| OpenAI Codex | `~/.agents/skills/` | `./install.sh --target codex` |
| Google Antigravity | `~/.gemini/antigravity/skills/` | `./install.sh --target antigravity` |
| All three | all directories | `./install.sh --target all` |

### Codex

- Codex discovers skills from `~/.agents/skills/`.
- Install notes live in `.codex/INSTALL.md`.
- Plugin metadata lives in `.codex-plugin/plugin.json` inside plugin directories.
- Marketplace metadata lives in `.agents/plugins/marketplace.json`.

### Google Antigravity

- Antigravity discovers skills from `~/.gemini/antigravity/skills/` (global) or `.agents/skills/` (workspace).
- Install notes live in `.antigravity/INSTALL.md`.
- Plugin metadata reuses `.codex-plugin/plugin.json` (same format).
- Workspace-level `.agents/skills/` is shared with Codex — same path, same format.

### Claude Code

- Claude Code discovers skills from `~/.claude/skills/`.
- Install with `./install.sh --target claude` or simply `./install.sh`.
- Plugin metadata lives in `.claude-plugin/plugin.json` inside plugin directories.

## Skill Conventions

- Every skill directory must contain `SKILL.md`.
- `SKILL.md` frontmatter must include `name` and `description`.
- The `description` field is the primary trigger mechanism; write it as "Use when..." scenarios.
- Keep large supporting context in `references/`, scripts in `scripts/`, and templates/assets in dedicated folders.
- Avoid hardcoded personal paths in reusable skills. Prefer resolving paths relative to the skill directory.

## Change Conventions

- Read the existing `SKILL.md` before modifying a skill.
- Update README tables when adding or renaming public skills.
- Keep Claude, Codex, and Antigravity install docs in sync when changing install behavior.
- Do not remove or rename a skill directory without confirming because it breaks existing symlinks.
- Do not hardcode secrets, API keys, or tokens.
