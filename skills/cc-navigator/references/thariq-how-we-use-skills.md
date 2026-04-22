# Thariq: Lessons from Building Claude Code — How We Use Skills

> Source: https://x.com/trq212/status/2033949937936085378
> Author: Thariq (@trq212) — Anthropic Engineer
> Date: 2026-03-17

## Overview

Skills have become one of the most used extension points in Claude Code. They're flexible, easy to make, and simple to distribute. But this flexibility also makes it hard to know what works best.

Anthropic has hundreds of skills in active use. A common misconception is that skills are "just markdown files", but the most interesting part is that they're folders that can include scripts, assets, data, etc. that the agent can discover, explore and manipulate. Skills also have configuration options including registering dynamic hooks.

## 9 Skill Categories

After cataloging all skills, they cluster into recurring categories. The best skills fit cleanly into one.

### 1. Library/SDK Skills

Skills that explain how to correctly use a library, CLI, or SDK. These often include a folder of reference code snippets and a list of gotchas.

Examples:
- billing-lib -- internal billing library: edge cases, footguns
- internal-platform-cli -- every subcommand with examples
- frontend-design -- make Claude better at your design system

### 2. Verification Skills

Skills that describe how to test or verify code is working. Often paired with external tools like Playwright, tmux, etc.

Extremely useful for ensuring Claude's output is correct. Worth having an engineer spend a week making these excellent.

Techniques: have Claude record a video of its output, enforce programmatic assertions on state at each step.

Examples:
- signup-flow-driver -- headless browser signup -> email verify -> onboarding
- checkout-verifier -- Stripe test cards, verify invoice state
- tmux-cli-driver -- interactive CLI testing requiring TTY

### 3. Data/Monitoring Skills

Skills that connect to data and monitoring stacks. Include libraries to fetch data with credentials, dashboard IDs, and common workflows.

Examples:
- funnel-query -- event joins for signup -> activation -> paid
- cohort-compare -- compare retention/conversion, flag significant deltas
- grafana -- datasource UIDs, cluster names, problem -> dashboard lookup

### 4. Workflow Automation Skills

Automate repetitive workflows into one command. Saving previous results in log files helps the model stay consistent.

Examples:
- standup-post -- aggregates ticket tracker + GitHub + Slack -> formatted standup
- create-ticket -- enforces schema, post-creation workflow
- weekly-recap -- merged PRs + closed tickets + deploys -> formatted recap

### 5. Scaffolding Skills

Generate framework boilerplate. Especially useful when scaffolding has natural language requirements.

Examples:
- new-workflow -- scaffolds service/workflow/handler with annotations
- new-migration -- migration file template plus common gotchas
- create-app -- new internal app with auth, logging, deploy pre-wired

### 6. Code Quality Skills

Enforce code quality. Can include deterministic scripts for maximum robustness. May run automatically via hooks or GitHub Actions.

Examples:
- adversarial-review -- spawns fresh-eyes subagent to critique, iterates until nitpicks only
- code-style -- enforces styles Claude does poorly by default
- testing-practices -- how to write tests and what to test

### 7. DevOps Skills

Fetch, push, and deploy code.

Examples:
- babysit-pr -- monitors PR -> retries flaky CI -> resolves merge conflicts -> auto-merge
- deploy-service -- build -> smoke test -> gradual rollout -> auto-rollback on regression
- cherry-pick-prod -- isolated worktree -> cherry-pick -> conflict resolution -> PR

### 8. Debugging/Investigation Skills

Take a symptom (Slack thread, alert, error signature), walk through multi-tool investigation, produce structured report.

Examples:
- service-debugging -- maps symptoms -> tools -> query patterns
- oncall-runner -- fetches alert -> checks usual suspects -> formats finding
- log-correlator -- given request ID, pulls matching logs from every system

### 9. Maintenance/Operations Skills

Routine maintenance with guardrails for destructive actions.

Examples:
- resource-orphans -- finds orphaned pods/volumes -> Slack -> soak -> confirm -> cleanup
- dependency-management -- org's dependency approval workflow
- cost-investigation -- "why did our bill spike" with specific buckets and queries

## Writing Best Skills

### Focus on what Claude doesn't know

Claude knows a lot about coding. Focus on information that pushes Claude out of its normal way of thinking. The frontend-design skill was built by iterating with customers on improving Claude's design taste, avoiding classic patterns like Inter font and purple gradients.

### Gotchas are the highest-signal content

Build up from common failure points Claude runs into. Update your skill over time to capture these.

### Progressive disclosure via folder structure

Think of the entire file system as context engineering. Tell Claude what files are in your skill, and it will read them at appropriate times.

- Point to other markdown files for details (e.g., references/api.md)
- Include template files in assets/ to copy and use
- Have folders of references, scripts, examples

### Be flexible, not rigid

Skills are reusable -- be careful of being too specific. Give Claude the information it needs with flexibility to adapt.

### Setup via config.json

Some skills need user context (e.g., Slack channel). Store setup info in config.json in the skill directory. If not set up, the agent asks the user.

### Optimize descriptions for trigger accuracy

The description field is not a summary -- it describes when to trigger.

### Skill memory via stored data

Store data in append-only text logs, JSON files, or SQLite databases. A standup-post skill might keep standups.log with history, so Claude knows what changed since yesterday.

Store in `${CLAUDE_PLUGIN_DATA}` for stability across upgrades.

### Give Claude executable code

Giving Claude scripts and libraries lets it spend turns on composition rather than reconstructing boilerplate. For example, helper functions for data fetching that Claude composes into analysis scripts.

### Session-scoped hooks

Skills can include hooks activated only when the skill is called. Examples:
- /careful -- blocks destructive commands via PreToolUse matcher
- /freeze -- blocks edits outside a specific directory

## Distribution

Two ways to share skills:
1. Check into repo (under ./.claude/skills) -- good for small teams
2. Plugin marketplace -- for scaling across org

Find useful skills organically. Sandbox folder for experiments, move to marketplace after traction. Have curation before release.

## Measuring skill usage

Use a PreToolUse hook to log skill usage. Find popular skills or undertriggering ones.
