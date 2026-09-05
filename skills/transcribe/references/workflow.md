# Speech transcription

Select available native transcription or an explicitly configured provider.
Identify input path/URL, language, duration and requested timestamps/speaker labels.
For video speech, use supported native media input or extract an audio working copy
with an available converter. Never claim to have inspected video actions from ASR.

## Bundled provider adapter

`scripts/transcribe.py <file_or_url> [-o output.md] [--json]` uses Volcengine ASR.
Read its help and check the current service documentation if setup/limits matter.
Check credential presence without printing its value. If absent, use an available
native route or explain the provider requirement; do not write shell startup files
or make the whole task fail solely because this optional key is missing.

Do not send private recordings to an additional service outside the authorized
task. Preserve the input and raw transcript before editorial changes. Inspect
adapter failures rather than assuming empty output means silence.

## Deliverable

Return actual transcript/output path when saving was requested, source, language,
timestamp coverage, speaker-label confidence and uncertain spans. Speaker IDs are
not identified people; use supplied names or reliable audio/context evidence,
otherwise retain anonymous labels. Do not force a speaker-identification question
when the requested transcription can be completed with labels.

Keep original wording distinct from corrections, summary and translation.
Timestamped quotations retain interval and transcript origin. A transcription
request does not itself authorize wiki archival or publication.
