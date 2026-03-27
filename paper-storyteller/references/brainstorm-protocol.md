# Brainstorm Protocol

Socratic dialogue to extract the paper's story before writing a single sentence. The output is a confirmed Story Outline that drives Phase 2 (writing).

## Rules

1. One question per message. Never batch questions.
2. Prefer multiple-choice when the user might not know what options exist. Use open-ended when you need the user's authentic voice.
3. Dialogue language is always Chinese (中文) — thinking in native language produces richer answers.
4. If the user gives a purely technical answer, follow up with: "如果你要跟一个聪明但不是本领域的朋友解释，你会怎么说？"
5. After each answer, briefly reflect back what you understood before asking the next question. This lets the user correct misunderstandings early.

## Opening Assessment (all papers, Q1-Q3)

### Q1: 一句话说清你的论文在干嘛

Purpose: Judge topic complexity + force user to distill core.

Follow-up trigger: If the answer contains jargon without intuition, ask: "如果你要跟一个聪明但不是本领域的朋友解释，你会怎么说？"

### Q2: 你觉得这篇论文最让你兴奋的 insight 是什么？

Purpose: Find the emotional anchor — the author's own excitement is often the best narrative entry point.

Depth signal: If the user struggles to articulate → high complexity → deep mode.

### Q3: 这个问题之前的人是怎么想的？他们哪里想错了/想少了？

Purpose: Establish "old world vs new world" narrative tension.

Depth signal: If the user gives a clear, structured contrast → fast track. If vague or scattered → deep mode.

## Adaptive Depth Decision

After Q3, evaluate:

```
FAST TRACK conditions (ALL must be true):
  - Q1: User gave a clear non-technical explanation (or reached one after follow-up)
  - Q2: User can name their excitement in 1-2 sentences
  - Q3: User clearly contrasts prior work limitations with their approach

If all true → fast track (Q4-Q5, ~5 rounds total)
Otherwise → deep mode (Q4d-Q8d, ~10 rounds total)
```

Announce the decision: "你的论文故事线已经比较清晰了，我们快节奏走几个问题就开始写" or "这个课题比较有深度，我们多聊几轮把故事挖透"

## Fast Track (Q4-Q5)

### Q4: 你的工作让你联想到什么？

Prompt: "可以是其他学科的概念、一个自然现象、一个历史故事、一部电影... 什么都行。如果暂时没灵感也没关系，我来搜一些候选类比。"

Purpose: Mine metaphor material.

If user has no inspiration: Use WebSearch to find cross-disciplinary analogies based on the paper's core mechanism. Search queries like:
- "[core mechanism] analogy in nature"
- "[core concept] metaphor physics biology"
- "[problem type] similar problem in [other field]"

Present 2-3 candidate metaphors as multiple choice.

### Q5: 你希望读者读完 intro 之后的感受是什么？

Options to offer:
- (A) "哇，这个问题原来可以这样想" — reframing感
- (B) "这个方向怎么之前没人做" — 空白发现感
- (C) "这个类比太精准了" — 隐喻共鸣感
- (D) "这个故事讲得真好，逻辑太顺了" — 叙事流畅感
- (E) 其他 (请描述)

Purpose: Define narrative goal and emotional arc for writing.

## Deep Mode (Q4d-Q8d)

### Q4-deep: 这个问题的"历史"是什么？

Prompt: "谁最早开始想这个问题？中间有哪些关键转折点？"

Purpose: Build intellectual lineage. The answers here directly feed into the Prior Art paragraph structure.

### Q5-deep: 如果这个问题完美解决了，世界会怎样？

Purpose: Extract the "big picture" from application value. This shapes the Context paragraph and the Conclusion's zoom-out.

### Q6-deep: 你的方法的核心 trick 是什么？用一个比喻说。

Purpose: Force out a method-level metaphor (not just problem-level). This feeds into the Method motivation paragraph.

If the user struggles: Offer mechanical analogies — "你的方法像是一个 ___，它接收 ___，通过 ___ 变成 ___"

### Q7-deep: 你的实验中最意外的发现是什么？

Purpose: Unexpected findings are the best story material. They can become:
- A hook in the intro ("Surprisingly, we found that...")
- An aha moment in the experiments section
- A seed for the conclusion's future directions

### Q8-deep: 有没有一个你很喜欢的论文 intro，你觉得它的感觉接近你想要的？

Purpose: Obtain a style reference anchor.

If user provides one: Read it with WebFetch, extract the structural and stylistic patterns, use as a concrete target for the writing phase.

If user has none: Skip — the style principles are sufficient.

## Story Outline (Phase 1 Output)

After all questions are answered, synthesize into this outline and present for confirmation:

```
## Story Outline

- **开篇意象/问题:** [The hook — a question, phenomenon, or concrete scene]
- **核心隐喻:** [The one metaphor that will be the paper's identity]
- **旧世界 vs 新世界:** [Prior art's framing vs your reframing]
- **知识谱系:** [Key intellectual ancestors and the thread connecting them to you]
- **Aha moment 位置:** [Which paragraph/moment the core insight lands]
- **情感弧线:** [curiosity/tension/surprise] → [understanding] → [conviction]
- **目标读后感:** [From Q5 — what the reader should feel]
- **写作顺序:** [Recommended: Introduction → Method motivation → Related Work → Experiments → Abstract → Conclusion]
```

Ask: "这个故事提纲 OK 吗？有什么想调整的？确认后我们开始写。"

Only proceed to Phase 2 after explicit user confirmation.
