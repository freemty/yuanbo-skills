---
name: unbox-cross-ref
description: >
  Cross-reference all unbox reports: backfill missing info from other reports,
  resolve factual conflicts. Run after accumulating multiple unbox reports.
  Triggers: /unbox-cross-ref, cross-ref, 交叉验证, 交叉补充.
---

# Unbox Cross-Reference — 报告交叉验证与补全

对 `unbox-output/` 下所有已有报告进行交叉比对：把散落在 A 报告里关于 B 的信息回填到 B，发现并修正事实冲突。

## When to Use

- User says `/unbox-cross-ref` or `交叉验证`
- After accumulating a batch of new unbox reports
- When user suspects reports have inconsistencies

## When NOT to Use

- Profiling new researchers → use `/unbox`
- Updating overview → manually edit `_overview.md`

## Command

`/unbox-cross-ref [directory]`

- Default directory: `~/unbox-output/`
- Optional: pass a different path

## Workflow

### Phase 1: Build Registry

1. Glob `{directory}/*.md`, exclude `_overview.md` and `_cross-ref.md`
2. For each report, extract from the `# Title` line:
   - English name
   - Chinese name (in parentheses)
   - Slug (filename without `.md`)
3. Build a registry: list of `{english_name, chinese_name, slug, aliases[]}`
   - Aliases include: first name, last name, full name variations, Chinese name, slug
   - Handle edge cases: "Carrie Lin" vs "Guying Lin", "mars-tin" vs "Ziqiao Ma"
4. Print registry to user for confirmation: `Found N reports, N people in registry`

### Phase 2: Extract Cross-Mentions (parallel subagents)

Split reports into groups of ~7. For each group, spawn one subagent with:

- The full registry (all people, not just their group)
- The full text of their group's reports
- The extraction prompt from `references/extract-prompt.md`

Each subagent outputs a structured list of cross-mentions to a temp file:
`{directory}/_tmp_extract_{group_id}.md`

Format per mention:
```
SOURCE: {slug of report containing the mention}
ABOUT: {slug of person being mentioned}
TYPE: {relationship | event | date | affiliation | personality}
FACT: {the specific fact, one line}
CONTEXT: {surrounding sentence for verification}
LINE: {approximate line number in source report}
```

### Phase 3: Merge + Diff (parallel subagents)

Collect all extraction files. Group mentions by `ABOUT` person.

For each person who has cross-mentions, spawn a subagent that:

1. Reads the person's own report
2. Reads all cross-mentions about them
3. For each mention, classifies as:
   - **BACKFILL** — info not present in person's own report → prepare addition
   - **CONFIRM** — info already present and consistent → skip
   - **CONFLICT** — info contradicts something in person's own report → prepare resolution
4. For CONFLICT items: compare evidence quality (primary source > secondary mention), check if either side cites a URL. Pick the more reliable version. If truly ambiguous, keep both with annotation.
5. Applies changes directly to the person's report using Edit tool:
   - **BACKFILL**: Add `> 📎 交叉补充 (来源: {source}.md): {fact}` at the end of the most relevant section
   - **CONFLICT**: Fix the incorrect text inline, add HTML comment `<!-- cross-ref: 原文为 X，{source}.md 记为 Y，已修正 -->`
6. Writes a summary of all changes made to `{directory}/_tmp_changes_{slug}.md`

**Parallelism**: Group people into batches of ~5, dispatch one subagent per batch.

Subagent prompt: `references/apply-prompt.md`

### Phase 4: Generate Report

After all apply-subagents complete:

1. Collect all `_tmp_changes_*.md` files
2. Generate `{directory}/_cross-ref.md`:

```markdown
# Cross-Reference Report

Generated: {date}
Reports scanned: {N}
People in registry: {N}

## Backfills ({count})

| 目标报告 | 补充内容 | 来源 |
|---------|---------|------|
| ... | ... | ... |

## Conflicts Resolved ({count})

| 目标报告 | 原文 | 修正为 | 来源 | 判断依据 |
|---------|------|--------|------|---------|
| ... | ... | ... | ... | ... |

## Unresolvable Conflicts ({count})

| 报告 A | 报告 B | 冲突内容 | 备注 |
|--------|--------|---------|------|
| ... | ... | ... | ... |
```

3. Clean up temp files: `rm {directory}/_tmp_*.md`
4. Print summary to user

## Important Constraints

- **No external research** — do not Google, fetch URLs, or call any API. All evidence comes from existing reports.
- **Exception for conflicts**: If a conflict cannot be resolved from report text alone AND both sides cite a URL, the apply-subagent MAY fetch those specific URLs to verify. No speculative searching.
- **Preserve report structure** — never add new sections, only append within existing sections or add to "未验证 / 待挖"
- **Idempotent** — running cross-ref twice should not duplicate backfills (check for existing `📎 交叉补充` before adding)
- **Don't touch `_overview.md`** — that's maintained separately
