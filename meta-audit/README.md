# meta-audit

AI coding tool 自动化成熟度审计。从本地使用数据 + 外部生态基准出发，产出 L0-L5 定位 + 5 轴雷达 + Top-3 行动项。

## Features

- **L0-L5 成熟度模型** — 基于 skills/hooks/headless/multi-agent/meta-learning 五维评估
- **外部基准对标** — GitHub API 查询 top repos (superpowers, awesome-claude-skills 等) 作为 P50/P99 参照
- **Friction → Action 映射** — 从 session facets 提取 friction 根因，映射到具体改进建议
- **历史趋势追踪** — 报告存档到 `~/.claude/audit-history/`，支持跨月对比
- **`--quick` / `--verbose` 模式** — 灵活控制深度

## Usage

```
/meta-audit              # 完整审计（含外部基准）
/meta-audit --quick      # 跳过外部基准，只用本地数据
/meta-audit --verbose    # 输出完整 friction detail + benchmark 原始数据
```

## Triggers

- "我的自动化水平怎么样"
- "我在哪个段位"
- "该优先建什么"
- "audit my setup"
- "how automated am I"
- 月度定期 / 里程碑完成后

## Output Example

```markdown
# Meta Audit — 2026-04-20

## 定位: L3 Hooked (前次 L2, +1)

## 雷达
| 维度 | 分数 | 生态 P50 | 差距 |
|------|------|---------|------|
| Skill 宽度 | 83 | 15 | +68 (top 1%) |
| Hook 深度 | 7/11 | 3/11 | +4 |
| Headless | 1 | 0 | +1 |
| Multi-agent | 6 | 2 | +4 |
| Meta-learning | ✅ | ❌ | — |

## Top-3 Friction → Top-3 Action
1. buggy_code (94x) → PostToolUse pyright/ruff hook
2. wrong_approach (78x) → PreToolUse constraint guards
3. tool_failure (23x) → 环境 preflight skill

## 与上次对比
- 新增: 4 hooks, reflection pipeline
- 改善: Hook 深度 0→7
- 退步: —
```

## Install

Already included in [yuanbo-skills](https://github.com/freemty/yuanbo-skills). If standalone:

```bash
# Symlink into Claude Code skills directory
ln -s /path/to/meta-audit ~/.claude/skills/meta-audit
```

## License

MIT
