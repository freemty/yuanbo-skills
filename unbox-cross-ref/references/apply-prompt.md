# Cross-Reference Apply Task

You are applying cross-reference findings to unbox researcher reports. You will backfill missing information and resolve factual conflicts.

## Your Assignments

You have been assigned the following people to update:

{ASSIGNMENTS}

Each assignment has:
- `slug`: the person's report filename (without .md)
- `report_path`: full path to their report
- `mentions`: list of cross-mentions about this person from other reports

## Task

For each person in your assignments:

### Step 1: Read the person's report

Use the Read tool to read their full report.

### Step 2: Classify each mention

For each cross-mention, determine:

**BACKFILL** — The fact is NOT present anywhere in the person's report.
- Check thoroughly: the info might be phrased differently or in a different section
- If the person's report already contains the same info (even partially), classify as CONFIRM

**CONFIRM** — The fact is already present in the person's report, consistent.
- No action needed, skip.

**CONFLICT** — The fact contradicts something in the person's report.
- Note both versions and their sources

### Step 3: Apply backfills

For each BACKFILL item:

1. Identify the most relevant section in the report to add it to:
   - Relationship info → "师门谱系" or "频繁合作者"
   - Event/date info → "性格信号" > "其他发现" or "时光机"
   - Affiliation info → "身份锚点"
   - Personality info → "性格信号" > "其他发现"
   - If no fitting section exists → "未验证 / 待挖"

2. Check for existing `📎 交叉补充` markers to avoid duplicates. If the same fact (even worded differently) already has a backfill marker, skip.

3. Add at the END of the chosen section (before the next `##` heading), using this format:
   ```
   > 📎 交叉补充 (来源: {source_slug}.md): {fact}
   ```

Use the Edit tool for each addition.

### Step 4: Resolve conflicts

For each CONFLICT item:

1. Compare evidence quality:
   - Primary source (the person's own homepage, their own blog post, official university page) > secondary mention in another person's report
   - Specific date > approximate date
   - More recent information > older information
   - Information with cited URL > uncited claim

2. If one side is clearly more reliable:
   - Edit the LESS reliable version to match the MORE reliable one
   - Add an HTML comment at the edit point:
     ```
     <!-- cross-ref: 原文为 "X"，{other_slug}.md 记为 "Y"，已修正为 Y (来源更可靠: {reason}) -->
     ```

3. If truly ambiguous (both sides have equal evidence):
   - Do NOT change either report
   - Add a note in the less-detailed report's "未验证 / 待挖" section:
     ```
     > ⚠️ 待验证 (与 {other_slug}.md 冲突): {description of conflict}
     ```

4. **Special case — conflict resolution with URL verification**:
   If both sides cite a URL and the conflict is about a verifiable fact (date, affiliation, title), you MAY fetch those specific URLs using:
   ```
   python3 ~/.claude/skills/web-fetcher/scripts/fetch.py <url>
   ```
   Only fetch URLs that are already cited in the reports. Do NOT do speculative Google searches.

### Step 5: Write change log

After processing all people in your batch, write a summary to `{CHANGES_FILE}`:

```markdown
# Changes for batch {BATCH_ID}

## {Person Name} ({slug})

### Backfills
- [section: 师门谱系] Added: "..." (from {source}.md)
- [section: 其他发现] Added: "..." (from {source}.md)

### Conflicts Resolved
- Changed "X" to "Y" in line ~{N} (based on: {reason})

### Conflicts Unresolved
- {slug_a}.md says "X", {slug_b}.md says "Y" — insufficient evidence

### Skipped (already present)
- {count} mentions confirmed as already present

---
```

## Important Rules

- **Preserve formatting** — match the indentation and style of the surrounding text
- **Don't restructure** — only append within existing sections, never reorganize
- **Be conservative** — when in doubt, put it in "未验证 / 待挖" rather than asserting it as fact
- **Idempotent** — check for existing `📎` and `⚠️` markers before adding
- **No external research** — only use information from the reports themselves, unless resolving a conflict with cited URLs
