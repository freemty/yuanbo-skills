# Unbox Investigation: {NAME}

You are investigating a researcher named **{NAME}**. Your goal is to build a rich personal profile — not a CV, but a portrait that reveals personality, motivations, and trajectory.

**Core principle: 删掉的比留下的更重要，变化本身就是信号。**

## Output

Write your report to: `{OUTPUT_DIR}/{SLUG}.md`

Use the exact template at the bottom of this document. Every section is optional — if you can't find info, skip it. Information quantity itself is a signal.

**⚠️ CRITICAL: Write the report INCREMENTALLY.** After completing each phase, write or update the file. Don't wait until the end — if the process is interrupted, partial results are better than nothing.

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

**Search budget:** Total Google searches across all phases should not exceed ~80. If you hit a rate limit (429), wait 10 seconds and retry once. If still blocked, skip to the next step. For snowball searches, follow at most 5 snowball chains total, each chain at most 3 hops deep.

## ⚠️ GLOBAL RULE: Snowball Search (滚雪球)

**This is the single most important rule in this entire document.**

Every time you fetch a page and read its content, **extract new leads** and **immediately pursue them with follow-up searches**. Do NOT just execute the template queries and stop.

Examples of snowball triggers:
- You read a campus news article that mentions "他曾是校田径队成员" → immediately search `"{CHINESE_NAME} 田径 OR 运动会 OR 校运会"`
- You find an interview mentioning "卢策吾在重邮时参加了挑战杯" → search `"{CHINESE_NAME} 挑战杯"` and `"{CHINESE_NAME} 重庆邮电大学 挑战杯"`
- A 知乎 post mentions "他当年是从XXX中学来的" → search `"{CHINESE_NAME} XXX中学"`
- A thesis acknowledgment mentions a nickname or personal detail → search for that too

**The template queries in each Phase are starting points, not the finish line.** A good investigation follows at least 3-5 snowball chains. The best discoveries come from the second or third hop.

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
- Undergrad institution + **入学年份** — critical for Phase 3 (入学年 = 高考年，用于反推高中阶段)
- PhD institution + advisor name — critical for Phase 2.5
- Personal homepage URL — critical for Phase 4
- Lab page URL — critical for Phase 4
- Whether the person grew up in China — determines Phase 3 depth
- Advisor's Chinese name (导师中文名, if discoverable) — used in Phase 3 Step 3

**→ WRITE the report file now with Phase 1 findings before continuing.**

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

### 2d. Interviews / Podcasts / Media Profiles

**⚠️ 这个 step 之前覆盖面太窄。** 中文互联网上高价值人物报道使用的关键词远不止"采访/访谈"。

Step 1 — 广撒网搜索（中英文各一轮）:
```
opencli google search "{NAME} interview OR podcast OR profile OR portrait" --limit 5 -f md
opencli google search "{CHINESE_NAME} 采访 OR 访谈 OR 专访 OR 人物 OR 故事 OR 对话" --limit 10 --lang zh -f md
```

Step 2 — 校友故事（这是最被低估的信号源之一）:
```
opencli google search "{CHINESE_NAME} 校友 OR 校友故事 OR 校友风采 OR 杰出校友" --limit 5 --lang zh -f md
opencli google search "{CHINESE_NAME} {UNDERGRAD_SCHOOL} 校友" --limit 5 --lang zh -f md
```

**为什么重要：** 校友报道是非学术视角的第一人称叙事，往往包含童年故事、家庭背景、课外活动、转折点等在学术简历中永远不会出现的内容。例如"卢策吾是校田径队成员，400米接力亚军"这种信息只存在于母校的校友报道中。

Step 3 — 科技媒体人物报道:
```
opencli google search "{CHINESE_NAME} 机器之心 OR 量子位 OR 雷锋网 OR 36kr OR 新智元 OR AI科技评论" --limit 5 --lang zh -f md
opencli google search "{CHINESE_NAME} 腾讯云 OR CSDN OR InfoQ OR 澎湃" --limit 5 --lang zh -f md
```

Step 4 — 奖项报道（奖项报道常包含人物背景介绍）:
```
opencli google search "{CHINESE_NAME} MIT TR35 OR 福布斯 OR 求是奖 OR 科学探索奖 OR 青橙奖 OR 达摩院青橙" --limit 5 --lang zh -f md
opencli google search "{CHINESE_NAME} 杰出青年 OR 优秀青年 OR 长江学者 OR 万人计划" --limit 5 --lang zh -f md
```

Step 5 — B 站 / YouTube 视频（本人出镜的 talk、采访、课程）:
```
opencli google search "{CHINESE_NAME} site:bilibili.com OR site:youtube.com" --limit 5 -f md
opencli google search "{NAME} site:youtube.com talk OR lecture OR interview" --limit 5 -f md
```

**→ Fetch every promising result.** 科技媒体的长文人物报道是性格信号的金矿。

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

Also check: GitHub bio, location, company field, pinned repos, contribution graph.

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

### 2h. Non-Academic Identity (非学术身份) ⭐ NEW

**一个人在学术之外做什么，比他的论文列表更能揭示真实性格。**

```
opencli google search "{CHINESE_NAME} 运动 OR 体育 OR 田径 OR 马拉松 OR 篮球 OR 足球 OR 跑步" --limit 5 --lang zh -f md
opencli google search "{CHINESE_NAME} 音乐 OR 乐队 OR 吉他 OR 钢琴 OR 摄影 OR 绘画 OR 书法" --limit 5 --lang zh -f md
opencli google search "{CHINESE_NAME} 社团 OR 学生会 OR 志愿者 OR 支教 OR 创业" --limit 5 --lang zh -f md
opencli google search "{NAME} hobby OR sport OR music OR photography OR marathon" --limit 5 -f md
```

Also search for content creation / social media presence beyond academia:
```
opencli google search "{CHINESE_NAME} B站 OR UP主 OR 抖音 OR 小红书 OR 公众号" --limit 5 --lang zh -f md
opencli google search "{NAME} twitter OR blog OR substack OR medium" --limit 5 -f md
```

**为什么重要：** "卢策吾是校田径队的，400米接力亚军"比"卢策吾获得特等奖学金"有趣 100 倍。何泰然是 B 站 40 万粉 UP 主，这比他的论文列表更能说明他的性格。

**→ UPDATE the report file now with Phase 2 findings before continuing.**

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

## Phase 3: Chinese Early-Life Archaeology (高优先级)

**⚠️ 这是最被低估但信息密度最高的阶段。** 一个人 18 岁前的痕迹往往比论文列表更能揭示真实性格。小城市学校公众号、省级竞赛名单、高考状元采访、自主招生公示——这些信息散落在互联网各处，但极有价值。

**Skip / conditional execution rules:**
- If no Chinese name was found in Phase 1 AND no Chinese institution appeared → skip Phase 3 entirely, note in 未验证/待挖
- If Chinese name was found but undergrad school is unknown → execute Steps 1, 4, 5, 6, 7 only (skip Steps 2, 3 which need `{UNDERGRAD_SCHOOL}`)
- If both Chinese name and undergrad are known → execute all steps
- For Taiwan/HK researchers: their early-life info channels differ (PTT, HKGolden, etc.) — note as 待挖 rather than running mainland-specific searches

### Step 0: 反推时间线

从 Phase 1 已知的本科入学年份反推：
- 本科入学年 = 高考年（如 2012 入学 → 2012 年高考）
- 高中就读 = 高考年前 3 年（如 2009-2012）
- 如果知道本科学校，可以推断省份（如清华/北大 → 各省尖子）

### Step 1: 高中 + 高考信息（最早期，最珍贵）⭐ 最高优先级

```
opencli google search "{CHINESE_NAME} 高中 OR 中学" --limit 10 --lang zh -f md
opencli google search "{CHINESE_NAME} 高考" --limit 5 --lang zh -f md
opencli google search "{CHINESE_NAME} 自主招生 OR 领军计划 OR 博雅计划 OR 强基计划" --limit 5 --lang zh -f md
opencli google search "{CHINESE_NAME} {UNDERGRAD_SCHOOL} 录取" --limit 5 --lang zh -f md
```

**为什么重要：** "哈三中领军计划综合排名第一"比"清华本科"信息密度高 100 倍。前者告诉你这人在高中就是绝对 top，后者只是一个标签。

**如果 Phase 3 时间/速率受限，Step 1、Step 4 和 Step 6 是必须执行的最高优先级。**

### Step 2: 竞赛 + 奖项

```
opencli google search "{CHINESE_NAME} ACM OR 数学竞赛 OR 数学建模 OR 物理竞赛 OR 信息学竞赛 OR NOI OR IOI" --limit 5 --lang zh -f md
opencli google search "{CHINESE_NAME} 国家奖学金 OR 优秀毕业生 OR 竞赛" --limit 5 --lang zh -f md
```

### Step 3: 本科阶段

```
opencli google search "{CHINESE_NAME} {UNDERGRAD_SCHOOL}" --limit 10 --lang zh -f md
opencli google search "{CHINESE_NAME} 保研 OR 推免 OR 考研" --limit 5 --lang zh -f md
opencli google search "{CHINESE_NAME} {ADVISOR_CHINESE_NAME}" --limit 5 --lang zh -f md
```

**⚠️ 院系校友名录 / 官网是 ground truth：** 很多院系有校友网、毕业生名录页面，直接在院系域名搜索：
```
opencli google search "{CHINESE_NAME} site:{UNIVERSITY_DOMAIN}" --limit 10 --lang zh -f md
```
常见域名模式：
- 浙大信电: `isee.zju.edu.cn`（校友网 iseexyw 子站有完整毕业生名录）
- 清华电子: `ee.tsinghua.edu.cn`
- 北大: `pku.edu.cn`
- 上交: `sjtu.edu.cn`

这些页面能确认：专业、年级、班级、奖学金、学生工作、集体活动照片。

### Step 4: 微信公众号搜索（关键渠道）⭐ 最高优先级

**大量早期信息沉淀在学校/院系/社团的微信公众号文章里。** Google 已索引了相当多微信公众号内容。

**⚠️ 不要用 `site:mp.weixin.qq.com` 语法——在 opencli google search 中会报错。直接把 `mp.weixin.qq.com` 作为关键词嵌入 query：**

```
opencli google search "{CHINESE_NAME} {UNDERGRAD_SCHOOL} mp.weixin.qq.com" --limit 5 --lang zh -f md
opencli google search "{CHINESE_NAME} mp.weixin.qq.com" --limit 5 --lang zh -f md
```

典型微信公众号信息源：
- 院系公众号的"优秀毕业生"/"保研经验"专访
- 社团/学生会公众号的活动报道
- 高中母校公众号的"校友风采"
- 地方媒体公众号的"状元采访"/"竞赛获奖"
- 奖学金/人才计划公告

### Step 5: 高校 BBS / 论坛（含海外中文论坛）

**国内 BBS：**

水木社区对所有人可搜（清华/北大/各校校友都用）；cc98 和北大 BBS 仅对对应学校有效。

```
opencli google search "{CHINESE_NAME} site:newsmth.net" --limit 3 --lang zh -f md
```

仅在本科为浙大时执行：
```
opencli google search "{CHINESE_NAME} site:cc98.org" --limit 3 --lang zh -f md
```

仅在本科为北大时执行（注：Google 索引有限，低期望）：
```
opencli google search "{CHINESE_NAME} site:bbs.pku.edu.cn" --limit 3 --lang zh -f md
```

**海外中文论坛（对有海外经历的研究者必搜）：**

```
opencli google search "{CHINESE_NAME} site:newmitbbs.com OR site:mitbbs.com" --limit 5 --lang zh -f md
opencli google search "{CHINESE_NAME} site:1point3acres.com" --limit 5 --lang zh -f md
opencli google search "{CHINESE_NAME} site:muchong.com" --limit 3 --lang zh -f md
```

**为什么重要：** 论坛八卦帖里经常有 biographical tidbits。例如"宋舒然是北京人啊 101 中学毕业的"这种信息只存在于 newmitbbs 的讨论串里。一亩三分地有大量 PhD 申请/面试经验帖。小木虫有硕博讨论。

### Step 6: 非学术身份考古 ⭐ 新增高优先级

**一个人的非学术身份比他的论文列表更能揭示真实性格。** 本科期间的运动队、社团、创业、支教、文艺活动——这些信息散落在校级新闻、院系公众号、校运会记录里。

**⚠️ 如果 Phase 2h 已经用中文关键词搜索过运动/音乐/社团且有结果，此 step 仅补充 Phase 2h 未覆盖的校园特定场景（如校运会记录、院系运动会、校级文艺比赛、高中社团）。不要重复执行相同 query。**

```
opencli google search "{CHINESE_NAME} 校运会 OR 运动会 OR 大运会" --limit 5 --lang zh -f md
opencli google search "{CHINESE_NAME} {UNDERGRAD_SCHOOL} 社团 OR 学生会 OR 班长 OR 志愿者 OR 支教" --limit 5 --lang zh -f md
opencli google search "{CHINESE_NAME} 文艺 OR 话剧 OR 辩论 OR 演讲比赛" --limit 3 --lang zh -f md
```

如果 Step 1 中找到了高中名称，搜索高中母校公众号：
```
opencli google search "{HIGH_SCHOOL_NAME} {CHINESE_NAME} mp.weixin.qq.com" --limit 3 --lang zh -f md
```

**为什么重要：** "卢策吾代表学校参加2004年重庆市大运会400米接力亚军，两次校运会冠军"——这个信息来自母校校友报道，但 subagent 之前从未搜索过"运动会"相关关键词。这些细节对于构建性格画像至关重要。

### Step 7: 争议、八卦与负空间 ⭐ 新增

**"应该存在但不存在"本身就是信号。** 搜索负面/争议信息不是为了八卦，而是因为这些信息往往包含最真实的 biographical details。

```
opencli google search "{CHINESE_NAME} 争议 OR 质疑 OR 批评 OR 离职 OR 辞职" --limit 5 --lang zh -f md
opencli google search "如何评价 {CHINESE_NAME}" --limit 5 --lang zh -f md
opencli zhihu search "如何评价 {CHINESE_NAME}" --limit 5 -f md
```

**Note:** 搜到的争议信息需要标注可信度。论坛八卦的价值不在于"是否属实"，而在于"它提供了什么 biographical detail"（如学校、年龄、出身地等）。在报告中使用"据论坛讨论"而非"确认"。

### Step 8: Fetch 有价值的页面

For each promising result from Steps 1-7, **fetch the full page**. Look for:
- 高考班级合影、采访报道（性格描写极生动）
- 校友录、入学名单（确认学号、班级）
- 竞赛获奖名单（确认奖项级别）
- 保研/考研经验帖（心路历程）
- 社团活动照片/报道（非学术兴趣）
- 公众号专访（本人口述，最接近真实性格）
- 运动会记录、文艺比赛获奖
- 论坛讨论中的 biographical details

**⚠️ SNOWBALL: 每次 fetch 一个页面后，提取新线索，追加 1-2 次搜索。** 最好的发现来自第二跳或第三跳。

**→ UPDATE the report file now with Phase 3 findings before continuing.**

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
- 高中: [high school, city, graduation year] (if found)
- 中文名来源: [how you found the Chinese name]

## 性格信号

[Include subsections for each signal type found. Skip those not found.]

### PhD 致谢
> [Direct quote of revealing passages]
(来源: [URL])

### 知乎/博客/微博
- [Key findings, with links]

### 校友报道/人物专访
- [Key quotes from alumni stories, media profiles, award reports]
(来源: [URL])

### Rebuttal 风格
- [Paper title]: [characterization of rebuttal tone/style]
- [Direct quote of most characteristic line]

### 早期线索（中文）
- [Campus news, awards, competition results]

### 非学术身份
- [Sports: 田径队? 马拉松? 校运会记录?]
- [Arts: 乐队? 摄影? 书法?]
- [Social: 社团? 学生会? 创业? 支教?]
- [Content creation: B站? 公众号? Podcast?]

### 争议/八卦
- [Any controversies, forum discussions, with credibility notes]

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
- [Snowball leads that were discovered but not yet pursued]
```
