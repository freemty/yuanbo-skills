---
name: clone-web
description: Use when recreating a web page locally, preserving a page's visual appearance, or reusing a previously captured design. Triggers on /clone-web <url>, /clone-web use <name>, /clone-web list.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - AskUserQuestion
  - Agent
user-invocable: true
---

# Clone Web

Read `references/workflow.md` after choosing `clone`, `use`, or `list`.

For a clone, capture the source page, assets, responsive states, and a visual
baseline. Implement from a local design contract, then compare rendered
screenshots at representative viewports until material differences are
explained. Preserve provenance and asset licenses.

Prefer the host's browser and screenshot interfaces. Do not treat HTML
structure alone as visual fidelity, and do not claim pixel parity without a
rendered comparison.
