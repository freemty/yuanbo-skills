# Compile Workflow

Step-by-step for `/unbox-to-wiki <name>` and `/unbox-to-wiki --batch`.

## Pre-flight

1. Resolve `<name>` to a profile file path:
   - Try `~/unbox-output/profiles/<name>.md` (exact slug)
   - If not found, try fuzzy match: `ls ~/unbox-output/profiles/ | grep -i <name>`
   - If still not found, report error and list closest matches

2. Check if wiki entry already exists:
   - `~/selfos/wiki/entities/<slug>.md`
   - If exists: ask user whether to overwrite or merge (use `--update` for merge)

## Step 1: Read the Profile

Read the full unbox profile. Identify:
- **一句话/opening quote** (usually at the top, after the H1)
- **身份锚定 table** (the identity table)
- **性格信号** (look for sections like 人格画像, The Portrait, personality signals)
- **师门谱系** (mentorship lineage, advisor relationships)
- **Research direction evolution** (the timeline/pivot points)
- **Wayback Machine findings** (the most revealing deletion or change)
- **Cross-reference notes** (the 📎 交叉补充 blocks)

## Step 2: Compress

Apply the compilation rules from SKILL.md:

### Identity (compress to 2-3 lines)
From the full identity table, extract only:
- Current role + institution
- PhD info (where, advisor)
- One distinguishing credential (e.g., "h-index 78", "CVPR Best Paper")

### Personality (pick top 1-2)
From all personality observations, select the ones that are:
- Most surprising (counterintuitive facts)
- Most actionable (patterns you can learn from)
- Most connecting (reveals something about research culture)

### Network (only wiki-connected nodes)
From 师门谱系 and collaborator mentions:
- Only include people who are OR could be wiki entities
- Format as `[[entities/slug]]` for those already in wiki
- Format as plain text for those not yet in wiki

### Directions (top 2-3 pivots)
From the research evolution timeline, keep only:
- Major direction changes (what they dropped and why)
- The current trajectory
- What it reveals about their research taste

## Step 3: Write Entity Page

Create `~/selfos/wiki/entities/<slug>.md` following the template in SKILL.md.

Key quality checks:
- [ ] Frontmatter is complete and valid YAML
- [ ] "Why They Matter" is personal/opinionated, not encyclopedic
- [ ] Total length is 30-60 lines
- [ ] At least one `[[cross-ref]]` to another wiki entity
- [ ] Ends with `Full profile: unbox-output/profiles/<slug>.md`

## Step 4: Write Source Page

Create `~/selfos/wiki/sources/unbox-<slug>.md`:

```yaml
---
title: "Unbox Profile: {Name}"
type: source
created: {today}
updated: {today}
sources: []
tags: [unbox, person]
summary: "Unbox researcher profile for {Name} — {one-line}"
source_type: "record"
---

## Summary

Compiled from unbox profiling tool ({date}). Full profile at `unbox-output/profiles/{slug}.md`.
Covers: identity anchoring, personality signals, mentorship lineage, research direction evolution, deleted content archaeology.

## Key Takeaways

- {Takeaway 1}
- {Takeaway 2}
- {Takeaway 3}

## Entities

- [[entities/{slug}]]
```

## Step 5: Cross-Reference

### 5a. Scan wiki for mentions of this person
```bash
grep -ri "{chinese name}\|{english name}" ~/selfos/wiki/ --include="*.md"
```
For each hit: add `[[entities/<slug>]]` link if not already present.

### 5b. Scan this profile for existing wiki entities
Read the profile's mentor/collaborator names. For each:
```bash
ls ~/selfos/wiki/entities/ | grep -i "<name-fragment>"
```
If found: add cross-ref link in the new entity page AND in the existing entity page.

### 5c. Scan other unbox profiles for this person
```bash
grep -ri "{name}" ~/unbox-output/profiles/ --include="*.md" -l
```
Note which other profiles mention this person. If those profiles are already in wiki, update their cross-refs.

## Step 6: Update Index

Add to `~/selfos/wiki/index.md` under `## Entities` > `### People`:

```markdown
- [[entities/<slug>]] — {summary from frontmatter}
```

Maintain alphabetical order within the People section.

## Step 7: Update Log

Append to `~/selfos/wiki/log.md`:

```markdown
## [{date}] unbox-to-wiki: compile {English Name} ({Chinese Name})

- **Input**: Unbox profile `unbox-output/profiles/<slug>.md` ({N} lines)
- **Output**:
  - Entity page: `wiki/entities/<slug>.md`
  - Source page: `wiki/sources/unbox-<slug>.md`
  - Cross-references updated: {list of pages touched}
- **Key signals**: {1-2 most notable things about this person}
```

## Step 8: Git Commit

```bash
git add wiki/entities/<slug>.md wiki/sources/unbox-<slug>.md wiki/index.md wiki/log.md
# Plus any cross-ref-updated pages
git commit -m "feat(wiki): compile unbox profile — {Name}"
```

## Batch Mode

For `--batch <name1> <name2> ...`:
1. Loop Steps 1-4 for each name
2. Run Step 5 (cross-ref) once for ALL new entries together (catches intra-batch links)
3. Single Step 6 (index update) with all new entries
4. Single Step 7 (log entry) listing all compiled names
5. Single Step 8 (commit) with all files
