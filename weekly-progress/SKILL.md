---
name: weekly-progress
description: Use when writing or completing a weekly progress document for a research/experiment project — filling in placeholder experiment sections, structuring overview and background, adding proper file references, and humanizing the result.
---

# Weekly Progress Doc Workflow

实验项目的周报从草稿到完稿的完整流程。

## 核心原则

**数据来自真实文件，绝不凭空捏造。** 每个实验的数字、结论都必须从 conclusion 文件或 result summary 里读出来，而不是根据描述推测。

---

## 文档结构模板

```
# Weekly Progress — Week N (日期范围)

## 概览
[项目目标 + Section 5 分类表（如有）]

## 背景与初始化
### [初始设置]
### [关键决策/问题]（如 PDF 解析方案、首次运行发现等）

## expXXa — [实验名称]
### 目的
### Setting
### 分析
### 结论

## expXXb — [实验名称]
（同上）

## 待讨论 / TODO

## Progress by Day
### 日期
- [x] 完成项
- [ ] 未完成项
```

---

## 实施步骤

### Step 1：读草稿，识别 placeholder

读目标 `.md` 文件，标记需要补全的实验章节（通常是"目的-setting-分析-结论"全空或只有一行描述）。

### Step 2：用 Explore agent 批量收集数据

一次性委托 Explore agent 读取所有相关文件，比逐个 Read 效率高得多：

```
subagent_type: Explore
prompt: |
  探索 [project_root]，需要收集：
  1. 各实验的 conclusion/summary 文件（exp*/conclusion.md、exp*/exp??_conclusions.md）
  2. 实验配置（run.py 或 config.yaml 里的变量、模型、paper 列表）
  3. 结果数据（results/summary.md、runs.log 里的数字）
  4. 涉及的 prompt 版本差异（prompt_versions.md）
  5. 工作流概览（README 或 docs/ 结构）
  要具体到数字，不要只说"结果良好"。
```

### Step 3：结构化写文档

每个实验章节严格遵循：

**目的**：一句话说清楚为什么做这个实验（上一个实验留下了什么问题？）

**Setting**：用 bullet list 列变量：
```markdown
- Prompt：`v00` × `v01`
- 模型：Haiku 4.5 / Sonnet 4.6 / Opus 4.6
- 总 runs：2 × 3 × 5 = 30
- 结论文档：[`exp/expXX/conclusion.md`](../../exp/expXX/conclusion.md)
```

**分析**：关键数据用表格，重要异常（bug 修复、数据矛盾）单独说明。

**结论**：直接给建议，不用再重复数据——读者已经看过分析了。

### Step 4：文件引用规范

所有路径必须可点击，两种形式择一：
- Markdown 链接：`[`path/to/file.md`](relative/path/to/file.md)`
- 行内代码：`` `path/to/file.md` ``（只读无需跳转时用这个）

### Step 5：应用 Humanizer-zh

写完后用 `/Humanizer-zh` 去 AI 味，重点处理：

- `**粗体标题：**` + 内容 的行内 label 格式 → 折进散文
- 结论区的编号 bold 列表 → 改成段落，保持逻辑不变
- "此外"、"彰显"、"实质性改善" 等 AI 词汇
- 过于对称的三段式结构

---

## 常见问题

| 问题 | 处理方式 |
|------|---------|
| 实验还没有 conclusion 文件 | Setting 可以写，分析/结论留空并注明"待运行" |
| 多个实验共用一套 attack，数据在哪 | 看 `workspaces/{paper}/.attacks/{attack_id}/eval_result.json` |
| Bug 修复影响了所有结论 | 在分析开头专门加"Bug 修复记录"表，说明影响 |
| 实验命名规则不清楚 | 数字是大版本（exp00/exp01），字母是小版本（a/b/c） |

---

## 引用 Skill

去 AI 味：`/Humanizer-zh`
