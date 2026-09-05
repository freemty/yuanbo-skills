# Source adapters

`fetch.py URL [-o FILE]` emits Markdown, diagnostics on stderr. `--format json`
emits `source_url`, `retrieved_at`, `backend`, `status`, `content_kind`, `content`,
`limitations`. Status is `ok`, `partial`, `blocked` or `unsupported`. Blocked and
unsupported return exit 1 while still emitting the evidence envelope. Partial
retrieval returns 0 with explicit limits; it is not full task completion.

The CLI tries installed source-specific adapters, then HTTP text extractors:

| Source | Optional adapters | Coverage |
| --- | --- | --- |
| X | xreach, opencli, Thread Reader | Root/author replies/other accounts when structured IDs exist; media links uninspected |
| YouTube/Bilibili | yt-dlp | Metadata and timestamped VTT/SRT/JSON3/SRV1 captions; no audio/frames |
| GitHub issues/PRs | gh | Issue/PR text |
| Xiaohongshu | mcporter | Source response, verify attribution |
| Zhihu/Reddit/arXiv/Weibo | opencli | Source response; paper pages need separate full-text validation |
| Other text | Jina Reader, markdown.new, basic HTML | Completeness requires task-specific checking |

These are implementation fallbacks, not an ordering requirement for the host.
Unavailable CLIs are skipped. Proxy configuration is inherited only when set.
Short valid content is allowed. Login/challenge/error pages and navigation-only
shells are rejected, but extraction heuristics cannot certify semantic completeness.
For troubleshooting use the installed CLI's help; paths are relative to the
discovered skill directory, not an author's machine.
