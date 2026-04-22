# skills.sh Publishing Guide

Rules and templates for publishing skills to [skills.sh](https://skills.sh/).

## Eligibility Checklist

Before publishing, a skill must pass both gates:

1. **Universal demand** — solves a problem most CC users have, not just a personal workflow
2. **Self-contained** — works without the publisher's private infra (personal CLIs, output paths, cross-skill hard deps)

## Repo Structure

Each skill published to skills.sh is its own GitHub repo. `npx skills add <owner>/<repo>` clones the repo root into `~/.claude/skills/<name>/`, so SKILL.md must be at root.

```
<skill-name>/                  # = GitHub repo name
├── SKILL.md                   # REQUIRED — skill definition (frontmatter + body)
├── README.md                  # REQUIRED — human-facing, follows template below
├── LICENSE                    # REQUIRED — MIT unless otherwise needed
├── CHANGELOG.md               # optional
├── references/                # optional — context docs loaded on demand
├── scripts/                   # optional — executable helpers
├── templates/                 # optional — assets copied into user projects
├── guides/                    # optional — subcommand deep dives
├── examples/                  # optional — sample outputs, previews
└── assets/                    # optional — icons, fonts, static files
```

## SKILL.md

### Frontmatter

Only two required fields:

```yaml
---
name: skill-name
description: >
  Use when <trigger scenario 1>, <trigger scenario 2>, or <trigger scenario 3>.
  Triggers: /skill-name, keyword1, keyword2.
---
```

Rules:
- `name`: lowercase, hyphens only, matches repo name
- `description`: **English**. CSO format — describe *when* to use, not *what* it does. Start with "Use when..."
- `allowed-tools`: optional, only if the skill needs to restrict tool access
- No other frontmatter fields needed for skills.sh

### Body

- English as primary language (Chinese annotations OK for bilingual skills)
- Keep under ~500 lines — offload detail to `references/` or `guides/`
- Progressive disclosure: SKILL.md body → references/ → scripts/
- No hardcoded personal paths (`~/my-output/`, `~/.claude/skills/other-skill/`)
- No hard dependencies on other skills — recommendations are fine, requirements are not
- If referencing other skills, use conditional language: "If you have X installed, you can..."

## README.md Template

```markdown
# skill-name

One-line hook — what this skill does for you.

A [Claude Code](https://claude.ai/claude-code) skill that [value proposition].

## When to Use

- Scenario 1
- Scenario 2
- Scenario 3

## Usage

\```
/skill-name                    # basic invocation
/skill-name --flag             # variant
\```

## How it works

[Brief description of the workflow/pipeline — 3-5 bullet points or a numbered list]

## Install

### Via skills.sh (recommended)

\```bash
npx skills add freemty/skill-name
\```

Works with Claude Code, Cursor, Codex, Windsurf, and [15+ other agents](https://skills.sh).

### Manual

\```bash
git clone https://github.com/freemty/skill-name.git ~/.claude/skills/skill-name
\```

## License

MIT
```

### README Rules

1. **Title** — `# skill-name` (matches repo)
2. **One-liner** — evocative, not generic
3. **When to Use** — bullet list of trigger scenarios
4. **Usage** — slash command examples with brief comments
5. **How it works** — optional but recommended for complex skills
6. **Install** — MUST include both `npx skills add` and manual `git clone`
7. **License** — at the bottom
8. Optional sections: Preview, Sources, Prerequisites, More from freemty

### Language

- README body: **English** (skills.sh is a global platform)
- Trigger keywords in description can include Chinese if the skill is bilingual
- SKILL.md body: English preferred, Chinese annotations OK for bilingual skills

## Standardization Checklist

When converting an existing skill for skills.sh publishing:

- [ ] SKILL.md is at repo root (not nested in `skills/<name>/`)
- [ ] `name` in frontmatter matches repo name, lowercase-hyphen only
- [ ] `description` is English, CSO format, starts with "Use when..."
- [ ] No hardcoded personal paths in SKILL.md
- [ ] No hard cross-skill dependencies (soft recommendations OK)
- [ ] SKILL.md body under ~500 lines
- [ ] README.md follows the template above
- [ ] README has `npx skills add freemty/<name>` install block
- [ ] README has manual `git clone` fallback
- [ ] LICENSE file exists (MIT)
- [ ] All references/scripts/templates use relative paths within the skill
- [ ] Chinese-only content translated to English (or made bilingual)
- [ ] Tested: `npx skills add freemty/<name>` installs correctly

## Published Skills

All published on 2026-04-22. Install via `npx skills add freemty/<name>`.

| Skill | Repo | What was done |
|-------|------|--------------|
| paper-storyteller | `freemty/paper-storyteller` | README rewrite, LICENSE added |
| paper-style | `freemty/paper-style` | Install header unified, LICENSE added |
| beamer-style | `freemty/beamer-style` | README rewrite, sister-skill ref softened, LICENSE added |
| writing-agents | `freemty/writing-agents` | New repo created, README + LICENSE added |
| cc-navigator | `freemty/cc-navigator` | Repo flattened (SKILL.md to root), README rewrite, Chinese tags → English |
| meta-audit | `freemty/meta-audit` | Full English translation, repo flattened, personal paths removed |

### Not yet published

| Skill | Repo | Remaining work |
|-------|------|---------------|
| paper-review | `freemty/paper-review` | Already on skills.sh; remove `labmate:domain-expert` hard ref |
| review-review | (part of paper-review) | Ships with paper-review plugin |
