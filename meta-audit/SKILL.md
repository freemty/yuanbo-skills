---
name: meta-audit
description: >
  Use when the user wants to assess their AI coding tool automation maturity,
  identify gaps vs ecosystem benchmarks, or decide what skills/hooks/workflows to build next.
  Triggers: "我的自动化水平怎么样", "我在哪个段位", "该优先建什么",
  "audit my setup", "how automated am I", monthly review, after major milestone.
---

# Meta Audit

从使用数据出发，对标外部生态基准，产出有证据的自动化成熟度定位 + 具体行动项。

## When to Use

- 每月定期审计 / 完成重大里程碑后
- 想知道"下一步该建什么"
- 感觉效率瓶颈但不确定瓶颈在哪

## When NOT to Use

- 日常 code review / 单次 session 回顾 / 纯项目进度检查

## Pipeline

1. **数据采集** — 本地 facets 解析 (sessions, friction_counts, goal_categories) + skill/hook/plugin 计数 + 30天 commit velocity
2. **外部基准** — `gh api` 查核心源 (superpowers-marketplace, anthropics/skills, everything-claude-code 等) 提取 skill/hook/plugin count。缓存 7 天。详见 `sources.md`。不可用则跳过并标注。
3. **分析定位** — L0-L5 打分 + 5轴雷达 + friction 根因映射
4. **输出报告** — Markdown 精简报告 + 存档到 `~/.claude/audit-history/{YYYY-MM-DD}.md`

## 成熟度模型 (L0-L5)

| Level | 定义 | 判定条件 |
|-------|------|---------|
| L0 Vanilla | 只用 CLAUDE.md | skills=0, hooks=0 |
| L1 Configured | 有 rules + 几个 skills | skills<15, hooks≤1 |
| L2 Skilled | 大量 skills，手动触发 | skills≥15, hooks<3 |
| L3 Hooked | skills + hooks + agents | hooks≥3, 有 project-level hooks |
| L4 Orchestrated | headless/cron + multi-agent | 有持久化 cron 或 GitHub Actions |
| L5 Autonomous | self-healing + meta-learning loop | 有 reflection pipeline |

## 雷达维度 (5 轴)

1. **Skill 宽度** — skill 数 / 生态 P99
2. **Hook 深度** — hook entries / 可用 event types (11)
3. **Headless 程度** — cron + CI/CD automation
4. **Multi-agent** — agent 定义数 + parallel dispatch
5. **Meta-learning** — reflection/self-improvement loop 存在性

## Friction → Action 映射

| Friction 类型 | 建议改进 |
|--------------|---------|
| wrong_approach 高 | PreToolUse guard hooks / CLAUDE.md constraints |
| buggy_code 高 | PostToolUse type-check hooks |
| tool_failure 高 | 环境 preflight skills |

## 报告结构

```
# Meta Audit — {date}
## 定位: L{N} (vs 前次 L{M})
## 雷达: 5维表 (分数 / 生态P50 / 差距)
## Top-3 Friction → Top-3 Action
## 与上次对比 (新增/改善/退步)
```

## 执行约束

- **不要自动执行改进** — 只输出建议，执行需人确认
- **facets 批量解析** — Python 处理，不要逐文件 Read
- **外部查询并行** — GitHub API 调用用 Agent 并行 spawn（用 `gh api` 或无认证 REST，注意 60 req/h 限制）
- **`--verbose`** — 输出完整 friction detail + benchmark 原始数据
- **`--quick`** — 跳过外部基准，只用本地数据

## Common Mistakes

| 错误 | 正确做法 |
|------|---------|
| 用"典型用户"做对比但无数据来源 | 引用具体 repo + star 数 |
| 把 skill 数量等同于成熟度 | L2→L3 关键是 hooks 不是 skills |
| 建议太多（10+ 行动项） | 最多 Top-3，focus 才能执行 |
| 对比数据过时 | 7 天 TTL 缓存，过期重新拉取 |
