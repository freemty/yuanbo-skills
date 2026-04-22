---
name: weekly-report
description: >
  Use when user asks for a weekly progress report for their manager.
  Triggers: 周报, weekly report, 写周报, 本周进展, 汇报.
---

# Weekly Report — 向上汇报式周报

## 核心原则

**写给领导看的 bullet points，不是写给自己的工作日志。**

每条 bullet 要有动机（为什么做）+ 成果（做到什么程度）+ 来源（设计文档/实验目录/链接）。

## 周期

每周四下午为截止点。当前周报范围 = 上周四 → 本周四。

## 执行步骤

### Step 1：确定扫描范围

如果用户指定了项目列表，用指定的。否则问用户要扫描哪些 repo。

### Step 2：批量收集 git 数据

用 Agent（general-purpose）并行扫描所有目标仓库：

```
对每个 repo 执行：
git log --oneline --since="<上周四>" --until="<本周四>"
git log --since="<上周四>" --until="<本周四>" --stat
```

子仓库也要检查（如 monorepo 下的子目录）。无 commit 的 repo 跳过。

### Step 3：补充证据来源

对有 commit 的项目，进一步查找：
- 设计文档：`docs/specs/*design*`
- 实验目录：`exp/`
- changelog / 版本记录
- localhost demo 链接（如有）

每条进展都需要挂一个来源。

### Step 4：写周报

#### 标题风格

项目标题用**编号 + 英文短语**，不用中文：

```
### 1. Integrity Review — fars-reviewer
### 2. Optimize Anything — hle-solver
### 3. Autotrain on PostTrainBench
```

#### 每条 bullet 的写法

**先说动机/问题，再说方案和结果**，不是干列成果：

```markdown
# 好：有动机
- 现在 review 条目太多 + context 过长：把可以解耦的拆成 3-agent 并行审计 pipeline

# 坏：干列成果
- 3-agent 并行审计 pipeline 上线
```

**可以带思考性备注**（问号结尾），表达未定结论：

```markdown
- 发现 agent 会先学习 general skill（写文档、搜索），后面演化出知识性 skill（化学、生物）→ 理想情况下的 skill evolve 最好不演化知识？
```

#### 保留什么

- 实验完成 + 关键结果数字
- 新系统/pipeline 上线（带动机说明）
- 设计文档产出（挂路径）
- 关键技术发现或思考（可带问号）
- benchmark 构建完成
- localhost demo 链接

#### 砍掉什么

- 初始化 / 搭骨架 / init skeleton
- 精读论文（改为「梳理相关工作」+ 结论）
- README 改写 / 文档格式调整
- dashboard / leaderboard（除非是交付物）
- 代码重构 / cleanup

#### 实验命名规则

每个实验 ID 必须附带短名解释：
`expID（agents × model，时长，benchmark）`

#### 文风要求

- 中英混写自然切换，不强求全中文
- 不用「此外」「值得注意的是」「显著提升」
- 不加总结段、不加过渡句
- 数字具体：87% 而不是「取得良好效果」
- 来源挂句尾：设计文档用 `（docs/specs/xxx.md）`，demo 用 http://localhost:xxxx/
- 子 bullet 可以写补充想法，不用严格格式

### Step 5：架构图（仅限新设计）

新系统/pipeline 用 ASCII 框图，作为对应条目下的 `<details>` 可折叠项，不单独成章节。

```markdown
- 条目描述...

    <details>
    <summary>架构名</summary>

    ```
    框图内容
    ```

    </details>
```

风格：`│▼├└──→` 箭头、缩进表示层级、一行一个节点。
仅新架构画图，bugfix/refactor/跑数不画。

### Step 6：输出

输出 `~/weekly-report/weekly-report-YYYY-MM-DD.md`。

```markdown
## 本周进展

### 1. 英文短语 — 项目名

- 动机：方案 + 结果（来源）
  - 补充想法

### 2. 英文短语 — 项目名

- ...

## 下周计划

> TODO（让用户口述填写）

## 需要协作项

> TODO（让用户口述填写）
```

### Step 7：迭代

输出初稿后，请用户确认：
1. 哪些项目要留 / 砍
2. 哪些条目需要调整粒度
3. 下周计划和协作项口述补充

根据反馈修改后输出终稿。
