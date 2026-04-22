# Ecosystem: SWE Workflow Frameworks

Opinionated skill/plugin collections that provide structured development workflows for Claude Code.

## Superpowers

> https://github.com/obra/superpowers

Core: Think before you code, decompose tasks to atomic size (2-5 min), subagent-driven development, mandatory TDD.

Key skills:
- `brainstorming` -- explore intent before implementation
- `writing-plans` -- structured implementation plan
- `test-driven-development` -- RED/GREEN/REFACTOR cycle
- `systematic-debugging` -- root cause investigation
- `dispatching-parallel-agents` -- concurrent independent tasks
- `verification-before-completion` -- verify before claiming done
- `requesting-code-review` / `receiving-code-review`
- `using-git-worktrees` -- isolated dev environments
- `finishing-a-development-branch` -- merge/PR/cleanup

Philosophy: Seven-stage closed loop, task atomization, two-stage verification, isolated workspaces, systematic over intuitive.

## gstack

> https://github.com/garrytan/gstack
> 44.2k stars

Garry Tan's exact Claude Code setup: 15 opinionated tools that serve as CEO, Designer, Eng Manager, Release Manager, Doc Engineer, and QA.

Key skills:
- `/office-hours` -- YC-style brainstorming (startup or builder mode)
- `/plan-ceo-review` -- CEO/founder-mode plan review, 10-star product thinking
- `/plan-eng-review` -- Eng manager architecture/data flow/edge case review
- `/plan-design-review` -- Designer's eye plan review
- `/design-consultation` -- Full design system creation
- `/ship` -- Ship workflow (test, review, bump, PR)
- `/qa` -- Systematic QA testing + iterative fix
- `/design-review` -- Visual QA with before/after screenshots
- `/review` -- Pre-landing PR review
- `/investigate` -- Systematic debugging with root cause
- `/browse` -- Headless browser for QA and dogfooding
- `/codex` -- Second opinion via OpenAI Codex CLI
- `/retro` -- Weekly engineering retrospective
- `/document-release` -- Post-ship documentation update

Philosophy: Full development lifecycle coverage, role-based skills, iterative review loop.

## LabMate

> https://github.com/freemty/labmate
> Research Harness for Claude Code

Keep your agent grounded in context, not lost in vibe coding. Designed for research and experiment workflows.

Features: experiment directory management, pipeline state tracking, context grounding for research tasks.

Best for: ML research, experiment tracking, academic paper workflows.

## Decision Guide

| Need | Framework |
|------|-----------|
| TDD-first, atomic task decomposition | Superpowers |
| Full lifecycle (plan -> design -> ship -> QA) | gstack |
| Research/experiment workflows | LabMate |
| Mix and match | Install multiple, they can coexist |
