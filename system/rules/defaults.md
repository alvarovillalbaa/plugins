# System — Operating Defaults & Routing Rules

Runtime-neutral policy for the system department plugin. Applies to every system skill and agent. This department maintains the other departments' capabilities, so its safety gates are strict: it edits the substrate everything else runs on.

## Department boundary

System owns skills, memory, knowledge, learning, brain ingestion, personalization, and repeatable improvement loops. It is **meta**: it improves how the other six departments work rather than doing their domain work. It does not produce customer-facing finance/sales/marketing output — it tunes the skills that do.

## Routing constraints

Route to the **narrowest** owning skill. The `skills-management` router selects maintenance children.

| Request shape | Route to |
| --- | --- |
| Continuous improvement orchestration | `auto-improve`, `loops` |
| Create/edit/audit skills | `skills-management` |
| Evaluate skill quality, regression-check behavior | `skill-eval-loop` |
| Persist/retrieve durable memory | `memory` |
| KB health, dedupe, canonical pages, drift repair | `knowledge-base` |
| Learn from sessions; extract reusable lessons | `learning`, `lessons` |
| Ingest external sources into the brain | `brain`, `ingestion` |
| Capture user preferences/voice/comms style | `personalize`, `communication-style`, `voice`, `calibration` |
| Positioning and ICP signal capture | `positioning`, `icp` |

Default improvement loop: `skill-eval-loop` scores behavior → `lessons`/`learning` extract findings → `skills-management` applies edits → re-eval. Default personalization loop: `calibration` reads accepted work → `communication-style`/`voice` update preference docs.

## Operating defaults

- **Edit memory/skills surgically.** Update or remove the specific entry; never bulk-rewrite or duplicate. Check for an existing entry before adding a new one.
- **Provenance on everything.** Lessons, KB entries, and memories record their source and date so future readers can judge staleness.
- **Capture the WHY.** Preferences and lessons store the reason, not just the rule, so edge cases can be judged later.
- **Memory is for cross-session facts**, not ephemeral task state. Don't persist conversation-scoped detail.
- **Verify before recalling.** A stored fact is a claim about a past moment — re-check current state before acting on it; trust observation over stale memory and update the record.
- **Improvements are evidence-driven.** Propose skill/prompt mutations from eval results or repeated corrections, not vibes.

## Safety gates (require explicit human approval)

- **Writing to other departments' skills**: editing another plugin's SKILL.md, references, or rules requires confirmation — it changes behavior org-wide.
- **Promoting lessons/memories to durable/shared stores**: promotion from draft to canonical is gated; keep candidates separate until approved.
- **Deleting or overwriting memory/KB entries**: investigate before removing — it may be load-bearing or in-progress work. Prefer update over delete.
- **Ingesting external content**: respect source licensing and privacy; do not ingest secrets or PII into shared knowledge.
- **Automated loops**: any self-running loop (`auto-improve`, `loops`) must be human-started and bounded; surface what it will change before it runs unattended.

## Quality bar

- A lesson without a source, trigger, and "how to apply" is not promotable.
- A skill change without an eval that demonstrates improvement is unproven — don't ship regressions.
- KB/memory edits leave the index consistent and free of duplicates.
- When a recalled memory conflicts with current state, fix the memory — don't act on the stale version.
