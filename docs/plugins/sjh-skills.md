# sjh-skills

- Source: https://github.com/jiahao-shao1/sjh-skills
- Category: peer skills repo（与 yuanbo-skills 同构的 research workflow skill collection）
- Relation: **replica** — 同样是个人 Claude Code skills monorepo，以研究者日常工作流为主线

## 一句话

Jiahao 的个人 skill 集合（15 个），围绕「发现论文 → 深读 → 做实验 → 记录 → 汇报」的 research workflow 组织；采用 plugin 形式通过 `/plugin marketplace` 分发，同时兼容 Codex 与 `npx skills`。

## 哲学 / Hardware

### 1. 按 research workflow 切 skill，不按工具切

skill 列表直接映射 researcher 的一天：

| 阶段 | Skill |
|------|-------|
| 发现 | `scholar-agent`（Scholar Inbox + NotebookLM 深读） |
| 深读 | `paper-analyzer`（causal chain：现象→实验设置→归因→解法） |
| 做实验 | `experiment-registry`（YAML + CLI 管 lifecycle）、`remote-cluster-agent`（Go daemon + rca CLI 操远程 GPU） |
| 记录 | `daily-summary`（sessions + commits + Notion timeline）、`notion-lifeos`（PARA + Make Time） |
| 协作 | `codex-review`（cross-model plan review，max 5 轮）、`handoff`（session 间 context 交接） |
| 基础设施 | `web-fetcher`（5 层 fallback：Jina → defuddle → markdown.new → OpenCLI → raw HTML）、`init-project`、`project-review`、`cmux`、`sync-docs`、`context-audit` |

对照 yuanbo-skills：我们的切法是「功能域」（yuanboizer-zh、weekly-report、web-fetcher），他按「研究阶段」切，因此每个 skill 都在链路里有明确上下游（scholar-agent 产出 → paper-analyzer 消费）。

### 2. Progressive disclosure 作为一等公民

有专门的 `context-audit` skill 审计三层架构（CLAUDE.md / rules / knowledge）的 progressive disclosure 合规性，检测：
- orphaned knowledge（没被索引）
- stale references（索引指向失效路径）
- CLAUDE.md index leakage（细节泄漏进 CLAUDE.md）

yuanbo-skills 的 `workflow.md` 只给了一条规则「文档必须进 CLAUDE.md 索引」，没有审计工具。值得抄。

### 3. Cross-model review 内置

`codex-review` skill 把「把方案丢给另一个模型审」做成了标准动作——不是偶发，而是默认流程的一部分。迭代上限 5 轮，防止无限来回。

对应 yuanbo-skills 里 meta-audit 的 `codex` plugin，但 sjh 把它提到了 workflow 核心位置。

### 4. Plugin 分发 > 手动 symlink

默认安装方式是 `/plugin marketplace add jiahao-shao1/sjh-skills`，plugin auto-updates from GitHub on startup。Codex 和 `npx skills` 是补充。

对照 yuanbo-skills：我们是 submodule + `install.sh` symlink 为主，plugin marketplace 作为 labmate-marketplace 的一部分。Sjh 的路线更干净，没有 submodule 管理成本。

### 5. 双入口但不重复

- `README.md` + `README.zh-CN.md`（英中双语）
- `AGENTS.md` vs `CLAUDE.md`（Codex vs Claude Code 各自入口，对应不同工具的 convention）
- `.codex/INSTALL.md` 是 Codex 安装的 self-contained 指令入口，用户只需 tell Codex："Fetch and follow …"

## 与 yuanbo-skills 的差异速查

| 维度 | sjh-skills | yuanbo-skills |
|------|-----------|---------------|
| 组织 | 纯 skill/（扁平），无 plugin/projects 分层 | skills/ + plugins/ + projects/（按类型分三层） |
| 分发 | plugin marketplace 为主 | submodule + install.sh symlink 为主 |
| skill 切法 | research workflow stage | 功能域 |
| 上游 benchmark | 无显式 audit skill | meta-audit plugin（对标 superpowers/gstack 等） |
| Codex 支持 | `.codex/INSTALL.md` self-contained | `docs/guides/codex-support.md` |
| Context 治理 | `context-audit` skill 做三层审计 | CLAUDE.md 索引约定（无 audit 工具） |

## 可借鉴点（待办）

1. **`context-audit` 等价物** — yuanbo-skills 可以加一个 skill 审计 `docs/` 索引与实际文件的一致性（目前只有 `find` 命令查 broken symlinks）。
2. **按 workflow 重排 landscape** — `docs/plugins/landscape.md` 目前按「plugins / third-party skills / MCP」切，可以加一栏「research workflow stage」映射。
3. **Plugin marketplace 分发** — 把 inline skills（web-fetcher、weekly-report、yuanboizer-zh）通过 labmate-marketplace 发布，减少用户手动 symlink。
4. **`handoff` skill** — session 交接输出结构化 context summary，比 `context-save` 更轻量（不落盘，直接打印）。

## Meta-audit 联动

sjh-skills 已加入 `plugins/meta-audit/sources.md` 作为 peer repo benchmark（Supplementary 层），用于衡量 yuanbo-skills 相对同类 researcher-facing skills 集合的覆盖率。
