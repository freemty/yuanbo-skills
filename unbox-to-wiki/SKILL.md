---
name: unbox-to-wiki
description: "Compile unbox researcher profiles into selfOS wiki entries. Selective, compressed, cross-referenced. Triggers: /unbox-to-wiki, unbox to wiki, 入库, researcher to wiki."
---

# Unbox → Wiki Compiler

Transforms raw unbox researcher profiles (~150-350 lines) into compact selfOS wiki entity pages (~30-60 lines). Not everyone gets in — only people relevant to the user's research trajectory.

## Architecture

```
Layer 1: unbox-output/profiles/     (raw, 150-350 lines each)
    ↓ compile (selective)
Layer 2: selfos/wiki/entities/      (compiled, 30-60 lines each)
    ↓ cross-reference
Layer 3: selfos/wiki/concepts/      (topic wikis reference people)
```

## Commands

| Command | Summary | Workflow |
|---------|---------|----------|
| `/unbox-to-wiki <name>` | Compile one profile into wiki | Read `references/compile-workflow.md` |
| `/unbox-to-wiki --batch <n1> <n2> ...` | Compile multiple profiles | Same workflow, loop per name |
| `/unbox-to-wiki --suggest` | Analyze all profiles, suggest who to add | Read `references/suggest-workflow.md` |
| `/unbox-to-wiki --update <name>` | Re-compile after profile update | Read existing wiki entry, merge changes |
| `/unbox-to-wiki --inject` | Enrich existing thin wiki entities with unbox data | See Inject Workflow below |

**For every command:** read the corresponding `references/` file before executing.

## Selection Criteria — Who Gets In?

NOT everyone. The wiki is personal — it contains people **relevant to the user**. Accept if ANY:

1. **User explicitly requests it** — `/unbox-to-wiki <name>`
2. **Research overlap** — works in the user's research area (ML systems, agents, etc.)
3. **Potential collaborator/advisor** — labs the user might join or interact with
4. **Network node** — connects 3+ other wiki entities (high graph centrality)
5. **Exceptional personality signal** — rare traits worth remembering (e.g., "deleted startup history from CV", "reversed from bottom to top in first year")

When running `--suggest`, score each profile 1-5 on these criteria and recommend those scoring >= 3.

## Compilation Rules — What to Keep

From a 200+ line profile, compile down to **30-60 lines** that follow the selfOS entity format.

### ALWAYS keep
- **一句话/定位** — The opening quote or one-line summary. This is the profile's thesis.
- **身份锚定 (compressed)** — Current role, institution, key credentials. As a table or 2-3 lines, not the full table.
- **Top 1-2 性格信号** — The most interesting/relevant personality observations. What makes this person *distinctive*, not just successful.
- **师门关系** — Only if it connects to other wiki nodes. Format as `[[entities/advisor-name]]` links.
- **Link back to full profile** — Always: `Full profile: unbox-output/profiles/<slug>.md`

### KEEP if relevant
- **Research direction evolution** — Only the key pivot points, not the full timeline
- **One standout deleted/hidden signal** — The most revealing Wayback Machine finding or deletion
- **Student/mentee connections** — Only if those people are also wiki entities

### NEVER include in wiki
- Full publication lists or citation counts
- Wayback Machine diff details (too granular)
- Raw source URLs (they're in the unbox profile)
- "未验证/待挖" sections (unverified speculation)
- Award lists (keep only the most distinctive 1-2)
- Full 人格画像 (compress to 1-2 bullets)

## Output Format

Every compiled entry MUST follow the selfOS entity page format:

```yaml
---
title: "{Chinese Name} ({English Name})"
type: entity
created: {today}
updated: {today}
sources: ["unbox-{slug}"]
tags: [person, unbox, {research-area}, {institution}]
summary: "{一句话 from profile}"
entity_type: "person"
---
```

### Required Sections

```markdown
# {Chinese Name} ({English Name})

> {一句话 — the opening quote or thesis from the unbox profile}

## Who

{2-3 sentences: current role, where they came from, what they're known for.
Use [[cross-refs]] to other wiki entities where possible.}

## Why They Matter

{1-2 paragraphs: what makes this person relevant to the user's world.
Research overlap, network connections, personality signals worth remembering.
This is the editorial core — not a Wikipedia summary, but a personal assessment.}

## Personality Signals

- **{Signal 1 title}**: {1-2 sentence description}
- **{Signal 2 title}**: {1-2 sentence description}

## Network

- Advisor: [[entities/{advisor}]] (if in wiki)
- Students: {notable names, link if in wiki}
- Collaborators: [[entities/{name}]] (if in wiki)
- {Other connections to wiki nodes}

## Key Directions

{2-3 bullet points on research trajectory — only the pivots that reveal taste/strategy}

---

Full profile: `unbox-output/profiles/{slug}.md`
```

## Cross-Reference Protocol

When adding a person to wiki, perform these checks:

### Step 1: Scan existing wiki for mentions
```
grep -r "{person's name}" ~/selfos/wiki/
```
If found: add `[[entities/{new-slug}]]` link in those pages.

### Step 2: Scan new profile for existing wiki entities
Read the unbox profile's 师门谱系 and collaborator mentions. For each name:
- Check if `~/selfos/wiki/entities/{name-slug}.md` exists
- If yes: add `[[entities/{name-slug}]]` cross-ref in both directions

### Step 3: Check other unbox profiles for mentions
```
grep -r "{person's name}" ~/unbox-output/profiles/
```
If mentioned in other profiles that are already in wiki: update cross-refs.

### Step 4: Update index and log
- Add entry to `wiki/index.md` under Entities > People
- Append operation to `wiki/log.md`
- Format: `## [{date}] unbox-to-wiki: compile {name}`

## Source Page Convention

Each compiled person also creates a lightweight source page:

```yaml
---
title: "Unbox Profile: {Name}"
type: source
created: {today}
updated: {today}
sources: []
tags: [unbox, person]
summary: "Unbox researcher profile for {Name}"
source_type: "record"
---

## Summary

Compiled from unbox profiling tool. Full profile at `unbox-output/profiles/{slug}.md`.

## Key Takeaways

- {2-3 bullets from profile}

## Entities

- [[entities/{slug}]]
```

Source slug format: `unbox-{person-slug}` (e.g., `unbox-jiajun-wu`).

## Batch Workflow

For `--batch`:
1. Read all named profiles
2. Compile each into entity page + source page
3. Run cross-reference protocol across ALL new entries (not just against existing wiki)
4. Batch-update `wiki/index.md` (one update, not N updates)
5. Single `wiki/log.md` entry listing all compiled names
6. Git commit: `feat(wiki): compile {N} unbox profiles — {name1}, {name2}, ...`

## Inject Workflow (`--inject`)

**Purpose:** Enrich existing thin wiki entity pages by pulling related information from unbox profiles — without creating new entities.

This solves the "Geoffrey Hinton has 18 lines in wiki but Jimmy Ba's unbox profile has rich details about Hinton's advising style" problem.

### Step 1: Identify thin entities

Scan `~/selfos/wiki/entities/` for person entities that are thin (< 25 lines OR sources list is empty):

```bash
for f in ~/selfos/wiki/entities/*.md; do
  lines=$(wc -l < "$f")
  type=$(grep 'entity_type:' "$f" | grep -o '"[^"]*"' | tr -d '"')
  if [ "$type" = "person" ] && [ "$lines" -lt 25 ]; then
    echo "THIN: $(basename $f) ($lines lines)"
  fi
done
```

### Step 2: Match against unbox graph

For each thin entity, search the unbox relationship graph (`~/unbox-output/graph.json`) and all profiles for mentions:

```bash
# Extract person name from wiki entity
name=$(grep 'title:' "$entity_file" | sed 's/.*"\(.*\)".*/\1/')
# Search all profiles for this name
grep -rl "$name" ~/unbox-output/profiles/
```

### Step 3: Extract injectable content

From each matching profile, extract passages **directly about the thin entity**:

- PhD thesis acknowledgments mentioning the person (e.g., Ba calling Hinton "most caring supervisor")
- 师门谱系 sections that describe the person as advisor/mentor
- Collaborator descriptions
- Anecdotes or quotes about the person from interviews

**Rule:** Only extract content where the thin entity is the **subject**, not just a passing mention.

### Step 4: Generate injection proposal

For each thin entity, produce a structured proposal:

```markdown
## Injection Proposal: {entity name}

Current: {N} lines, {M} sources
Potential injections from unbox:

### From profiles/{profile-slug}.md
> "{direct quote or paraphrase about this person}"
→ Inject into: {section} | New section: {proposed section}

### From profiles/{other-slug}.md
> "{another relevant passage}"
→ Inject into: {section}
```

**Present all proposals to the user for confirmation before executing.**

### Step 5: Execute injection

For each approved injection:
- Append content to existing entity with source attribution: `(via unbox: [[profiles/{slug}]])`
- Update the entity's `sources:` list to include `"unbox-{profile-slug}"`
- Update the entity's `updated:` date
- Run cross-reference protocol (new `[[entities/...]]` links if needed)

### Step 6: Also consider concept/synthesis enrichment

Check if thin **concept** or **synthesis** pages reference the same topic areas as unbox profiles. For example:
- `concepts/diffusion-models.md` could reference Durk Kingma (Variational Diffusion Models)
- `synthesis/scaling-vs-efficiency.md` could reference Song Han (efficient ML)

This is lower priority than entity injection but can be done in the same pass.

## Common Mistakes

- **Writing a Wikipedia article instead of a personal wiki entry** — The "Why They Matter" section must be personal and opinionated, not neutral encyclopedia prose
- **Including too much** — If the wiki entry is over 60 lines, you kept too much. Compress harder. The full profile is always linked.
- **Forgetting cross-refs** — The whole point of wiki compilation is creating a connected graph. An isolated entity page is a failure.
- **Skipping the source page** — selfOS convention requires a source page for every ingest operation. The unbox profile IS the source.
- **Not updating index.md** — Every new entity must appear in the master index
- **Copying unverified claims** — The "未验证" section exists for a reason. Don't promote speculation into the wiki.
