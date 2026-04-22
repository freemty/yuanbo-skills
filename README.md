# yuanbo-skills

Personal Claude Code skills collection by yuanbo.

## Install

```bash
git clone --recurse-submodules https://github.com/freemty/yuanbo-skills ~/code/projects/ybskills
cd ~/code/projects/ybskills
./install.sh
```

## Skills

<!-- BEGIN SKILLS -->

### Writing & Style

| Skill | Description |
|-------|-------------|
| [yuanboizer-zh](skills/yuanboizer-zh/) | Personal style polisher — rewrites compressed drafts to sound like Yuanbo |
| [flipradio-write-skill](skills/flipradio-write-skill/) | FlipRadio critical style: guided writing + polish (two skills in one) |
| [paper-storyteller](skills/paper-storyteller/) | Narrative-driven academic paper writing (Wu/Efros/Liu/Freeman/Isola style) |
| [writing-agents](skills/writing-agents/) | Guide for authoring custom Claude Code agent markdown files |

### Research & Knowledge

| Skill | Description |
|-------|-------------|
| [unbox-skills](plugins/unbox-skills/) | Researcher deep profiling — personality, early career, mentorship lineage, direction evolution. Includes unbox, unbox-graph, unbox-to-wiki |
| [selfos](projects/selfos/) | Personal knowledge base — ingest, compile, query wiki, context recovery *(private)* |
| [no-more-fomo](skills/no-more-fomo/) | AI daily digest from Twitter KOLs, lab blogs, podcasts, arxiv, HackerNews |
| [paper-review](skills/paper-review/) | Multi-role academic peer review — 4 expert agents cross-review, outputs venue-ready form fields |

### Academic Visual Identity

| Skill | Description |
|-------|-------------|
| [paper-style](skills/paper-style/) | Paper color theme system — 5 themes for figures, tables, diagrams |
| [beamer-style](skills/beamer-style/) | Beamer slide theme system — shares the same 5-theme color system |

### Productivity

| Skill | Description |
|-------|-------------|
| [weekly-report](skills/weekly-report/) | Weekly progress report for managers |
| [web-fetcher](skills/web-fetcher/) | Unified URL fetcher — auto-routes Twitter/YouTube/Bilibili/小红书/GitHub etc. |
| [cc-navigator](skills/cc-navigator/) | Claude Code workflow navigator — recommends the right skill/agent/tool from 11 sources |
| [meta-audit](plugins/meta-audit/) | AI automation maturity audit — L0-L5 scoring, ecosystem benchmarks, Top-3 actions |
| [labmate](plugins/labmate/) | Research harness for Claude Code — experiments, papers, knowhow, agents (independent plugin) |
<!-- END SKILLS -->

## Repo Structure

```
skills/          Single-skill directories (11)
plugins/         Multi-skill plugins (3)
projects/        Standalone projects (1: selfos)
docs/            Plugin notes, knowhow, conventions
scripts/         Build & validation scripts
```

## Third-party Dependencies

Installed automatically by `install.sh`:

| Skill | Source |
|-------|--------|
| notion-lifeos | [jiahao-shao1/openclaw-skill-notion-lifeos](https://github.com/jiahao-shao1/openclaw-skill-notion-lifeos) |
| proactive-agent | [halthelobster/proactive-agent](https://github.com/halthelobster/proactive-agent) |

## External Plugins

Managed via Claude Code plugin system, not included in this repo.

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
