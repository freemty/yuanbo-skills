# Meta Audit — Benchmark Sources

Phase 2 外部基准查询的数据源清单。用 `gh api` 查询，缓存 7 天到 `~/.claude/audit-cache/benchmark.json`。

## 核心源（默认模式必查）

| 源 | 查什么 | 给什么信号 | 查询方式 |
|----|--------|-----------|---------|
| `obra/superpowers-marketplace` | plugins 列表 + 每个 plugin 的 skills 数 | P99 power user 的 skill/workflow 标杆 | `gh api repos/obra/superpowers-marketplace/git/trees/main?recursive=1` |
| `anthropics/skills` | 目录结构 + spec 版本 | 官方 skill 标准 + reference skill 数 | `gh api repos/anthropics/skills/git/trees/main?recursive=1` |
| `anthropics/claude-plugins-official` | marketplace 目录 plugins 数 | 官方生态规模 | `gh api repos/anthropics/claude-plugins-official/contents/plugins` |
| 本地 `~/.claude/plugins/installed_plugins.json` | 已装 plugin 数 + 版本 | 自身 plugin 覆盖率 | 直接读文件 |
| `affaan-m/everything-claude-code` | skills/ 目录 + stars | 社区 best practices 汇总规模 | `gh api repos/affaan-m/everything-claude-code` |

## 辅助源（--verbose 模式追加）

| 源 | 查什么 | 给什么信号 |
|----|--------|-----------|
| `ComposioHQ/awesome-claude-skills` | star 数 + README skill 列表 | 社区增速/热度 |
| showcase 配置（ChrisWiles 等） | settings.json 中 hooks/skills | 典型 power user 配置对标 |
| `openai/codex` | feature list + stars | 竞品能力对齐 |
| `nicepkg/claude-code-skill` | 索引的 skill 总数 | 生态广度（long tail） |

## 提取字段

每个源提取后归一化为：

```json
{
  "source": "obra/superpowers-marketplace",
  "stars": 160000,
  "skill_count": 42,
  "hook_count": 6,
  "plugin_count": 8,
  "has_headless": true,
  "has_multi_agent": true,
  "fetched_at": "2026-04-20T12:00:00Z"
}
```

## 统计基准计算

从核心源聚合后计算：

- **P50**: 所有源的中位数（skill_count, hook_count 等）
- **P99**: 取最大值（通常是 superpowers 或用户自身）
- **生态均值**: 去掉最高最低后的平均

## 缓存策略

- 路径: `~/.claude/audit-cache/benchmark.json`
- TTL: 7 天（`fetched_at` + 7d < now → 过期重拉）
- GFW/rate-limit fallback: 用过期缓存，报告中标注 "基准数据来自 {date} 缓存"
- 首次无缓存: 必须至少查一个核心源，否则 Phase 2 标记 "不可用"

## 认证

- 优先用 `gh api`（自带 `gh auth` token）
- 无 `gh` 环境: 无认证 REST API，60 req/h 限制，够用（核心源 5 次请求）
- 若全部失败: 跳过 Phase 2，标注原因
