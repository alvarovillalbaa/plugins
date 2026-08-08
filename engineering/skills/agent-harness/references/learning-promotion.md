# Identity And Documentation Promotion

Last updated: 2026-04-25

Use learning artifacts to improve the right source of truth. Do not promote everything everywhere.

## Promotion order

Promote in this order:

1. `learning/` artifacts
2. Root instruction docs (the UPPERCASE set `use-afs` defines)
3. Human-facing markdown docs that should persist for collaborators

If the knowledge is useful only as session memory, stop at `learning/`.

## File roles

| File | What belongs there | Update bar |
|---|---|---|
| `AGENTS.md` | Stable operating rules, repo facts, agent stance, and general customization to the user's/codebase's ways of working | Repeated or explicitly stated, actionable, durable |
| `USER.md` | User context, roles, and interaction patterns | When a durable fact about the user changes how agents work |
| `LOOPS.md` | Repo-wide operational processes — how planning and spec-writing are done, and other feedback cycles | Durable process guidance, not one feature's transient plan |
| `TASTE.md` | Quality standards, decision heuristics, constraints, trade-off rules, and the design language | Rare, heuristic or standard clearly needed |
| `VISION.md` | Strategic direction for the workspace | When durable direction changes |
| `GAPS.md` | Unresolved gaps in human or agent understanding | When a gap is worth tracking until closed |
| `README.md` | Human-facing overview or usage facts | When a teammate would need it |
| `ARC.md` | Structural decisions, ownership, boundaries | When architecture changed or was clarified |
| `TESTS.md` / `TESTING.md` | Durable test workflows and pitfalls | When test strategy or gotchas changed |
| `SETUP.md` | Environment, setup, bootstrap behavior | When operational steps changed |
| AFS log surface | Development log entries | After any meaningful code or doc change |
| AFS lesson surface | Verified reusable insights | When a discovery should change future behavior |
| AFS fact surfaces | Durable context about user/company/project, by fact type | When teammates would make wrong assumptions without it |
| AFS fix surface | Error solutions | After solving a non-obvious or recurring problem |
| AFS audit surface | Reports, ADRs, post-mortems, analytical audits | When the artifact is historical and investigative |
| AFS plan surface | Historical implementation plans | When the artifact explains how one change should be executed |
| AFS spec surface | Living desired-state behavior contracts | When the rule should remain current, not historical |
| AFS source registry | Monitored URL/source registries | When source monitoring itself is durable knowledge |
| `lib/` | Generated drafts or support artifacts | When a reusable generated artifact should persist |
| `references/` | Stable lookup/reference material | When teammates need a factual reference surface |
| `cookbooks/` | Repo-specific technical guidance | When a pattern needs broader documentation in this codebase |
| `knowledge/` | Timeless maintained knowledge | When the content should compound and stay canonical |
| `runbooks/` | Exact operational workflows | When the content is a repeatable procedure |
| `research/` | Ongoing engineering research | When the work is exploratory but still source-of-truth |
| `official-documentation/` | Copied external official docs | When the repo keeps vendor/source docs locally |
| `context/` | Goals, roadmap, budget, preferences, values, other contextual docs | When the repo needs current shared context |

## `AGENTS.md`

Update only when the signal is:

- stable across future sessions
- actionable enough to change agent behavior
- repeated at least twice, or explicitly stated as a durable rule
- not already covered by a more authoritative instruction

Maintain or add these sections when needed:

```markdown
## Learned Preferences

- ...

## Learned Codebase Facts

- ...
```

Do not store:

- secrets
- one-off task requests
- temporary branch or PR context
- contradictory bullets without resolving them

## Agent stance (`AGENTS.md`)

Update only for persistent tension in how the agent collaborates.

Examples:

- The user repeatedly corrects the agent to be more direct.
- The agent consistently over-explains and the correction is enduring.
- The team prefers a sharper review posture across sessions.

Do not change the agent stance for a single hurried session.

## Standards and heuristics (`TASTE.md`)

Update when a missing or broken heuristic caused avoidable time loss or poor decisions.

Examples:

- A sync versus async choice keeps being re-litigated with the same answer.
- A migration safety heuristic proved necessary and repeatable.

Write concise heuristics that help future decision making.

## Processes and design language (`LOOPS.md` / `TASTE.md`)

Update these when the learning changes the repo-wide documentation contract:

- `LOOPS.md` — how planning should be done, how plans should be shaped, and how specs should be written and what they must define
- `TASTE.md` — the design system and frontend interaction language for the repo

Confirm the current root-doc set with `use-afs` before writing; it owns which file holds which responsibility.

Do not use these files for one feature's local content when a dated plan or a living spec surface is the narrower source of truth.

## Other markdown docs

Promote there when the knowledge is for humans first, not just agents.

### Promote to `README.md` when

- the change affects how to use, run, or understand the repo
- a teammate would miss an important entry point without it

### Promote to `ARC.md` when

- module ownership changed
- a boundary or rationale was clarified
- a design constraint must remain visible

### Promote to `TESTS.md` or `TESTING.md` when

- a recurring test pattern or fixture rule emerged
- a known false assumption in tests was corrected

### Promote to `SETUP.md` when

- install, bootstrap, credentials flow, or local runtime setup changed

### Promote to AFS docs when

Use the `code-documentation` contract to choose the narrowest correct surface — terse change notes, verified lessons, durable facts, reusable fixes, analytical audits, historical plans, living specs, references, cookbooks, knowledge, runbooks, stored results, or research.

Resolve the concrete path and the timestamp format through `use-afs`; it is the only authority for both. If it is not installed, stop and report the install command. Living docs carry `Last updated: YYYY-MM-DD`.

## Conflict handling

If new knowledge conflicts with existing docs:

1. Check whether the old doc is stale.
2. If stale, update in place.
3. If the signal is still uncertain, keep it in `learning/` and record the open question in the episode or decision trace.
4. Do not publish contradictory guidance into `AGENTS.md`, `README.md`, or `ARC.md`.

## Promotion hygiene

- Update the smallest authoritative file that should own the knowledge.
- Prefer refining an existing section instead of appending another near-duplicate section.
- Mention source artifacts in the edit when useful, but do not clutter user-facing docs with internal bookkeeping.
