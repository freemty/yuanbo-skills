---
name: swiss-knife-design
description: >
  Use when building or styling any web page, project page, HTML presentation, dashboard,
  leaderboard, or visual asset for Yuanbo Yang's projects. Also use when reviewing
  existing frontend for visual consistency, or when user says: 我的设计, 个人风格,
  homepage style, project page, 配色, slides风格, 做个网页, 用我的风格.
---

# Swiss Knife Design — Personal Brand System

Black + white + red. Red is a scalpel, not a paintbrush.

## When to Use

- Building any HTML/CSS page for Yuanbo's projects
- Styling an existing dashboard/leaderboard to match brand
- Creating project pages, presentations, landing pages
- Auditing frontend for visual consistency
- User mentions: 个人风格, 我的设计, Swiss Knife, 配色方案

**NOT for:** Paper figures (use `/paper-style`), Beamer slides (use `/beamer-style` with accent override `#C6011F`)

## Quick Reference

| Token | Light | Dark |
|-------|-------|------|
| `--bg` | `#FFFFFF` | `#0A0A0A` |
| `--text` | `#000000` | `#F0F0F0` |
| `--text-secondary` | `#333333` | `#B0B0B0` |
| `--text-tertiary` | `#666666` | `#999999` |
| `--accent` | `#C6011F` | `#E53935` |
| `--border` | `#E0E0E0` | `#222222` |

| Role | Font |
|------|------|
| Display | EB Garamond + Noto Serif SC |
| Body | Inter |
| Mono | JetBrains Mono |

## Core Rules

1. **Red = lines only** — borders, rules, small badges. Never body text.
2. **Black absolute, white pure** — no warm tints, no cream, no gray-blacks.
3. **Dormant → Alive** — images start faded, restore on hover.
   - Light: `brightness(1.3) saturate(0.2) contrast(0.7)` → normal
   - Dark: `brightness(0.5)` → normal
4. **Default dark** — `data-theme="dark"` on `<html>`, toggle saves to localStorage.
5. **Sharp geometry** — 4px radius max on containers, 16px on photos. No blobs/gradients/shadows.

## Brand Mark

Serif "Y" + red dot (bottom-right). Used as favicon (inline SVG) and nav logo (28px).

## Red Placement

**Static:** nav brand mark, section header short bar (24pt left of rule), list left-borders (2px), highlight card left-border (3px), badge fills (red bg + white text).

**Hover only:** titles, links, nav items, hero name (synced with photo restore).

**Never:** body text, dates, button fills, large backgrounds.

## Applying to Existing Projects

For projects with `design-tokens.css`: copy `templates/design-tokens-override.css` over it. Same variable names, instant brand switch.

```bash
cp ~/.claude/skills/swiss-knife-design/templates/design-tokens-override.css \
   path/to/shared/design-tokens.css
```

For new pages: read `templates/base.css` for full implementation reference.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Red on text | Move to border/underline |
| Warm white (#FAF8F4) | Use `#FFFFFF` |
| Gray-black (#1A1A1A for text) | Use `#000000` |
| Grayscale filter in dark mode | Use `brightness()` only — grayscale looks dirty on dark |
| Large border-radius (12px+) | Max 4px containers, 16px photos |
| Shadows for depth | Use borders and background contrast |

## File Reference

| File | Purpose |
|------|---------|
| `templates/base.css` | Full homepage CSS (light + dark) |
| `templates/design-tokens-override.css` | Drop-in replacement for any project's tokens |
| `templates/tokens.json` | Machine-readable design tokens |
