---
name: agent-slides
description: Use when creating analysis slides for ML experiments, ablation studies, attack recall benchmarks, or multi-factor benchmarks — especially when results span multiple models, prompts, or configurations and need cross-factor comparison tables, recall/FPR tables, heatmaps, inject-vs-detect case studies, and FP analysis.
---

# agent-slides — 实验分析 Slides 构建模式

从实验结果数据（logs、summary.md、audit reports）生成结构完整、自解释的 HTML 展示 slides。

## 核心原则

**每个 ablation 元素都需要至少一张解释页**，出现在结果页之前。受众不应在还不清楚"X 是什么"时就先看"X 的表现"。

## Slide 结构模板

```
1. 标题页          — 实验名、设计矩阵摘要（N papers × M models × K prompts）
2. 动机与目的      — 为什么做这个实验，三个目标
3. 判定/评估标准   — 每个 verdict/metric 的精确定义 + 关键区别（如 WARN vs FAIL）
4. 实验设计        — 完整矩阵卡片
── Ablation 解释区（每个变量一张）──
5. 数据集/论文介绍  — 每个 subject 一行：ID、标题、领域、特殊性
6. 模型能力对比    — 能力维度表（推理深度、准确率、倾向性）
7. Prompt 版本对比 — 逐条列出实际差异，预期 vs 实际效果
── 结果区 ──
8. 行为画像        — 各配置的 PASS/FAIL/WARN 档案（带动画条形图）
9. 分布总览        — 堆叠条形图（所有组合并排）
10. 热力图（关键发现）— 最突出的 paper × section 矩阵
── 深度分析区 ──
11. Case 1         — 真正发生的高质量 bug，含模型判定梯度
12. Case 2         — 另一类别的代表性 case
13. 章节风险排名   — 横向条形图（按 FAIL 总数排序）
14. 变量效果对比   — 数值对比表 + 每个变量的三条发现
── 总结 ──
15. 核心结论       — 4 条，每条附数据支撑
```

## 内容来源规则

| 内容类型 | 来源 |
|---------|------|
| 模型行为数据 | `analyze.py` 生成的 `summary.md` |
| Case study 细节 | 直接读 `.review/{task_id}/integrity_audit.md` |
| 论文描述 | `paper_grobid.md` 前 10 行 abstract |
| Prompt 差异 | `agents/prompts/sys_*/` 两个版本文件对比 |

**不要从记忆中重建数据**，Case 细节必须来自实际 audit 报告。

## 可视化选型

| 场景 | 用什么 |
|------|--------|
| 一个变量下 N 配置的分布 | 堆叠横向条形图（PASS/FAIL/WARN 分段） |
| Paper × Model 交叉矩阵 | 热力图表格（彩色 verdict badge） |
| 单一 paper 的所有 section | 行高亮热力图（突出行用背景色） |
| 单变量排名 | 单色横向条形图（按值排序） |
| 配置能力对比 | 普通 HTML 表格（行 = 维度，列 = 配置） |
| 发现/结论 | Finding Card（左侧彩色 border：红=critical，黄=warning，蓝=info） |

## 视觉风格规范

**技术内部报告用 GitHub Dark 主题（生产标准）：**

```css
--bg: #0d1117;         /* 主背景 */
--bg2: #161b22;        /* 卡片/面板背景 */
--bg3: #21262d;        /* 嵌套元素背景 */
--border: #30363d;     /* 边框 */
--text: #e6edf3;       /* 正文 */
--muted: #8b949e;      /* 辅助文字 */
--accent: #58a6ff;     /* 高亮蓝 */
--accent2: #79c0ff;    /* 次高亮 */
--pass: #3fb950;       --fail: #f85149;
--warn: #e3b341;       --pending: #8b949e;
```

字体：`Inter`（正文）+ `JetBrains Mono`（数据/代码/标签）

**尺寸全部用 `clamp()` 实现响应式**，不用 media query 切断点：
```css
--title-size: clamp(2rem, 5.5vw, 4rem);
--body-size:  clamp(0.75rem, 1.3vw, 1rem);
--small-size: clamp(0.6rem, 0.95vw, 0.8rem);
```

**Verdict badge CSS（使用 CSS 变量 + 半透明背景）：**
```css
.badge-pass { color: var(--pass); background: rgba(63,185,80,.15); }
.badge-fail { color: var(--fail); background: rgba(248,81,73,.15); font-weight:700; }
.badge-warn { color: var(--warn); background: rgba(227,179,65,.15); }
.badge-pending { color: var(--pending); background: rgba(139,148,158,.12); }
```

## Finding Card 组件

```html
<div class="finding critical">   <!-- critical=红, warning=黄, info=蓝 -->
  <div class="finding-title">标题</div>
  <div class="finding-desc">具体描述，含数据</div>
</div>
```

用于：动机页的目标、Prompt 差异解释、Case Study 的每条矛盾、核心结论。

## Glossary Slide 组件

当 slides 包含领域术语（Recall、FPR、pp、Ablation 等），**必须在结果页之前插入术语表页**。分组展示，每组 3-5 个术语：

```css
.glossary-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 1rem;
}
.glossary-item {
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: .75rem 1rem;
}
.glossary-term {
  font-family: 'JetBrains Mono', monospace;
  color: var(--accent);
  font-weight: 600;
  margin-bottom: .25rem;
}
.glossary-def { color: var(--muted); font-size: var(--small-size); }
.glossary-section-label {
  color: var(--text);
  font-weight: 600;
  margin: 1rem 0 .5rem;
  padding-bottom: .25rem;
  border-bottom: 1px solid var(--border);
}
```

分组示例：核心指标（Recall / FPR / pp）、实验设计（Combo / Ablation / v00-v01）、审计规则（5.1-5.8 各类别一句话定义）。

## Case Study 选取原则

选 2-3 个 case，标准：
1. **跨模型一致性最高的**（e.g. 6/6 全员 FAIL）— 证明是真实缺陷
2. **模型判定梯度明显的**（e.g. Haiku PASS → Opus WARN → Sonnet FAIL）— 展示灵敏度差异
3. **不同 bug 类型的**（e.g. 引文造假 + 内部不一致）— 覆盖不同 audit 类别

每个 case 页包含：具体的错误内容（引文原文、矛盾数值）+ 各配置判定表。

## Slide 结构模板 B — Attack Recall Benchmark（单配置 × 多论文）

用于 exp01a 类型：固定最优配置，对多篇论文注入缺陷后评估 recall。

```
1. 标题页          — 实验名、配置摘要（N papers × 1 config）
2. 实验设计        — 三阶段 pipeline（Attack → Review → Evaluate）
3. Per-Paper 结果  — 逐论文 recall/FPR 表格 + inline bar charts
4. Category 分布   — 各缺陷类别检出率 + 盲区标注
5-6. Case Study ×2 — 注入缺陷 vs 审计检出（inject/detect 对照布局）
7. FP 分析         — 误报原因拆解 + 与其他实验 FPR 对比
8. 结论            — Finding Cards grid + Next Steps
```

### Pipeline 可视化组件

三列 grid + 箭头连接，用于展示 attack-then-audit 流程：

```css
.pipeline {
  display: grid;
  grid-template-columns: 1fr auto 1fr auto 1fr;
  align-items: start;
}
.pipeline-arrow { color: var(--muted); padding: 0 .75rem; }
.pipeline-col {
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 1rem;
}
```

### Per-Paper Recall 表格

HTML table + inline bar chart（纯 CSS div），每行一篇论文：

```html
<td>
  <div class="bar-wrap">
    <div class="bar-fill-pass" style="width:100%"></div>
    <span class="bar-label">100%</span>
  </div>
</td>
```

HIT/FP/n-a 用不同颜色 class：`.hit-ok`（绿）、`.hit-fp`（红）、`.hit-na`（灰）

### Bug Layout（Inject vs Detect 对照）

两栏 grid：左侧注入缺陷卡片，右侧审计检出代码面板。

```css
.bug-layout {
  display: grid;
  grid-template-columns: 1fr 1.4fr;
  gap: 1.5rem;
}
.ba-card.injected { border-color: var(--fail); background: rgba(248,81,73,.05); }
.ba-card.detected { border-color: var(--pass); background: rgba(63,185,80,.05); }
```

右侧 `.code-panel` 用 `status-ok` / `status-bad` 前缀标记每行检出状态。底部可加 `lesson-box`（左侧黄色 border）总结观察。

### FP 分析页

与 bug-layout 类似，但左侧展示"未注入 → 被误判"的时间线，右侧用 finding-card grid 展示原因分析。关键：标注 FP 可能是论文固有缺陷（非真正 FP）。

## Slide 结构模板 C — Multi-Factor Ablation（多 combo × 多论文）

用于 exp01b 类型：N 个配置组合（模型 × prompt）× M 篇论文，评估 recall/FPR。

```
1. 标题页          — 实验名、设计矩阵（N combos × M papers）
2. 实验设计        — Pipeline + 矩阵卡片
3. 术语表          — Glossary slide（核心指标 / 实验设计 / 审计规则）
── 结果区 ──
4. 总览热力图      — Combo × Paper 的 recall/FPR 矩阵（彩色 badge）
5. 变量效果        — 按单因素（模型 / prompt）拆分的对比表
6. Category 分布   — 各缺陷类别的检出率对比
── 深度分析区 ──
7-8. Case Study ×2 — inject/detect 对照 + 各 combo 判定差异
9. FP 分析         — 误报拆解 + 跨 combo 对比
── 总结 ──
10. 结论           — Finding Cards + 推荐配置
```

**与模板 B 的区别**：模板 B 是单配置，关注"哪些论文/类别检出好"；模板 C 是多配置，关注"哪种组合效果最好"。

## 主题一致性规则

**同一项目的所有实验 slides 必须使用相同视觉主题。** 如果旧 slides 用了不同主题（如 Tailwind 色板、Space Grotesk 字体），优先迁移 CSS 变量到标准 GitHub Dark 主题，而不是重建整个文件。

迁移步骤：
1. 替换 `:root` 中的所有颜色变量为 GitHub Dark tokens
2. 替换字体声明为 Inter + JetBrains Mono
3. 更新 verdict badge 的颜色和背景
4. 检查 nav dots、progress bar、grid background 等装饰元素

## 常见错误

| 错误 | 修正 |
|------|------|
| 先展示模型结果，再解释模型是什么 | ablation 解释页必须在对应结果页之前 |
| case study 从总结中重述，不含具体证据 | 读 audit report 原文，引用具体行号/数值 |
| 所有图都用柱状图 | 交叉矩阵用热力图，单因素排名用横条图 |
| 结论页只有文字 | 每条结论附数据（"89 FAILs vs 13 FAILs"） |
| 忘记 viewport fitting | 每张 slide `height: 100vh; overflow: hidden`，文字全用 `clamp()` |
| 术语堆砌不解释 | 有 Recall/FPR/pp/Ablation 等术语时，必须加 Glossary slide |
| 多实验 slides 主题不统一 | 同项目所有 slides 统一用 GitHub Dark，旧 slides 迁移 CSS 变量 |
| Slide ID 硬编码后忘记重编号 | 插入新 slide 后检查所有 `id="slide-N"`、counter、nav 链接 |

## 相关 Skill

**REQUIRED SUB-SKILL:** 使用 `frontend-slides` 构建 HTML 文件，视觉风格指定 **"Dark Botanical"** 或 **"Terminal Green"** preset（技术内部报告风格）。
