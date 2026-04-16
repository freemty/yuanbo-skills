# Suggest Workflow

Step-by-step for `/unbox-to-wiki --suggest`.

## Purpose

Analyze all 77 unbox profiles and recommend which ones are most worth adding to the selfOS wiki, based on relevance to the user.

## Step 1: Read Current Wiki State

1. Read `~/selfos/wiki/index.md` to know what's already in wiki
2. Read `~/selfos/wiki/overview.md` to understand the user's research identity
3. List existing entity pages: `ls ~/selfos/wiki/entities/`
4. Identify the user's research areas, interests, and network from wiki content

## Step 2: Scan All Profiles (Lightweight)

For each of the 77 profiles in `~/unbox-output/profiles/`:
- Read only the first 30 lines (enough for identity anchoring + opening quote)
- Extract: name, current role, institution, research area, h-index if visible
- Check if already compiled into wiki (skip if yes)

## Step 3: Score Each Profile

Score 1-5 on each criterion (from SKILL.md):

| Criterion | Weight | What to Look For |
|-----------|--------|------------------|
| Research overlap | 2x | Same or adjacent field to user's work |
| Network proximity | 2x | Advisor/student/collaborator of someone in wiki |
| Graph centrality | 1x | Mentioned in 3+ other profiles' cross-ref notes |
| Personality signal | 1x | Exceptional/unusual traits worth remembering |
| Institution relevance | 1x | At institutions the user might interact with |

**Composite score** = (research_overlap * 2) + (network_proximity * 2) + graph_centrality + personality_signal + institution_relevance

Maximum: 35 points.

## Step 4: Cross-Reference Density Check

For high-scoring candidates (composite >= 15), do a deeper check:
```bash
grep -c "{name}" ~/unbox-output/profiles/*.md
```
Count how many OTHER profiles mention this person. High cross-mention count = high graph centrality.

Also check:
```bash
grep -ri "{name}" ~/selfos/wiki/ --include="*.md" -c
```
If already mentioned in wiki pages but without their own entity page, they're a strong candidate.

## Step 5: Generate Recommendations

Output format:

```markdown
## Recommended for Wiki (Score >= 20)

### Tier 1: High Priority
| Name | Score | Key Reason |
|------|-------|------------|
| ... | 28 | ... |

### Tier 2: Worth Adding
| Name | Score | Key Reason |
|------|-------|------------|
| ... | 22 | ... |

## Maybe Later (Score 15-19)
| Name | Score | Key Reason |
|------|-------|------------|
| ... | 17 | ... |

## Skip (Score < 15)
{Count} profiles not recommended. Reasons: distant research area, no wiki connections, etc.
```

For each recommended person, include:
- One-line from their profile (the thesis/opening quote)
- Primary reason they should be in wiki
- Which existing wiki entities they connect to

## Step 6: Offer Batch Compile

After presenting recommendations:
> "Want me to compile the Tier 1 recommendations? Run: `/unbox-to-wiki --batch name1 name2 ...`"

## Performance Notes

- This workflow reads ~77 files (first 30 lines each) — about 2300 lines total
- Use parallel reads where possible
- Cache the profile summaries for the session — don't re-read if the user immediately runs --batch
- For the scoring, err on the side of fewer, higher-quality recommendations over comprehensive lists
