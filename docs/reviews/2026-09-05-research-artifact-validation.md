# Research artifact iteration: validation record

Date: 2026-09-05. Base: outer `2c0005e`. Branch:
`codex/research-artifact-contracts-20260905`, with separate Paper Storyteller and
Paper Style feature worktrees. Main checkout and installed skill targets are not
changed by this iteration. No push, merge, plugin release or environment migration.

Inner commits: Paper Storyteller `79fdfa1`; Paper Style `6e4c75d` (both on
`codex/artifact-contracts-20260905`). The outer feature branch records their gitlinks.

## Standard used

Keep domain taste and verified reference structure, adapt execution to the task,
and judge completion from observed artifacts. The skill-creator independent
forward-test guidance informed the isolated consumer tasks; writing-skills testing
was applied proportionally, without its automatic deployment or rigid workflow
requirements overriding the user's scope. Existing successful behavior was retained.

## Independent consumer results

The baseline agents read the original skill and its references at the base commit.
Fresh forward-test agents read the changed skill. They received task inputs, not
the suspected instruction defect or a target answer. These are single-run examples,
not a statistically controlled model/reasoning benchmark. No reasoning default changed.

All research fixtures are explicitly authored synthetic inputs, not publications
or evidence of a real serving improvement. They require no invented citations.

| Task | Baseline observation | Changed-skill output and review |
| --- | --- | --- |
| Five-minute queue explanation | 8-page storyboard: cover, TOC, 4 explanation pages, four-takeaway page, source page | 5-page PDF, including 4 substantive pages; one utilization/waiting tension, exact calculation, scope and callback retained; no TOC quota |
| Twelve-minute midpoint theorem | 11-page storyboard; already respected proof and no-experiment boundary | 8-page PDF with definitions, statement, complete proof, unique optimum, example and geometry limit; no ablation or invented source figure |
| Eight-minute adaptive draft proposal | 10-page storyboard; already labeled concern, proposal and no results | 7-page PDF with unmeasured concern, correctness contract, candidate policy, planned grid/metrics and falsifiers; no achieved performance claim |
| Polish one Methods paragraph | Already stayed local, preserving the identity and no-speed-test qualification | Same successful scope after cleanup; no required metaphor, interview or whole-paper rewrite |
| Correct an overstated introduction | Additional targeted forward test, not a matched baseline | Preserved competing `dynamic2025`, narrowed novelty to the memory cap, kept the supplied 12% result and p=0.01 with one-load scope; did not erase supported statistical significance |
| Existing venue palette integration | Instructions depended on editing/loading class-specific components | Real before/after PDF with only the requested table shading changed; source/class hashes, dimensions, font family, existing logo macro, anonymity and resolved natbib citation retained |

Forward task names in this run: `slides_baseline`, `prose_baseline`,
`slides_forward`, `prose_forward`. Duration figures above are requested talk lengths
and storyboard allocations, not measured rehearsals or task-execution timing.

### Retained Methods output

Given vectors a,b in R^d, we compute and return m=(a+b)/2. The objective
F(x)=||x-a||²+||x-b||² admits the decomposition
F(x)=2||x-m||²+||a-b||²/2, which shows that m is its unique minimizer.
This result applies only to squared Euclidean distance. We have not tested
computational speed against other solvers.

### Retained introduction output

Load-adaptive scheduling already exists in `\cite{dynamic2025}`, but that method
lacks a memory cap. Our contribution is to add a memory cap to load-aware
scheduling. In a controlled experiment at one tested load, our scheduler achieved
12% lower median latency than a fixed scheduler, a statistically significant
difference in a two-sided test across independent runs (p=0.01). We have not
compared our scheduler with `\cite{dynamic2025}`, evaluated other load regimes,
or established theoretical guarantees.

## Result-driven fixes

1. **Late initializer conflict:** original Research Slides initializer wrote four
   TeX files and `figs/` before finding a conflicting source manifest. Regression
   now checks that every existing file and directory remains untouched on conflict.
2. **Preview deletion:** original render helper deleted a sentinel `page-001.png`.
   Both render entry points now create unique child directories; prior previews survive.
3. **Empty/invalid page input:** empty selection previously passed and nonnumeric
   input leaked a conversion traceback. Both now fail with a specific message.
4. **False rebuild success:** after injecting a previously absent conditional
   `colors.tex`, latexmk reused the baseline PDF. The test initially missed this;
   adding a check that the palette actually entered the log exposed it. The helper
   now forces a fresh latexmk pass while retaining convergence management.
5. **Personal template behavior:** real compilation exposed its abstract-before-title
   contract and a broken empty-logo check. Documentation preserves the former;
   the class and split title component now handle the empty logo without trying
   to include an empty filename. A brace error during the split was caught and fixed.
6. **Recorder interpretation:** real XeTeX records `extractbb --version` as an
   input. It is now an explicit non-file freshness warning, not a missing asset.
7. **LuaTeX environment:** the installed TeX Live 2021 first lacked a writable
   font cache, then spent over six minutes initializing a fresh isolated database.
   That test-owned process was stopped. Commands now have configurable timeouts
   and terminate their process group on timeout rather than hanging indefinitely.
8. **Paper setup:** preflight includes both Python and LaTeX files, destination
   symlinks are refused, identical setup is a no-op, and all five theme selections
   agree across both languages. Ordinary write-error rollback is not advertised
   as crash-atomic behavior.

## Actual artifact evidence

Independent agent outputs and full QA record:
`/private/tmp/research-artifact-forward-20260905/QA-REPORT.md`.
The reviewer opened all 20 final slide PNGs at 180 dpi, including a second review
after adding a waiting-time label and improving argmin spacing. No unresolved
clipping, overlap, missing glyph or invented-result defect was observed.

The parent rebuilt the retained sources in
`/private/tmp/research-examples-rebuilt-20260905/`, inspected queue page 4, theorem
page 5 and proposal page 5, and byte-compared all 20 rebuilt PNGs against the
independently reviewed renders: identical. Source notes, manifests, storyboards
and all three `.tex` files are committed under `tests/fixtures/research-artifacts/`;
layout files are taken from the existing bundled starter during reconstruction.

Paper/engine integration succeeded in
`/private/tmp/research-artifact-builds-20260905-h/` with XeLaTeX and pdfLaTeX.
The parent visually inspected the one-page venue before/after and personal report
from attempt `e`; later fixes concern engine execution, not those layouts. The
venue's only observed visual difference was the requested light-blue table cell.
No official conference class was supplied: this is an authored two-column fixture
with anonymity, geometry, natbib, hyperref and an existing logo macro, not a claim
of universal venue compatibility.

Real engine checks cover converged cross-references, changed included-source
staleness rejection, explicit engine choice, local latexmk configuration, and
automatic pdfLaTeX fallback with XeLaTeX/LuaLaTeX/latexmk absent from PATH. The
standalone preview CLI also retained an existing sentinel image. No native reader
or model outcome was replaced by a mocked success.

## Reproduce

Run from a fully populated feature worktree. Use new output directories each time:

```bash
python3 skills/research-slides/scripts/test_template.py
python3 skills/research-slides/scripts/test_workflows.py
python3 skills/paper-style/tests/test_init.py
python3 tests/test-artifact-builds.py --out /private/tmp/artifact-check-new --engines xelatex pdflatex
python3 tests/test-research-examples.py --out /private/tmp/research-examples-new
python3 scripts/validate_skills.py
bash tests/test-context-audit.sh
bash tests/test-install.sh
git diff --check
```

The first three checks pass (template contract, 7 workflow tests, 4 paper setup
tests including five-theme subcases). Format validation: 51/51 public entries.
Context audit: 0 errors, 7 review signals, 4 checker tests passed. Installer tests
passed using temporary HOME; existing installed Codex/Claude paths were not changed.
Both changed submodule diffs were also checked for whitespace errors.

The integration script defaults to all three engines. Omitting `--engines` retries
LuaLaTeX too; `--tex-cache` can reuse a task-specific temporary cache. Do not label
the selected two-engine run as an all-engine pass.

## Resource dispositions

| Skill | Changed | Reviewed and retained |
| --- | --- | --- |
| Research Slides | Entry, SD profile, modes, paper patterns, writing rules, QA; build/render/init helpers; behavior tests | Visual-style, figure extraction, citation/media evidence, multi-agent routing, worked SD example, host metadata and all visual assets |
| Paper Storyteller | Entry, style checklist/principles, all six section guides, README | Optional brainstorm protocol, host allowed-tools metadata, original attributed style examples |
| Paper Style | Entry, init/inject/guard guides, initializer/tests, dependency and preamble split, empty-logo handling, README/changelog | Five color values/palettes, Python API, matplotlib style, examples and license; class typography/layout otherwise retained |

No old rule was merely relocated to an unexamined reference. No Beamer Style
submodule, third-party `latex-document`, LabMate hook, selfOS record or historical
research artifact was changed.

## Remaining limits

- LuaLaTeX completed-build verification remains pending on a working font-cache
  runtime. Neither a mock nor the available binary's existence counts as a pass.
- No current official conference-template certification, physical projection test,
  timed rehearsal or multi-run Light/Medium model comparison was performed.
- `--no-compile` only checks known recorder inputs; newly appearing conditional
  files and external preprocessing/bibliography dependencies can require rebuilding.
- The numerical fixture derives from supplied premises; the proposal is untested.
- Initializer rollback covers ordinary errors, not process crashes or concurrent
  edits occurring after the final preflight. Review conflicts before using `--force`.
- This iteration is locally committed, not installed, merged or pushed. Deployment
  remains a separate user-authorized step.
