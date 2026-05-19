---
name: transcribe
description: "Use when user provides an audio file path (.mp3/.wav/.m4a/.aac) or says 转写/录音转文字/帮我转写. Also triggers on meeting recordings, voice memos, or any speech-to-text request."
user-invocable: true
---

# /transcribe — Audio Transcription

Transcribe audio files using Volcengine (火山引擎) ASR API. Supports speaker diarization, punctuation, and timestamps.

## When to Use

- User provides audio file path (mp3/wav/m4a/aac/ogg/opus/pcm/amr/spx)
- User says "转写", "录音转文字", "帮我转写", "/transcribe"
- Meeting recordings, voice memos, any speech-to-text request

**Not for:** live streaming ASR, TTS, video-only files

## Setup Guide

If `VOLCENGINE_ASR_API_KEY` is not set, output this and STOP:

```
### 🔑 火山引擎 ASR 设置

1. 打开 https://console.volcengine.com/speech/app
2. 注册/登录（支持手机号）
3. 点击「语音识别」→「大模型语音识别」→「立即试用」（20 小时免费）
4. 在控制台创建 API Key
5. 设置环境变量：

   echo 'export VOLCENGINE_ASR_API_KEY="你的key"' >> ~/.zshrc
   source ~/.zshrc

设置好后再次运行 /transcribe 即可。
```

## Quick Reference

| Constraint | Limit |
|-----------|-------|
| Max file size | 100MB |
| Max duration | 2 hours |
| Formats | mp3, wav, m4a, aac, ogg, opus, pcm, amr, spx |
| Languages | Chinese (primary) + 23 others |
| Features | speaker diarization, punctuation, timestamps, ITN |

## Flow

### 0. Check API Key

```bash
echo "${VOLCENGINE_ASR_API_KEY:-NOT_SET}"
```

If `NOT_SET` → print Setup Guide and stop.

### 1. Transcribe

```bash
VOLCENGINE_ASR_API_KEY="$VOLCENGINE_ASR_API_KEY" python3 scripts/transcribe.py "<file_path>" -o /tmp/transcript-output.md
```

### 2. Present Result

Show: duration, speaker count, first few lines. Ask user what to do next.

## Script

The transcription script lives at `scripts/transcribe.py` in this skill directory (or at the project's `scripts/transcribe.py`).

Usage:
```bash
python3 scripts/transcribe.py <file_or_url> [-o output.md] [--json]
```

## Common Mistakes

- Attempting transcription without checking API key first
- Not saving raw transcript before any post-processing
- Forgetting to ask user to identify speakers
