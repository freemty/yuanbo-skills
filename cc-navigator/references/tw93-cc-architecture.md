# Tw93: 你不知道的 Claude Code -- 架构、治理与工程实践

> Source: https://x.com/HiTw93/status/2032091246588518683
> Author: Tw93 (@HiTw93)
> Date: 2026-03-12

## 起源

源于半年深度使用 Claude Code、两个账号每月 40 刀氪金的踩坑经验。刚开始当 ChatBot 用，后来发现：上下文越来越乱、工具越来越多但效果越来越差、规则越写越长却越不遵守。研究了 Claude Code 本身之后才意识到，这不是 Prompt 问题，而是这套系统的设计就是这样的。

## 六层架构

把 Claude Code 拆成六层来看：

只强化其中一层，系统就会失衡：CLAUDE.md 写太长，上下文先污染自己了；工具堆太多了，选择就搞不清楚了；subagents 开得到处都是，状态就漂移了；验证这步跳过了，出了问题根本不知道是哪里挂的。

## 核心循环

Claude Code 的核心不是"回答"，而是一个反复循环的代理过程：

```
收集上下文 -> 采取行动 -> 验证结果 -> [完成 or 回到收集]
     ^                    v
  CLAUDE.md          Hooks / 权限 / 沙箱
  Skills             Tools / MCP
  Memory
```

卡住的地方几乎从来不是模型不够聪明，更多时候是给了它错误的上下文，或者写出来了但根本没法判断对不对，也没法撤回。

## 扩展系统选择

- 给 Claude 新动作能力用 Tool/MCP
- 给它一套工作方法用 Skill
- 需要隔离执行环境用 Subagent
- 要强制约束和审计用 Hook
- 跨项目分发用 Plugin

## 上下文治理

很多人把上下文当"容量问题"，但卡住的地方通常不是不够长，而是太吵了，有用的信息被大量无关内容淹没了。

### 200K 上下文的真实可用空间

```
200K 总上下文
+-- 固定开销 (~15-20K)
|   +-- 系统指令: ~2K
|   +-- 所有启用的 Skill 描述符: ~1-5K
|   +-- MCP Server 工具定义: ~10-20K  <- 最大隐形杀手
|   +-- LSP 状态: ~2-5K
|
+-- 半固定 (~5-10K)
|   +-- CLAUDE.md: ~2-5K
|   +-- Memory: ~1-2K
|
+-- 动态可用 (~160-180K)
    +-- 对话历史
    +-- 文件内容
    +-- 工具调用结果
```

一个典型 MCP Server（如 GitHub）包含 20-30 个工具定义，每个约 200 tokens，合计 4,000-6,000 tokens。接 5 个 Server，光这部分固定开销就到了 25,000 tokens（12.5%）。

### 加载分层策略

```
始终常驻    -> CLAUDE.md：项目契约 / 构建命令 / 禁止事项
按路径加载  -> rules：语言 / 目录 / 文件类型特定规则
按需加载    -> Skills：工作流 / 领域知识
隔离加载    -> Subagents：大量探索 / 并行研究
不进上下文  -> Hooks：确定性脚本 / 审计 / 阻断
```

偶尔用的东西就不要每次都加载进来。

### CLAUDE.md 最佳实践

- 保持短、硬、可执行，优先写命令、约束、架构边界。Anthropic 官方自己的 CLAUDE.md 大约只有 2.5K tokens
- 把大型参考文档拆到 Skills 的 supporting files，不要塞进 SKILL.md 正文
- 使用 .claude/rules/ 做路径/语言规则，不让根 CLAUDE.md 承担所有差异
- 长会话主动用 /context 观察消耗，不要等系统自动压缩后再补救

### 会话管理

- 任务切换优先 /clear，同一任务进入新阶段用 /compact
- 把 Compact Instructions 写进 CLAUDE.md，压缩后必须保留什么由你控制，不由算法猜

### Tool Output 噪声

cargo test 一次完整输出动辄几千行，git log、find、grep 在稍大的仓库里也能轻松塞满屏幕。这些输出 Claude 并不需要全看，但只要它出现在上下文里，就是实实在在的 token 消耗。

RTK (Result Toolkit) 的思路：在命令输出到 Claude 之前自动过滤，只留决策需要的核心信息。比如 cargo test：

```
# 原始输出：几千行
# RTK 之后：
  cargo test: 262 passed (1 suite, 0.08s)
```

### 自动压缩的陷阱

默认压缩算法按"可重新读取"判断，早期的 Tool Output 和文件内容会被优先删掉，顺带把架构决策和约束理由也一起扔了。解决方案：

```markdown
## Compact Instructions

When compressing, preserve in priority order:

1. Architecture decisions (NEVER summarize)
2. Modified files and their key changes
3. Current verification status (pass/fail)
4. Open TODOs and rollback notes
5. Tool outputs (can delete, keep pass/fail only)
```

### HANDOFF.md

更主动的方案：在开新会话前，先让 Claude 写一份 HANDOFF.md，把当前进度、尝试过什么、哪些走通了、哪些是死路、下一步该做什么写清楚。下一个 Claude 实例只读这个文件就能接着做，不依赖压缩算法的摘要质量。

## Plan Mode

核心是把探索和执行拆开，探索阶段不动文件，确认方案后再执行：

- 探索阶段以只读操作为主
- Claude 可以先澄清目标和边界，再提交具体方案
- 执行成本在计划确认之后才发生

按两下 Shift+Tab 进入 Plan Mode。进阶玩法是开一个 Claude 写计划，再开一个 Codex 以"高级工程师"身份审这个计划。

## Skills 设计原则

### 描述符优化

每个启用的 Skill，描述符常驻上下文：

```yaml
# 低效（~45 tokens）
description: |
  This skill helps you review code changes in Rust projects.
  It checks for common issues like unsafe code, error handling...
  Use this when you want to ensure code quality before merging.

# 高效（~9 tokens）
description: Use for PR reviews with focus on correctness.
```

### 描述的正确写法

- 描述要让模型知道"何时该用我"，而不是"我是干什么的"
- 有完整步骤、输入、输出和停止条件
- 正文只放导航和核心约束，大资料拆到 supporting files
- 有副作用的 Skill 要显式设置 disable-model-invocation: true

### disable-auto-invoke 策略

- 高频（>1 次/会话） -> 保持 auto-invoke，优化描述符
- 低频（<1 次/会话） -> disable-auto-invoke，手动触发
- 极低频（<1 次/月） -> 移除 Skill，改为文档

### Skill 结构示例

```
.claude/skills/
+-- incident-triage/
    +-- SKILL.md
    +-- runbook.md
    +-- examples.md
    +-- scripts/
        +-- collect-context.sh
```

### Skill 类型

类型一：检查清单型（质量门禁） -- 发布前跑一遍确保不漏项

类型二：工作流型（标准化操作） -- 显式调用 + 内置回滚步骤

类型三：领域专家型（封装决策框架） -- 按固定路径收集证据

### 常见错误

- 描述过短：description: help with backend（任何后端工作都能触发）
- 正文过长：几百行工作手册全塞进 SKILL.md 正文
- 一个 Skill 覆盖 review、deploy、debug、docs、incident 五件事
- 有副作用的 Skill 允许模型自动调用

## 工具设计原则

给 Claude 的工具和给人写的 API 不是一回事。给人用的 API 往往追求功能齐全，但给 agent 用，重点不是功能堆得多完整，而是让它更容易用对。
