# Testing

This document describes how to validate plugins, skills, and scripts in this repository.

## Skill Validation

Run the full skill validator to check frontmatter, structure, and conflicts:

```bash
python scripts/validate_skills.py .
```

This runs three checks in sequence:
1. **Frontmatter** — every `SKILL.md` has a valid `name` and `description`.
2. **Structure** — all department plugin directories follow the expected layout.
3. **Conflicts** — no two skills in the same plugin share the same name or id.

## Plugin Manifest Validation

Validate all JSON manifests (`.claude-plugin/`, `.codex-plugin/`, `.cursor-plugin/`):

```bash
bash scripts/validate-json.sh
```

## External Skill Check

Verify that all external skill references in `references/external-skills.yaml` are resolvable:

```bash
python scripts/check-external-skills.py
```

## Skill Meta Check

Check `.skillmeta.yml` completeness across all installed skills:

```bash
python scripts/skillctl.py meta check --root . --require-all
```

## Legal Language Check

Validate that no skill files contain disallowed legal language:

```bash
bash scripts/validate-legal-language.sh
```

## Running All Checks

To run every check in sequence:

```bash
python scripts/validate_skills.py . \
  && bash scripts/validate-json.sh \
  && python scripts/check-external-skills.py
```

A zero exit code from each script means all checks passed.

## Adding New Skills

When adding a new skill, run the full suite before opening a PR to catch:
- Missing or malformed frontmatter in `SKILL.md`
- Missing `.skillmeta.yml`
- Broken references to `external-skills.yaml` entries
- Duplicate skill names within the same department plugin
