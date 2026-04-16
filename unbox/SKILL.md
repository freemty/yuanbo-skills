---
name: unbox
description: >
  Use when profiling researchers beyond their publication list — personality,
  early career, mentorship lineage, direction evolution, deleted content.
  Triggers: /unbox, 开盒, researcher profile, 'who is this author'.
---

# Unbox — 研究者画像调研

不是查简历，是拼人。发表列表谁都能查，要挖的是性格信号、早期经历、方向演变、师门关系。

## When to Use

- User says `/unbox` or `开盒`
- User asks to research/profile researchers ("这人什么背景", "who is this author")
- User pastes a paper link and wants to know about the authors
- User wants to understand a research group's composition

## When NOT to Use

- Looking up a single paper's content → use `web-fetcher` or `scholar-agent`
- Adding researchers to selfOS wiki → use `selfos` skill after unbox
- General topic research → use `deep-research`

## Command

`/unbox <input>`

Input is one of:
- arXiv URL: `https://arxiv.org/abs/...`
- OpenReview URL: `https://openreview.net/forum?id=...`
- Comma-separated names: `"Alice Zhang, Bob Li, Charlie Wang"`
- Local file path (one name per line)

## Workflow

**Before executing, read `references/subagent-prompt.md` for the full per-person pipeline.**

### Step 1: Parse Input

Determine input type:

| Input | Detection | Action |
|-------|-----------|--------|
| `https://arxiv.org/abs/...` | URL regex | Fetch page via `python3 ~/.claude/skills/web-fetcher/scripts/fetch.py <url>`, extract author list |
| `https://openreview.net/forum?id=...` | URL regex | Fetch page via `fetch.py`, extract author list |
| Comma-separated string | Contains `,` and no URL scheme | Split by `,`, trim whitespace |
| File path | File exists on disk | Read file, one name per line |

For paper links: after extracting authors, display the list and ask user to confirm or remove names before proceeding.

### Step 2: Create Output Directory

```bash
mkdir -p unbox-output
```

Use `unbox-output/` in the current working directory. If it already exists, that's fine — files will be overwritten.

### Step 3: Dispatch Subagents

For each researcher name, spawn one subagent using the Agent tool:

- **All subagents launch in parallel** (single message with multiple Agent tool calls)
- Each subagent receives the full prompt from `references/subagent-prompt.md` with `{NAME}` replaced
- Each subagent writes its report to `unbox-output/{slug}.md`
- Slug: lowercase name, spaces replaced with `-`, remove non-ascii (e.g., "Alice Zhang" → `alice-zhang`)

Example Agent call:
```
Agent({
  description: "Unbox: Alice Zhang",
  prompt: "<contents of subagent-prompt.md with {NAME} = Alice Zhang>",
  mode: "bypassPermissions"
})
```

### Step 4: Assemble Overview

After all subagents complete, read all generated reports and create `unbox-output/_overview.md`:

```markdown
# Unbox Report

Generated: {date}
Source: {input description}
Researchers: {count}

| 姓名 | 机构 | 一句话 | 报告 |
|------|------|--------|------|
| ... | ... | ... | [链接](slug.md) |
```

The "一句话" for each person is extracted from the `## 一句话` section of their report.

### Step 5: Report to User

Print the overview table and the path to `unbox-output/`.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| 用 `fetch.py` 抓知乎 → 403 | 必须用 `opencli zhihu search/download/question` |
| 从新闻报道推断本科院校 | 个人主页 bio 页面是 ground truth，优先级最高 |
| 只搜英文不搜中文 | 中国研究者的早期经历（竞赛、保研）全在中文搜索里 |
| 不搜高中/高考信息 | 从本科入学年反推高考年，搜 "{中文名} 高中/高考/自主招生"，信息密度远超本科标签 |
| 忽略微信公众号 | 大量早期信息沉淀在学校/院系/社团公众号，用 Google 搜 "{中文名} mp.weixin.qq.com"（注意：不要用 `site:` 语法，直接作为关键词） |
| 不查高校 BBS | 水木社区 (newsmth.net) 有入学名单、院系讨论；cc98.org 有浙大信息 |
| 不查海外中文论坛 | newmitbbs.com 和一亩三分地 (1point3acres.com) 有大量 biographical tidbits |
| Wayback Machine 是唯一的时光机 | 先查 GitHub Pages 源码仓库的 git log，精确到天 |
| 只看发表列表 | 性格信号（thesis 致谢、知乎、rebuttal 风格）才是核心 |
| 忽略 conference tutorials | Tutorial 比 paper 更能看出判断力和思想 flow |
| 对单个名字没加消歧 | "Hao Zhang" 有几十个同名人，加 institution/paper 关键词 |
| 只搜"采访/访谈" | 中文人物报道关键词更多：专访、人物、故事、校友故事、校友风采 |
| 不搜非学术特质 | 运动队、社团、乐队、创业等信息藏在校级新闻和校友报道里 |
| 不搜科技媒体 | 机器之心/量子位/雷锋网/36kr/腾讯云的人物长文是性格信号金矿 |
| 不搜奖项报道 | MIT TR35/求是奖/科学探索奖的报道常包含详细人物背景 |
| 搜一次就停 | 必须滚雪球：每次 fetch 页面后提取新线索，追加搜索 |
| 不搜"如何评价 XXX" | 知乎"如何评价"类问题是中文互联网上最集中的人物讨论 |
