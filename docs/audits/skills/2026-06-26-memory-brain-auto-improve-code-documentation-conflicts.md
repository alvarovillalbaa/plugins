# Memory, Brain, Auto-Improve, and Code-Documentation Conflict Audit - 2026-06-26

## Summary

This audit reviews the current conflicts between the memory-management, second-brain, auto-improve, and code-documentation skill families.

Status: Done on 2026-06-26.

The active canonical names in this repo are `memory`, `brain`, `ingestion`, `auto-improve`, and `code-documentation`. Do not reintroduce the older `memory-management` or `second-brain` slugs as alias skills; route that capability through the canonical owners.

Current state is better than the earlier monolithic skill split: `auto-improve` is now registered in `system/profile.yaml`, represented in `skills-chaining-map.md`, and backed by `scripts/skillctl.py`. The ownership and schema conflicts identified below have been resolved by the completion pass.

## Completion Evidence

Implemented remediation:

- Normalized the documentation AFS taxonomy to `facts/` instead of `items/`.
- Normalized default timestamped AFS paths to `YYYY/MM-DD/`.
- Renamed the durable-fact template to `engineering/skills/code-documentation/templates/fact.md`.
- Added `BRAIN.md` for this repo's partial-AFS adaptation and `docs/audits/skills/` mapping.
- Added `references/docs/promotion-matrix.md`.
- Referenced the promotion matrix from `memory`, `brain`, `ingestion`, `learning`, `agent-harness`, and `code-documentation`.
- Classified autoimprove round logs/results as generated review artifacts under `.skill-improvements/`, not canonical memory.
- Added `.skillmeta.yml` coverage for `engineering/skills/code-documentation`.
- Fixed and tested `skillctl` private-signal classification so public safety text mentioning secrets is not treated as private data.

Validation:

- Pass: `python3 scripts/validate_skills.py`.
- Pass: `python3 scripts/skillctl.py meta check --root .`.
- Pass: `python3 scripts/skillctl.py trace-origin system/skills/memory/SKILL.md engineering/skills/code-documentation/SKILL.md`.
- Pass: `python3 -m unittest scripts.tests.test_skillctl`.
- Pass: `git diff --check`.
- Pass: targeted search found no `items/`, `memory/autoimprove`, or old `YYYY/YYYY-MM-DD` AFS defaults in the edited owner surfaces.

## Evidence Map

| Surface | Current role | Evidence |
|---|---|---|
| `system/skills/memory/SKILL.md` | Claude-style memory stack: `CLAUDE.md`, `.claude/rules/`, auto-memory, session memory | Owns `/si:*` review, promote, extract, status, and remember flows. It is not AFS-native. |
| `system/skills/brain/SKILL.md` | Router for `BRAIN.md`-bounded second-brain work | Delegates raw/source compilation to `ingestion`; chains to `memory`, `knowledge-base`, `research`, and `reporting`. |
| `system/skills/brain/references/brain_contract.md` | Brain boundary and strict-AFS contract | Uses `facts/`, `steers/`, `models/`, `reflections/`, and default `YYYY/MM-DD/` dated folders. |
| `system/skills/ingestion/SKILL.md` | Raw/source ingestion and Memory-to-knowledge compilation | Compiles `raw/` plus repo-local Memory folders into canonical `knowledge/`. |
| `system/skills/auto-improve/SKILL.md` | Improvement router | Routes skill changes to `skill-eval-loop`, memories to `memory`, brain knowledge to `brain`/`ingestion`, personalization to `personalize`, loops to `loops`, and harness work to `agent-harness`. |
| `engineering/skills/agent-harness/references/autoimprove.md` | Batch prompt/reference improvement loop | Writes generated round artifacts under `.skill-improvements/` and uses `scripts/skillctl.py`. |
| `engineering/skills/code-documentation/SKILL.md` | AFS documentation routing | Uses `facts/` for durable facts and `*/YYYY/MM-DD/*.md` for timestamped docs. |
| `skills-chaining-map.md` | Canonical skill taxonomy | Includes `auto-improve` as a system parent and routes it to skill, memory, brain, ingestion, personalize, and loops lanes. |
| `scripts/skillctl.py` | Source/runtime provenance helper | Present in the current worktree and validates existing `.skillmeta.yml` files. |

## Ranked Findings

All ranked findings in this section are resolved. They are retained as historical context for the implementation pass.

### P1 - AFS Memory Taxonomy Is Split Across Two Owners

`brain_contract.md` defines strict AFS Memory as `logs/`, `lessons/`, `facts/`, `fixes/`, `steers/`, `models/`, and `reflections/`, with default date folders `YYYY/MM-DD/`.

`code-documentation` defines Memory as `logs/`, `lessons/`, `items/`, and `fixes/`, with `*/YYYY/YYYY-MM-DD/*.md`.

Impact:
- Agents can store the same durable fact in `facts/` or `items/`.
- Brain ingestion searches `facts/`, but code-documentation writes facts to `items/`.
- Strict AFS from `brain` and repo docs from `code-documentation` will create competing timestamp conventions.

Recommended owner decision:
- Make `brain_contract.md` the broader AFS schema owner because it governs second-brain boundaries and raw-to-knowledge compilation.
- Make `code-documentation` the doc-placement owner inside that schema.
- Either rename `items/` to `facts/` in code-documentation or explicitly map `items/` as the code-documentation alias for `facts/` in `brain_contract.md`, `wiki_compiler.md`, `/compile-raw`, and `find-docs.sh`.
- Pick one timestamp convention. The user-specified AFS convention for this audit is `YYYY/MM-DD/`; the repo currently uses `docs/audits/skills/` and older docs use `YYYY/YYYY-MM-DD/`.

### P1 - `code-documentation` Is Outside `skillctl` Provenance

`auto-improve` relies on `.skillmeta.yml` to classify whether a change is upstream-safe, local/private, generated/runtime, or a personalization template.

Current `skillctl` evidence:
- `system/skills/auto-improve/SKILL.md`: `upstream-safe`
- `system/skills/brain/SKILL.md`: `upstream-safe`
- `system/skills/ingestion/SKILL.md`: `upstream-safe`
- `engineering/skills/agent-harness/SKILL.md`: `upstream-safe`
- `engineering/skills/code-documentation/SKILL.md`: `upstream-safe`

Impact:
- Auto-improve cannot safely propose upstream changes to the documentation skill, even though `code-documentation` is a central downstream owner for AFS conflicts.
- Improvements that touch the docs taxonomy can be incorrectly blocked or treated as local-only.

Recommended fix:
- Add `.skillmeta.yml`, personalization schema, and upstream contribution policy to `engineering/skills/code-documentation/`.
- Then run `python3 scripts/skillctl.py trace-origin engineering/skills/code-documentation/SKILL.md` and require it to classify as `upstream-safe`.

### P1 - Memory Skill Is Misclassified By The Private-Signal Scanner

`scripts/skillctl.py trace-origin system/skills/memory/SKILL.md` now reports `upstream-safe`.

The matched term is the word `secrets` in the safety sentence "Storing credentials or secrets in any memory file - never." This is a false positive in a public safety rule, not private data.

Impact:
- Auto-improve can block changes to the memory skill even when those changes are generic and upstream-safe.
- This directly interferes with the requested memory-management lane.

Recommended fix:
- Change `skillctl` private-data detection from broad substring matching to context-aware patterns.
- Treat safety guidance that bans secrets as non-sensitive when it does not contain actual secret material.
- Add a focused test that classifies `system/skills/memory/SKILL.md` as `upstream-safe`.

### P2 - Autoimprove Output Uses `memory/autoimprove/`, Not AFS

`agent-harness` autoimprove now writes generated run artifacts under `.skill-improvements/`.

That location is not the same as:
- Claude auto-memory under `~/.claude/projects/.../memory/`
- strict AFS Memory folders from `brain`
- code-documentation timestamped `logs/`, `lessons/`, `items/`, `fixes/`, `audits/`, `raw/`, and `plans/`
- generated/runtime output from the source/runtime model

Impact:
- Improvement artifacts can look like durable memory while actually being generated review artifacts.
- Brain ingestion may treat repo-local `memory/` as a knowledge input if a future rule broadens discovery.
- Code-documentation has no clear routing rule for autoimprove results.

Recommended fix:
- Classify autoimprove round logs and results as generated/review artifacts, not canonical memory.
- Prefer `.skill-improvements/` for patch bundles and generated improvement reports.
- Keep only durable lessons or adopted rules in AFS paths after human review.

### P2 - Brain Boundary Rules Cannot Fully Activate In This Repo

The brain skill requires exactly one active `BRAIN.md` before canonical knowledge writes. This checkout now has a repo-level `BRAIN.md`.

The repo's actual audit convention is `docs/audits/skills/`, shown by the existing 2026-06-22 and 2026-06-26 skill audit files. That is a partial-AFS convention, not strict root AFS.

Impact:
- Strict AFS instructions would put this report under `audits/2026/06-26/`, while repo convention puts it under `docs/audits/skills/`.
- Agents following brain strictly would stop before writing; agents following code-documentation would proceed into timestamped docs.

Recommended fix:
- Add a repo-level `BRAIN.md` or root documentation policy that declares this repo's adaptation mode.
- If the intended mode is partial-AFS, explicitly map `audits/` to `docs/audits/skills/` for skill audits.
- Until then, prefer the existing repo convention for audits and record the mismatch in the audit body.

### P2 - `memory` And `brain` Share Inputs But Not Lifecycles

`memory` curates Claude memory into `CLAUDE.md` or `.claude/rules/` and removes promoted entries from auto-memory. `brain` treats Memory folders as evidence inputs that can compile into `knowledge/`.

Impact:
- The same learning can be promoted into enforced rules by `memory`, compiled into `knowledge/` by `brain`, or documented by `code-documentation`.
- There is no single promotion matrix saying which durable learning belongs in `CLAUDE.md`, `.claude/rules/`, `facts/` or `items/`, `lessons/`, `fixes/`, `knowledge/`, or `cookbook/`.

Recommended fix:
- Add a shared promotion matrix referenced by `memory`, `brain`, `ingestion`, `learning`, `agent-harness`, and `code-documentation`.
- Keep `memory` responsible for runtime instruction priority.
- Keep `brain` responsible for canonical knowledge and source provenance.
- Keep `code-documentation` responsible for human-readable placement once the AFS path has been selected.

## Owner Boundary Matrix

| Need | Canonical owner | Secondary chains | Notes |
|---|---|---|---|
| Review Claude auto-memory health | `memory` | `skills-management` | Do not route to `brain` unless the output becomes canonical knowledge. |
| Promote recurring behavior into enforced instructions | `memory` | `code-documentation` when human docs also change | Target `CLAUDE.md` or `.claude/rules/`; remove duplicate memory entries. |
| Ingest raw sources or repo Memory into knowledge | `brain` + `ingestion` | `research`, `reporting`, `code-documentation` | Requires exactly one `BRAIN.md` for writes. |
| Improve skill prompts, references, scripts, or evals | `auto-improve` -> `skill-eval-loop` | `code-documentation`, `quality-assurance` | Must pass `skillctl` provenance and privacy classification. |
| Improve harness/autoresearch loops | `auto-improve` -> `agent-harness` | `skill-eval-loop`, `quality-assurance` | Generated improvement artifacts should not masquerade as durable memory. |
| Place durable human-readable docs | `code-documentation` | `brain` for AFS schema, `memory` for runtime rules | Current conflict: `items/` vs `facts/`, and date convention mismatch. |

## Non-Findings

- `auto-improve` is not missing from the current taxonomy. It appears in `system/profile.yaml` and `skills-chaining-map.md`.
- `scripts/skillctl.py` is present in the current worktree and `python3 scripts/skillctl.py meta check --root .` validates eight metadata files.
- The earlier `second-brain` monolith should remain retired. The current split between `brain` and `ingestion` is the right direction.

## Recommended Remediation Order

1. Done: AFS taxonomy uses `facts/` and default timestamp convention `YYYY/MM-DD/`.
2. Done: `code-documentation` has `.skillmeta.yml` coverage.
3. Done: `skillctl` private-signal false positives for public safety text are fixed and tested.
4. Done: autoimprove artifacts route to `.skill-improvements/`.
5. Done: repo-level `BRAIN.md` declares partial-AFS mapping.
6. Done: shared promotion matrix links `memory`, `brain`, `ingestion`, `learning`, `agent-harness`, and `code-documentation`.

## Validation Notes

Commands run during this audit pass:

```sh
python3 scripts/validate_skills.py
git diff --check
python3 scripts/skillctl.py meta check --root .
python3 scripts/skillctl.py trace-origin system/skills/auto-improve/SKILL.md
python3 scripts/skillctl.py trace-origin engineering/skills/code-documentation/SKILL.md
python3 scripts/skillctl.py trace-origin system/skills/brain/SKILL.md system/skills/memory/SKILL.md system/skills/ingestion/SKILL.md engineering/skills/agent-harness/SKILL.md
```

Observed results:

- `validate_skills.py`: passed for 141 skill files.
- `git diff --check`: passed.
- `skillctl meta check`: passed for eight metadata files.
- `auto-improve`, `brain`, `ingestion`, and `agent-harness` traced as `upstream-safe`.
- `code-documentation` traces as `upstream-safe`.
- `memory` traces as `upstream-safe`.

## Final Recommendation

Keep the current router split. Do not recreate `memory-management` or `second-brain` as compatibility aliases.

The contract cleanup is done: the AFS schema is aligned, `code-documentation` has provenance metadata, and `skillctl` classifies the covered memory/documentation owners as upstream-safe.
