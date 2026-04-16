---
name: unbox-backfill
description: >
  Read existing researcher profiles and run targeted searches to fill in missing
  sections added by the upgraded subagent-prompt (non-academic identity, alumni stories,
  overseas forums, controversy, snowball leads, award reports, video presence).
  Also pursues explicit "未验证/待挖" leads. Triggers: /unbox-backfill, backfill, 补全.
---

# Unbox Backfill — 存量报告定向补全

已有 77 份研究者画像，大多写于 prompt 升级前，缺少以下维度：
- 非学术身份（运动、音乐、社团、内容创作）
- 校友故事 / 媒体人物报道
- 海外中文论坛（newmitbbs、一亩三分地、小木虫）
- 争议 / 八卦 / 负空间
- 滚雪球追踪（从已有页面提取的线索）
- 奖项报道搜索
- B站 / YouTube 出镜

另外 65 份报告有明确的 "未验证/待挖" 段落，列出了未验证线索。

## When to Use

- User says `/unbox-backfill` or `backfill` or `补全`
- User wants to enrich existing profiles without re-running full investigation
- User wants to chase "未验证/待挖" leads

## When NOT to Use

- Profiling new researchers → use `/unbox`
- Cross-referencing between reports → use `/unbox-cross-ref`
- Single quick lookup → use `web-fetcher`

## Command

```
/unbox-backfill              # all 77 profiles, prioritized by gap count
/unbox-backfill <name>       # specific person (fuzzy match on English/Chinese name or slug)
/unbox-backfill --top N      # top N profiles by gap count (default: 10)
/unbox-backfill --dry-run    # show gap analysis only, no searches
```

## Workflow

**Before executing, read `references/backfill-prompt.md` for the per-person backfill subagent prompt.**

### Step 1: Gap Analysis

For each target profile, read the file and extract:

1. **Identity anchors** (carry forward to subagent, do NOT re-search):
   - English name, Chinese name
   - Undergrad school + year, PhD school + advisor
   - Personal homepage URL, GitHub username
   - Whether the person grew up in China

2. **Missing sections** — check which of these are absent or empty:

   | Section | Detection | Gap ID |
   |---------|-----------|--------|
   | 非学术身份 | No "非学术" or "运动/音乐/社团" content in 性格信号 | `non-academic` |
   | 校友报道/媒体专访 | No "校友" or "专访/人物报道" beyond basic interview | `alumni-media` |
   | 海外论坛 | No mention of newmitbbs, 1point3acres, muchong | `overseas-forums` |
   | 争议/八卦 | No "争议" or "如何评价" content | `controversy` |
   | 奖项报道 | No award coverage details (just award names listed) | `award-reports` |
   | B站/YouTube | No video presence beyond embedded talks | `video-presence` |
   | 科技媒体 | No 机器之心/量子位/雷锋网/36kr coverage | `tech-media` |
   | 微信公众号 | No mp.weixin.qq.com sourced content | `wechat-mp` |

3. **未验证/待挖 leads** — parse items from the "未验证 / 待挖" section:
   - Extract each bullet as a lead
   - Ignore items already marked `[x]` (resolved)
   - Classify each as actionable (has a concrete search strategy) or speculative

4. **Priority score** = count of missing sections + count of actionable 未验证 leads

Print the gap analysis table:

```
| Profile | Score | Missing Sections | 未验证 Leads | Chinese? |
|---------|-------|-----------------|-------------|----------|
| tairan-he | 9 | non-academic, overseas-forums, ... | 12 | Yes |
| hao-zhang | 7 | alumni-media, controversy, ... | 8 | Yes |
| alexei-efros | 4 | video-presence, ... | 10 | No |
```

If `--dry-run`, stop here.

### Step 2: Build Backfill Prompts

For each profile (sorted by priority score descending):

1. Read `references/backfill-prompt.md`
2. Replace placeholders:
   - `{NAME}` — English name
   - `{CHINESE_NAME}` — Chinese name (or "N/A" if unknown)
   - `{SLUG}` — filename slug
   - `{OUTPUT_DIR}` — path to profiles directory (e.g., `~/unbox-output/profiles`)
   - `{UNDERGRAD_SCHOOL}` — undergrad school name
   - `{UNDERGRAD_YEAR}` — undergrad entry year
   - `{PHD_SCHOOL}` — PhD school
   - `{ADVISOR}` — PhD advisor name
   - `{HOMEPAGE}` — personal homepage URL
   - `{GITHUB_USERNAME}` — GitHub username
   - `{IS_CHINESE}` — "yes" or "no"
   - `{GAP_SECTIONS}` — comma-separated list of gap IDs from Step 1
   - `{PENDING_LEADS}` — the actual text of actionable 未验证/待挖 items
   - `{EXISTING_REPORT_PATH}` — absolute path to the existing report

### Step 3: Dispatch Subagents

**Batch size: 5 parallel subagents at a time.**

Dispatch order: sorted by priority score (most gaps first).

For each batch:
1. Launch 5 subagents in parallel, each with the filled backfill prompt
2. Wait for all 5 to complete
3. Before launching the next batch, check rate limit status:
   - If any subagent reported 429 errors, wait 30 seconds
   - Otherwise, proceed immediately

Example Agent call:
```
Agent({
  description: "Backfill: Tairan He (何泰然)",
  prompt: "<filled backfill-prompt.md>",
  mode: "bypassPermissions"
})
```

Each subagent writes its findings to a temp file:
`{OUTPUT_DIR}/_backfill_{SLUG}.md`

### Step 4: Merge Results

After each batch completes, merge results into the original profiles.

For each `_backfill_{SLUG}.md`:

1. **Read the backfill output** — it's structured with section markers (see backfill-prompt.md output format)
2. **Read the original profile**
3. **Apply changes using Edit tool:**

   | Backfill Type | Merge Strategy |
   |---------------|---------------|
   | New section content (e.g., `### 非学术身份`) | If section header doesn't exist → insert before `## 未验证` (or at end). If section exists but is thin → append bullets at end of section |
   | Enhanced existing section | Append new bullets at end of the section, prefixed with `> 🔍 补全 ({date}): ` |
   | New 未验证/待挖 items from snowball | Append to existing 未验证 list |
   | Resolved 未验证 items | Change `- [ ]` to `- [x]` and append resolution |

4. **Idempotency check**: Before adding any content, search for the key phrase in the existing report. Skip if already present.
5. **Delete temp file** after successful merge

### Step 5: Summary Report

After all batches complete, print:

```
## Backfill Summary

Profiles processed: N
Sections added: N
Leads resolved: N
Leads added (snowball): N
Rate limit pauses: N

### Per-profile changes
| Profile | Sections Added | Leads Resolved | New Leads |
|---------|---------------|----------------|-----------|
| ... | ... | ... | ... |
```

## Chinese vs Non-Chinese Logic

The backfill prompt adapts based on `{IS_CHINESE}`:

| Dimension | Chinese Researcher | Non-Chinese Researcher |
|-----------|-------------------|----------------------|
| Phase 3 (early-life) | Full: 高中/高考/竞赛/公众号/论坛/非学术身份/争议 | Skip entirely |
| Overseas forums | newmitbbs + 1point3acres + muchong | Skip |
| 校友报道 | Chinese university alumni pages | English university alumni profiles |
| 科技媒体 | 机器之心/量子位/雷锋网/36kr | TechCrunch, Wired, The Verge, Quanta |
| B站 | Search bilibili.com | Skip |
| YouTube | Search if not already covered | Search for talks/interviews |
| 争议/知乎 | "如何评价" + 知乎 search | Skip (or English controversy search) |
| Search budget | ~25 Google searches max | ~15 Google searches max |

## Search Budget

Each backfill subagent has a budget of ~20-30 Google searches total (vs ~80 for full investigation).
Allocation:
- Gap sections: ~3 searches per gap section
- 未验证 leads: ~2 searches per actionable lead
- Snowball: ~5 searches reserved for follow-up

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Re-running Phase 1 identity searches | Identity is PRE-EXTRACTED. Subagent receives it as input. |
| Overwriting existing content | NEVER overwrite. Always APPEND with `> 🔍 补全` prefix. |
| Duplicating cross-ref backfills | Check for existing `📎 交叉补充` and `🔍 补全` markers before adding |
| Running all 77 at once | Batch size 5. Rate limits are real. |
| Searching for non-Chinese person on 知乎 | Only if they have a Chinese name and mainland connections |
| Fetching 知乎 with fetch.py | Use `opencli zhihu search/download/question` |
| Using `site:mp.weixin.qq.com` syntax | Use `mp.weixin.qq.com` as plain keyword in query |
| Marking lead as resolved without evidence | Must cite URL or specific finding |
