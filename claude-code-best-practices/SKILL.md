---
name: claude-code-best-practices
description: >
  Use when unsure what to do next, starting a new task, needing workflow guidance,
  or asking "how should I approach this". Recommends optimal skill, agent, or
  workflow based on task type and current situation.
---

# Claude Code Best Practices

## Overview

This skill analyzes your current task type and recommends the optimal workflow, skill, or agent to use. It serves as a decision router backed by synthesized principles from 8 curated sources including the Superpowers framework, AReaL, official Anthropic engineering guides, and Manus. Core principle: think before you code, verify before you ship.

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
| **Multi-file change** | "migrate", "rename across", "unify interface" |

### Recommend Workflow

Based on task type, follow this decision tree:

```
START
  |
  +-- Planning/Design needed?
  |     YES -> /superpowers:brainstorming (explore intent)
  |             then /superpowers:writing-plans (create plan)
  |     NO  -> continue
  |
  +-- Is this a bug/test failure?
  |     YES -> /superpowers:systematic-debugging
  |            + provide minimal reproduction demo (shrink context, precision skyrockets)
  |     NO  -> continue
  |
  +-- Is this a new feature/implementation?
  |     YES -> /superpowers:test-driven-development (write test first)
  |            then implement
  |     NO  -> continue
  |
  +-- Are there 2+ independent tasks?
  |     YES -> /superpowers:dispatching-parallel-agents
  |            or /superpowers:subagent-driven-development (same session)
  |     NO  -> continue
  |
  +-- Need isolation from main branch?
  |     YES -> /superpowers:using-git-worktrees
  |     NO  -> continue
  |
  +-- Implementation done?
  |     YES -> /superpowers:verification-before-completion
  |            then /superpowers:requesting-code-review
  |     NO  -> continue
  |
  +-- Ready to merge/ship?
  |     YES -> /superpowers:finishing-a-development-branch
  |     NO  -> continue
  |
  +-- Received review feedback?
        YES -> /superpowers:receiving-code-review
        NO  -> assess what's blocking and advise
```

## Skills Quick Reference

### Workflow and Process

| Skill | When to Use |
|-------|-------------|
| `superpowers:brainstorming` | Before any creative work -- explore intent, requirements, design |
| `superpowers:writing-plans` | Have spec/requirements, need structured implementation plan |
| `superpowers:executing-plans` | Have a plan, need to execute across sessions with review checkpoints |
| `superpowers:test-driven-development` | Before writing implementation code -- RED/GREEN/REFACTOR |
| `superpowers:systematic-debugging` | Bug, test failure, or unexpected behavior |
| `superpowers:dispatching-parallel-agents` | 2+ independent tasks that can run concurrently |
| `superpowers:subagent-driven-development` | Execute independent tasks within current session |
| `superpowers:verification-before-completion` | About to claim work is done -- verify first |
| `superpowers:requesting-code-review` | After completing a task, before merge |
| `superpowers:receiving-code-review` | After getting review feedback, need to address comments |
| `superpowers:using-git-worktrees` | Need isolated development environment for parallel work |
| `superpowers:finishing-a-development-branch` | Ready to merge/ship a completed branch |
| `superpowers:writing-skills` | Creating or editing Claude Code skills |

### Content and Presentation

| Skill | When to Use |
|-------|-------------|
| `frontend-design` (anthropics/skills) | Web UI, landing pages, dashboards, frontend design |

### Utilities

| Skill | When to Use |
|-------|-------------|
| `find-skills` (vercel-labs/skills) | Discover and install community skills |
| `claude-api` (anthropics/skills) | Building applications with the Claude API |

---

## Best Practices Knowledge Base

### Source 1: Superpowers Framework
> https://github.com/obra/superpowers
> Core: Think before you code, decompose tasks to atomic size (2-5 min), subagent-driven development, mandatory TDD

- **Seven-stage closed loop**: design refinement -> environment setup -> task decomposition -> autonomous execution -> test-first -> quality gate -> completion handling
- **Task atomization**: break complex work into 2-5 minute atomic tasks, each with precise execution specs and acceptance criteria
- **Mandatory TDD**: test-driven development is not optional -- full RED-GREEN-REFACTOR cycle
- **Two-stage verification**: every subtask passes two review stages to ensure quality gating
- **Isolated workspaces**: git worktree creates independent dev environments for parallel work without interference
- **Systematic over intuitive**: ordered, repeatable processes over ad-hoc decisions
- **Simplicity as design goal**: keep designs concise, avoid over-engineering

### Source 2: Vibe Coding AReaL (Starcat)
> https://zhuanlan.zhihu.com/p/2003269671630165191
> https://github.com/inclusionAI/AReaL
> Core: 32 days of zero-handwritten distributed RL framework development, 178 sessions with only 26% fully completed

- **AI is a planning amplifier, not a coding replacement**: 74 planning sessions vs only 9 from-scratch coding sessions; Read 25,000 times >> Edit 14,000 times
- **Layered config architecture**: CLAUDE.md as slim router + rules/ (auto-activated by path) + agents/ (domain experts) + skills/ (workflow templates) + commands/ (automation)
- **Evidence-driven**: design verification before writing code; tests are the contract between you and AI
- **Minimal reproduction demo**: when debugging, distill a minimal repro script first -- shrinking context dramatically improves AI root-cause accuracy
- **Specialized agent division**: dedicated expert agents per domain (FSDP/Archon/Megatron/RL algorithm/cluster scheduling), tiered models (haiku for execution / sonnet for review / opus for reasoning)
- **Agent read-only principle**: expert agents have no Write/Edit permissions -- advisors only, code changes stay with the main agent
- **Dynamic code review**: /pr-review auto-assembles expert teams based on PR content, assigns different-capability models by risk level for parallel review
- **Nested planning**: big plan -> phases -> sub-plans, context controlled at each layer; batch read, batch write
- **Multi-session parallelism**: multitasking (different tasks boost throughput) + pass@k (same task with different constraints, pick best); 402 parallel events
- **74% detours are normal**: zero-handwritten does not mean zero-friction; encode preferences into rules, set checkpoints at every step

### Source 3: Claude Code Official -- How It Works
> https://code.claude.com/docs/how-claude-code-works

- **Agentic loop three stages**: gather context -> take action -> verify results, iterating until complete
- **Dual-engine architecture**: reasoning model (Claude handles logic) + tool system (executes operations) working in concert
- **Dynamic context management**: auto-compress old tool outputs and conversation summaries, prioritize user requests and key code
- **Session continuity**: `--continue` resumes original session, `--fork-session` creates new session preserving history
- **Checkpoint rollback**: all file edits can be rolled back via checkpoints (independent of Git)
- **Extension layered architecture**: Skills (on-demand loading) -> Subagents (independent context) -> MCP (external connections) -> Hooks (automation)
- **Memory system**: CLAUDE.md first 200 lines loaded every session, auto-memory saves pattern recognition across sessions
- **Conversational interaction**: supports real-time interruption and course correction; giving verification tools (tests, screenshots) improves outcomes

### Source 4: Claude Code Official -- Hooks Guide
> https://code.claude.com/docs/hooks-guide

- **Four hook types**: command (shell), http (POST endpoint), prompt (single-turn LLM evaluation), agent (multi-turn verification)
- **19 lifecycle events**: SessionStart -> UserPromptSubmit -> PreToolUse -> PostToolUse -> SessionEnd and more, full coverage
- **Matcher filtering**: regex for precise trigger control (tool name, session source, notification type)
- **Decision control**: allow/deny/ask -- three permission decisions via structured JSON with permissionDecision + additionalContext
- **Three-layer config scope**: user global -> project-level -> local project, multi-level stacking
- **Prompt hooks**: for scenarios needing AI judgment, model returns ok/reason decision, defaults to Haiku
- **Agent hooks**: for codebase state checks, spawns subagent for multi-turn tool-call verification (default 60s timeout, max 50 turns)
- **Common patterns**: desktop notifications, auto-formatting, sensitive file protection, post-compact context re-injection, config change auditing

### Source 5: Anthropic -- Effective Context Engineering
> https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
> Core: Context quality over quantity -- find the "minimal high-signal token set"

- **Quality > quantity**: the goal is the minimal high-signal token set, not piling on information
- **System prompt balance**: avoid brittle hard-coded conditional logic; be explicit enough to guide yet flexible enough to adapt
- **Incremental iteration**: start with a minimal system prompt, add clarity based on failure modes
- **Tool design -- remove redundancy**: minimize functional overlap, each tool has a clear independent purpose
- **Self-documenting tool parameters**: "engineer clarity test" -- if a human engineer can't determine the right choice, the agent won't do better
- **Curated examples over exhaustive lists**: diverse, well-formed examples convey expected behavior; examples are the most powerful LLM communication
- **Just-in-time retrieval**: use lightweight identifiers (file paths, URLs) for dynamic fetching, not pre-loading all data
- **Conversation history compression**: summarize history near context limits, retain architectural decisions, discard redundant output
- **Structured notes system**: maintain persistent external memory files (e.g., NOTES.md) to track long-term task progress
- **Finite attention budget**: performance degrades gradually (not cliff-edge) with context growth; diminishing marginal returns exist
- **Subagent divide-and-conquer**: specialized agents each maintain clean context, return only 1000-2000 token summaries
- **Match strategy to task**: session continuity uses compression, iterative dev uses notes, parallel exploration uses multi-agent

### Source 6: Anthropic -- Demystifying Evals for AI Agents
> https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents
> Core: Evals are the infrastructure foundation for agent quality

- **Three eval types**: single-turn (prompt -> response), multi-turn (interactive state changes), agentic (multi-step tool calls)
- **Code graders first**: string matching, binary tests, result verification -- fast, cheap, reproducible
- **Hybrid grading strategy**: deterministic graders (unit tests) + LLM quality scoring
- **Start from small samples**: 20-50 real failure cases; ensure two experts can agree on pass/fail
- **Pass@k vs Pass^k**: pass@k measures discovery potential (at least 1 success), pass^k measures consistency (all succeed)
- **Isolated test environments**: each trial maintains clean state, prevents state leakage
- **Outcome-based scoring**: do not penalize effective alternative paths
- **Detect eval saturation**: 100% pass rate = eval is broken, add more challenging cases
- **Treat evals like unit tests**: establish ownership, update regularly as the agent evolves

### Source 7: Manus -- Context Engineering for AI Agents
> https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus
> Core: Good AI agents need context engineering, not just prompt engineering

- **KV cache hit rate is the #1 metric**: cache saves 10x cost ($0.30 vs $3 per million tokens)
- **Stable prompt prefix**: avoid timestamps and dynamic content that invalidate KV cache
- **Append-only context structure**: ensure serialization determinism, prevent silent cache invalidation
- **Logit masking over dynamic tool modification**: don't add/remove tool definitions mid-execution, use token masking to control available actions
- **File system as extended memory**: 128K window is not enough -- store large observations in external files
- **Reversible compression**: keep URLs and file paths so information can be recovered, not permanently lost
- **Control attention via restatement**: agent periodically rewrites task summary at context end to prevent goal drift
- **Retain failed attempts**: error attempts implicitly update model beliefs, reducing repeated mistakes
- **Introduce controlled variability**: avoid same few-shot examples causing pattern lock-in
- **Context-first over fine-tuning**: prioritize context engineering for fast iteration

### Source 8: Community Resources
> Claude Code & Codex best practices collection

- **Skills.sh**: https://skills.sh/ -- discover and install community skills for Claude Code
- **OpenClaw Setup**: https://github.com/jiahao-shao1/openclaw-setup -- configuration and commonly-used skills integration
- **Happy**: https://github.com/slopus/happy -- mobile/web client for Codex and Claude Code

---

## Synthesized Key Principles

### 1. Think Before Code -- AI is a Planning Amplifier
- Give AI global context, not isolated small tasks (AReaL)
- Nested plans: big plan -> phases -> sub-tasks with clear I/O and verification (AReaL)
- Brainstorm -> Plan -> Execute -> Verify -> Review -- always in this order (Superpowers)
- Batch read, batch write -- keep context clean per step (AReaL)
- 74 planning sessions vs 9 coding sessions -- planning time far exceeding coding time is normal (AReaL)

### 2. Evidence-Driven -- Tests are the Contract
- Design verification BEFORE writing code (AReaL)
- TDD is mandatory, not optional: RED -> GREEN -> REFACTOR (Superpowers)
- Minimal reproduction demo for bugs -- shrink context, precision skyrockets (AReaL)
- Multi-layer verification: pre-commit -> domain review -> regression tests (AReaL)
- Start from 20-50 real failure cases, not hundreds -- small evals, iterate fast (Anthropic Evals)
- Pass@k for potential, Pass^k for consistency -- know which metric you need (Anthropic Evals)

### 3. Context Engineering -- Quality Over Quantity
- Find the "minimal high-signal token set" -- not more info, better info (Anthropic CE)
- KV cache hit rate is the #1 production metric for agents (Manus)
- Stable prompt prefix + append-only structure to preserve cache (Manus)
- Incremental system prompts: start minimal, add clarity per failure mode (Anthropic CE)
- File system as extended memory -- 128K is not enough for long tasks (Manus)
- Reversible compression: keep URLs/paths so info can be recovered (Manus)
- Periodic task summary restatement at context end to prevent goal drift (Manus)

### 4. Agent Architecture -- Isolate and Specialize
- Skill = knowledge injection (passive), Agent = independent context (active) (AReaL)
- Expert agents: read-only, no Write/Edit -- advisors not executors (AReaL)
- Model tiering: haiku (high-freq execution) / sonnet (review) / opus (deep reasoning) (AReaL)
- Sub-agents return 1000-2000 token summaries, not full output (Anthropic CE)
- Heavy output -> delegate to subagent to protect main context
- Agents cannot spawn sub-agents -- design flat, not recursive
- Tool design: minimize overlap, self-documenting params, "engineer clarity test" (Anthropic CE)

### 5. Context Hygiene -- Protect the Window
- CLAUDE.md as slim router, not encyclopedia -- first 200 lines always loaded (Official)
- Auto-compress old tool outputs, prioritize user requests and key code (Official)
- Attention budget is finite -- performance degrades gradually with context growth (Anthropic CE)
- Avoid last 20% of context window for complex tasks
- Split role sub-agents for diverse perspectives without polluting main context
- `--continue` to resume, `--fork-session` for branches (Official)
- Curated examples > exhaustive lists -- examples are the most powerful LLM communication (Anthropic CE)

### 6. Continuous Improvement -- The System Evolves
- Configuration engineering is a first-class practice -- iterate .claude/ like code (AReaL)
- 74% of sessions are partial completions -- friction is normal, reduce via checkpoints (AReaL)
- Auto-memory saves pattern recognition across sessions; CLAUDE.md first 200 lines always loaded (Official)
- Eval saturation detection: 100% pass rate = eval is broken, add harder cases (Anthropic Evals)

### 7. Parallel Execution -- Scale Smart
- Multitasking: different sessions on different tasks -> improve throughput (AReaL)
- Pass@k: same problem, different constraints -> pick best result (AReaL)
- Git worktree for physical isolation of parallel work (Superpowers + AReaL)
- Know when to STOP parallelizing -- shared wrong assumption = waste (AReaL)
- Checkpoints at every boundary -- verify before continuing (Superpowers)
- Introduce controlled variability to prevent pattern lock-in (Manus)

### 8. Hooks as Automation Backbone
- Four types: command, http, prompt, agent -- choose by complexity (Official)
- 19 lifecycle events cover the full agent loop (Official)
- Use prompt hooks for AI judgment, agent hooks for codebase verification (Official)
- Auto-format, lint, sensitive file protection, context re-injection (Official)
- Three-layer config: user global -> project -> local project (Official)
