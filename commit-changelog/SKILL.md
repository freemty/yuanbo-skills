---
name: commit-changelog
description: Use when creating git commits, updating CHANGELOG.md, or committing changes that span nested repos or submodules. Triggers on user requests like "commit", "/commit", "changelog", or when changes exist in both a parent and nested repository.
---

# Commit & Changelog

## Overview

Standardized commit messages and changelog entries. Covers nested repo workflows where changes must be committed in multiple repositories.

## Quick Reference

### Commit Format

```
<type>(scope)?: <summary>

- what changed
- impact: <module/behavior>
- verification: <cmd or note>
```

### Types

| Type | 用途 | Type | 用途 |
|------|------|------|------|
| `feat` | 新功能 | `fix` | Bug 修复 |
| `docs` | 文档 | `refactor` | 重构 |
| `test` | 测试 | `chore` | 构建/工具链 |
| `perf` | 性能 | `build` | 构建系统 |

Breaking change: `feat!: <summary>`

### Changelog Format

```markdown
## vX.Y.Z @author - YYYY-MM-DD

### 新增
### 变更
### 修复
### 构建与工具链
### 其他
```

## Nested Repo / Submodule Workflow

When changes span a parent repo and a nested repo (submodule or gitignored independent repo):

**MUST commit in BOTH repos, inner first:**

```
1. Inner repo (nested): commit + push
2. Outer repo (parent): commit (references inner change) + push
```

### Inner Repo Commit

Standard commit — describe what changed in the nested project:

```bash
cd path/to/nested-repo
git add <files>
git commit -m "$(cat <<'EOF'
feat(auth): add Bedrock support for container execution

- copy ~/.claude config to job dir for Bedrock auth
- pass AWS env vars to Apptainer container
- add model name mapping for Bedrock IDs

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
EOF
)"
git push
```

### Outer Repo Commit

Reference the nested repo update. If gitignored (not a submodule), describe changes made to the nested repo:

```bash
cd path/to/parent-repo
git add <files>
git commit -m "$(cat <<'EOF'
feat(PostTrainBench): add Bedrock auth + connectivity test

- run_task.sh: copy .claude config, pass AWS env vars
- agents/claude/solve.sh: Bedrock model ID mapping
- tests/test_bedrock_connectivity.sh: 6-step verification
- impact: Claude agent can run via AWS Bedrock in CN servers

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
EOF
)"
```

If it IS a git submodule, stage the submodule pointer update:

```bash
git add path/to/submodule   # stages the new commit hash
git commit -m "chore(submodule): update PostTrainBench to <short-hash>"
```

### Decision: Which Repo Gets What

| 变更位置 | Inner commit | Outer commit |
|----------|-------------|-------------|
| Only inner files | Yes | Only if submodule pointer needs updating |
| Only outer files | No | Yes |
| Both repos | Yes (first) | Yes (second, reference inner) |
| Inner is gitignored | Yes (independent) | Describe inner changes in outer message |

## Rules

1. **Inner first** — always commit nested repo before parent
2. **One commit, one concern** — split feature/fix from deps/toolchain
3. **Title ≤72 chars**, imperative mood ("add" not "added")
4. **Body = why**, not what (the diff shows what)
5. **HEREDOC for multi-line** — ensures correct formatting
6. **Co-Authored-By** — always include for AI-assisted commits

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Commit outer without committing inner first | Submodule pointer points to unpushed commit |
| Forget to push inner repo | Others can't resolve submodule reference |
| Same message for both repos | Each repo's commit should describe its own scope |
| Giant commit spanning unrelated changes | Split into separate commits by concern |
| Committing secrets (.env, API keys) | Check `git diff --staged` before commit |
