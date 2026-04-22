---
name: cc-navigator
description: >
  Use when unsure what to do next, starting a new task, feeling stuck or lost,
  needing workflow guidance, or asking "how should I approach this".
---

# CC Navigator

Your Claude Code workflow navigator. Recommends the right skill, agent, or tool for any task — synthesized from 11 authoritative sources including Anthropic's official skills repo, the CC creator's tips, and Anthropic engineers' guides. Core principle: think before you code, verify before you ship.

For deep dives on any source or tool, see the `references/` directory.

## When to Use

- "How should I approach this?" — unsure where to start
- Starting a new feature, bug fix, or refactor session
- Feeling overwhelmed by a large task — need to break it down
- Don't know which skill or agent to reach for
- Between steps — just finished something, what's next?
- Want to learn how CC works under the hood
- Need to find the right tool for web access, testing, or presentation

**When NOT to use:**
- You already know exactly what to do and which skill to invoke
- Mid-execution of a plan (stay in your current skill)

## Decision Framework

### Classify the Task

| Task Type | Signal |
|-----------|--------|
| **New feature** | "add", "implement", "create", "build" |
| **Bug fix** | "fix", "broken", "error", "failing", stack trace |
| **Refactor** | "refactor", "clean up", "reorganize", "migrate" |
| **Debug** | "why", "not working", "hang", "crash", "slow" |
| **Exploration** | "how does", "explain", "what is", "understand" |
| **Review** | "review", "check", "before merge", "PR" |
| **Planning** | "how should I", "approach", "design", "architect" |
| **Writing** | "write", "document", "blog", "slides", "presentation" |
| **Web access** | "fetch", "browse", "scrape", "read this URL" |

### Recommend Workflow

```
START
  +-- Planning/Design needed?
  |     YES -> brainstorming (explore intent)
  |             then writing-plans (create plan)
  |
  +-- Is this a bug/test failure?
  |     YES -> systematic-debugging
  |            + minimal reproduction demo (shrink context, precision skyrockets)
  |
  +-- Is this a new feature/implementation?
  |     YES -> test-driven-development (write test first)
  |
  +-- Are there 2+ independent tasks?
  |     YES -> dispatching-parallel-agents
  |            or subagent-driven-development (same session)
  |
  +-- Need isolation from main branch?
  |     YES -> using-git-worktrees
  |
  +-- Implementation done?
  |     YES -> verification-before-completion
  |            then requesting-code-review
  |
  +-- Ready to merge/ship?
  |     YES -> finishing-a-development-branch
  |
  +-- Received review feedback?
        YES -> receiving-code-review
        NO  -> assess what's blocking and advise
```

## Synthesized Key Principles

### 1. Think Before Code — AI is a Planning Amplifier

- Give AI global context, not isolated small tasks (AReaL)
- Nested plans: big plan -> phases -> sub-tasks with clear I/O and verification (AReaL)
- Brainstorm -> Plan -> Execute -> Verify -> Review — always in this order (Superpowers)
- Start every complex task in plan mode; pour energy into the plan so Claude can 1-shot the implementation (Boris)
- Let one Claude write the plan, another review it as a staff engineer (Boris)
- Use sprint contracts: generator and evaluator negotiate testable success criteria before implementation (Harness Design)
- 74 planning sessions vs 9 coding sessions — planning time exceeding coding time is normal (AReaL)

### 2. Evidence-Driven — Tests are the Contract

- Design verification BEFORE writing code (AReaL)
- TDD is mandatory, not optional: RED -> GREEN -> REFACTOR (Superpowers)
- Minimal reproduction demo for bugs — shrink context, precision skyrockets (AReaL)
- Say "Prove to me this works" and have Claude diff behavior between main and your branch (Boris)
- Challenge Claude: "Grill me on these changes and don't make a PR until I pass your test" (Boris)
- Separate generator from evaluator — self-evaluation bias is real; use external agent to critique (Harness Design)

### 3. Context Hygiene — Protect the Window

- 200K window is not all yours: MCP tools eat ~10-20K, Skill descriptors ~1-5K, system ~2K (Tw93)
- Keep CLAUDE.md short, hard, executable; Anthropic's own is ~2.5K tokens (Tw93)
- Task switch -> /clear; same task new phase -> /compact (Tw93)
- Write Compact Instructions in CLAUDE.md to control what survives compression (Tw93)
- Write HANDOFF.md before ending long sessions so the next Claude can continue (Tw93)
- Offload tasks to subagents to keep main context clean (Boris)
- Use /context to monitor consumption; don't wait for auto-compression (Tw93)

### 4. Skills Engineering — Progressive Disclosure

- Three-level loading: metadata (~100 words, always in context) -> SKILL.md body (<500 lines, on trigger) -> bundled resources (unlimited, on demand) (Official)
- A skill is a folder, not just a markdown file — include scripts, assets, data (Thariq Skills)
- SKILL.md = navigation + core constraints; large references go to supporting files (Tw93, Thariq, Official)
- Description = primary trigger mechanism; be "pushy" — Claude tends to undertrigger (Official)
- Description should include both what it does AND specific contexts for when to use it (Official)
- Gotchas are the highest-signal content in any skill (Thariq Skills)
- High-freq (>1/session) -> auto-invoke; low-freq -> disable-auto-invoke; rare -> remove (Tw93)
- 9 skill categories: Library, Verification, Data, Workflow, Scaffolding, Quality, DevOps, Debug, Maintenance (Thariq Skills)
- If you do something more than once a day, make it a skill (Boris)
- Explain why > heavy MUSTs — LLMs have good theory of mind, reasoning beats rigid rules (Official)
- Eval-driven development: draft -> test with baseline -> human review -> improve -> repeat (Official skill-creator)

### 5. Tool Design — See Like an Agent

- Give agent tools shaped to its abilities, not human-complete APIs (Thariq Agent)
- ~20 tools in CC; bar to add a new one is high — one more option to think about (Thariq Agent)
- Progressive disclosure adds functionality without adding tools (Thariq Agent)
- As models improve, old tools may constrain — revisit assumptions (Thariq Agent: TodoWrite -> Task)
- Claude is increasingly good at building its own context given the right search tools (Thariq Agent)
- Stress-test harness assumptions: as models improve, components become non-load-bearing — simplify (Harness Design)

### 6. Parallel Execution — Scale Smart

- 3-5 git worktrees at once, each running its own Claude — single biggest productivity unlock (Boris)
- Multitasking (different sessions on different tasks) + pass@k (same task, different constraints) (AReaL)
- Know when to STOP parallelizing — shared wrong assumption = waste (AReaL)
- Checkpoints at every boundary — verify before continuing (Superpowers)

### 7. Invest in Your CLAUDE.md

- After every correction: "Update your CLAUDE.md so you don't make that mistake again" (Boris)
- Claude is eerily good at writing rules for itself (Boris)
- Ruthlessly edit over time — keep iterating (Boris)
- Use .claude/rules/ for path/language rules; don't make root CLAUDE.md carry all differences (Tw93)
- Layered config: CLAUDE.md as slim router + rules/ + agents/ + skills/ + commands/ (AReaL)

### 8. Hooks as Automation Backbone

- Four types: command, http, prompt, agent — choose by complexity (Official Hooks)
- 19 lifecycle events cover the full agent loop (Official Hooks)
- Use prompt hooks for AI judgment, agent hooks for codebase verification (Official Hooks)
- Skills can register session-scoped hooks: /careful blocks destructive commands, /freeze scopes edits (Thariq Skills)
- RTK pattern: filter tool output before it reaches Claude, keep only decision-relevant info (Tw93)

## Ecosystem Quick Reference

For detailed setup, usage, and decision guides, read the corresponding file in `references/`.

### Web Access & Network (references/ecosystem-web-access.md)

| Tool | Invoke | Use When |
|------|--------|----------|
| `/web-fetcher` | **已有** | 5-tier fallback: Jina → defuddle → markdown.new → OpenCLI → raw HTML |
| `/agent-reach` | **已有** (gstack) | Multi-platform access (Twitter, YouTube, Reddit, XHS...) |
| `/browse` | **已有** (gstack) | Browser automation with Playwright |
| Jina Reader | 内置于 web-fetcher | Quick webpage -> markdown (`r.jina.ai/URL`) |
| markdown-proxy | 需安装 | Login-required pages (X/Twitter, WeChat) |

### Remote Execution (references/jiahao-shao1-skills.md)

| Tool | Invoke | Use When |
|------|--------|----------|
| remote-cluster-agent | 需安装 | CC operates remote GPU clusters via MCP (~0.1s latency) |

### SWE Workflow (references/ecosystem-workflow.md)

| Framework | Invoke | Use When |
|-----------|--------|----------|
| Superpowers | **已有** (plugin) | TDD-first, atomic task decomposition, structured process |
| gstack | **已有** (plugin) | Full lifecycle: plan -> design -> ship -> QA -> retro |
| `/labmate` | **已有** | Research/experiment workflows |

### Information Presentation (references/ecosystem-presentation.md)

| Tool | Invoke | Use When |
|------|--------|----------|
| `/beamer-style` | **已有** | Slide decks, Beamer presentations |
| `/design-html` | **已有** (gstack) | Web UI, landing pages, dashboards |
| frontend-slides | 需安装 | PPT-format slide decks |

## Sources

1. **Superpowers** — https://github.com/obra/superpowers
2. **AReaL** — https://zhuanlan.zhihu.com/p/2003269671630165191
3. **CC Official: How It Works** — https://code.claude.com/docs/how-claude-code-works
4. **CC Official: Hooks** — https://code.claude.com/docs/hooks-guide
5. **Boris Cherny** — https://x.com/bcherny/status/2017742741636321619 (references/boris-cherny-cc-tips.md)
6. **Tw93** — https://x.com/HiTw93/status/2032091246588518683 (references/tw93-cc-architecture.md)
7. **Thariq: Skills** — https://x.com/trq212/status/2033949937936085378 (references/thariq-how-we-use-skills.md)
8. **Thariq: Agent Design** — https://x.com/trq212/status/2027463795355095314 (references/thariq-seeing-like-an-agent.md)
9. **Harness Design** — https://www.anthropic.com/engineering/harness-design-long-running-apps
10. **Anthropic Skills** — https://github.com/anthropics/skills (references/anthropic-skills-official.md)
11. **jiahao-shao1** — https://github.com/jiahao-shao1 (references/jiahao-shao1-skills.md)

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Jumping straight to code without planning | Brainstorm first, even for "simple" tasks — 74% of sessions detour (AReaL) |
| Writing tests after implementation | Tests-after = "what does this do?" Tests-first = "what should this do?" |
| Stuffing everything into CLAUDE.md | Keep it a slim router (<200 lines); use rules/, agents/, skills/ for details |
| Running one agent for everything | Tier models: haiku for execution, sonnet for review, opus for reasoning |
| Ignoring context window limits | MCP tools alone eat 10-20K tokens; delegate heavy output to subagents |
| Skipping verification before claiming done | Always run tests/checks and confirm output before asserting success |
| Skills with vague descriptions | Description = primary trigger; be "pushy" — Claude undertriggers by default (Official) |
| Writing rigid MUSTs instead of reasoning | Explain why it matters — LLMs respond better to reasoning than commands (Official) |
| Not investing in CLAUDE.md | After every correction: "Update your CLAUDE.md so you don't make that mistake again" |
