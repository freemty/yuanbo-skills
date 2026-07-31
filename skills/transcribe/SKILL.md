---
name: transcribe
description: Use when an audio or video file needs speech-to-text transcription.
user-invocable: true
---

# Transcribe

Resolve this skill's directory and inspect the interface:

```bash
python3 <skill-dir>/scripts/transcribe.py --help
```

Read `references/workflow.md` only for provider setup, edge cases, and output
handling. Verify the input file and duration before calling a paid provider.
Return the transcript path and note language, speaker handling, and uncertain
segments.

Do not archive, summarize, or publish a transcript unless the user requested
that additional action.
