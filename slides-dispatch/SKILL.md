---
name: slides-dispatch
description: Use when creating analysis slides for ML experiments or presentations. Automatically delegates heavy HTML generation to a subagent to keep the main context clean. Replaces direct use of agent-slides and frontend-slides.
---

# slides-dispatch -- Subagent-Delegated Slides Generation

This skill is a thin dispatcher. It gathers requirements in the main context, then spawns a subagent to do all heavy lifting (reading skill docs, reading data, generating HTML). The main context stays clean for experiment work.

## Workflow

### Step 1: Gather Requirements (in main context)

Collect the following from the user. Ask if not provided:

| Field | Example |
|-------|---------|
| **experiment_id** | `exp01b` |
| **experiment_type** | `attack-recall` (Template B) or `multi-factor` (Template C) or `ablation` (Template A) |
| **data_dir** | `/path/to/experiment/results/` |
| **output_path** | `/path/to/output/slides.html` |
| **key_files** | summary.md, specific audit reports, analyze.py output |
| **extra_instructions** | any special requests (e.g. "focus on FP analysis", "include 3 case studies") |

### Step 2: Delegate to Subagent

Use the **Agent tool** (general-purpose, model: sonnet) to spawn a subagent with the prompt below. Set `run_in_background: false` since we need the result.

**CRITICAL**: Do NOT read the skill files yourself. Do NOT generate HTML yourself. ALL of that happens inside the subagent.

```
Prompt template (fill in the gathered values):
---
You are a slides generation specialist. Your task:

1. Read the skill guide at ~/.claude/skills/agent-slides/skill.md
2. Read the visual/animation guide at ~/.claude/skills/frontend-slides/skill.md
3. Read experiment data from: {data_dir}
   - Key files: {key_files}
4. Generate a complete HTML presentation following Template {A/B/C} from agent-slides skill
5. Write the final HTML to: {output_path}

Experiment: {experiment_id}
Type: {experiment_type}
Extra instructions: {extra_instructions}

IMPORTANT:
- Read ALL data from actual files. Never fabricate data.
- Follow the visual style guide exactly (GitHub Dark theme, Inter + JetBrains Mono fonts)
- Every slide must fit in one viewport (100vh, no scroll)
- Use clamp() for all font sizes
- The HTML must be a single self-contained file (inline CSS/JS, no dependencies)
---
```

### Step 3: Report Back (in main context)

After the subagent completes, report to the user:
- Output file path
- Number of slides generated (from subagent's response)
- Any issues the subagent flagged

Do NOT paste the HTML content into the main context.

## Template Selection Guide

| Keyword in experiment | Template |
|-----------------------|----------|
| ablation, multi-model comparison, cross-factor | A (full ablation) |
| attack recall, single config, inject/detect | B (attack recall) |
| multi-factor, combo, N configs x M papers | C (multi-factor ablation) |

## Model Selection for Subagent

- **sonnet** (default): fast, good for standard slides
- **opus**: use only if user requests extra-complex layouts or deep case study analysis
