# yuanbo-skills

Personal Claude Code skills collection by yuanbo.

## Install

```bash
git clone https://github.com/freemty/yuanbo-skills ~/code/projects/ybskills
cd ~/code/projects/ybskills
./install.sh
```

## My Skills

| Skill | Description |
|-------|-------------|
| paper-storyteller | Narrative-driven academic paper writing (Wu/Efros/Liu/Freeman/Isola style) |
| no-more-fomo | AI daily digest from Twitter, labs, podcasts |
| writing-agents | Guide for authoring custom Claude Code agents |
| [cc-navigator](https://github.com/freemty/cc-navigator) | CC workflow navigator — skill/agent/tool recommendation (independent repo) |
| flipradio-write | Guided writing in FlipRadio critical public intellectual style |
| flipradio-polish | Polish articles against FlipRadio 10-dimension style framework |
| web-fetcher | Unified URL fetcher — auto-routes Twitter/YouTube/Bilibili/小红书/GitHub/知乎/Reddit/微博 to best tool, fallback to Jina Reader |
| unbox | Researcher deep profiling — personality, early career, mentorship lineage, direction evolution, deleted content |
| unbox-cross-ref | Cross-reference unbox reports — backfill missing info, resolve factual conflicts across all profiles |
| meta-audit | AI automation maturity audit — L0-L5 scoring, ecosystem benchmarks, Top-3 actions |
| yuanboizer-zh | Personal style polisher — rewrites compressed drafts to sound like Yuanbo |

## Third-party References

Plugins and skill collections I use alongside my own. These are installed via their own systems, not included in this repo.

### Plugins (managed via Claude Code plugin system)

| Plugin | Skills | Author | Source |
|--------|--------|--------|--------|
| superpowers | 14 skills: brainstorming, TDD, debugging, writing-plans, executing-plans, code review, git worktrees, etc. | claude-plugins-official | Installed via Claude Code plugin system |
| everything-claude-code | 28 skills: coding-standards, python/golang/django/springboot patterns, security-review, eval-harness, etc. | Last Strike | Installed via Claude Code plugin system |
| labmate | 5 agents: domain-expert, exp-manager, project-advisor, slides-maker, viz-frontend + 13 hooks | labmate-marketplace | Installed via Claude Code plugin system |

### Skill Collections (installed manually)

| Collection | Description | Author | Source |
|------------|-------------|--------|--------|
| sjh-skills | Research workflow skills (scholar-agent, research-paper-writing, fars-system, hle-solver, etc.) | jiahao-shao1 (嘉豪) | [jiahao-shao1/sjh-skills](https://github.com/jiahao-shao1/sjh-skills) |
| baoyu-skills | Content generation skills (humanizer, Humanizer-zh, notebooklm, nano-banana, etc.) | JimLiu (宝玉) | [JimLiu/baoyu-skills](https://github.com/JimLiu/baoyu-skills) |
| ljg-skills | Learning & writing skills | lijigang | [lijigang/ljg-skills](https://github.com/lijigang/ljg-skills) |

### Individual Skills (installed via find-skills / manual)

| Skill | Description | Source |
|-------|-------------|--------|
| find-skills | Skill discovery and installation | [nicepkg/claude-code-skill](https://github.com/nicepkg/claude-code-skill) |
| notion-lifeos | Notion LifeOS PARA system integration | [jiahao-shao1/openclaw-skill-notion-lifeos](https://github.com/jiahao-shao1/openclaw-skill-notion-lifeos) |
| agent-reach | Multi-platform internet access tools | [nicepkg/claude-code-skill](https://github.com/nicepkg/claude-code-skill) |

## License

MIT
