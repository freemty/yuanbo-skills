# Citation and Source Credit

## Slide Footnotes

Use standard paper format:

`Author et al., Title, arXiv:xxxx.xxxxx`

For online sources:

`Figure source: Organization, Title, URL label`

Keep footnotes semi-transparent and bottom-left. Put each source on its own line; do not run several citations together as one wrapped paragraph. Do not put only an arXiv id without author/title.

## Beamer Macros

The bundled `research-main.tex` starter provides:

```latex
\paperlink{label}{url}
\arxivcite{2503.09573}
\stdcite{Arriola et al.}{Block Diffusion}{2503.09573}
\slidecite{Figure source: \stdcite{Arriola et al.}{Block Diffusion}{2503.09573}}
```

For multiple citations in the same footnote:

```latex
\slidecite{\cDFlash\citesep \cJetSpec\citesep \cDSpark}
```

For a webpage or image, show the exact clickable URL:

```latex
\slidecite{Figure source: \webcite{TNG Technology Consulting, Prefill and Decode}{https://huggingface.co/blog/tngtech/llm-performance-prefill-decode-concurrent-requests}}
```

## References Slide

- Put References near the end.
- Use one or two dense pages and compact columns.
- Include author, title, and clickable arXiv or source URL.
- Keep one reference per line and ensure the links remain large enough to click in the PDF.
- Keep backup slides after References when they are not part of the main narrative.

## Source Credit Rules

- Any figure/table from a paper: cite the paper as `Figure source:` or `Table source:`.
- Any blog/website image: cite the exact webpage URL or image URL.
- Any self-redrawn figure based on a paper: cite `Adapted from: ...`.
- Any online material fetched during the task must leave a visible source trail in the deck.
- Keep a source manifest while authoring: asset path, source URL, figure/table number, page, crop, and claim supported.
