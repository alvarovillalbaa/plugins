# Testing

This document describes how to validate plugins, skills, and scripts in this repository.

## Skill Validation

Run the full skill validator to check frontmatter, structure, and conflicts:

```bash
python3 scripts/validate_skills.py .
```

This runs six checks in sequence:
1. **Frontmatter** — every `SKILL.md` has a valid `name` and `description`.
2. **Structure** — all department plugin directories follow the expected layout.
3. **Conflicts** — no two skills in the same plugin share the same name or id.
4. **Hooks/scripts** — registrations, ownership, portability, executable
   contracts, placeholder absence, and per-skill documentation coverage.
5. **Rules** — canonical contract shape, full local-skill routing coverage,
   qualified cross-plugin routes, duplicate policy, and portability.
6. **Commands** — complete profile/catalog inventory, unique capability owners,
   no same-name skill shadowing, thin workflow contracts, and portability.

## Plugin Manifest Validation

Validate all JSON manifests (`.claude-plugin/`, `.codex-plugin/`, `.cursor-plugin/`):

```bash
bash scripts/validate-json.sh .
claude plugin validate --strict .
for department in engineering finances marketing product productivity sales system; do
  claude plugin validate --strict "$department"
done
```

The `claude` commands are the authoritative Claude manifest/component check
when the CLI is installed. The repository validators remain runtime-neutral.

## Hook and Script Boundary Audit

Inventory all plugin/skill hooks and scripts, resolve registered handlers, and
check coverage, ownership conflicts, excess placeholders, and portability:

```bash
python3 scripts/audit_hooks_scripts.py .
```

Render the per-plugin and per-skill coverage matrix:

```bash
python3 scripts/audit_hooks_scripts.py . --report docs/audits/plugins/hooks-scripts-current.md
```

## Rule Coverage and Conflict Audit

Validate every department rule contract, profile-to-rule skill coverage,
cross-plugin route qualification, duplicate policy lines, and hardcoded private
or organization-specific identifiers:

```bash
python3 scripts/audit_rules.py .
```

## Command Coverage and Conflict Audit

Validate every active command against the canonical capability registry,
including profile parity, unique ownership, same-plugin skill collisions,
retired-command absence, size, duplicate bodies, and portability:

```bash
python3 scripts/audit_commands.py .
```

Render the complete ownership and boundary matrix:

```bash
python3 scripts/audit_commands.py . --report docs/audits/plugins/commands-current.md
```

## External Skill Check

Verify that all external skill references in `references/external-skills.yaml` are resolvable:

```bash
python3 scripts/check-external-skills.py
```

## Skill Meta Check

Check `.skillmeta.yml` completeness across all installed skills:

```bash
python3 scripts/skillctl.py meta check --root . --require-all
```

## Installer And Runtime Contracts

Exercise the project-local flattened installer, no-loss update behavior, and
dynamic runtime-variable resolution through the bundled test runner:

```bash
python3 -m unittest scripts.tests.test_project_installer
python3 -m unittest scripts.tests.test_runtime_context
python3 -m unittest scripts.tests.test_skillctl_project_runtime
```

These tests use temporary repositories. They must cover every installable
component type, whole-plugin expansion, collision handling, persistent lock
state, disjoint local/upstream merges, staged conflicts, personalization
preservation, and dry-run behavior. Reconciliation coverage must also prove
typed-selector filtering, default and explicit bundle destinations, exact
base/local/incoming exports when snapshots exist, honest base-unavailable
metadata for legacy managed blocks, safe representation of missing/binary/tree
values, rejection of symlinks and unsafe paths, and byte-for-byte preservation
of managed targets, locks, existing staged conflict artifacts, and
personalization during export.

Post-review adoption coverage must separately prove that `--accept-local`:

- supports dry-run without writes and requires interactive confirmation or
  explicit `--yes` before mutation;
- accepts multiple unique component conflict IDs atomically while leaving
  unselected conflicts and their artifacts untouched;
- rejects unknown IDs, managed-block IDs, duplicate IDs, incompatible
  selectors/`--output`, and tampered staged or saved-base digests;
- never edits the component target or invokes AI, and rolls metadata changes
  back if any selected adoption fails; and
- leaves the adopted current local value as a preserved customization when a
  later upstream update changes the latest accepted base.

## Generated Discovery Artifacts

Verify that the machine-readable catalog and LLM-facing indexes exactly match
the current plugin profiles and component frontmatter:

```bash
python3 scripts/generate_discovery_catalog.py --check
python3 -m unittest scripts.tests.test_generate_discovery_catalog
```

Validate the typed, arbitrarily deep, cycle-safe component graph:

```bash
python3 scripts/component_graph.py build --check
python3 -m unittest scripts.tests.test_component_graph
```

## Legal Language Check

Validate that no skill files contain disallowed legal language:

```bash
bash scripts/validate-legal-language.sh
```

## Running All Checks

To run every check in sequence:

```bash
python3 scripts/validate_skills.py . \
  && python3 scripts/audit_hooks_scripts.py . \
  && python3 scripts/audit_rules.py . \
  && python3 scripts/audit_commands.py . \
  && python3 scripts/run_skill_tests.py . \
  && python3 scripts/generate_discovery_catalog.py --check \
  && python3 scripts/component_graph.py build --check \
  && bash scripts/validate-json.sh . \
  && python3 scripts/check-external-skills.py
```

A zero exit code from each script means all checks passed.

## Adding New Skills

When adding a new skill, run the full suite before opening a PR to catch:
- Missing or malformed frontmatter in `SKILL.md`
- Missing `.skillmeta.yml`
- Broken references to `external-skills.yaml` entries
- Duplicate skill names within the same department plugin
