# Introduction Guide

## Narrative Goal

In 4-6 paragraphs, take the reader from "curious" to "convinced". The introduction is a story with rising tension and a satisfying resolution.

## Writing Rhythm

```
¶1  Hook — a phenomenon, question, or concrete image that makes the reader pause and want to know more
¶2  Context — why this problem matters (big picture, applications, what's at stake)
¶3  Prior Art — what others did, woven as a narrative thread (not a list)
¶4  Gap — where old methods break down, and WHY (the technical root cause). This is the emotional climax.
¶5  Our Approach — your insight + method. The core metaphor lands here. This paragraph answers the tension built in ¶3-4.
¶6  Results Preview + Contributions — close with the most striking numbers and a bullet list of contributions
```

## Pre-Writing: Backward Reasoning

Before writing, answer these in order:

1. What technical problem do we solve, and why is there no well-established solution?
2. What are our contributions (new task? new metric? new technique? new insight)?
3. Why can our method work in essence — what is the core mechanism?
4. How do we use prior methods to *lead readers* to the challenge we solved?

Then write forward: task → prior art → gap → our approach → results.

## Paragraph-Level Guidance

### ¶1 Hook

**Do:** Open with a question (Wu/Isola style), a concrete scene (Freeman style), or a vivid observation (Liu style). The hook should be specific to YOUR paper, not generic to the field.

**Don't:** "Recent advances in X have achieved remarkable progress..." / "X is an important problem in computer vision..." / "With the rapid development of deep learning..."

**Structure options (pick one):**
- Question-first: "What would it take to [achieve X]? [Follow with why this matters]"
- Scene-first: "[Describe a concrete phenomenon]. [Connect to the technical problem]"
- Observation-first: "[State a surprising fact or counter-intuitive observation]. [Use it to motivate the problem]"

### ¶2 Context

Place the problem in its broader landscape. Why should the reader care beyond the immediate task?

Connect to applications, but don't just list them. Show what's at stake: "Without solving X, we cannot achieve Y, which means Z remains out of reach."

### ¶3 Prior Art (Intellectual Lineage)

This paragraph is NOT "X [1] did A. Y [2] did B. Z [3] did C."

Instead, tell the *story of ideas*:
- "The dominant approach has been to... This line of work, pioneered by [X], established..."
- "A complementary thread explored... building on [Y]'s insight that..."
- "More recently, [Z] showed that... opening the door to..."

Each method mentioned should *lead toward* the gap you're about to reveal. Omit methods that don't serve this narrative.

### ¶4 Gap (Tension Climax)

State what current methods cannot do, AND the technical root cause.

**Structure:** [Limitation] + [Technical reason] + [Why this matters]

"However, these approaches share a fundamental limitation: [what breaks]. This stems from [root technical cause]. As a result, [consequence that motivates your work]."

The reader should finish this paragraph feeling: "We really need a new way of thinking about this."

**Warning:** Do NOT frame this as "naive baseline has problem, we fix it." This makes work look incremental. Frame it as a *structural gap* in current thinking.

### ¶5 Our Approach

The core metaphor lands here. Connect your insight to the gap:

"[Our key insight] is that [reframing]. Based on this, we propose [method name], which [one-sentence mechanism]."

Then concrete implementation: "Specifically, [step 1], [step 2], [step 3]."

Then advantages: "In contrast to [prior approach], our method [advantage 1]. Additionally, [advantage 2]."

### ¶6 Results + Contributions

Lead with the most striking experimental result. Then list contributions as bullets.

Keep contributions concrete and verifiable — each bullet should map to an experiment or a section.

## Quality Checklist

1. Does ¶1 create genuine curiosity (not just state importance)?
2. Does ¶3 read as a story of ideas (not a citation list)?
3. Does ¶4 make the reader feel the gap is real and important?
4. Does ¶5 feel like a natural resolution to ¶4's tension?
5. Is the core metaphor present and vivid?
6. Are all claims in ¶6 backed by experiments?
7. Is terminology stable (no term changes between paragraphs)?
