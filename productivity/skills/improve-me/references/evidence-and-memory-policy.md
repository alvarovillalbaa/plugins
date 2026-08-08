# Evidence and Memory Policy

## Evidence ledger

Record every material item with this shape:

| Field | Requirement |
| --- | --- |
| `id` | Use a stable local identifier. |
| `claim` | State one observable claim or one explicitly labeled inference. |
| `kind` | Use `fact` or `inference`; represent absent coverage as `not evaluated` in the output. |
| `source` | Name the conversation turn, file, memory note, or artifact. |
| `source_type` | Use `current`, `loaded_memory`, `repo_local_memory`, or `approved_private`. |
| `observed_at` | Use an ISO date when known; otherwise write `unknown` and lower confidence. |
| `fresh_until` | Add when the claim can expire or the source defines a validity window. |
| `basis_ids` | For an inference, list the facts that support it. |

Treat current user statements as facts about what the user reported, not automatic proof of an external outcome. Preserve this distinction in wording.

## Freshness

Classify each claim:

- `current`: observed in the active period or still inside `fresh_until`.
- `stale`: outside a known validity window or contradicted by newer evidence.
- `unknown`: missing a usable date or freshness rule.

Use stale evidence as historical context, not as proof of the current state. Prefer an explicit `not evaluated` result over filling a gap with an old memory.

## Inference discipline

Support each inference with evidence IDs. State a plausible alternative explanation when it would materially change the recommendation. Lower confidence when the evidence comes from a single perspective, covers only unusual events, or lacks outcome data.

Never infer protected or sensitive traits, diagnoses, mental-health conditions, trauma, intent, or moral character. Reframe the analysis around observable work patterns and controllable behavior.

## Source permissions

Use the current conversation, already loaded memory, and repo-local memory without expanding source access. Before querying any new private connector, state the source and purpose and obtain explicit authorization. Never treat a request for coaching as permission to inspect inboxes, calendars, messages, HR files, or private drives.

Before writing durable memory, show the exact candidate, destination, provenance, and retention implication. Obtain separate approval for the write even when the underlying evidence was authorized for reading.

## Prioritization rubric

Rank leverage points qualitatively using:

1. Expected effect on the stated outcome.
2. Evidence strength and freshness.
3. Degree of user control.
4. Reversibility and cost of the experiment.

Select at most three. Prefer a smaller plan that can produce learning within two to six weeks.
