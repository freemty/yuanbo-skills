# Multi-platform support

One authored skill source serves different hosts. Shared bodies describe
capabilities and evidence contracts; invocation, permissions and plugin formats
remain host-specific. A shared SKILL.md does not imply identical native tools.

| Host | Standalone discovery | Plugin path / invocation |
| --- | --- | --- |
| Claude Code | ~/.claude/skills | Claude marketplace; /plugin-name:skill |
| Codex | ~/.agents/skills | Codex marketplace recommended; $plugin-name:skill or /skills |
| Antigravity / other Agent Skills hosts | Host-supported skill directory / selector | Verify that host's plugin support; do not assume a Codex manifest is compatible |

## Codex

```bash
codex plugin marketplace add /path/to/yuanbo-skills
codex plugin add labmate@yuanbo-skills
bash install.sh --target codex
```

The installer links standalone/bundled skills and skips plugin-owned entries by
default. Install other needed plugins (papermate, paper-review, meta-audit,
unbox-skills) through the same marketplace; do not also register global copies.

Legacy builds without plugins may use `--include-plugin-skills` instead.
Before `--prune-plugin-skill-links`, inventory the actual targets and installed
replacements. Prune applies to all plugin-skill links into the checkout running
the installer, not arbitrary copies or other worktrees. Real directories are
never removed. The September local migration findings and rollback boundaries
are in [installation migration](../reviews/2026-09-05-installation-migration.md).

## Discovery and precedence

`scripts/skill_inventory.py` is shared by format validation, context audit and
installation. Current inventory: 51 public entries, with workspace skills separate.
Standalone skills precede plugin legacy entries, then bundled project entries.
The first same-named directory wins with a warning; this matters for todo and
transcribe. Plugin namespaces and standalone names are not interchangeable.

```bash
python3 scripts/skill_inventory.py
python3 scripts/skill_inventory.py --workspace
```

Claude/Antigravity installer behavior is retained. `--target all` applies the
plugin exclusion only to Codex. Do not install hidden project-skill templates.
A real destination directory is skipped, not overwritten.

## Verify each layer

1. Source: format/reference and behavioral tests.
2. Metadata: manifest/version/policy checks.
3. Installation: enabled plugin registry and actual discovery, not cache presence.
4. Execution: correct source version, available fallback and host-trusted hooks.

```bash
bash tests/test-capability-refactor.sh
bash plugins/labmate/tests/test-codex-plugin-smoke.sh
```

The installer and plugin smoke use temporary HOME/Codex directories. The plugin
smoke requires an available compatible CLI and does not prove actual model
completion or hook trust. Restart/review hooks only during an authorized real
migration. No helper automatically changes global model/reasoning settings.
