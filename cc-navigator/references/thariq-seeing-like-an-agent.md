# Thariq: Lessons from Building Claude Code — Seeing like an Agent

> Source: https://x.com/trq212/status/2027463795355095314
> Author: Thariq (@trq212) — Anthropic Engineer
> Date: 2026-02-27

## Overview

One of the hardest parts of building an agent harness is constructing its action space. Claude acts through Tool Calling, but there are many ways tools can be constructed.

The key framework: give the agent tools shaped to its own abilities. But how do you know what those abilities are? You pay attention, read its outputs, experiment. You learn to see like an agent.

## Case Study: AskUserQuestion Tool

Goal: improve Claude's elicitation (ability to ask questions).

### Iteration 1: Questions in ExitPlanTool

Added an array of questions alongside the plan. This confused Claude because it was simultaneously asking for a plan and questions about the plan. What if answers conflicted with the plan?

### Iteration 2: Modified markdown output format

Asked Claude to output bullet point questions with alternatives in brackets, then parsed as UI. Claude was okay at this but not guaranteed -- it would append extra sentences, omit options, or use different formats.

### Iteration 3: Dedicated tool (final)

Created a tool Claude could call at any point, particularly during plan mode. When triggered, shows a modal blocking the agent's loop until the user answers.

Benefits:
- Structured output from Claude
- Ensured multiple options for users
- Composable (Agent SDK, skills can reference it)
- Claude seemed to like calling this tool -- outputs worked well

Key lesson: Even the best designed tool doesn't work if Claude doesn't understand how to call it.

## Case Study: TodoWrite to Task Tool

### TodoWrite (original)

Claude needed a Todo list to keep on track. Wrote or updated Todos displayed to the user. Even then Claude forgot what to do, so system reminders were inserted every 5 turns.

### Problems as models improved

- Reminders made Claude think it had to stick to the list instead of modifying it
- Opus 4.5 got better at subagents, but how could subagents coordinate on shared Todos?

### Task Tool (replacement)

Whereas Todos kept the model on track, Tasks helped agents communicate with each other. Tasks could include dependencies, share updates across subagents, and the model could alter and delete them.

Key lesson: As model capabilities increase, tools that were once needed might now be constraining. Constantly revisit previous assumptions.

## Case Study: Search and Progressive Disclosure

### RAG (original)

Used a vector database to find context. Required indexing and setup, could be fragile. More importantly, Claude was given context instead of finding it itself.

### Grep tool (improvement)

By giving Claude a Grep tool, it could search files and build context itself. As Claude gets smarter, it becomes increasingly good at building its own context given the right tools.

### Skills and progressive disclosure (current)

Claude reads skill files that reference other files recursively. Common use: adding more search capabilities (API instructions, database query patterns).

Over a year, Claude went from not being able to build its own context, to doing nested search across several layers of files to find exactly what it needed.

Progressive disclosure is now a common technique to add new functionality without adding a tool.

## Tool Count Discipline

Claude Code currently has ~20 tools. The bar to add a new tool is high because it gives the model one more option to think about.

### Example: Claude Code self-knowledge

Claude didn't know enough about how to use Claude Code itself. Options:
1. Put all info in system prompt -- adds context rot, interferes with main job (writing code)
2. Progressive disclosure -- give Claude a link to its docs to search
3. Guide subagent -- Claude Code Guide subagent with extensive search instructions

They chose option 3. Added to Claude's action space without adding a tool.

## Key Takeaways

- Designing tools is as much art as science
- Depends on model, goal, and environment
- Experiment often, read your outputs, try new things
- What works for one model may not be best for another
- See like an agent
