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

## Codex Support

- Codex discovers skills from `~/.agents/skills/`.
- Install this repo for Codex with `./install.sh --target codex`.
- Codex-specific install notes live in `.codex/INSTALL.md`.
- Codex plugin metadata lives in `.codex-plugin/plugin.json` inside plugin directories.
- Marketplace metadata for local Codex plugin discovery lives in `.agents/plugins/marketplace.json`.

## Claude Support

- Claude Code discovers skills from `~/.claude/skills/`.
- Install this repo for Claude with `./install.sh --target claude` or simply `./install.sh`.
- Claude plugin metadata lives in `.claude-plugin/plugin.json` inside plugin directories.

## Skill Conventions

- Every skill directory must contain `SKILL.md`.
- `SKILL.md` frontmatter must include `name` and `description`.
- The `description` field is the primary trigger mechanism; write it as "Use when..." scenarios.
- Keep large supporting context in `references/`, scripts in `scripts/`, and templates/assets in dedicated folders.
- Avoid hardcoded personal paths in reusable skills. Prefer resolving paths relative to the skill directory.

## Change Conventions

- Read the existing `SKILL.md` before modifying a skill.
- Update README tables when adding or renaming public skills.
- Keep Claude and Codex install docs in sync when changing install behavior.
- Do not remove or rename a skill directory without confirming because it breaks existing symlinks.
- Do not hardcode secrets, API keys, or tokens.
