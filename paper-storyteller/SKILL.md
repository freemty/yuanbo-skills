---
name: paper-storyteller
description: |
  Use when drafting or revising any section of an ML/CV/NLP paper and wanting narrative
  quality — not just structural correctness. Triggers: user says 写论文, 写 intro, paper
  writing, 润色论文, 论文故事, 写 abstract/related work/method/conclusion, narrative,
  storytelling, or asks to improve paper writing style. Also use when existing intro feels
  generic ("Recent advances in X...") or lacks a story arc.
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - WebSearch
  - WebFetch
  - AskUserQuestion
---

# Paper Storyteller

Write academic papers with the narrative flair of Jiajun Wu, Alexei Efros, Ruoshi Liu, Bill Freeman, and Phillip Isola. Question-driven, metaphor-rich, story-arc-aware — the opposite of template-filling.

## Three-Phase Workflow

```
Phase 1: BRAINSTORM → Socratic dialogue to extract the paper's story
Phase 2: WRITE     → Dynamic retrieval + section-by-section drafting
Phase 3: POLISH    → Automatic style checklist verification
```

**Always start at Phase 1** unless the user explicitly provides a completed Story Outline or asks to jump to a specific section.

---

## Phase 1: Brainstorm

**Load:** `references/brainstorm-protocol.md`

Follow the protocol exactly:
1. Ask Q1-Q3 (one question per message, in Chinese)
2. After Q3, decide fast track vs deep mode based on the criteria in the protocol
3. Announce the decision to the user
4. Complete the remaining questions (fast: Q4-Q5; deep: Q4d-Q8d)
5. Synthesize answers into a **Story Outline**
6. Present the Story Outline and get explicit user confirmation
7. Do NOT proceed to Phase 2 until the user confirms

**Dynamic metaphor search:** If the user can't think of a metaphor in Q4/Q4d, use WebSearch to find cross-disciplinary analogies. Search for the paper's core mechanism + "analogy/metaphor" + fields like physics, biology, cognitive science, architecture, music. Present 2-3 candidates as multiple choice.

---

## Phase 2: Write

**Prerequisites:** Confirmed Story Outline from Phase 1.

### Step 1: Ask writing preferences

Ask the user:
- "你想先写哪个 section？（推荐顺序：Introduction → Method motivation → Related Work → Experiments narrative → Abstract → Conclusion）"
- "每个 section 你想逐段确认，还是整个 section 一次性输出？"

### Step 2: For each section

1. **Load** the section guide: `references/sections/[section-name].md`
2. **Load** style principles: `references/style-principles.md` (keep in context throughout writing)
3. **Search** for topic-relevant allusions if needed:
   - For intro hooks: search for concrete phenomena or historical examples related to the paper's core concept
   - For intellectual lineage: search for the problem's history and key conceptual breakthroughs
   - For method motivation: search for analogies that illuminate the mechanism
4. **Write** the section following the section guide's writing rhythm
5. **Language:** Dialogue with user in Chinese. Written output matches the paper's target language (English for English papers, Chinese for Chinese papers).

### Writing Rules

1. One paragraph at a time if user chose paragraph-by-paragraph; full section if they chose batch mode
2. After writing each paragraph, briefly note which Story Outline element it serves
3. Keep the core metaphor consistent — use the SAME metaphor established in the Story Outline
4. Preserve structural rigor from the section guide while injecting narrative quality
5. Do not sacrifice technical precision for style — method details and experiment numbers must be exact

---

## Phase 3: Polish

**Load:** `references/style-checklist.md`

After completing each section (or after all sections are done):

1. Run every applicable check from the checklist against the written text
2. Output results in the specified format (✅/❌ per item)
3. For each ❌, provide a specific revision suggestion that references the Story Outline
4. Run the anti-pattern scan
5. Ask the user: "要我根据这些建议修改吗？还是你自己改？"
6. If user wants auto-fix: revise and re-run the checklist to verify

---

## Section Guide Index

Load only the section you're currently working on:

| Section | Guide File |
|---------|-----------|
| Introduction | `references/sections/introduction.md` |
| Abstract | `references/sections/abstract.md` |
| Related Work | `references/sections/related-work.md` |
| Method | `references/sections/method.md` |
| Experiments | `references/sections/experiments.md` |
| Conclusion | `references/sections/conclusion.md` |

