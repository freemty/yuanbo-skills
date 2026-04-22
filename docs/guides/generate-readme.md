# generate_readme.py

Auto-generate README.md skill tables from a centralized `SKILLS` dict. Replaces content between `<!-- BEGIN SKILLS -->` / `<!-- END SKILLS -->` markers.

## Usage

```bash
# Preview tables to stdout (no file changes)
python3 scripts/generate_readme.py

# Update README.md in place
python3 scripts/generate_readme.py --write
```

## When to Run

- After adding or removing a skill/plugin/project
- After changing a skill's category or description
- After renaming a directory

## Adding a New Skill

1. Edit `scripts/generate_readme.py`, add an entry to the `SKILLS` dict:

```python
"my-new-skill": {
    "category": "Productivity",
    "description": "One-line human-readable description",
    "type": "plugin",  # optional, defaults to "skill"
},
```

2. If the category is new, add it to `CATEGORIES` list (controls display order).

3. Run `python3 scripts/generate_readme.py --write`.

## Type Mapping

| `type` value | Directory |
|-------------|-----------|
| `skill` (default) | `skills/` |
| `plugin` | `plugins/` |
| `project` | `projects/` |

## Validation

The script warns on:
- **MISSING**: Skill listed in dict but no `SKILL.md` found on disk
- **UNLISTED**: Directory has `SKILL.md` but not in `SKILLS` dict
- **UNKNOWN CATEGORY**: Category not in `CATEGORIES` list

Warnings print to stderr; safe to run in CI.
