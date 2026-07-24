# yuanbo-skills

Personal agent skills collection by yuanbo. Compatible with **Claude Code**, **OpenAI Codex**, and **Google Antigravity**.

## Install

### Claude Code

```bash
git clone --recurse-submodules https://github.com/freemty/yuanbo-skills ~/code/projects/ybskills
cd ~/code/projects/ybskills
./install.sh
```

This links every public skill into `~/.claude/skills/`.

### Codex

Tell Codex:

```text
Fetch and follow instructions from https://raw.githubusercontent.com/freemty/yuanbo-skills/refs/heads/main/.codex/INSTALL.md
```

Or manually:

```bash
git clone --recurse-submodules https://github.com/freemty/yuanbo-skills ~/.codex/yuanbo-skills
cd ~/.codex/yuanbo-skills
codex plugin marketplace add ~/.codex/yuanbo-skills
codex plugin add labmate@yuanbo-skills
./install.sh --target codex
```

Codex plugins are the recommended path for multi-skill packages such as
Labmate. The installer links standalone skills into `~/.agents/skills/` and
skips plugin-owned skills by default, preventing duplicate registration. Older
Codex builds without plugin support can opt into legacy links with
`--include-plugin-skills`.

### Google Antigravity

Tell Antigravity (agy CLI or desktop app):

```text
Fetch and follow instructions from https://raw.githubusercontent.com/freemty/yuanbo-skills/refs/heads/main/.antigravity/INSTALL.md
```

Or manually:

```bash
git clone --recurse-submodules https://github.com/freemty/yuanbo-skills ~/.antigravity/yuanbo-skills
cd ~/.antigravity/yuanbo-skills
./install.sh --target antigravity
```

This links every public skill into `~/.gemini/antigravity/skills/`.

### Installable Skill Keys

All three platforms use the same `SKILL.md`/`skill.md` sources (Agent Skills
open standard). Claude Code and Antigravity link all skills. Codex links
standalone skills and loads plugin-owned skills through its marketplace by
default.

Skill keys:

```text
academic-writing
analyze-experiment
beamer-style
cc-navigator
clone-web
commit-changelog
compile-check
de-ai
digest
figure-qa
flipradio-polish
flipradio-write
hook-recipes
init-project
interview
meta-audit
monitor
new-experiment
no-more-fomo
paper-plot
paper-review
paper-storyteller
paper-style
paper-writing-qa
pre-submit-challenge
read-paper
review-review
research-slides
section-guard
survey-literature
swiss-knife-design
sync-paper
thought
todo
transcribe
unbox
unbox-graph
unbox-to-wiki
update-docs
update-knowhow
update-project-skill
visualize
web-fetcher
weekly-report
wiki
wiki-help
writing-agents
yuanboizer-zh
```

## Skills

<!-- BEGIN SKILLS -->

### Writing & Style

| Skill | Description |
|-------|-------------|
| [yuanboizer-zh](skills/yuanboizer-zh/) | Personal style polisher — rewrites compressed drafts to sound like Yuanbo |
| [flipradio-write-skill](skills/flipradio-write-skill/) | FlipRadio critical style: guided writing + polish (two skills in one) |
| [paper-storyteller](skills/paper-storyteller/) | Narrative-driven academic paper writing (Wu/Efros/Liu/Freeman/Isola style) |
| [writing-agents](skills/writing-agents/) | Guide for authoring custom coding-agent subagent markdown files |

### Research & Knowledge

| Skill | Description |
|-------|-------------|
| [unbox-skills](plugins/unbox-skills/) | Researcher deep profiling — personality, early career, mentorship lineage, direction evolution. Includes unbox, unbox-graph, unbox-to-wiki |
| [selfos](projects/selfos/) | Personal knowledge base — ingest, compile, query wiki, context recovery *(private)* |
| [no-more-fomo](skills/no-more-fomo/) | AI daily digest from Twitter KOLs, lab blogs, podcasts, arxiv, HackerNews |
| [paper-review](plugins/paper-review/) | Multi-role academic peer review — 4 expert agents cross-review, outputs venue-ready form fields. Includes review-review audit |
| [papermate](plugins/papermate/) | Paper writing QA pipeline — section guard, figure QA, compile check, pre-submit challenge |

### Academic Visual Identity

| Skill | Description |
|-------|-------------|
| [paper-style](skills/paper-style/) | Paper color theme system — 5 themes for figures, tables, diagrams |
| [beamer-style](skills/beamer-style/) | Beamer slide theme system — shares the same 5-theme color system |
| [research-slides](skills/research-slides/) | Multi-mode research Beamer workflow — audience-first story, source-native evidence, and rendered QA |

### Productivity

| Skill | Description |
|-------|-------------|
| [weekly-report](skills/weekly-report/) | Weekly progress report for managers |
| [web-fetcher](skills/web-fetcher/) | Unified URL fetcher — auto-routes Twitter/YouTube/Bilibili/小红书/GitHub etc. |
| [cc-navigator](skills/cc-navigator/) | Agent workflow navigator — recommends the right skill, agent, tool, or workflow |
| [meta-audit](plugins/meta-audit/) | AI automation maturity audit — L0-L5 scoring, ecosystem benchmarks, Top-3 actions |
| [labmate](plugins/labmate/) | Research harness for AI coding agents — experiments, papers, knowhow, and project memory |
| [swiss-knife-design](skills/swiss-knife-design/) | Personal web design system — project pages, dashboards, leaderboards, slides with consistent visual identity |
| [transcribe](skills/transcribe/) | Audio transcription — speech-to-text via Whisper for meetings, voice memos, recordings |
| [clone-web](skills/clone-web/) | Local webpage cloning and visual archive workflow |
<!-- END SKILLS -->

## Repo Structure

```
skills/            Single-skill directories (14)
plugins/           Multi-skill plugins (5)
projects/          Standalone projects (1: selfos)
.codex/            Codex install instructions
.antigravity/      Antigravity install instructions
.agents/plugins/   Codex/Antigravity local plugin marketplace metadata
docs/              Plugin notes, knowhow, conventions
scripts/           Build & validation scripts
```

## Third-party Dependencies

Attempted automatically by `install.sh`. If a network clone fails, local skills still install and the dependency is reported as a warning.

| Skill | Source |
|-------|--------|
| notion-lifeos | [jiahao-shao1/openclaw-skill-notion-lifeos](https://github.com/jiahao-shao1/openclaw-skill-notion-lifeos) |
| proactive-agent | [halthelobster/proactive-agent](https://github.com/halthelobster/proactive-agent) |

## External Plugins

Managed via platform-specific plugin systems, not included in this repo.

| Plugin | What it does |
|--------|-------------|
| superpowers | Brainstorming, TDD, debugging, plans, code review, git worktrees (14 skills) |
| plugin-dev | Plugin/skill/agent/hook development helpers |
| chrome-devtools-mcp | Browser automation via Chrome DevTools Protocol |
| huggingface-skills | HuggingFace papers, datasets, model training, Gradio, transformers.js |

## Related

| Repo | Description |
|------|-------------|
| [cc-research-playbook](https://github.com/freemty/cc-research-playbook) | AI Researcher 的 Claude Code 实践指南（组会 slides） |
| [wechat-to-agent](https://github.com/freemty/wechat-to-agent) | 微信聊天记录 → AI Agent 数据平台（MCP Server） |

## License

MIT
