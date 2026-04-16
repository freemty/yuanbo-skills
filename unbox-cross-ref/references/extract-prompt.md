# Cross-Reference Extraction Task

You are scanning unbox researcher reports to extract **cross-mentions** — places where report A mentions a fact about person B.

## Registry

Below is the full registry of all people with reports. You are looking for mentions of ANY of these people in the reports assigned to you.

```
{REGISTRY}
```

## Your Reports

You have been assigned the following reports to scan:

{REPORT_LIST}

## Task

For each report, scan the full text and find every mention of another person from the registry. For each mention, extract a structured record.

### What counts as a cross-mention

- A says "B was my advisor" → relationship
- A says "interned at Adobe, host: B" → event about B
- A says "B joined the lab in 2019" → date about B
- A says "B is now at Google DeepMind" → affiliation about B
- A says "B's rebuttal style is aggressive" → personality about B
- A says "collaborated with B on paper X" → relationship
- A says "B left CUHK in 2022" → event + date about B

### What does NOT count

- A mentions B only in their own publication list (e.g., "B. Smith" as a co-author name in a paper title) — unless there's additional context
- A mentions B in the "原始来源" section as a URL
- Generic references like "the lab" or "the advisor" without naming a specific registry person

### Output Format

Write your output to: `{OUTPUT_FILE}`

Use this exact format, one block per mention, separated by blank lines:

```
SOURCE: {slug}
ABOUT: {slug}
TYPE: {relationship | event | date | affiliation | personality}
FACT: {concise one-line fact}
CONTEXT: {the actual sentence or phrase from the report, verbatim}
LINE: {line number}
```

Example:
```
SOURCE: yinghao-xu
ABOUT: kai-zhang
TYPE: event
FACT: 2023.6-2023.9 徐英豪在 Adobe Research 实习，host 是 Kai Zhang
CONTEXT: 增加 Adobe 实习: 2023.6-2023.9 at Adobe Research (host: Kai Zhang)
LINE: 106

SOURCE: yinghao-xu
ABOUT: yujun-shen
TYPE: personality
FACT: 沈宇军是徐英豪"对科研生涯产生巨大影响的第二个人"
CONTEXT: 沈宇军在他知乎文中被称为「对我科研生涯产生巨大影响的第二个人」
LINE: 167
```

### Important

- Be thorough — scan every line, not just headers
- Include the verbatim context so downstream can verify
- One mention per block, don't merge multiple facts
- If the same fact appears multiple times in the same report, only extract once
- Do NOT extract self-references (A's report mentioning A)
