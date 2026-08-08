# Lesson Extraction Reference

Reference for creating, curating, and promoting lessons from repo work, user corrections, and successful workflows. A lesson is a reusable, durable insight that changes future behavior — not a log of what happened. Capture the *why* so edge cases can be judged later. Promotion to shared/durable stores is human-gated.

## What a lesson is (and isn't)

- **Is**: a generalizable rule or insight that, applied next time, produces better work. ("Integration tests here must hit a real DB because mocks masked a broken migration.")
- **Isn't**: a task log, a one-off fact about current state, a fix recipe already captured in the code/commit, or anything derivable by reading the repo or `git log`.

The test: *would knowing this in a future, different session change what I do?* If no, it's not a lesson.

## Sources of lessons

| Source | Signal |
| --- | --- |
| **User corrections** | "No, don't do X" / "stop doing Y" — strongest signal of a gap |
| **Validated successes** | "Yes, exactly" / accepted an unusual choice without pushback — confirms an approach |
| **Repeated friction** | The same mistake or question recurring across sessions |
| **Surprising outcomes** | Something that didn't work as expected, or a non-obvious approach that did |
| **Workflow wins** | A sequence/method that worked well and should be repeated |

Capture from **both** failure and success. Extracting only corrections makes you avoid past mistakes but drift away from validated approaches and grow over-cautious.

## Extraction process

1. **Notice the signal** — a correction, a confirmation, a recurring pattern, a surprise.
2. **Generalize carefully** — abstract from the specific instance to the reusable rule, but don't over-generalize from a single data point. One correction may be situational; a pattern is a rule.
3. **Capture the why** — the reason/incident behind the rule. This is the most valuable part: it lets future-you judge whether the lesson applies to a new edge case.
4. **Scope it** — global / project / task-type / context-specific. Mis-scoped lessons cause friction.
5. **Check for duplicates** — update an existing lesson rather than adding a near-duplicate.
6. **Record provenance** — source and date, so staleness can be judged.

## Lesson format

A good lesson is structured so it can be applied and re-evaluated:
- **Rule** — the actionable insight, stated first and plainly.
- **Why** — the reason or incident that motivates it (judge edge cases from this).
- **How to apply** — when/where it kicks in (the trigger).
- **Scope** — how broadly it holds.
- **Source + date** — provenance for trust and staleness.
- **Links** — related lessons/memories for coherence.

Lead with the rule; a lesson buried in narrative won't be applied.

## Curation

Lessons accumulate; curate so the set stays sharp:
- **Dedupe** — merge overlapping lessons into one canonical statement.
- **Reconcile contradictions** — newer/validated lessons supersede older ones; resolve, don't stack conflicting rules.
- **Retire stale lessons** — ones tied to removed features, old tools, or changed preferences. Verify against current reality before keeping.
- **Strengthen with repetition** — a lesson confirmed multiple times is high-confidence; a one-off is provisional.
- **Keep them findable** — tag and index so the right lesson surfaces at the right time.

## Promotion (candidate → durable/shared)

Not every captured lesson belongs in the shared, durable store immediately:
1. **Draft as a candidate** — captured but not yet authoritative.
2. **Validate** — confirmed by repetition, by the user, or by a successful re-application.
3. **Promote** — move to the durable/shared store with full format and provenance.
4. **Gate promotion** — promotion is a human-approval step, especially when the lesson will change behavior org-wide. Keep candidates separate until reviewed.

This mirrors knowledge-base promotion — provisional until earned.

## Quality gates

- **Generalizable, not a log** — if it's just "what happened," it's not a lesson.
- **Why is mandatory** — a rule without its reason can't be applied to edge cases.
- **Not derivable elsewhere** — don't store what `git log`, the code, or CLAUDE.md already says.
- **Both successes and failures** — guard against over-caution by capturing what worked.
- **Verify before relying** — a lesson is a claim from when it was written; re-check current state.
- **Promotion is human-gated** — durable/shared lessons need approval.

## Handoffs

- Durable persistence → `memory`.
- Communication/style preferences specifically → `calibration`, `communication-style`, `voice`.
- Broader knowledge entries → `knowledge-base`.
- Lessons that should change a skill → `plugins-management`, `skill-eval-loop`.
- Running the extraction on a cadence → `loops`, `learning`.
