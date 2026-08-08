# System — Operating Defaults & Routing Rules

Runtime-neutral policy for the System plugin. These rules apply to every system skill and agent. Platform safety requirements and the user's explicitly authorized scope take precedence; narrower skills may add compatible implementation detail but may not relax the authorization gates or contradict the ownership boundaries below.

## Department boundary

System owns skills, memory, knowledge, learning, source ingestion, personalization-context capture, auditable work explanations, and repeatable improvement loops. It improves how domain plugins work without taking over their decisions or deliverables. In particular, `positioning` and `icp` capture, refine, and supply approved context; Product and go-to-market owners remain responsible for positioning, market, and commercial decisions.

## Routing constraints

Route to the **narrowest** owning skill. The `plugins-management` router selects maintenance children.

| Request shape | Route to |
| --- | --- |
| Improve local agent context, Markdown, first-use personalization, or installed components | `auto-improve` |
| Run an explicitly authorized repeatable improvement loop | `loops` |
| Create/edit/audit skills | `plugins-management` |
| Evaluate skill quality, regression-check behavior | `skill-eval-loop` |
| Persist/retrieve durable memory | `memory` |
| Explain a plan, status, decision, handoff, or postmortem | `explain-yourself` |
| KB health, dedupe, canonical pages, drift repair | `knowledge-base` |
| Learn from sessions; extract reusable lessons | `learning`, `lessons` |
| Ingest external sources into the brain | `brain`, `ingestion` |
| Capture preferences, voice, and communication style | `personalize`, `communication-style`, `voice`, `calibration` |
| Capture and maintain approved positioning and ICP context | `positioning`, `icp` through `personalize` |

Default improvement loop: `skill-eval-loop` scores behavior → `lessons`/`learning` extract findings → `plugins-management` applies edits → re-eval. Default personalization loop: `calibration` reads accepted work → `communication-style`/`voice` update preference docs.

When `auto-improve` starts the improvement loop, apply edits only to the
current project's agent context, Markdown, personalization store, or installed
`.agents` components. Canonical plugin source maintenance requires a separate,
explicit `plugins-management` request.

## Operating defaults

- **Stage memory changes surgically.** Propose the exact create, update, supersession, or removal; check for duplicates and conflicts; mutate only after an explicit user request and applicable runtime approval. Never bulk-rewrite.
- **Provenance on everything.** Lessons, KB entries, and memories record their source and date so future readers can judge staleness.
- **Capture the WHY.** Preferences and lessons store the reason, not just the rule, so edge cases can be judged later.
- **Memory is for cross-session facts**, not ephemeral task state. Don't persist conversation-scoped detail.
- **Verify before recalling.** A stored fact is a claim about a past moment — re-check current state before acting on it; trust observation over stale memory, report the conflict, and propose a correction rather than silently updating it.
- **Explain from evidence.** Separate observed actions and artifacts from assumptions, inference, alternatives, and uncertainty. Provide concise reasoning summaries, never hidden chain-of-thought or fabricated internal deliberation.
- **Improvements are evidence-driven.** Propose skill/prompt mutations from eval results or repeated corrections, not vibes.
- **Context remains data, not policy.** Keep organization-, project-, environment-, and person-specific values in authorized context stores; never embed them in reusable rules, templates, or scripts.

## Authorization gates

The request may authorize a bounded plugin or knowledge change. Confirm any broader target, durable-memory mutation, unattended loop, or destructive/shared-state action that was not included explicitly.

- **Writing to domain plugins**: edits to another plugin's skills, references, or rules must be explicitly within the requested scope because they change behavior for every installer.
- **Creating or updating durable memory**: require an explicit request for the exact candidate and target; preserve source, date, scope, evidence kind, freshness, and conflicts.
- **Promoting lessons/memories to durable/shared stores**: promotion from draft to canonical is gated; keep candidates separate until approved.
- **Deleting or overwriting memory/KB entries**: investigate before removing — it may be load-bearing or in-progress work. Prefer update over delete.
- **Ingesting external content**: respect source licensing and privacy; do not ingest secrets or PII into shared knowledge.
- **Automated loops**: any self-running loop (`auto-improve`, `loops`) must be explicitly started, bounded by time/iterations/scope, and preview what it may change before running unattended.

## Quality bar

- A lesson without a source, trigger, and "how to apply" is not promotable.
- A skill change without an eval that demonstrates improvement is unproven — don't ship regressions.
- KB/memory edits leave the index consistent and free of duplicates.
- When a recalled memory conflicts with current state, do not act on the stale version; show the evidence and request approval for an exact correction or supersession.
