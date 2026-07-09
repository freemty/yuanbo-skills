# transcribe

Audio transcription skill using Volcengine ASR.

Use when an audio file path is provided or the user asks for speech-to-text transcription.

## Install

Use the repo installer:

```bash
./install.sh --target codex
```

Manual Codex install:

```bash
ln -sf "$(pwd)" ~/.agents/skills/transcribe
```

## Setup

Set `VOLCENGINE_ASR_API_KEY` before running transcription.
