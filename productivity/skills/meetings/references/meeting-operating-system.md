# Meeting Operating System

## Canonical meeting record

Maintain this minimum shape:

| Field | Rule |
| --- | --- |
| `meeting_id` | Keep stable across preparation and follow-through. |
| `title` | Use the real title or a clearly labeled working title. |
| `scheduled_start`, `scheduled_end` | Use ISO timestamps with offsets when known. |
| `objective` | State the outcome the meeting should create. |
| `decisions_needed` | Phrase each as a decision question. |
| `participants` | Record only authorized names and relevant roles. |
| `sources` | List every pre-read, note, transcript, or prior meeting used. |
| `decisions` | Record text, owner, date, provenance, and revisit trigger. |
| `actions` | Record ID, action, one owner, due date, status, and source meeting. |
| `open_questions` | Preserve unresolved questions without converting them to actions. |
| `follow_up_drafts` | Keep drafts separate from sent communications. |

## Preparation priority

Rank meetings using qualitative evidence across:

1. decision criticality and reversibility;
2. proximity of deadline;
3. dependencies on or from other meetings;
4. participant time cost;
5. current preparation gap.

Explain the top priorities rather than presenting false precision. Move an asynchronous update out of the meeting when no live decision or relationship outcome requires synchronous time.

## Agenda design

Lead with the decision or working session. Put context in a pre-read when possible. For every agenda item, define the owner, desired result, required input, and timebox. Reserve explicit close time for decisions, actions, owners, and due dates.

## Capture discipline

Keep four distinct lanes:

- `notes`: what was said or shown;
- `decisions`: what the authorized group chose;
- `actions`: a commitment with one owner and due date;
- `open questions`: unresolved items with no commitment yet.

Do not promote a suggestion to a decision or a discussion topic to an action. Mark missing owners and dates `unresolved` and surface them in the close.

## Portfolio conflicts

Check for:

- overlapping meeting times for required participants;
- the same decision being made differently in two meetings;
- duplicate action IDs or duplicate commitments;
- one action assigned to different owners;
- incompatible due dates;
- an action due before its dependency decision;
- owner overload concentrated on the same date.

Preserve the source meeting on every consolidated row so the user can resolve conflicts from evidence.

## Recurring continuity

Start from the latest authorized meeting record. Carry forward only open decisions, unresolved questions, and incomplete actions. Mark previous context stale when owners, scope, or dates changed. Propose durable memory candidates for stable preferences or long-lived decisions, but request separate approval before writing them.

## Connector and action safety

Treat connectors as optional adapters. Ask before reading a new private source. Treat read authorization as read-only. Draft messages and calendar changes locally; require explicit confirmation immediately before sending, scheduling, recording, inviting, declining, or changing any external record.
