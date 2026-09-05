# Skills 第二轮处置清单 — 2026-09-05

审查基线：`b6aee12f8d23149d1ecfeed1ea1c60ed6c2adf0c`。原改革分支先快进到 main，再在隔离工作树实施。
清单按**文件处置**记录，不把“未改文件”或“静态通过”冒充真实模型验收。
具体回归、证据与未完成项见 [验证记录](2026-09-05-skill-capability-validation.md)。
本清单已包含 [LabMate/selfOS wiki 补改](2026-09-05-wiki-capability-followup.md)。

## 51 个公开入口

共享发现规则列出 51 个入口，而非 51 个无重名的全局注册名。
`todo` 与 `transcribe` 存在不同用途的入口，安装优先级保持兼容。

| 入口 | 审查后的处置与边界 |
| --- | --- |
| `skills/beamer-style/SKILL.md` | 保留主题和模板；尊重项目编译引擎、已有 profile 与目录。 |
| `skills/cc-navigator/SKILL.md` | 按文本/视觉/脚本能力路由；生态历史文章不作为强制操作。 |
| `skills/clone-web/SKILL.md` | 不再以 Playwright 为唯一前提；保留同视口与交互验收。 |
| `skills/flipradio-write-skill/flipradio-polish/SKILL.md` | 保留个人风格 rubric，去除工具名和逐建议重复审批。 |
| `skills/flipradio-write-skill/flipradio-write/SKILL.md` | 保留用户立场与文风，去除固定问答轮数和逐节等待。 |
| `skills/no-more-fomo/SKILL.md` | 保留 RSS/API、缓存和增量；媒体覆盖按需深入。 |
| `skills/paper-storyteller/SKILL.md` | 保留研究叙事知识；比喻、段落数和访谈轮数不再是门槛。 |
| `skills/paper-style/SKILL.md` | 保留配色/LaTeX/matplotlib 模板，初始化采用平台中立说明。 |
| `skills/research-slides/SKILL.md` | 保留 SD 默认 profile、黑白 Metropolis、知识结构和 PDF QA。 |
| `skills/swiss-knife-design/SKILL.md` | 保留个人视觉语言；具体用户/产物 profile 优先，不盲目覆盖。 |
| `skills/transcribe/SKILL.md` | 原生音频与可选 ASR 均可；字幕/音频不冒充视频观察。 |
| `skills/web-fetcher/SKILL.md` | 缩小触发；Markdown 兼容、JSON envelope、短文本与时间戳覆盖。 |
| `skills/weekly-report/SKILL.md` | 保留证据式周报文风；不强制委派或再确认已给计划。 |
| `skills/writing-agents/SKILL.md` | 保留 Claude 专属 schema；共享角色可普通子任务或主线程执行。 |
| `skills/yuanboizer-zh/SKILL.md` | 保留个人语气 rubric 与原文含义；未改写风格样例。 |
| `plugins/labmate/skills/analyze-experiment/SKILL.md` | 保留实验证据与对照判断；共享路由去强制委派。 |
| `plugins/labmate/skills/commit-changelog/SKILL.md` | 保留显式提交意图、精确暂存和 nested commit 顺序。 |
| `plugins/labmate/skills/init-project/SKILL.md` | 不因普通目录缺状态而自动初始化；保留幂等和双入口。 |
| `plugins/labmate/skills/monitor/SKILL.md` | 保留一次调用一次检查；调度、重试与杀进程另按任务授权。 |
| `plugins/labmate/skills/new-experiment/SKILL.md` | 保留 typed plan/apply/check、实验命名和状态格式。 |
| `plugins/labmate/skills/read-paper/SKILL.md` | 保留 paper packet 和页/公式/图表定位；继承已有保存意图，按指定项目/wiki 目的地保存。 |
| `plugins/labmate/skills/survey-literature/SKILL.md` | 按可用能力获取原文；综述结论须对应实际阅读覆盖。 |
| `plugins/labmate/skills/todo/SKILL.md` | 保留项目 TODO 数据格式与确定性接口。 |
| `plugins/labmate/skills/update-docs/SKILL.md` | 区分观察、用户表述、决策、假设与解决；按已授权目的地保存，不自动双写 wiki。 |
| `plugins/labmate/skills/update-knowhow/SKILL.md` | 显式归档，可独立执行；未解决调查可如实保存，不冒充已验证修复。 |
| `plugins/labmate/skills/update-project-skill/SKILL.md` | 按需只读扫描，主线程可执行；保留镜像与事实验证。 |
| `plugins/labmate/skills/visualize/SKILL.md` | 保留数值来源和实际渲染检查；共享角色路由按需委派。 |
| `plugins/meta-audit/SKILL.md` | 共享发现与描述解析；错误和审查信号分离，不以数量评级。 |
| `plugins/meta-audit/hook-recipes/SKILL.md` | 六个只读适配模板；删除通用配额、假拦截器及强制审批。 |
| `plugins/paper-review/SKILL.md` | 角色数量按风险；全文证据、当前 venue 表单、完整交付。 |
| `plugins/paper-review/review-review/SKILL.md` | 缺失证据列为未验证；不强制子 agent 或每字段等待。 |
| `plugins/papermate/skills/compile-check/SKILL.md` | 保留编译日志质量边界；默认 hook 仅当前调用真实诊断。 |
| `plugins/papermate/skills/figure-qa/SKILL.md` | 保留数据/可读性 QA；实际看图，尺寸规则是默认而非普适。 |
| `plugins/papermate/skills/paper-writing-qa/SKILL.md` | 按相关维度审查；无无差别字数/插图/禁词门槛。 |
| `plugins/papermate/skills/pre-submit-challenge/SKILL.md` | 保留 adversarial evidence review；不强凑问题和 reviewer 分数。 |
| `plugins/papermate/skills/section-guard/SKILL.md` | 保留 label/ref 检查；合法前向引用不再作为错误。 |
| `plugins/papermate/skills/sync-paper/SKILL.md` | 仅按提交/推送意图同步精确目标；内层干净不等于外层完成。 |
| `plugins/unbox-skills/unbox/SKILL.md` | 按未解问题研究；身份冲突重核、来源日期与媒体观察分开。 |
| `plugins/unbox-skills/unbox-graph/SKILL.md` | 去断链和重复脚本；显式 root、预览、保留数据、原子写。 |
| `plugins/unbox-skills/unbox-to-wiki/SKILL.md` | 选择性编译，原始证据溯源；不自动 commit。 |
| `projects/selfos/.claude/skills/academic-writing/SKILL.md` | 保留学术清晰度、含义和证据边界。 |
| `projects/selfos/.claude/skills/de-ai/SKILL.md` | 保留显式去味触发与原意，不引入新的写作声音。 |
| `projects/selfos/.claude/skills/digest/SKILL.md` | 只读且不扩大日期范围；跨月归档和未提交记录按证据区分。 |
| `projects/selfos/.claude/skills/interview/SKILL.md` | 保留一次一个问题与原话先存；去固定 CLI/轮数，不伪造 updated 或清除未解决项。 |
| `projects/selfos/.claude/skills/note/SKILL.md` | 保留 typed verbatim blocks 和生命周期；helper 显式 root 避免安装位置重定向。 |
| `projects/selfos/.claude/skills/paper-plot/SKILL.md` | 保留数据来源、绘图模板、统计和视觉检查。 |
| `projects/selfos/.claude/skills/thought/SKILL.md` | 保留原话、历史日期和重试身份；显式 root 优先，不自动推荐访谈。 |
| `projects/selfos/.claude/skills/todo/SKILL.md` | 保留 T/R 与归档格式；先归档后移出，恢复时按 ID/原文去重，不自动 ingest。 |
| `projects/selfos/.claude/skills/transcribe/SKILL.md` | 保留 ASR/原文/分析格式；遵从请求输出位置，仅授权 wiki 归档才写入该库。 |
| `projects/selfos/.claude/skills/wiki/SKILL.md` | 统一目标 root、只读/写入边界和多模态覆盖；原件/用户原话/分析分离，初始化中立，部分来源可重试。 |
| `projects/selfos/.claude/skills/wiki-help/SKILL.md` | 按宿主输出精简帮助，不假定 slash 语法或将导航变成执行。 |

## 工作区与供应商边界

- 主 checkout 中被忽略的 `.agents/skills/caveman/SKILL.md`：已审查，未复制、注册或改写。
  压缩模式不得覆盖用户所需的可读性/证据；持续激活及固定节省比例不能当成保证。
- 系统/第三方文件不修改。旧 web-fetcher 真实目录、writing-skills、
  agent-reach 双入口和旧导航框架的发现/执行冲突见
  [本机迁移清单](2026-09-05-installation-migration.md)。
- 所有宿主有效 metadata 保留。Claude allowed-tools 的现有文件读写、
  搜索和提问授权按用途保留，不把它们复制进共享正文，也不把调用 skill
  当作安装、发帖或推送的授权。
- read-paper 的现有 packet 字段、selfOS 数据 schema、SD profile 与既有产物保持；
  原研究档案、wiki、raw、增长材料没有改写。

## 逐资源处置

机器可复核版本见 [resource inventory](2026-09-05-skill-capability-resources.json)：
含路径、retain/rewrite/merge/delete、原因和现存内容 SHA256。
rewrite 也涵盖新增的执行/验证资源；保留不意味着每个后端都做过 live 测试。
历史文章和风格样例按来源参考保留，不继承其安装/强制工作流。
被引用的安装指南中的宿主路径是合法安装说明，因此审查提示不被消成零。

| 文件 | 处置 |
| --- | --- |
| `plugins/labmate/.agents/skills/project-skill/SKILL.md` | rewrite |
| `plugins/labmate/.claude/skills/project-skill/SKILL.md` | rewrite |
| `plugins/labmate/agents/domain-expert.md` | retain |
| `plugins/labmate/agents/exp-manager.md` | retain |
| `plugins/labmate/agents/project-advisor.md` | retain |
| `plugins/labmate/agents/slides-maker.md` | retain |
| `plugins/labmate/agents/viz-frontend.md` | retain |
| `plugins/labmate/hooks/arxiv-detect` | delete |
| `plugins/labmate/hooks/brainstorm-remind` | delete |
| `plugins/labmate/hooks/hook-utils` | rewrite |
| `plugins/labmate/hooks/hooks.json` | rewrite |
| `plugins/labmate/hooks/post-analyze-remind` | delete |
| `plugins/labmate/hooks/post-commit-changelog` | delete |
| `plugins/labmate/hooks/post-docs-remind` | delete |
| `plugins/labmate/hooks/post-knowhow-remind` | delete |
| `plugins/labmate/hooks/post-maintenance` | rewrite |
| `plugins/labmate/hooks/post-new-experiment-monitor` | delete |
| `plugins/labmate/hooks/post-read-paper-survey` | delete |
| `plugins/labmate/hooks/post-skill-stale` | delete |
| `plugins/labmate/hooks/pre-compact-archive` | delete |
| `plugins/labmate/hooks/pre-compact-remind` | delete |
| `plugins/labmate/hooks/pre-compact-summary` | rewrite |
| `plugins/labmate/hooks/run-hook.cmd` | retain |
| `plugins/labmate/hooks/session-start` | rewrite |
| `plugins/labmate/hooks/worktree-suggest` | rewrite |
| `plugins/labmate/references/agent-routing.md` | rewrite |
| `plugins/labmate/references/archival-contract.md` | rewrite |
| `plugins/labmate/references/check_agent_parity.sh` | rewrite |
| `plugins/labmate/references/download_results.sh` | rewrite |
| `plugins/labmate/references/experiment-template/README.md` | rewrite |
| `plugins/labmate/references/experiment-template/analyze.py` | retain |
| `plugins/labmate/references/experiment-template/config.yaml` | retain |
| `plugins/labmate/references/experiment-template/run.py` | retain |
| `plugins/labmate/references/gitignore-rules.md` | rewrite |
| `plugins/labmate/references/instruction-template-general.md` | retain |
| `plugins/labmate/references/instruction-template-research.md` | retain |
| `plugins/labmate/references/launch_exp.py` | rewrite |
| `plugins/labmate/references/monitor_exp.sh` | rewrite |
| `plugins/labmate/references/project-skill-template.md` | retain |
| `plugins/labmate/references/viewer-app.py` | retain |
| `plugins/labmate/references/viewer-static/index.html` | retain |
| `plugins/labmate/scripts/init_project.py` | rewrite |
| `plugins/labmate/scripts/lifecycle.py` | rewrite |
| `plugins/labmate/scripts/new_experiment.py` | retain |
| `plugins/labmate/scripts/project_snapshot.py` | retain |
| `plugins/labmate/scripts/release.sh` | rewrite |
| `plugins/labmate/scripts/sync-version.py` | retain |
| `plugins/labmate/scripts/todo.py` | retain |
| `plugins/labmate/skills/analyze-experiment/SKILL.md` | retain |
| `plugins/labmate/skills/analyze-experiment/agents/openai.yaml` | retain |
| `plugins/labmate/skills/commit-changelog/SKILL.md` | retain |
| `plugins/labmate/skills/commit-changelog/agents/openai.yaml` | retain |
| `plugins/labmate/skills/init-project/SKILL.md` | rewrite |
| `plugins/labmate/skills/init-project/agents/openai.yaml` | retain |
| `plugins/labmate/skills/monitor/SKILL.md` | retain |
| `plugins/labmate/skills/monitor/agents/openai.yaml` | retain |
| `plugins/labmate/skills/new-experiment/SKILL.md` | retain |
| `plugins/labmate/skills/new-experiment/agents/openai.yaml` | retain |
| `plugins/labmate/skills/read-paper/SKILL.md` | rewrite |
| `plugins/labmate/skills/read-paper/agents/openai.yaml` | retain |
| `plugins/labmate/skills/read-paper/references/paper-acquisition.md` | rewrite |
| `plugins/labmate/skills/read-paper/scripts/validate-paper-packet.py` | retain |
| `plugins/labmate/skills/survey-literature/SKILL.md` | rewrite |
| `plugins/labmate/skills/survey-literature/agents/openai.yaml` | retain |
| `plugins/labmate/skills/todo/SKILL.md` | retain |
| `plugins/labmate/skills/todo/agents/openai.yaml` | retain |
| `plugins/labmate/skills/update-docs/SKILL.md` | rewrite |
| `plugins/labmate/skills/update-knowhow/SKILL.md` | rewrite |
| `plugins/labmate/skills/update-knowhow/agents/openai.yaml` | retain |
| `plugins/labmate/skills/update-project-skill/SKILL.md` | rewrite |
| `plugins/labmate/skills/update-project-skill/agents/openai.yaml` | retain |
| `plugins/labmate/skills/visualize/SKILL.md` | retain |
| `plugins/labmate/skills/visualize/agents/openai.yaml` | retain |
| `plugins/labmate/slides/references/agent-slides.md` | rewrite |
| `plugins/labmate/slides/references/frontend-slides.md` | rewrite |
| `plugins/meta-audit/SKILL.md` | retain |
| `plugins/meta-audit/hook-recipes/SKILL.md` | rewrite |
| `plugins/meta-audit/references/context-engineering-rubric.md` | retain |
| `plugins/meta-audit/scripts/collect_claude.py` | rewrite |
| `plugins/meta-audit/scripts/context_audit.py` | rewrite |
| `plugins/meta-audit/scripts/skill_inventory.py` | rewrite |
| `plugins/paper-review/SKILL.md` | rewrite |
| `plugins/paper-review/references/review-workflow.md` | rewrite |
| `plugins/paper-review/references/role-templates.md` | rewrite |
| `plugins/paper-review/references/venue-formats.md` | rewrite |
| `plugins/paper-review/review-review/SKILL.md` | retain |
| `plugins/paper-review/review-review/references/audit-rubric.md` | rewrite |
| `plugins/papermate/agents/writing-reviewer.md` | retain |
| `plugins/papermate/hooks/hook-utils` | retain |
| `plugins/papermate/hooks/hooks.json` | rewrite |
| `plugins/papermate/hooks/post-compile-check` | rewrite |
| `plugins/papermate/hooks/post-plot-figure-qa` | delete |
| `plugins/papermate/hooks/post-section-change-guard` | delete |
| `plugins/papermate/hooks/post-tex-edit-sync-remind` | delete |
| `plugins/papermate/hooks/post-writing-qa-remind` | delete |
| `plugins/papermate/hooks/run-hook.cmd` | retain |
| `plugins/papermate/references/ai-flavor-patterns.md` | retain |
| `plugins/papermate/references/writing-qa-rubric.md` | rewrite |
| `plugins/papermate/scripts/compile_feedback.py` | rewrite |
| `plugins/papermate/skills/compile-check/SKILL.md` | retain |
| `plugins/papermate/skills/figure-qa/SKILL.md` | rewrite |
| `plugins/papermate/skills/paper-writing-qa/SKILL.md` | retain |
| `plugins/papermate/skills/pre-submit-challenge/SKILL.md` | rewrite |
| `plugins/papermate/skills/section-guard/SKILL.md` | rewrite |
| `plugins/papermate/skills/sync-paper/SKILL.md` | rewrite |
| `plugins/unbox-skills/scripts/graph_sync.py` | rewrite |
| `plugins/unbox-skills/unbox-graph/SKILL.md` | retain |
| `plugins/unbox-skills/unbox-graph/references/graph-contract.md` | rewrite |
| `plugins/unbox-skills/unbox-graph/references/sync-script.md` | rewrite |
| `plugins/unbox-skills/unbox-to-wiki/SKILL.md` | retain |
| `plugins/unbox-skills/unbox-to-wiki/references/compile-workflow.md` | rewrite |
| `plugins/unbox-skills/unbox-to-wiki/references/suggest-workflow.md` | rewrite |
| `plugins/unbox-skills/unbox-to-wiki/references/wiki-compiler-contract.md` | rewrite |
| `plugins/unbox-skills/unbox/SKILL.md` | retain |
| `plugins/unbox-skills/unbox/references/backfill-prompt.md` | rewrite |
| `plugins/unbox-skills/unbox/references/entity-subagent-prompt.md` | rewrite |
| `plugins/unbox-skills/unbox/references/merge-utils.md` | rewrite |
| `plugins/unbox-skills/unbox/references/runtime-contract.md` | rewrite |
| `plugins/unbox-skills/unbox/references/search-playbook.md` | rewrite |
| `plugins/unbox-skills/unbox/references/subagent-prompt.md` | rewrite |
| `projects/selfos/.claude/skills/academic-writing/SKILL.md` | retain |
| `projects/selfos/.claude/skills/academic-writing/references/style-rules.md` | retain |
| `projects/selfos/.claude/skills/de-ai/SKILL.md` | retain |
| `projects/selfos/.claude/skills/de-ai/references/rubric.md` | retain |
| `projects/selfos/.claude/skills/digest/SKILL.md` | rewrite |
| `projects/selfos/.claude/skills/digest/references/workflow.md` | rewrite |
| `projects/selfos/.claude/skills/interview/SKILL.md` | rewrite |
| `projects/selfos/.claude/skills/interview/references/interview-workflow.md` | rewrite |
| `projects/selfos/.claude/skills/interview/references/modes.md` | rewrite |
| `projects/selfos/.claude/skills/note/SKILL.md` | rewrite |
| `projects/selfos/.claude/skills/note/references/workflow.md` | rewrite |
| `projects/selfos/.claude/skills/paper-plot/SKILL.md` | retain |
| `projects/selfos/.claude/skills/paper-plot/references/templates.md` | retain |
| `projects/selfos/.claude/skills/paper-plot/templates/bar_vertical.py` | retain |
| `projects/selfos/.claude/skills/paper-plot/templates/style.py` | retain |
| `projects/selfos/.claude/skills/thought/SKILL.md` | rewrite |
| `projects/selfos/.claude/skills/thought/references/workflow.md` | rewrite |
| `projects/selfos/.claude/skills/todo/SKILL.md` | rewrite |
| `projects/selfos/.claude/skills/todo/references/add-workflow.md` | retain |
| `projects/selfos/.claude/skills/todo/references/done-workflow.md` | rewrite |
| `projects/selfos/.claude/skills/todo/references/list-workflow.md` | retain |
| `projects/selfos/.claude/skills/todo/references/today-workflow.md` | retain |
| `projects/selfos/.claude/skills/transcribe/SKILL.md` | rewrite |
| `projects/selfos/.claude/skills/transcribe/references/volcengine-asr.md` | rewrite |
| `projects/selfos/.claude/skills/transcribe/references/wiki-archive.md` | rewrite |
| `projects/selfos/.claude/skills/wiki-help/SKILL.md` | rewrite |
| `projects/selfos/.claude/skills/wiki/SKILL.md` | rewrite |
| `projects/selfos/.claude/skills/wiki/references/evidence-acquisition.md` | rewrite |
| `projects/selfos/.claude/skills/wiki/references/ingest-workflow.md` | rewrite |
| `projects/selfos/.claude/skills/wiki/references/lint-workflow.md` | rewrite |
| `projects/selfos/.claude/skills/wiki/references/page-templates.md` | rewrite |
| `projects/selfos/.claude/skills/wiki/references/query-workflow.md` | rewrite |
| `projects/selfos/.claude/skills/wiki/references/sync-workflow.md` | rewrite |
| `projects/selfos/.claude/skills/wiki/references/synthesize-workflow.md` | rewrite |
| `projects/selfos/.claude/skills/wiki/scripts/wiki-search.sh` | rewrite |
| `scripts/check_release.py` | rewrite |
| `scripts/context_audit.py` | retain |
| `scripts/generate_readme.py` | rewrite |
| `scripts/review_inventory.py` | rewrite |
| `scripts/skill_inventory.py` | rewrite |
| `scripts/validate_skills.py` | rewrite |
| `skills/beamer-style/SKILL.md` | retain |
| `skills/beamer-style/guides/guard.md` | rewrite |
| `skills/beamer-style/guides/init.md` | rewrite |
| `skills/beamer-style/templates/beamer-colors.tex` | retain |
| `skills/beamer-style/templates/layout-classic.tex` | retain |
| `skills/beamer-style/templates/layout-focus.tex` | retain |
| `skills/beamer-style/templates/layout-metropolis.tex` | retain |
| `skills/beamer-style/templates/layout-minimal.tex` | retain |
| `skills/beamer-style/templates/layout-research.tex` | retain |
| `skills/cc-navigator/SKILL.md` | retain |
| `skills/cc-navigator/references/anthropic-skills-official.md` | retain |
| `skills/cc-navigator/references/boris-cherny-cc-tips.md` | retain |
| `skills/cc-navigator/references/ecosystem-presentation.md` | rewrite |
| `skills/cc-navigator/references/ecosystem-web-access.md` | rewrite |
| `skills/cc-navigator/references/ecosystem-workflow.md` | rewrite |
| `skills/cc-navigator/references/jiahao-shao1-skills.md` | retain |
| `skills/cc-navigator/references/thariq-how-we-use-skills.md` | retain |
| `skills/cc-navigator/references/thariq-seeing-like-an-agent.md` | retain |
| `skills/cc-navigator/references/tw93-cc-architecture.md` | retain |
| `skills/clone-web/SKILL.md` | retain |
| `skills/clone-web/references/workflow.md` | rewrite |
| `skills/flipradio-write-skill/flipradio-polish/SKILL.md` | retain |
| `skills/flipradio-write-skill/flipradio-polish/references/rubric-and-workflow.md` | rewrite |
| `skills/flipradio-write-skill/flipradio-write/SKILL.md` | retain |
| `skills/flipradio-write-skill/flipradio-write/references/style-and-workflow.md` | rewrite |
| `skills/no-more-fomo/SKILL.md` | rewrite |
| `skills/no-more-fomo/references/phase2.md` | rewrite |
| `skills/no-more-fomo/references/process.md` | rewrite |
| `skills/no-more-fomo/references/sources.md` | rewrite |
| `skills/no-more-fomo/scripts/deploy.sh` | retain |
| `skills/no-more-fomo/template/digest.html` | retain |
| `skills/no-more-fomo/template/index.html` | retain |
| `skills/paper-storyteller/SKILL.md` | retain |
| `skills/paper-storyteller/references/brainstorm-protocol.md` | rewrite |
| `skills/paper-storyteller/references/sections/abstract.md` | rewrite |
| `skills/paper-storyteller/references/sections/conclusion.md` | rewrite |
| `skills/paper-storyteller/references/sections/experiments.md` | rewrite |
| `skills/paper-storyteller/references/sections/introduction.md` | rewrite |
| `skills/paper-storyteller/references/sections/method.md` | rewrite |
| `skills/paper-storyteller/references/sections/related-work.md` | rewrite |
| `skills/paper-storyteller/references/style-checklist.md` | rewrite |
| `skills/paper-storyteller/references/style-principles.md` | rewrite |
| `skills/paper-style/SKILL.md` | retain |
| `skills/paper-style/guides/guard.md` | rewrite |
| `skills/paper-style/guides/init.md` | rewrite |
| `skills/paper-style/guides/inject.md` | rewrite |
| `skills/paper-style/templates/academic.mplstyle` | retain |
| `skills/paper-style/templates/colors.tex` | retain |
| `skills/paper-style/templates/mystyle.cls` | retain |
| `skills/paper-style/templates/paper_palette.py` | retain |
| `skills/paper-style/templates/preamble.tex` | retain |
| `skills/research-slides/SKILL.md` | retain |
| `skills/research-slides/agents/openai.yaml` | retain |
| `skills/research-slides/references/citation-and-source-credit.md` | rewrite |
| `skills/research-slides/references/figure-extraction-workflow.md` | rewrite |
| `skills/research-slides/references/multi-agent-workflow.md` | rewrite |
| `skills/research-slides/references/paper-slide-patterns.md` | retain |
| `skills/research-slides/references/qa-workflow.md` | rewrite |
| `skills/research-slides/references/speculative-decoding-reference-profile.md` | retain |
| `skills/research-slides/references/story-modes.md` | retain |
| `skills/research-slides/references/visual-style.md` | retain |
| `skills/research-slides/references/worked-example.md` | retain |
| `skills/research-slides/references/writing-rules.md` | retain |
| `skills/research-slides/scripts/check_deck.py` | retain |
| `skills/research-slides/scripts/crop_whitespace.py` | retain |
| `skills/research-slides/scripts/init_research_deck.py` | retain |
| `skills/research-slides/scripts/render_check_pages.py` | retain |
| `skills/research-slides/scripts/test_template.py` | retain |
| `skills/swiss-knife-design/SKILL.md` | rewrite |
| `skills/swiss-knife-design/templates/base.css` | retain |
| `skills/swiss-knife-design/templates/design-tokens-override.css` | retain |
| `skills/swiss-knife-design/templates/tokens.json` | retain |
| `skills/transcribe/SKILL.md` | rewrite |
| `skills/transcribe/references/workflow.md` | rewrite |
| `skills/transcribe/scripts/transcribe.py` | retain |
| `skills/web-fetcher/SKILL.md` | rewrite |
| `skills/web-fetcher/references/capability-selection.md` | rewrite |
| `skills/web-fetcher/references/media-evidence.md` | rewrite |
| `skills/web-fetcher/references/routing-and-fallbacks.md` | merge |
| `skills/web-fetcher/references/source-adapters.md` | rewrite |
| `skills/web-fetcher/scripts/fetch.py` | rewrite |
| `skills/web-fetcher/scripts/test_fetch.py` | rewrite |
| `skills/weekly-report/SKILL.md` | retain |
| `skills/weekly-report/references/report-rubric.md` | rewrite |
| `skills/writing-agents/SKILL.md` | retain |
| `skills/writing-agents/references/claude-code-agents.md` | rewrite |
| `skills/writing-agents/references/host-adapters.md` | retain |
| `skills/yuanboizer-zh/SKILL.md` | retain |
| `skills/yuanboizer-zh/references/style-rubric.md` | retain |
| `tests/test-capability-refactor.sh` | rewrite |
| `tests/test-context-audit.sh` | rewrite |
| `tests/test-install.sh` | rewrite |
| `tests/test_context_audit.py` | rewrite |
