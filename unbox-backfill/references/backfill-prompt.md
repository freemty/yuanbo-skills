# Backfill Investigation: {NAME}

You are running a **targeted backfill** on an existing researcher profile for **{NAME}** ({CHINESE_NAME}).
The full investigation was already done. You are NOT re-running Phase 1 (identity) or the full pipeline.
Your job: fill specific gaps and chase specific leads.

## Pre-extracted Identity (DO NOT re-search these)

- **English name**: {NAME}
- **Chinese name**: {CHINESE_NAME}
- **Undergrad**: {UNDERGRAD_SCHOOL} ({UNDERGRAD_YEAR})
- **PhD**: {PHD_SCHOOL}, advisor: {ADVISOR}
- **Homepage**: {HOMEPAGE}
- **GitHub**: {GITHUB_USERNAME}
- **Chinese background**: {IS_CHINESE}

## Existing Report

The current report is at: `{EXISTING_REPORT_PATH}`

Read it first to understand what's already been covered. Do NOT duplicate existing content.

## Gap Sections to Fill

{GAP_SECTIONS}

## Pending Leads (from 未验证/待挖)

{PENDING_LEADS}

## Output

Write your findings to: `{OUTPUT_DIR}/_backfill_{SLUG}.md`

Use the structured format below. Only include sections where you found new information.

**Write incrementally** — after each search block, update the output file.

## Tools Available

| Task | Tool | Command |
|------|------|---------|
| Google search (English) | opencli | `opencli google search "query" --limit 10 -f md` |
| Google search (Chinese) | opencli | `opencli google search "query" --limit 10 --lang zh -f md` |
| Fetch any webpage | fetch.py | `python3 ~/.claude/skills/web-fetcher/scripts/fetch.py <url>` |
| 知乎搜索 | opencli | `opencli zhihu search "query" --limit 10 -f md` |
| 知乎专栏下载 | opencli | `opencli zhihu download --url "URL" -f md` |
| 知乎问题+回答 | opencli | `opencli zhihu question <ID> --limit 5 -f md` |
| GitHub user | Bash | `gh api users/USERNAME` |
| GitHub repos | Bash | `gh api "users/USERNAME/repos?sort=stars&per_page=10"` |

**知乎注意：** 必须用 `opencli zhihu` 系列命令，`fetch.py` 会 403。

**Rate limiting:** Wait 1-2 seconds between consecutive Google searches. Total budget: ~25 searches.

**微信公众号搜索注意：** 不要用 `site:mp.weixin.qq.com`，直接把 `mp.weixin.qq.com` 作为关键词。

## Search Playbook

Execute ONLY the sections listed in "Gap Sections to Fill" above. Skip everything else.

### If `non-academic` is in gap list:

Search for non-academic identity (sports, arts, clubs, content creation):

```
opencli google search "{CHINESE_NAME} 运动 OR 体育 OR 田径 OR 马拉松 OR 篮球 OR 跑步" --limit 5 --lang zh -f md
opencli google search "{CHINESE_NAME} 音乐 OR 乐队 OR 摄影 OR 书法 OR 绘画" --limit 5 --lang zh -f md
opencli google search "{CHINESE_NAME} 社团 OR 学生会 OR 志愿者 OR 支教 OR 创业" --limit 5 --lang zh -f md
opencli google search "{NAME} hobby OR sport OR music OR photography" --limit 5 -f md
```

Content creation / social media beyond academia:
```
opencli google search "{CHINESE_NAME} B站 OR UP主 OR 抖音 OR 小红书 OR 公众号" --limit 5 --lang zh -f md
opencli google search "{NAME} twitter OR blog OR substack OR medium" --limit 5 -f md
```

### If `alumni-media` is in gap list:

Alumni stories and media profiles (highest-value personality source):

```
opencli google search "{CHINESE_NAME} 校友 OR 校友故事 OR 校友风采 OR 杰出校友" --limit 5 --lang zh -f md
opencli google search "{CHINESE_NAME} {UNDERGRAD_SCHOOL} 校友" --limit 5 --lang zh -f md
opencli google search "{CHINESE_NAME} 采访 OR 访谈 OR 专访 OR 人物 OR 故事 OR 对话" --limit 10 --lang zh -f md
opencli google search "{NAME} interview OR profile OR portrait" --limit 5 -f md
```

For non-Chinese researchers:
```
opencli google search "{NAME} alumni story OR alumni profile OR featured graduate" --limit 5 -f md
opencli google search "{NAME} interview TechCrunch OR Wired OR Quanta OR The Verge" --limit 5 -f md
```

### If `overseas-forums` is in gap list (Chinese researchers only):

```
opencli google search "{CHINESE_NAME} site:newmitbbs.com OR site:mitbbs.com" --limit 5 --lang zh -f md
opencli google search "{CHINESE_NAME} site:1point3acres.com" --limit 5 --lang zh -f md
opencli google search "{CHINESE_NAME} site:muchong.com" --limit 3 --lang zh -f md
```

Note: Forum gossip value is biographical details (school, age, hometown), not whether claims are "true".
Mark forum-sourced info with credibility note: "据论坛讨论".

### If `controversy` is in gap list:

```
opencli google search "{CHINESE_NAME} 争议 OR 质疑 OR 批评 OR 离职 OR 辞职" --limit 5 --lang zh -f md
opencli google search "如何评价 {CHINESE_NAME}" --limit 5 --lang zh -f md
opencli zhihu search "如何评价 {CHINESE_NAME}" --limit 5 -f md
```

For non-Chinese researchers:
```
opencli google search "{NAME} controversy OR criticism OR left OR resigned" --limit 5 -f md
```

### If `award-reports` is in gap list:

Award reports often contain detailed personal background that doesn't appear elsewhere:

```
opencli google search "{CHINESE_NAME} MIT TR35 OR 福布斯 OR 求是奖 OR 科学探索奖 OR 青橙奖" --limit 5 --lang zh -f md
opencli google search "{CHINESE_NAME} 杰出青年 OR 优秀青年 OR 长江学者 OR 万人计划" --limit 5 --lang zh -f md
```

For non-Chinese researchers:
```
opencli google search "{NAME} award profile OR fellowship announcement OR prize citation" --limit 5 -f md
```

### If `video-presence` is in gap list:

```
opencli google search "{CHINESE_NAME} site:bilibili.com" --limit 5 -f md
opencli google search "{NAME} site:youtube.com talk OR lecture OR interview" --limit 5 -f md
```

### If `tech-media` is in gap list (Chinese researchers primarily):

```
opencli google search "{CHINESE_NAME} 机器之心 OR 量子位 OR 雷锋网 OR 36kr OR 新智元" --limit 5 --lang zh -f md
opencli google search "{CHINESE_NAME} 腾讯云 OR CSDN OR InfoQ OR 澎湃" --limit 5 --lang zh -f md
```

### If `wechat-mp` is in gap list (Chinese researchers only):

```
opencli google search "{CHINESE_NAME} {UNDERGRAD_SCHOOL} mp.weixin.qq.com" --limit 5 --lang zh -f md
opencli google search "{CHINESE_NAME} mp.weixin.qq.com" --limit 5 --lang zh -f md
```

## Chasing Pending Leads

For each item in "Pending Leads" above:

1. Read the lead carefully — what specific question does it ask?
2. Design 1-2 targeted searches to answer it
3. If a URL is mentioned in the lead, fetch it directly
4. If the search yields an answer, mark it as RESOLVED with evidence
5. If the search yields nothing, mark it as STILL_PENDING

**Budget: ~2 searches per lead, max 10 leads per run.**

## CRITICAL: Snowball Rule

Every time you fetch a page and read its content, **extract new leads** and follow up with 1-2 additional searches. The best discoveries come from the second hop.

Examples:
- Article mentions "他曾获得ACM区域赛银牌" -> search `"{CHINESE_NAME} ACM 区域赛"`
- Alumni page mentions high school name -> search `"{CHINESE_NAME} {HIGH_SCHOOL}"`
- Forum post mentions a nickname or detail -> follow that thread

**Reserve 5 searches from your budget for snowball follow-ups.**

## Output Template

Write findings using this exact structure:

```markdown
# Backfill: {NAME} ({CHINESE_NAME})

Date: {YYYY-MM-DD}
Gap sections searched: {list}
Leads pursued: {count}

## NEW_SECTION: 非学术身份
<!-- Only include if non-academic section is new to the report -->
- [Finding with source URL]
- [Finding with source URL]

## APPEND: 性格信号 > 校友报道/人物专访
<!-- Append to existing section -->
- [New finding from alumni story, with URL]

## APPEND: 性格信号 > 争议/八卦
<!-- Append to existing section -->
- [Finding, with credibility note]

## APPEND: 性格信号 > 其他发现
<!-- Append to existing section -->
- [Tech media coverage finding]
- [Award report finding]
- [Video presence finding]

## LEAD_RESOLVED: {original lead text}
Status: RESOLVED
Evidence: {what was found, with URL}

## LEAD_RESOLVED: {original lead text}
Status: STILL_PENDING
Notes: {what was searched, why it failed}

## NEW_LEADS: 未验证/待挖 (snowball)
<!-- New leads discovered during this backfill -->
- [New lead from snowball search]
- [New lead from snowball search]

## SEARCH_LOG
<!-- Track budget usage -->
Total Google searches: N/25
Total fetches: N
Rate limit hits: N
```

## Important Rules

1. **DO NOT re-search identity.** Chinese name, school, advisor are given. Use them directly.
2. **DO NOT repeat searches already reflected in the existing report.** Read the report first.
3. **Fetch every promising result.** A search without fetching the top results is wasted.
4. **Snowball is mandatory.** After every fetch, extract at least one new lead if possible.
5. **Mark credibility.** Forum gossip: "据论坛讨论". Self-reported: "据本人知乎". Official: "据校方网站".
6. **Budget discipline.** ~25 Google searches total. If hitting rate limits, prioritize gap sections over pending leads.
7. **Write incrementally.** Update the output file after each search block, not at the end.
