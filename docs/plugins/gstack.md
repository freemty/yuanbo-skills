# gstack

- **Source:** [garrytan/gstack](https://github.com/garrytan/gstack)
- **Type:** Skill Collection
- **Category:** workflow
- **Stars:** 79.7K | **Forks:** 11.5K
- **License:** MIT
- **Tags:** sprint, review, qa, design, ship, browser, multi-agent

## 概述

Garry Tan（YC CEO）的 Claude Code 工具栈。23 个 skill 组成完整 sprint 流程：Think → Plan → Build → Review → Test → Ship → Reflect。核心理念：单人 + 正确工具 > 传统团队。

## 23 Skills（按阶段）

| Phase | Skill | Role | Function |
|-------|-------|------|----------|
| Think | /office-hours | YC Office Hours | 6 个 forcing questions，输出 design doc |
| Think | /plan-ceo-review | CEO | 4 modes: Expansion/Selective/Hold/Reduction |
| Plan | /plan-eng-review | Eng Manager | 架构、数据流、ASCII 图、edge cases |
| Plan | /plan-design-review | Senior Designer | 每个维度 0-10 评分，AI Slop 检测 |
| Plan | /plan-devex-review | DX Lead | 开发者 persona、TTHW benchmark |
| Plan | /design-consultation | Design Partner | 从零构建设计系统 |
| Build | /design-shotgun | Design Explorer | 4-6 AI mockup 变体 + taste memory |
| Build | /design-html | Design Engineer | Pretext 计算布局，30KB，零依赖 |
| Build | /autoplan | Review Pipeline | CEO → design → eng 自动串联 |
| Review | /review | Staff Engineer | 找 CI 通过但生产爆炸的 bug，auto-fix |
| Review | /codex | Second Opinion | OpenAI Codex 独立审查，cross-model 分析 |
| Review | /cso | CSO | OWASP Top 10 + STRIDE |
| Review | /investigate | Debugger | Iron Law: 无调查不修复 |
| Test | /qa | QA Lead | 真浏览器，找 bug → 修 → 生成回归测试 |
| Test | /qa-only | QA Reporter | 同上但只报告不改代码 |
| Test | /design-review | Designer Who Codes | 审计 + 修复，atomic commits |
| Test | /devex-review | DX Tester | 实测 onboarding，计时 TTHW |
| Test | /benchmark | Perf Engineer | Core Web Vitals、资源大小 |
| Ship | /ship | Release Engineer | sync main → tests → coverage → PR |
| Ship | /land-and-deploy | Release Engineer | merge → CI → verify production |
| Ship | /canary | SRE | 部署后监控循环 |
| Ship | /document-release | Tech Writer | 自动更新所有过时文档 |
| Reflect | /retro | Eng Manager | 周报、shipping streaks、per-person |
| Reflect | /learn | Memory | 跨 session 持久化学习 |

## Key Takeaways

- 真正的创新在系统层面（阶段架构 + 串联机制），不是单个 skill 的复杂度
- `/autoplan` 自动编排多个 review skill，是 "skill 组合 skill" 的标杆实现
- Checkpoint mode：WIP 自动提交 + `/context-restore` 恢复 session，解决长 session 断点续传
- `/design-shotgun` taste memory：学习用户设计偏好，5%/week 衰减防止过时
- `/pair-agent`：首个跨 AI vendor 浏览器协同（scoped tokens + tab isolation）
- Prompt injection defense：6 层防御（ML classifier + Haiku check + canary token + verdict combiner）
- 10+ AI agent 兼容（Claude/Codex/Cursor/Gemini/OpenClaw/Kiro/Factory/...）

## Relevance

- **`/research-sprint` 灵感：** 参考 `/autoplan` 做 文献 → 实验 → 分析 → 写作 的自动串联
- **Checkpoint 机制：** 对 labmate 长实验 session 和 paper-storyteller 长篇写作有实际价值
- **"Iron Law" 原则：** "无调查不修复" 直接适用于实验失败诊断（fars-autotrain）
- **`/document-release` 模式：** `/ship` 自动跑文档更新，yuanbo-skills 可以在提交时自动更新 README 表格
- **注意：** gstack 面向产品工程 sprint，yuanbo-skills 面向研究工作流，不要照搬产品侧的 design/QA/deploy 流程
