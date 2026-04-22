# Anthropic Official Skills Repository

Source: https://github.com/anthropics/skills (Apache 2.0 + source-available)

Anthropic's official reference implementation for Agent Skills — folders of instructions, scripts, and resources that Claude loads dynamically. Contains 17 example skills, the Agent Skills Spec, a skill template, and the `skill-creator` meta-skill.

## Skill Anatomy (Official Structure)

```
skill-name/
├── SKILL.md          (required — frontmatter + instructions)
├── scripts/          (executable code for deterministic/repetitive tasks)
├── references/       (docs loaded into context as needed)
└── assets/           (templates, icons, fonts used in output)
```

**Required frontmatter:**
```yaml
---
name: my-skill-name
description: When to trigger + what it does
---
```

## Progressive Disclosure — Three-Level Loading

This is the official Anthropic model for skill context management:

| Level | What | When Loaded | Size Guidance |
|-------|------|-------------|---------------|
| **1. Metadata** | name + description | Always in context | ~100 words |
| **2. SKILL.md body** | Navigation + core constraints | When skill triggers | <500 lines ideal |
| **3. Bundled resources** | references/, scripts/, assets/ | On demand | Unlimited; scripts execute without loading |

Key implication: SKILL.md is NOT where you dump everything. It's a router that points to deeper resources.

## Description as Trigger Mechanism

The `description` field is the **primary mechanism** that determines whether Claude invokes a skill. Claude sees skills in an `available_skills` list and decides based on description alone.

### Anthropic's guidance on description writing:

- Include **both** what the skill does AND specific contexts for when to use it
- All "when to use" info goes in description, not in the body
- Be **"pushy"** — Claude has a tendency to **undertrigger** (not use skills when they'd help)
- Bad: `"How to build a dashboard"`
- Good: `"How to build a dashboard. Use this whenever the user mentions dashboards, data visualization, internal metrics, or wants to display any kind of data, even if they don't explicitly ask for a 'dashboard.'"`

### Triggering behavior:
- Claude only consults skills for tasks it can't easily handle on its own
- Simple, one-step queries may not trigger even with perfect description match
- Complex, multi-step, or specialized queries reliably trigger when description matches
- Eval queries should be substantive enough that Claude would benefit from consulting a skill

## Skill Writing Principles

### Explain Why > Heavy MUSTs

> "Try hard to explain the **why** behind everything you're asking the model to do. Today's LLMs are *smart*. They have good theory of mind and when given a good harness can go beyond rote instructions and really make things happen."

> "If you find yourself writing ALWAYS or NEVER in all caps, that's a yellow flag — reframe and explain the reasoning so that the model understands why the thing you're asking for is important."

### Writing Style
- Use **imperative form** in instructions
- Start with a draft, then look at it with fresh eyes and improve
- Use theory of mind — make the skill general, not narrow to specific examples

### Output Format Pattern
```markdown
## Report structure
ALWAYS use this exact template:
# [Title]
## Executive summary
## Key findings
## Recommendations
```

### Examples Pattern
```markdown
## Commit message format
**Example 1:**
Input: Added user authentication with JWT tokens
Output: feat(auth): implement JWT-based authentication
```

## Skill Development Loop (from skill-creator)

The official Anthropic methodology for creating and iterating on skills:

```
1. Capture Intent
   - What should this skill enable Claude to do?
   - When should this skill trigger?
   - What's the expected output format?

2. Interview & Research
   - Edge cases, input/output formats, success criteria
   - Check available MCPs for research

3. Draft SKILL.md

4. Test with 2-3 realistic prompts
   - Run with-skill AND baseline (no skill) in parallel
   - Grade assertions against outputs

5. Human Review
   - Qualitative: look at outputs, give feedback
   - Quantitative: pass rates, timing, token usage

6. Improve based on feedback
   - Generalize (skill must work millions of times, not just test cases)
   - Keep prompt lean (remove what's not pulling weight)
   - Explain why (not heavy MUSTs)
   - Look for repeated work across test cases → bundle into scripts/

7. Repeat until satisfied

8. Description Optimization
   - Generate 20 trigger eval queries (10 should-trigger, 10 should-not)
   - Near-misses are the most valuable negative cases
   - Run optimization loop to improve trigger accuracy
```

### Key insight on improvement:

> "We're trying to create skills that can be used a million times across many different prompts. Rather than put in fiddly overfitty changes, or oppressively constrictive MUSTs, if there's some stubborn issue, try branching out and using different metaphors, or recommending different patterns of working."

## Domain Organization Pattern

When a skill supports multiple domains/frameworks:

```
cloud-deploy/
├── SKILL.md           (workflow + selection logic)
└── references/
    ├── aws.md
    ├── gcp.md
    └── azure.md
```

Claude reads only the relevant reference file — keeps context lean.

## Example Skills in the Repo

| Category | Skills |
|----------|--------|
| **Creative & Design** | algorithmic-art, canvas-design, theme-factory, slack-gif-creator |
| **Development** | claude-api, mcp-builder, webapp-testing, web-artifacts-builder, frontend-design |
| **Enterprise** | brand-guidelines, internal-comms, doc-coauthoring |
| **Documents** | docx, pdf, pptx, xlsx (source-available, used in production Claude) |
| **Meta** | skill-creator (the skill for making skills) |

## Comparison with Community Practices

| Topic | anthropics/skills (Official) | Community (Thariq, Superpowers, etc.) |
|-------|------------------------------|---------------------------------------|
| Structure | SKILL.md + scripts/ + references/ + assets/ | Same, independently discovered |
| Size limit | <500 lines for SKILL.md | Tw93: keep CLAUDE.md short; Thariq: progressive disclosure |
| Description | "Pushy" to combat undertriggering | Thariq: "when to trigger, not what I do" |
| Writing style | Explain why > MUSTs | Superpowers: rigid skills follow exactly |
| Testing | Full eval loop with baseline + blind comparison | Superpowers: TDD on features, not skills themselves |
| Iteration | Skill-specific improvement methodology | Boris: "if you do something >1/day, make it a skill" |

The official approach adds **eval-driven skill development** — treating the skill itself as a product that needs testing and iteration, not just the code it helps produce.
