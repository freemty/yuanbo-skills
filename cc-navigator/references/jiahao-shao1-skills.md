# jiahao-shao1 Skills Ecosystem

Source: https://github.com/jiahao-shao1

研究者型 Claude Code 用户，专注学术研究工作流自动化。5 个核心 skill + 2 个独立项目，覆盖从论文发现到 GPU 集群管理的完整研究链路。

## sjh-skills 主仓库 (5 skills)

https://github.com/jiahao-shao1/sjh-skills

| Skill | 用途 | 亮点 |
|-------|------|------|
| **scholar-agent** | 论文发现 + 深度阅读 | Scholar Inbox 个性化推荐 + NotebookLM 无幻觉分析，~500 token/query vs ~50K/paper |
| **cmux** | 终端多 agent 编排 | Ghostty 分屏 + 子 Claude Code 实例 + 内嵌浏览器 + markdown 渲染 |
| **daily-summary** | 每日工作总结 | 聚合 CC sessions + git commits + Notion tasks → 中文时间线报告 |
| **notion-lifeos** | PARA 生活管理 | Notion API 实现任务/笔记/日志的自然语言操作 |
| **web-fetcher** | URL 内容提取 | 五级降级：Jina Reader → defuddle.md → markdown.new → OpenCLI → raw HTML |

## 独立项目

### remote-cluster-agent (3 stars)

https://github.com/jiahao-shao1/remote-cluster-agent

让 Claude Code 操作远程 GPU 集群的 MCP server。核心设计：

- **双模式路由**: Agent 模式 (~0.1s, 持久 SSH + JSON-Lines 协议) / Sentinel 模式 (~1.5s, per-command SSH)
- **零依赖 agent**: 集群端 ~100 行 Python，无需安装任何包
- **Mutagen 实时同步**: 本地编辑 → 即时同步 → 远程执行 → 结果回传
- **多节点管理**: 通过 `node` 参数路由到不同 GPU 节点

工作流: edit locally → sync instantly → run remotely → read results locally

### scholar-inbox (独立 CLI + SDK)

https://github.com/jiahao-shao1/scholar-inbox

Scholar Inbox 逆向 API 的 Python 客户端：
- `scholar-inbox digest` — 每日个性化论文推荐
- `scholar-inbox rate` — 评分反馈优化推荐
- `scholar-inbox collections` — 论文集合管理
- `scholar-inbox trending` — 热门论文发现
- 支持 JSON 输出，可被其他 agent 调用

## 设计模式值得参考

### 1. 研究工作流闭环
```
论文发现 (scholar-agent)
  → 深度阅读 (NotebookLM)
  → 实验执行 (remote-cluster-agent)
  → 日志同步 (Mutagen)
  → 工作总结 (daily-summary)
  → 任务管理 (notion-lifeos)
```

### 2. 五级降级策略 (web-fetcher)
不依赖单一服务，多层 fallback 保证可用性。与 baoyu-url-to-markdown 的 Chrome CDP 方式互补。

### 3. 双模式 MCP (remote-cluster-agent)
Agent 模式追求速度 (0.1s)，Sentinel 模式保证可靠性 (1.5s)。自动降级，无需用户干预。

### 4. 零依赖远程部署
集群端 agent 仅 ~100 行 Python + stdlib，解决了 GPU 服务器环境受限的问题。

## 与我们现有 skill 的对比

| 需求 | jiahao-shao1 | 我们已有 |
|------|-------------|---------|
| 论文阅读 | scholar-agent (Scholar Inbox + NotebookLM) | notebooklm skill, rope2sink |
| GPU 集群 | remote-cluster-agent (MCP + Mutagen) | server-setup, fars-autotrain |
| 终端编排 | cmux | cmux (同源) |
| 每日总结 | daily-summary | no-more-fomo (偏新闻) |
| 生活管理 | notion-lifeos | notion-lifeos (同源) |
| 网页抓取 | web-fetcher (5 级降级) | agent-reach, WebFetch |
| 工作流导航 | 无 | cc-navigator |

## 推荐关注

1. **remote-cluster-agent** — 最独特的贡献，解决了 CC 远程执行的核心痛点
2. **scholar-agent** — Scholar Inbox + NotebookLM 的组合思路有启发
3. **web-fetcher 五级降级** — 多源 fallback 是好的工程模式
4. **daily-summary** — 多数据源聚合的思路可以复用
