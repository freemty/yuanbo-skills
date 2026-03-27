# Experiments Guide

## Narrative Goal

Use experiments to answer the questions implicitly raised in the intro. Each experiment is an answer, not just a number.

## Writing Rhythm

```
Setup     — datasets, baselines, metrics, implementation details
Main      — comparison with SOTA (answers: "Is this better?")
Ablation  — component analysis (answers: "Which parts matter?")
Analysis  — deeper investigation (answers: "Why does it work?" / "Where does it fail?")
```

## Narrative Ordering

The ORDER of experiments tells a story. Arrange them to build confidence:

1. First, show the method works (main comparison)
2. Then, show WHY it works (ablations)
3. Then, show HOW FAR it works (generalization / stress tests)
4. End with the most surprising or insightful finding

Each experiment/ablation opens with one sentence stating what question it answers:
"To evaluate whether [X] contributes to [Y], we..."

## Style Rules

**Return to restraint here.** Let data speak. Story quality shows in:
- The ordering of experiments (narrative arc)
- The framing sentences (connecting results back to intro claims)
- NOT in the language itself (no "remarkably", "impressively")

**Table/Figure rules:**
- Caption above table, below figure
- Use booktabs style (toprule/midrule/bottomrule)
- Label metric direction (PSNR ↑, LPIPS ↓)
- One table = one message. Don't mix unrelated results.
- Highlight best/second-best with subtle emphasis

## Quality Checklist

1. Does every experiment answer a specific question stated in one sentence?
2. Are all claims in Abstract/Introduction backed by reported numbers?
3. Are baselines recent, relevant, and fairly evaluated?
4. Is ablation tied to every key design claim?
5. Are failure modes / limitations honestly shown?
