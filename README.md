# yuanbo-skills

Personal Claude Code skills collection by yuanbo.

## Install

```bash
git clone --recurse-submodules https://github.com/freemty/yuanbo-skills ~/code/projects/ybskills
cd ~/code/projects/ybskills
./install.sh
```

## My Skills

### Writing & Style

| Skill | Description |
|-------|-------------|
| [yuanboizer-zh](yuanboizer-zh/) | Personal style polisher — rewrites compressed drafts to sound like Yuanbo |
| [flipradio-write-skill](flipradio-write-skill/) | FlipRadio critical style: guided writing + polish (two skills in one) |
| [paper-storyteller](paper-storyteller/) | Narrative-driven academic paper writing (Wu/Efros/Liu/Freeman/Isola style) |
| [writing-agents](writing-agents/) | Guide for authoring custom Claude Code agent markdown files |

### Research & Knowledge

| Skill | Description |
|-------|-------------|
| [unbox-skills](unbox-skills/) | Researcher deep profiling — personality, early career, mentorship lineage, direction evolution. Includes unbox, unbox-graph, unbox-to-wiki |
| [selfos](selfos/) | Personal knowledge base — ingest, compile, query wiki, context recovery *(private)* |
| [no-more-fomo](no-more-fomo/) | AI daily digest from Twitter KOLs, lab blogs, podcasts, arxiv, HackerNews |

### Academic Visual Identity

| Skill | Description |
|-------|-------------|
| [paper-style](paper-style/) | Paper color theme system — 5 themes for figures, tables, diagrams |
| [beamer-style](beamer-style/) | Beamer slide theme system — shares the same 5-theme color system |

### Productivity

| Skill | Description |
|-------|-------------|
| [weekly-report](weekly-report/) | Weekly progress report for managers |
| [web-fetcher](web-fetcher/) | Unified URL fetcher — auto-routes Twitter/YouTube/Bilibili/小红书/GitHub etc. |
| [cc-navigator](cc-navigator/) | Claude Code workflow navigator — recommends the right skill/agent/tool from 11 sources |
| [meta-audit](meta-audit/) | AI automation maturity audit — L0-L5 scoring, ecosystem benchmarks, Top-3 actions |
| [labmate](labmate/) | Research harness for Claude Code — experiments, papers, knowhow, agents (independent plugin) |

## Third-party Dependencies

Installed automatically by `install.sh`:

| Skill | Source |
|-------|--------|
| notion-lifeos | [jiahao-shao1/openclaw-skill-notion-lifeos](https://github.com/jiahao-shao1/openclaw-skill-notion-lifeos) |
| proactive-agent | [halthelobster/proactive-agent](https://github.com/halthelobster/proactive-agent) |

## Plugins I Use

Managed via Claude Code plugin system, not included in this repo.

| Plugin | What it does |
|--------|-------------|
| superpowers | Brainstorming, TDD, debugging, plans, code review, git worktrees (14 skills) |
| plugin-dev | Plugin/skill/agent/hook development helpers |
| chrome-devtools-mcp | Browser automation via Chrome DevTools Protocol |
| huggingface-skills | HuggingFace papers, datasets, model training, Gradio, transformers.js |

## License

MIT
