# Unbox Investigation: {NAME}

You are investigating a researcher named **{NAME}**. Your goal is to build a rich personal profile — not a CV, but a portrait that reveals personality, motivations, and trajectory.

**Core principle: 删掉的比留下的更重要，变化本身就是信号。**

## Output

Write your report to: `{OUTPUT_DIR}/{SLUG}.md`

Use the exact template at the bottom of this document. Every section is optional — if you can't find info, skip it. Information quantity itself is a signal.

## Tools Available

You MUST use these specific tools. Do not attempt to use tools that aren't listed here.

| Task | Tool | Command |
|------|------|---------|
| Google search (English) | opencli | `opencli google search "query" --limit 10 -f md` |
| Google search (Chinese) | opencli | `opencli google search "query" --limit 10 --lang zh -f md` |
| Fetch any webpage | fetch.py | `python3 ~/.claude/skills/web-fetcher/scripts/fetch.py <url>` |
| Semantic Scholar API | curl | `curl -s "https://api.semanticscholar.org/graph/v1/author/search?query=NAME&fields=name,affiliations,homepage,paperCount,citationCount,hIndex"` |
| Semantic Scholar papers | curl | `curl -s "https://api.semanticscholar.org/graph/v1/author/AUTHOR_ID/papers?fields=title,year,venue,citationCount,authors&limit=100"` |
| Wayback Machine snapshots | curl | `curl -s "https://web.archive.org/cdx/search/cdx?url=URL&output=json&collapse=timestamp:6"` |
| Wayback Machine fetch | fetch.py | `python3 ~/.claude/skills/web-fetcher/scripts/fetch.py "https://web.archive.org/web/TIMESTAMP/URL"` |
| GitHub user | Bash | `gh api users/USERNAME` |
| GitHub repos | Bash | `gh api "users/USERNAME/repos?sort=stars&per_page=10"` |
| 知乎搜索 | opencli | `opencli zhihu search "query" --limit 10 -f md` |
| 知乎专栏文章下载 | opencli | `opencli zhihu download --url "https://zhuanlan.zhihu.com/p/xxx" -f md` |
| 知乎问题+回答 | opencli | `opencli zhihu question <QUESTION_ID> --limit 5 -f md` |

**知乎注意：** 知乎有严格反爬，`fetch.py` 会 403。必须用 `opencli zhihu` 系列命令。专栏文章下载后保存在 `./zhihu-articles/` 目录下。

**Rate limiting:** Wait 1-2 seconds between consecutive Google searches to avoid blocks.

## Phase 1: Anchor Identity (do this first)

Goal: Figure out who this person is. Extract seeds for later phases.

1. **Google search** `"{NAME}" researcher OR professor OR PhD`
   - Identify: personal homepage, Google Scholar, LinkedIn, institutional page
   - If results are ambiguous (common name), add context clues (e.g., the paper title or co-author names from the original input)

2. **⚠️ CRITICAL: Fetch personal homepage + bio page FIRST**
   - 如果 Step 1 找到了个人主页（如 `haozhang.ai`），**立即 fetch 主页和 bio/about 子页面**
   - 常见 bio URL 模式: `/bio`, `/about`, `/about-me`, `/cv`
   - 个人主页上的自述是 **ground truth**，优先级高于任何第三方来源（新闻报道、Google 搜索摘要）
   - 如果主页和其他来源有冲突，**以主页为准**
   ```
   python3 ~/.claude/skills/web-fetcher/scripts/fetch.py "https://HOMEPAGE/"
   python3 ~/.claude/skills/web-fetcher/scripts/fetch.py "https://HOMEPAGE/bio/"
   python3 ~/.claude/skills/web-fetcher/scripts/fetch.py "https://HOMEPAGE/about/"
   ```
   （404 就跳过，不是所有人都有 bio 子页面）

3. **Google Scholar page** — fetch the URL from step 1
   - Extract: current affiliation, research areas, co-authors list, citation count

4. **Semantic Scholar API** — search by name
   - Extract: authorId, h-index, paper count, top papers
   - If multiple matches, pick the one whose affiliation/papers overlap with Google Scholar results

5. **Google search** `"{NAME}" CV OR resume filetype:pdf`
   - If found, fetch and scan for: undergrad school, Chinese name, awards, internships

**Key outputs to carry forward:**
- Chinese name (中文名) — critical for Phase 3
- Undergrad institution — critical for Phase 3
- PhD institution + advisor name — critical for Phase 2.5
- Personal homepage URL — critical for Phase 4
- Lab page URL — critical for Phase 4

## Phase 2: Personality Mining (core — spend the most time here)

Try each source in order. Skip if not found after 2-3 search attempts.

### 2a. PhD Thesis Acknowledgments

**Strategy: 先找校方 alumni 页面，再抓 PDF。** 大多数学校的院系网站有 alumni 页面，直接列出 thesis title + PDF 链接。这比搜 "acknowledgment" 关键词可靠得多。

Step 1 — 找到 thesis 页面:
```
opencli google search "{NAME} PhD thesis site:{UNIVERSITY_DOMAIN}" --limit 5 -f md
opencli google search "{NAME} alumni site:{UNIVERSITY_DOMAIN}" --limit 5 -f md
opencli google search "{NAME} dissertation {UNIVERSITY_NAME}" --limit 5 -f md
```

常见 thesis 仓库模式:
- CMU: `ri.cmu.edu/alumni/{name}/` or `kilthub.cmu.edu`
- Stanford: `purl.stanford.edu` or `searchworks.stanford.edu`
- MIT: `dspace.mit.edu`
- Berkeley: `escholarship.org`
- UMich: `deepblue.lib.umich.edu`

Step 2 — 从页面中提取 PDF 链接，fetch PDF。

Step 3 — 致谢通常在 PDF 的最前面几页（罗马数字页码部分）或最后几页。搜索 "Acknowledgment" 关键词定位。

Quote the most revealing passages — 感谢了谁、用什么语气、提到了什么非学术的事。

### 2b. Personal Blog / About Page
```
opencli google search "{NAME} blog OR 'about me' OR personal" --limit 5 -f md
```
Look for non-academic self-expression. What do they write about when not doing research?

### 2c. 知乎 / 微博 (if Chinese name found)

**知乎必须用 opencli zhihu，不要用 fetch.py（会 403）。**

Step 1 — 搜索知乎内容:
```
opencli zhihu search "{CHINESE_NAME}" --limit 10 -f md
opencli zhihu search "{NAME} {CHINESE_NAME}" --limit 5 -f md
```

Step 2 — 对搜索到的知乎专栏文章，用 download 命令获取全文:
```
opencli zhihu download --url "https://zhuanlan.zhihu.com/p/XXXXXX" -f md
```
（下载后文件在 `./zhihu-articles/` 目录下，用 Read 工具读取）

Step 3 — 对搜索到的知乎问题，用 question 命令获取回答:
```
opencli zhihu question <QUESTION_ID> --limit 5 -f md
```

Step 4 — 微博搜索（用 Google，微博本身没有好的 CLI）:
```
opencli google search "{CHINESE_NAME} 微博" --limit 5 -f md
```

Look for personal opinions, life reflections, non-academic posts.

### 2d. Interviews / Podcasts
```
opencli google search "{NAME} interview OR podcast OR 采访 OR 访谈" --limit 5 -f md
```
Prioritize non-academic interviews that reveal personality.

### 2e. OpenReview Rebuttal Style
```
opencli google search "{NAME} site:openreview.net" --limit 5 -f md
```
Find papers where they are the primary author. Read the rebuttal/response to reviewers. Note:
- Tone: defensive / collaborative / aggressive / humorous?
- Strategy: point-by-point rebuttal? Additional experiments? Appeal to authority?
- Quote the most characteristic lines.

### 2f. GitHub Side Projects
If a GitHub username was found:
```bash
gh api "users/{USERNAME}/repos?sort=stars&per_page=20" --jq '.[] | "\(.name) ★\(.stargazers_count) — \(.description)"'
```
Filter out paper-code repos (usually named after papers). What remains reveals personal interests.

### 2g. Conference Tutorials, Invited Talks & Slides

**这是最被低估的信号源。** Tutorial/talk 是按"人能听懂"的逻辑组织的，不像 paper 充满技术包装。一个人选择在什么时间点做什么 tutorial，暴露了他对趋势的判断。

Step 1 — 搜索 conference tutorials（最高价值）:
```
opencli google search "{NAME} tutorial ICML OR NeurIPS OR ICLR OR OSDI OR SOSP" --limit 10 -f md
opencli google search "{NAME} tutorial site:icml.cc OR site:neurips.cc OR site:iclr.cc" --limit 5 -f md
```

Step 2 — 搜索 invited talks / keynotes:
```
opencli google search "{NAME} invited talk OR keynote OR workshop talk" --limit 5 -f md
```

Step 3 — 搜索公开 slides（很多人把 slides 放 Google Drive / SlideShare / 个人主页）:
```
opencli google search "{NAME} slides filetype:pdf OR site:docs.google.com OR site:slideshare.net" --limit 5 -f md
```

Step 4 — 如果找到 tutorial/talk 链接，fetch 页面，关注：
- **Talk 标题和时间点** — 什么时候讲了什么话题，是追风还是预判？
- **Slides 内容** — 哪些观点在当时是超前的？哪些后来被验证了？
- **合作者** — 和谁一起做 tutorial 暴露了核心圈子

**为什么重要：** 一个人在 2022 年中做 "Parallelization for Big Models" tutorial，比他 2023 年发 vLLM paper 更能说明他的判断力——因为 tutorial 是在 ChatGPT 爆发前布局的。

## Phase 2.5: Mentorship Lineage & Academic Siblings

Once you know the PhD advisor:

1. **Advisor's lab page**
```
opencli google search "{ADVISOR_NAME} lab members OR students OR group" --limit 5 -f md
```
Fetch the lab page. Extract current students and alumni. Note entry years if available.

2. **Advisor's Google Scholar co-authors**
```
opencli google search "{ADVISOR_NAME} site:scholar.google.com" --limit 3 -f md
```
Fetch the Scholar page. The "co-authors" sidebar lists frequent collaborators — high-frequency ones are likely students.

3. **Mathematics Genealogy Project**
```
opencli google search "{ADVISOR_NAME} site:genealogy.math.ndsu.nodak.edu" --limit 3 -f md
```
Traces the advisor-of-advisor chain.

4. **Advisor's advisor (academic grandparent)**
```
opencli google search "{ADVISOR_NAME} PhD advisor OR supervisor OR dissertation" --limit 5 -f md
```

## Phase 3: Chinese-Language Deep Dive

**Skip this phase entirely if no Chinese name was found in Phase 1.**

Use the Chinese name + undergrad institution as search seeds:

```
opencli google search "{CHINESE_NAME} {UNDERGRAD_SCHOOL}" --limit 10 --lang zh -f md
opencli google search "{CHINESE_NAME} 保研 OR 推免 OR 考研" --limit 5 --lang zh -f md
opencli google search "{CHINESE_NAME} ACM OR 数学竞赛 OR 数学建模 OR 物理竞赛" --limit 5 --lang zh -f md
opencli google search "{CHINESE_NAME} {ADVISOR_CHINESE_NAME}" --limit 5 --lang zh -f md
opencli google search "{CHINESE_NAME} 国家奖学金 OR 优秀毕业生 OR 竞赛" --limit 5 --lang zh -f md
```

For each promising result, fetch the full page. Look for:
- Campus news articles
- Scholarship / award announcements
- Competition results
- BBS / forum posts mentioning them
- 保研/考研 experience posts

## Phase 4: Wayback Machine Archaeology + GitHub Pages 源码考古

**Core principle: 删掉的比留下的更重要，变化本身就是信号。**

### ⚠️ FIRST: Check if homepage is GitHub Pages

很多研究者的个人主页是 GitHub Pages 托管的。如果是，**git log 比 Wayback Machine 精确 100 倍**。

Step 1 — 检测是否有 GitHub Pages 源码仓库:
```bash
# 如果已知 GitHub username (如 zhisbug):
gh api "repos/{USERNAME}/site" --jq '{name, created_at, pushed_at}' 2>/dev/null
gh api "repos/{USERNAME}/{USERNAME}.github.io" --jq '{name, created_at, pushed_at}' 2>/dev/null
gh api "repos/{USERNAME}/homepage" --jq '{name, created_at, pushed_at}' 2>/dev/null
```

Step 2 — 如果找到，查看 commit history:
```bash
gh api "repos/{USERNAME}/{REPO}/commits?per_page=50" --jq '.[] | "\(.commit.author.date | split("T")[0]) \(.commit.message | split("\n")[0])"'
```

Step 3 — 对有意义的 commit（如 "update bio", "update research", "add new project"），看 diff:
```bash
gh api "repos/{USERNAME}/{REPO}/commits/{SHA}" --jq '.files[] | "\(.filename) +\(.additions) -\(.deletions)"'
```

这比 Wayback Machine 好在：
- **精确到天**而非按月采样
- **能看到每次具体改了什么**（diff），不需要人肉对比两个快照
- **commit message 本身就是信号**（"remove internship from CV" vs "update bio"）

### If no GitHub Pages: Use Wayback Machine

For each URL found in earlier phases (personal homepage, lab page, LinkedIn, CV PDF URL):

### Step 1: Get snapshot list
```bash
curl -s "https://web.archive.org/cdx/search/cdx?url={URL}&output=json&collapse=timestamp:6&limit=50"
```

### Step 2: Sample snapshots
Pick one snapshot per year (earliest available). If less than 3 snapshots exist, skip this URL.

### Step 3: Fetch and diff
For each sampled snapshot:
```
python3 ~/.claude/skills/web-fetcher/scripts/fetch.py "https://web.archive.org/web/{TIMESTAMP}/{URL}"
```

Compare adjacent years. Look for:
- **Research interest wording changes** — "NLP" → "multimodal" → "foundation models" tells a direction story
- **Deleted content** — removed internships, removed projects, removed collaborators
- **Lab member changes** — who joined, who disappeared
- **Self-description evolution** — how they position themselves over time

### Step 4: Synthesize timeline
Create a chronological summary of meaningful changes, not just a list of snapshots.

## Output Template

Write the report using this exact structure:

```markdown
# {ENGLISH_NAME} ({CHINESE_NAME})

## 一句话
[One sentence that captures the MOST interesting/revealing things about this person.
This is the most important line in the entire report. Make it vivid and specific.
Bad: "Stanford PhD working on ML" — boring, anyone can see that.
Good: "湖大数学系出身, 博士致谢里感谢了他的猫, rebuttal 风格硬刚, 2021 年从 NLP 急转多模态"]

## 身份锚点
- 现任: [current position]
- 导师: [PhD advisor]
- 本科: [undergrad school, major, year]
- 中文名来源: [how you found the Chinese name]

## 性格信号

[Include subsections for each signal type found. Skip those not found.]

### PhD 致谢
> [Direct quote of revealing passages]
(来源: [URL])

### 知乎/博客/微博
- [Key findings, with links]

### Rebuttal 风格
- [Paper title]: [characterization of rebuttal tone/style]
- [Direct quote of most characteristic line]

### 早期线索（中文）
- [Campus news, awards, competition results]

### 其他发现
- [GitHub side projects, interviews, podcasts, anything else interesting]

## 时光机 (Wayback Diff)

### 个人主页变迁
- [YYYY-MM]: [description of state]  ← [interpretation]
- [YYYY-MM]: [description of change]  ← [interpretation]

### 被删除的内容
- [What was removed, when, and from where]

### 快照链接
- [YYYY-MM description](https://web.archive.org/web/TIMESTAMP/URL)

## 师门谱系

### 导师
- [Advisor name] ([institution]) — 研究方向: [areas]

### 导师的导师
- [Lineage chain]

### 同门（按年份）
- [YYYY 入组]: [Name] (现 [current position])
- [YYYY 入组]: **{NAME}** ← 本人

### 频繁合作者（非同门）
- [Name] ([affiliation]) — [relationship: N papers together, etc.]

## 发表（精选，按影响力）
- [Top 5-10 papers by citation count, with venue and year]
（完整列表: [Google Scholar link]）

## 原始来源
- Google Scholar: [link]
- Semantic Scholar: [link]
- Personal page: [link]
- PhD Thesis: [link]
- [Other sources found]

## 未验证 / 待挖
- [Unconfirmed findings, leads not followed up]
- [Things you searched for but couldn't find]
```
