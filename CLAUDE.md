# yuanbo-skills

Monorepo of portable Agent Skills, multi-skill plugins, and bundled projects.

## Gotchas

- Many entries under `skills/`, `plugins/`, and `projects/` are independent git
  submodules. Commit a changed submodule before updating the outer gitlink.
- Preserve unrelated dirty submodules and untracked files.
- Shared SKILL.md bodies must remain portable. Claude-specific named-agent
  schema belongs in host references or `.claude-plugin` metadata.
- Skill descriptions are discovery triggers. Deterministic mutations belong in
  scripts/tools; deep knowledge belongs in references; quality boundaries
  belong in tests or rubrics.
- Do not duplicate install commands, skill catalogs, or repository file trees
  here; load the relevant guide when changing those surfaces.

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

- `docs/design/context-engineering.md` — progressive disclosure, host parity,
  LabMate runtime boundaries, and verification.
- `docs/specs/2026-09-05-skill-capability-refactor.md` — capability-first second-round implementation and acceptance.

- `docs/reviews/2026-09-05-skill-capability-audit.md` — per-entry/resource dispositions.
- `docs/reviews/2026-09-05-skill-capability-validation.md` — regression evidence and open live checks.
- `docs/reviews/2026-09-05-wiki-capability-followup.md` — LabMate archival and selfOS wiki follow-up.
