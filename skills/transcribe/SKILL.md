---
name: transcribe
description: Use when an audio or video file needs speech-to-text transcription. Triggers on audio file paths (.mp3/.wav/.m4a/.aac), 转写, 录音转文字, 帮我转写, meeting recordings, voice memos, or any speech-to-text request.
user-invocable: true
---

# Transcribe

Use an available native transcription capability when it meets the requested
language, timestamp and speaker needs. The bundled provider adapter is optional.
For that adapter, resolve this skill's directory and inspect the interface:

```bash
python3 <skill-dir>/scripts/transcribe.py --help
```

Read `references/workflow.md` only for provider setup, edge cases, and output
handling. Verify the input file and duration before calling a paid provider.
Return the transcript path and note language, speaker handling, and uncertain
segments. Keep timestamps for quotations or media alignment. Transcribing a video's
audio does not establish screen content or visible actions.

Do not archive, summarize, or publish a transcript unless the user requested
that additional action.
