# Method Guide

## Narrative Goal

The motivation paragraph (¶1) continues the intro's story — the reader should feel the method is the natural consequence of the insight. After that, switch to precision mode.

## Writing Rhythm

```
¶1  Motivation + Overview — natural language, connects to intro's story. Points to pipeline figure.
¶2+ Module sections — each module: motivation → design → technical advantage
    Technical precision here. No forced metaphors next to equations.
¶N  Implementation details — hyperparameters, training, practical details
```

## Pre-Writing

Before writing, answer for each module:
1. How does it run? (forward process: input → steps → output)
2. Why do we need it? (what problem does it solve)
3. Why does it work? (technical advantage over alternatives)

## Motivation Paragraph (¶1)

This is the ONLY paragraph in Method that needs story quality. It bridges from the intro's narrative to the technical details.

Structure:
1. One sentence restating the core insight (echo intro's ¶5, don't repeat verbatim)
2. One sentence pointing to the pipeline figure
3. Brief roadmap: "Section 3.1 describes..., Section 3.2 addresses..., Section 3.3 details..."

## Module Subsections

Each module follows: **motivation → design → advantage**

**Motivation:** "A remaining challenge is [X]. To address this, we introduce [module]."

**Design:** Describe specific structures first, then forward process in execution order.
- "We represent ... with ..."
- "Given [input], we first ... then ... finally ..."
- "This produces [output], which is used for ..."

**Advantage:** "In contrast to [alternative], our approach [concrete benefit] because [technical reason]."

## Style Rules

- Motivation paragraphs: natural language + occasional analogy is fine
- Technical paragraphs: clean, precise, no metaphors wedged next to equations
- Term consistency: once you name something, never change the name
- Forward process: strict execution order, a reader should be able to re-implement from this

## Quality Checklist

1. Can a reader re-implement the method from this section alone?
2. Does each module have explicit motivation, design, and advantage?
3. Are terms stable across all subsections?
4. Is the motivation paragraph connected to the intro's story?
