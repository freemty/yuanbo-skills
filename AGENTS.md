# yuanbo-skills

Monorepo of portable Agent Skills, multi-skill plugins, and bundled projects.

## Gotchas

- Many entries under `skills/`, `plugins/`, and `projects/` are independent git
  submodules. Commit a changed submodule before updating the outer gitlink.
- Preserve unrelated dirty submodules and untracked files.
- Shared SKILL.md bodies must remain portable. Put Claude/Codex invocation and
  policy differences in host metadata or install docs.
- Skill descriptions are discovery triggers. Deterministic mutations belong in
  scripts/tools; deep knowledge belongs in references; quality boundaries
  belong in tests or rubrics.
- Codex plugin skills are installed through the marketplace. Legacy global
  symlinks must not duplicate them.

## Verification

```bash
python3 scripts/validate_skills.py
bash tests/test-context-audit.sh
bash tests/test-install.sh
git diff --check
```

Platform and publishing details live under `docs/guides/` and the three install
documents.

## Design references

- `docs/specs/2026-09-05-research-artifact-contracts.md` — result-driven slide, story and LaTeX template iteration.

- `docs/design/context-engineering.md` — progressive disclosure, host parity,
  LabMate runtime boundaries, and verification.
- `docs/specs/2026-09-05-skill-capability-refactor.md` — capability-first second-round implementation and acceptance.

- `docs/reviews/2026-09-05-skill-capability-audit.md` — per-entry/resource dispositions.
- `docs/reviews/2026-09-05-skill-capability-validation.md` — regression evidence and open live checks.
- `docs/reviews/2026-09-05-wiki-capability-followup.md` — LabMate archival and selfOS wiki follow-up.
