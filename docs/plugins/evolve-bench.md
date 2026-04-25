# evolve_bench

- Source: https://github.com/Sisyphe-lee/evolve_bench
- Category: research harness reference（不是 skill/plugin，是一个完整的 AI-driven research project 的 harness 范本）
- Relation: **hardware behind the replica** — yuanbo-skills 里 labmate、fars-autotrain、fars-reviewer、hle-solver 这类 research agent 系统的参考实现

## 一句话

EvolveBench 是 VLA benchmark 的 diagnosis-guided evolution pipeline；但**真正值得归档的不是 benchmark 逻辑，而是它下面那套 agent harness**——一个被作者显式设计为「可迁移到任意 research 项目」的 session + evidence + orchestrator 框架。

README 自己就承认：

> Copy `harness/` — protocols are project-agnostic
> Rewrite `research/spec/` — define your project's schemas
> Initialize `research/memory/` — empty task board, config, state files
> Adapt `.claude/skills/` — keep report/review/direction
> Write `CLAUDE.md` — hard rules + navigation

这正是 fars-autotrain / hle-solver 这些项目一直在摸索的：**如何让 Claude Code session 成为可 cold-start、可并行、可交接的 research unit**。

## 三条设计哲学（README 原文）

### 1. Light entry, many pointers

> `CLAUDE.md` contains only hard rules and navigation tables. Details live in protocol files, specs, and memory. An agent always has a stable entry point.

CLAUDE.md 不写内容，只写「硬规则 + 去哪找细节」。Agent 每次进场读一个极小的 CLAUDE.md，然后按任务类型跳到对应的 protocol / spec / memory 文件。

对照 yuanbo-skills 自己的 CLAUDE.md：目前还在把 "Common Operations" 命令塞进 CLAUDE.md，算是中间态。进一步可以把命令迁到 `docs/guides/ops.md` 再从 CLAUDE.md 指向它。

### 2. Two-stage closure

> Experiment sessions record observations (`/report`). Coordinator sessions absorb results across runs (`/review`). Run-level observations never directly become global conclusions.

**单次实验 session 不直接改动全局结论**。它只写自己的 `report.md`。只有 coordinator session 在读完 2-3 个 report 之后，才更新 `task_board.md` 和 hypothesis 状态。

这是对 "single agent 直接改全局 memory" 的反模式——防止单次抖动污染长期记忆。对应到 fars / labmate 里：每个 experiment session 应该只写自己的 run 目录，review session 做汇总。

### 3. File is state

> All scheduling, experiment, and review state lives in files (JSON, markdown). Any session can cold-start from files alone. No in-memory state survives session boundaries.

Session 可以随时被 kill、重启、迁移到另一台机。所有 scheduling / lock / 进度都在文件里（`dispatch_state.json`、`task_board.md`、`status.json`）。

对应到 labmate/fars：目前 running-exp tracker 已经是 file-based，但是 orchestrator 层（谁在跑什么、谁在 review）还缺这套 protocol。

## Harness 目录结构（可直接抄）

```
CLAUDE.md                    # 硬规则 + 导航
harness/
  protocols/                 # 项目无关的 agent 协议
    session_lifecycle.md     # session 生命周期：创建 run 目录 → 跑实验 → 写 report → /report 关闭
    evidence_chain.md        # 每个 run 必须产出 report.md + status.json + artifacts
    coordinator.md           # review/direction session 怎么工作
    operations.md            # tmux / orchestrator / GPU lock 等实操
    design_principles.md     # 上面三条哲学的展开
    sub_agent_contract.md    # 主 session 与 subagent 之间的输入输出契约
  decisions.md               # 决策日志：tension、rejected alternatives、重访触发条件
.claude/skills/
  report/                    # run-level 关闭
  review/                    # cross-run 吸收
  direction/                 # 战略层审计（phase 完成或异常时）
  orchestrate/               # tmux 多 session 自动调度
research/
  spec/                      # 项目专属：benchmark protocol、failure taxonomy、hypotheses
  memory/                    # 运行态：task_board.md、dispatch_state.json、current_config.md
  runs/rNN_description/      # 每次实验独立目录
    report.md                # YAML frontmatter (run_id/task_ref/hypothesis/status/verdict/key_metrics) + 叙事 + Lessons
    status.json              # 结构化完成信号（orchestrator 读它）
    *.json / *.jsonl         # artifacts
  infrastructure/            # 程序化保证，不依赖 prompt 纪律
    validate_report.py       # report.md 完整性检查（YAML 字段、必要章节、Lessons、artifacts）
    next_run.sh              # 原子 run ID 分配（mkdir POSIX atomic）
    coordinator/runtime.py   # GPU lock manager（auto-claim / cleanup / snapshot）
    coordinator/worktree.py  # git worktree 隔离高危源码改动
    infra_utils.py           # 原子 JSON 写、UTC 时间戳、git rev
  retro/                     # 回溯
```

关键原则：**programmatic tools > prompt discipline**。`validate_report.py` 是 gate，不是建议；`next_run.sh` 靠 POSIX `mkdir` 原子性防并发；GPU lock 用文件锁而非 prompt 约定。

## Hard Rules（值得全文抄）

> 0. Absolute honesty — never write that something was done if it wasn't
> 1. Respond in Chinese
> 2. Never delete key research assets without explicit permission
> 3. Core source modifications go through worktree isolation
> 4. Never kill other sessions' processes
> 5. Release resources after experiments
> 6. First action in a session: create run directory and report.md
> 7. Results claims must include full context (model, round, seed, episodes)
> 8. Session must reach a closed conclusion: accept, reject, downgrade, or explicit next step

规则 0、3、4、6、8 特别关键：

- **规则 0**（honesty）和 fars-reviewer 的 integrity audit 同根同源。
- **规则 3**（worktree isolation）— 改核心代码一律走 git worktree，防止实验 session 污染主分支。
- **规则 4**（不杀别人进程）— 多 session 共存的硬底线。
- **规则 6**（首动作建 run 目录）— 保证 "file is state" 从一开始就成立。
- **规则 8**（必须 closed conclusion）— session 不能无结论结束，accept/reject/downgrade/next step 四选一。

## Orchestrator 模式

> Orchestrator reads task_board.md → tmux new-window → launches worker Claude sessions
> polls status.json every 10 min → detects completion
> triggers /review after 2-3 experiments → triggers /direction on phase completion
> self-replaces when context grows heavy

几个关键属性：
- **Opt-in overlay** — 不启动 orchestrator 一切手动也能跑
- **Zero new constraints** — 给 `/report` 加了一个 `status.json` 输出，仅此而已
- **Max 3 parallel workers**，GPU 分配下放给 worker 自己调 `runtime.py`
- **Self-replace** — 当 orchestrator session context 变重，它会 spawn 一个新 orchestrator 接班

对照 labmate 的 exp-manager agent：目前是被动查询（"帮我看下实验"），evolve_bench 的 orchestrator 是主动轮询 + 触发。

## Decision Log（值得照做）

`harness/decisions.md` 记录每个设计决策的：
- **tension that prompted the decision**（为什么要决策）
- **rejected alternatives and why**（为什么没选别的）
- **trigger conditions for revisiting**（什么时候重新考虑）

这比 ADR 更 agent-friendly——未来 agent 能判断当前情况是否满足 "revisit trigger"。

## 可借鉴点（面向 yuanbo-skills / labmate / fars-* 的落地清单）

1. **把 harness/ 作为 labmate plugin 的核心模块** — 目前 labmate 偏 agent 和 hook，缺 harness 层（protocols + evidence chain + orchestrator）。可以把 evolve_bench/harness/ 作为模板引入。
2. **`report.md` + `status.json` 双文件约定** — fars-autotrain 的 run 目录目前只有 ad-hoc 输出，应统一到这套结构，让 orchestrator / reviewer 能机读。
3. **`validate_report.py` 等价物** — 作为 report skill 的 gate，而不是 prompt 里写「请包含以下字段」。
4. **Hard Rules 进 CLAUDE.md** — yuanbo-skills 目前 rules 散落在 `~/.claude/rules/*.md`，可以把这 8 条规则的等价物提到每个 research 项目的 CLAUDE.md 顶部。
5. **Worktree isolation for core edits** — 已经有 superpowers:using-git-worktrees skill，可以绑定到「改 core 代码」的自动触发。
6. **Decision log 格式统一** — yuanbo-skills 当前 CHANGELOG 偏「做了什么」，可以加 `docs/decisions.md` 记「为什么选 X 不选 Y + 何时 revisit」。

## Meta-audit 联动

evolve_bench 不是 skill benchmark（它不按 skill-per-feature 组织），而是 **research harness benchmark**。建议在 `plugins/meta-audit/sources.md` 里新开一类 "Research Harness Benchmarks"，把它和未来的 AReaL、Superpowers-for-research 放一起——这类 repo 衡量的不是「skill 覆盖率」，而是「session 生命周期成熟度」。
