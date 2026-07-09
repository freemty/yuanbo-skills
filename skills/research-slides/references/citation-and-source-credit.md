# Citation and Source Credit

## Slide Footnotes

Use standard paper format:

`Author et al., Title, arXiv:xxxx.xxxxx`

For online sources:

`Figure source: Organization, Title, URL label`

Keep footnotes semi-transparent and bottom-left. Do not put only an arXiv id without author/title.

## Beamer Macros

The `beamer-style` `layout-research` template provides:

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

## References Slide

- Put References near the end.
- Use dense columns.
- Include author, title, and clickable arXiv or source URL.
- Keep backup slides after References when they are not part of the main narrative.

## Source Credit Rules

- Any figure/table from a paper: cite the paper as `Figure source:` or `Table source:`.
- Any blog/website image: cite the exact webpage URL or image URL.
- Any self-redrawn figure based on a paper: cite `Adapted from: ...`.
- Any online material fetched during the task must leave a visible source trail in the deck.
