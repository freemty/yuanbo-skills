# Installing yuanbo-skills for Codex

Use the Codex plugin marketplace for plugins and global skill links for
standalone skills. Do not install the same plugin both ways.

## Prerequisites

- Git
- OpenAI Codex CLI

## Installation

1. Clone the repository:

   ```bash
   git clone --recurse-submodules https://github.com/freemty/yuanbo-skills.git ~/.codex/yuanbo-skills
   ```

2. Add the checkout as a local plugin marketplace and install the plugins you
   want. For Labmate:

   ```bash
   cd ~/.codex/yuanbo-skills
   codex plugin marketplace add ~/.codex/yuanbo-skills
   codex plugin add labmate@yuanbo-skills
   ```

3. Link standalone skills:

   ```bash
   ./install.sh --target codex
   ```

   By default the installer skips skills owned by a directory with
   `.codex-plugin/plugin.json`. This prevents each plugin skill from appearing
   twice.

4. Restart Codex. Review plugin hooks with `/hooks` before trusting them.

## Existing Installations

If an older checkout linked plugin skills globally, remove only the symlinks
managed by this repository:

```bash
./install.sh --target codex --prune-plugin-skill-links
```

This operation never removes real directories or standalone skill links.
Restart Codex afterward.

## Legacy Codex Without Plugin Support

If your Codex build cannot install local plugins, use global skill links
instead:

```bash
./install.sh --target codex --include-plugin-skills
```

Do not also install the corresponding Codex plugin. This legacy mode supplies
skills only; plugin hooks and metadata are unavailable.

## Install a Single Standalone Skill

```bash
git clone --recurse-submodules https://github.com/freemty/yuanbo-skills.git ~/.codex/yuanbo-skills
mkdir -p ~/.agents/skills
ln -sf ~/.codex/yuanbo-skills/skills/web-fetcher ~/.agents/skills/web-fetcher
ln -sf ~/.codex/yuanbo-skills/skills/paper-style ~/.agents/skills/paper-style
```

## Local Plugin Marketplace

The marketplace index is `.agents/plugins/marketplace.json`. These plugins have
Codex manifests:

- `plugins/labmate/.codex-plugin/plugin.json`
- `plugins/meta-audit/.codex-plugin/plugin.json`
- `plugins/paper-review/.codex-plugin/plugin.json`
- `plugins/papermate/.codex-plugin/plugin.json`
- `plugins/unbox-skills/.codex-plugin/plugin.json`

## Hooks Compatibility

The labmate and papermate Codex plugin manifests point to standalone `hooks/hooks.json` files. Hook scripts are best-effort: they run when the host supports local plugin hooks and degrade silently when optional shell dependencies such as `jq`, `gh`, or project files are unavailable.

## Third-Party Skills

`install.sh` also attempts to install these optional third-party skills into `~/.agents/skills/`:

- `notion-lifeos`
- `proactive-agent`

If a network clone fails, the installer reports a warning and keeps the local yuanbo skills installed.

## Verify

```bash
codex plugin list
ls -la ~/.agents/skills/
```

Plugin-owned skills should come from `codex plugin list`; standalone skills
should have symlinks under `~/.agents/skills/`.

## Updating

```bash
cd ~/.codex/yuanbo-skills
git pull --recurse-submodules
codex plugin marketplace upgrade yuanbo-skills
codex plugin add labmate@yuanbo-skills
./install.sh --target codex
```

Restart Codex and review changed hook hashes.

## Uninstalling

Remove this repository's plugin-skill links:

```bash
./install.sh --target codex --prune-plugin-skill-links
```

Use `codex plugin` commands to uninstall plugins. Remove standalone symlinks
individually if you no longer want them.
