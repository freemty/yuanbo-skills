# Style Checklist

Run after writing each section. Output per-item pass/fail with specific revision suggestions.

## How to Use

1. After completing a section draft, load this file
2. Run each applicable check against the written text
3. Output results in the format shown at the bottom
4. For each ❌, provide a specific revision suggestion referencing the Story Outline from Phase 1

## Universal Checks (all sections)

| # | Check | Pass Criterion |
|---|-------|---------------|
| 1 | No boilerplate opening | First sentence is NOT any of: "Recent advances/In recent years/With the development of/X is an important problem" |
| 2 | Question-driven opening | First two paragraphs discuss a problem or phenomenon, not a method or technique |
| 3 | Core metaphor present | At least one cross-disciplinary or concrete analogy exists, used without over-explaining |
| 4 | Concrete entry point | Opening has a specific, perceivable scene/example/image, not pure abstraction |
| 5 | Narrative continuity | Each paragraph's final sentence naturally leads to the next paragraph's topic |
| 6 | Intellectual lineage | Prior work is presented as a thread of ideas, not a citation list |
| 7 | Restrained voice | No "remarkably/significantly/impressively/notably"; no self-congratulation |
| 8 | Metaphor consistency | Core metaphor in this section matches the one established in the Story Outline |

## Introduction-Specific

| # | Check | Pass Criterion |
|---|-------|---------------|
| 9 | Gap has tension | After reading ¶3-4, reader feels "we need a new approach" — not flat narration |
| 10 | Aha moment placed correctly | Core insight appears AFTER the gap, BEFORE method details |

## Abstract-Specific

| # | Check | Pass Criterion |
|---|-------|---------------|
| 11 | Complete arc | Hook, gap, method, results all present in 150-250 words |
| 12 | No orphan concepts | Every concept in abstract also appears in the introduction |

## Related-Work-Specific

| # | Check | Pass Criterion |
|---|-------|---------------|
| 15 | Intellectual threads | Organized by idea threads, not chronology or method category |
| 16 | Novelty verifiable | Your difference from prior work is stated in technical terms |

## Method-Specific

| # | Check | Pass Criterion |
|---|-------|---------------|
| 17 | Motivation connected | ¶1 continues the intro's story, not a cold restart |
| 18 | Re-implementable | A reader could re-implement from this section alone |

## Experiments-Specific

| # | Check | Pass Criterion |
|---|-------|---------------|
| 19 | Question-first framing | Each experiment opens with one sentence stating what question it answers |
| 20 | Failure modes shown | Limitations or failure cases are honestly reported |

## Conclusion-Specific

| # | Check | Pass Criterion |
|---|-------|---------------|
| 13 | Closed loop | Opening sentence echoes intro's hook (question/scene/observation) |
| 14 | Zoom-out with space | Final 1-2 sentences point to bigger question without spelling out specific next steps |

## Anti-Pattern Scan (automatic, all sections)

Scan the written text for these patterns and flag any found:

| Pattern | Detection Rule |
|---------|---------------|
| Connector pileup | 3+ instances of "Furthermore/Moreover/Additionally/In addition" in one section |
| Filler phrases | Any instance of "It is worth noting/It should be noted/Importantly" |
| Mechanical structure | Every paragraph follows identical topic-detail-summary shape |
| Passive voice wall | More than 60% of sentences in a paragraph use passive voice |
| Citation cluster | More than 3 citation brackets in a single sentence (e.g., [1,2,3,4]) |
| Vague attribution | "Many researchers/Several studies/Previous work" without specific names |

## Output Format

```
## Style Check: [Section Name]

✅ No boilerplate opening — opens with [what it opens with]
✅ Question-driven — first two paragraphs focus on [problem]
❌ Core metaphor — missing. Story Outline specifies "[metaphor]". Suggestion: add it to ¶[N] when describing [specific point].
✅ Concrete entry point — uses [scene/example]
❌ Narrative continuity — ¶3→¶4 transition is abrupt. Suggestion: add a bridging sentence about [specific connection].
✅ Intellectual lineage — threads through [X] → [Y] → [Z]
✅ Restrained voice — no flagged words
✅ Metaphor consistency — "[metaphor]" matches Story Outline

Anti-patterns found:
⚠️ Connector pileup: 4 instances of "Moreover" — replace 3 with cause-effect transitions

Passed: 6/8 universal + 2/2 section-specific
Action items: 2 revisions needed
```
