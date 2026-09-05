# Installing yuanbo-skills for Codex

Use the repository marketplace for plugins and one standalone source per skill.
Do not combine plugin registration with global symlinks for the same skills.

## Existing local checkout

```bash
codex plugin marketplace add /path/to/yuanbo-skills
codex plugin add labmate@yuanbo-skills
codex plugin add meta-audit@yuanbo-skills
codex plugin add paper-review@yuanbo-skills
codex plugin add papermate@yuanbo-skills
codex plugin add unbox-skills@yuanbo-skills
bash /path/to/yuanbo-skills/install.sh --target codex
```

The installer links standalone and bundled project skills, skips plugin-owned
entries by default, and preserves real directories. It can attempt optional
third-party clones; inspect the script when installation scope matters.
An existing personal selfOS checkout should remain the source of its wiki/capture
skills. Preserve those links instead of redirecting them to a bundled data checkout.

For a fresh clone, initialize the needed submodules. The bundled selfOS submodule
uses a private repository and requires access; that is not required to use the
standalone skills or other plugins.

## Updating and migrating old installs

Update Git sources without discarding dirty work, then rerun the supported plugin
install command for each changed plugin. A configured Git marketplace can first
be refreshed with `codex plugin marketplace upgrade yuanbo-skills`; a local
marketplace reads its updated checkout.

Before removing old registrations, inspect installed/enabled state and actual
link targets. Back up real directories, link targets and registry metadata.
Install and verify replacement plugins first. The managed cleanup is:

```bash
bash /path/to/yuanbo-skills/install.sh --target codex --prune-plugin-skill-links
```

Prune applies to all plugin-skill links into that exact checkout. It does not
remove real directories or links into other checkouts. The installer also
refreshes standalone links, including bundled selfOS entries; preserve or restore
a verified live selfOS source when that is the intended destination.
Old real `web-fetcher` and `paper-style` directories require separate review and
recoverable backup before replacement.

Use `--include-plugin-skills` only for a legacy host without plugin support.
Do not install both modes. Keep unrelated vendors and broken legacy links outside
a migration unless explicitly selected.

## Verification

```bash
codex plugin list --marketplace yuanbo-skills --json
python3 scripts/validate_skills.py
bash tests/test-capability-refactor.sh
```

Installed/enabled registry state is not proof of actual model execution or hook
trust. Start a new task/session after reinstalling and review changed hooks in
the host's supported interface. Check that namespaced plugin skills appear once
and standalone links point to the intended source. SelfOS and the standalone
collection both have a transcribe entry: select one global source, not two copies.

See [platform support](guides/codex-support.md) and
[the migration inventory](reviews/2026-09-05-installation-migration.md).
