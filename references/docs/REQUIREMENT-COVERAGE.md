# Requirement Coverage

This document maps the installation, discoverability, personalization, dynamic
context, relationship, and update requirements to their executable owners.

## Installation

| Requirement | Implementation | Verification |
| --- | --- | --- |
| Own interactive command is the first choice | `scripts/plugins install` and `project_installer.prompt_selectors` | Interactive tests cover whole-plugin number selection and per-component selection. |
| Install complete plugins | Typed selector `plugin:<plugin>` | Whole-plugin test expands every declared component. |
| Install individual skills, commands, rules, and agents | Typed selectors `skill:`, `command:`, `rule:`, and `agent:` | Four-type install test and CLI end-to-end smoke. |
| Always use the project-local flat layout | `.agents/{skills,commands,rules,agents}` | Installer rejects path escapes and never creates `.agents/<plugin>/`. |
| Handle flat-name collisions | Deterministic plugin-qualified names and atomic target migration | Multi-plugin and late-collision migration tests. |
| Offer multiple methods with clear favorites | `references/docs/INSTALLATION.md` | The first-party interactive and explicit commands are marked as favorites; secondary methods state their limits. |

## Discovery And Positioning

| Requirement | Implementation | Verification |
| --- | --- | --- |
| LLM-readable repository discovery | Generated `llms.txt` and `llms-full.txt` | Deterministic generator drift check. |
| Machine-readable inventory | Generated `catalog.json` | Profile-to-filesystem reconciliation and schema-shape tests. |
| Developer-agent indexing hints | Generated `context7.json` | JSON validation and drift check. |
| Software and citation metadata | `codemeta.json` and `CITATION.cff` | Linked from the generated canonical document index. |
| SEO, AEO, GEO, and LLM terminology | Marketing manifests and catalog descriptions | All platform manifests parse and all Codex plugin manifests pass plugin validation. |

The repository deliberately does not advertise a hosted agent endpoint, OpenAPI
service, MCP server, `robots.txt`, or sitemap because no canonical hosted service
exists here. Discovery files link to real source assets only.

## Personalization And Dynamic Variables

| Requirement | Implementation | Verification |
| --- | --- | --- |
| Most components are personalizable | `runtime-contract.json` enables inherited personalization for skills, commands, rules, and agents | Installed registry exposes the inherited variables for every installed component. |
| Personalize on first relevant use | Installed `rules/agent-runtime.md` routes initialization through `auto-improve` to `personalize`; the interactive `context` flow prompts for required invocation values | Runtime policy, interactive prompt, and project sync integration tests. |
| Accept values dynamically at use time | `scripts/plugins context <typed-id> --set name=value`, with optional `--render`/`--output` substitution for `{{dotted.name}}` and `$ARGUMENTS` | Precedence and rendering tests cover invocation, session, project, defaults, component opt-out, and unresolved placeholders. |
| Keep sensitive or invocation-only data ephemeral | Runtime variable definitions and persistence guards | Tests reject sensitive persistence and keep invocation scope out of the project store. |

Project personalization lives in `.agents/personalization.local.json`, is mode
`0600`, is ignored by Git through a bounded managed block, and is outside the
managed component snapshots.

## Recursive Relationships

| Requirement | Implementation | Verification |
| --- | --- | --- |
| Arbitrarily deep chaining | Iterative breadth-first resolver with no fixed depth cap | Focused test resolves a 1,200-hop graph. |
| Parallel fan-out | Every breadth level records parallel and sequential candidate groups for host relevance selection | Graph resolver tests. |
| Internal and external skills | Typed `skill:` and `external-skill:` nodes populated from the source map and registries | Graph build and conflict checks. |
| Two-sided chaining and cycles | Visit-once traversal reports re-entry edges instead of rejecting or executing them again | Cycle tests and 179 preserved live cycle edges. |
| Plugin and cross-element references | Full generated `component-graph.json`, sourced from the typed overlay in `references/component-graph.json` plus repository inventories | Live graph contains plugin-to-plugin, agent-to-command, command-to-skill, and rule-to-skill routes. |
| Invoke only available components | Installed project graph marks each node; `graph resolve --project . --available-only` filters unavailable targets and reports blocked edges | Installed-aware graph tests cover unavailable targets and roots. |

The resolver's “unbounded” contract means arbitrary finite depth. Its output is a
conditional relationship closure: the host must prune it to task-relevant candidates
before invoking anything. Cycles remain expressive relationships without becoming
infinite execution loops.

## Reinstall And Update Safety

| Requirement | Implementation | Verification |
| --- | --- | --- |
| Preserve personalization | Personalization paths are excluded from source snapshots and local store is outside managed components | Reinstall integration test preserves the file byte-for-byte. |
| Preserve local changes | Saved upstream bases plus conservative three-way merge | Disjoint-edit, local-addition, local-deletion, and upstream-deletion tests. |
| Preserve renamed or removed components | Default update installs declared rename targets, retains predecessors and unknown removals as registry `orphaned` records, and updates the remaining components | Known-rename and mixed current/orphan update regression tests. |
| Never overwrite an unmanaged path | Ownership preflight before any swap | Unmanaged target and ownership-change tests. |
| Keep conflicts recoverable | Local file stays in place; incoming version is staged under `.agents/.updates`; lock and registry stay conflicted | Conflict persistence and resolution tests. |
| Export reviewable three-way conflict context | Opt-in `scripts/plugins reconcile --project <path> [selectors] [--output <dir>]` bundles recorded base, current local, and staged/generated incoming artifacts when available | Reconciliation tests cover component files and trees plus modified `AGENTS.md` and `README.md` managed blocks. |
| Keep AI reconciliation provider-neutral and suggestion-only | Bundles contain `manifest.json` and `REVIEW.md`; export mode never invokes AI, applies patches, mutates managed targets or locks, or persists secrets | No-mutation tests compare managed targets and lock state before and after export and exercise default and explicit output directories. |
| Represent incomplete or non-text context honestly | Bundle metadata records missing, binary, and tree values; legacy support entries mark unavailable base content, while symlinks and other unsafe entries are rejected | Legacy-lock and artifact-kind regression tests reject fabricated base content and unsafe path traversal. |
| Adopt a human-reviewed component resolution without editing it | Repeatable `--accept-local <conflict-id>` validates selected saved artifacts, requires confirmation or `--yes`, and atomically removes only selected component conflict/staged/base metadata while preserving the current local target | Required adoption coverage includes dry-run, confirmation, repeated IDs, digest tampering, atomic rollback, untouched targets and unrelated conflicts, and a later update preserving the adopted customization. |
| Keep managed document customization outside generated blocks | Managed-block conflict IDs are not accepted by `--accept-local`; restore the generated incoming block and retain project text outside its markers | Required managed-block coverage rejects adoption and verifies bounded-block restoration through normal update. |
| Avoid partial component installs | All selected components and the lock are preflighted and committed as one rollback-capable transaction | Multi-component preflight, interruption rollback, and recovery tests. |
| Improve project docs without replacing user content | Bounded managed blocks in `AGENTS.md`, `README.md`, and `.gitignore`; direct runtime indexes use `.plugin-support-lock.json`, are preflighted, and each changed file is replaced atomically | Reinstall integration tests preserve user-authored content, refuse unmanaged or locally modified support files, and reject symlink traversal before component commit. |

The no-loss update guarantees apply to first-party components tracked by
`.agents/.plugin-lock.json`. Optional provider-owned external skills use the separate
external registry installer, which defaults to `.agents/skills` but is not claimed as
part of the first-party merge lock. Runtime indexes and documentation blocks are
preflighted before the component transaction and written atomically per file; they are
not part of the single component-and-lock rollback unit.

Reconciliation bundles are ignored local review artifacts under
`.agents/.updates/reconcile/`, not managed source or proof that a conflict was
resolved. Export remains suggestion-only. After manual review and application,
a component resolution is completed either by normal update convergence or by
the separate confirmation-gated `--accept-local` metadata adoption. The latter
never edits the target and does not apply to managed document blocks.

## Validation Commands

```bash
python3 -m unittest \
  scripts.tests.test_project_installer \
  scripts.tests.test_runtime_context \
  scripts.tests.test_component_graph \
  scripts.tests.test_generate_discovery_catalog \
  scripts.tests.test_skillctl \
  scripts.tests.test_skillctl_project_runtime
python3 scripts/generate_discovery_catalog.py --check
python3 scripts/component_graph.py build --check
python3 scripts/skillctl.py structure check --root .
python3 scripts/skillctl.py meta check --root . --require-all
python3 scripts/skillctl.py conflicts check --root .
python3 scripts/validate_skills.py .
python3 scripts/audit_agents.py .
python3 scripts/audit_commands.py .
python3 scripts/audit_rules.py .
python3 scripts/audit_hooks_scripts.py .
python3 scripts/run_skill_tests.py .
bash scripts/validate-json.sh .
```
