---
name: meetings
description: >-
  Prepare, support, and close out meetings: briefs, agendas, notes, decisions,
  action tracking, and follow-ups, for a single meeting or a recurring portfolio.
---

# Meetings

Turn meetings into decisions and owned follow-through. Support a single meeting or coordinate a portfolio without inventing context, attendees, decisions, or commitments.

## Workflow

1. Select the mode: `prepare`, `capture`, `close`, `recurring continuity`, `portfolio`, or `full cycle`.
2. Define the meeting set, time horizon, desired outcomes, participants, source material, and constraints. Mark unknown inputs instead of filling them from assumptions.
3. Use user-provided context by default. Access calendar, email, Slack, Drive, transcripts, or other private connectors only when the user explicitly requests or authorizes that source for this task.
4. Apply [`references/meeting-operating-system.md`](references/meeting-operating-system.md) for the selected phase.
5. For multiple meetings, rank preparation by decision criticality, deadline, dependency, participant cost, and preparation gap. Detect schedule, decision, ownership, and deadline conflicts.
6. Render the artifact with [`templates/meeting-portfolio.md`](templates/meeting-portfolio.md). Preserve provenance for every decision and commitment.
7. Draft follow-up messages, calendar language, and reminders without sending or scheduling them.
8. Apply [`references/post-run-checklist.md`](references/post-run-checklist.md)
   and ask for approval only when the user requests a gated external action.

## Children

Keep this skill childless. Handle single- and multi-meeting modes through one shared contract so decisions and actions remain composable.

## Phase Rules

### Prepare

- State the meeting objective, decisions required, success condition, and non-goals.
- Build a concise participant and context brief from authorized evidence.
- Order agenda items around decisions and preparation dependencies, not presentation sequence alone.
- Assign an owner and timebox to each agenda item when known.
- Surface missing pre-reads, unresolved conflicts, and questions that could make the meeting unnecessary.

### Capture

- Separate notes, decisions, open questions, risks, and actions.
- Record the decision text, decision owner, source moment or artifact, date, and any explicit expiry or revisit trigger.
- Record every action with one owner and one due date. Mark absent fields `unresolved`; never invent them.
- Treat transcripts as source material, not perfect truth. Preserve speaker uncertainty and correct obvious transcription ambiguity only when evidence supports it.
- Never start recording or transcription. Require explicit approval at the point of action and respect participant consent, organizational policy, and applicable law.

### Close

- Lead with decisions and changed commitments.
- Reconcile actions against earlier meeting artifacts and flag duplicates or conflicts.
- Draft channel-appropriate follow-up messages with owners and dates.
- Create memory candidates for durable decisions or recurring preferences, but never write them without separate approval.

### Coordinate a Portfolio

- Produce one row per meeting with priority, objective, preparation state, decisions needed, and deadline.
- Track cross-meeting dependencies and identify decisions that unblock later meetings.
- Detect overlapping attendance, incompatible decisions, duplicate commitments, owner overload, and contradictory due dates.
- Keep each meeting's provenance intact when rolling actions into the shared portfolio.

## External Action Gates

Require explicit confirmation immediately before:

- sending a message or follow-up;
- creating, moving, accepting, declining, or cancelling a calendar event;
- inviting or removing participants;
- starting a recording, transcript, or live note bot;
- changing an external task, CRM, project, or documentation system;
- writing a decision, preference, or relationship detail to durable memory.

Treat prior authorization to read a connector as read-only unless the user separately authorizes a mutation.

## Output Contract

Return the relevant subset of:

1. `Portfolio overview` with priorities and conflicts
2. `Meeting brief` with objective, participants, context, decisions needed, and non-goals
3. `Agenda` with owners and timeboxes
4. `Notes and open questions`
5. `Decision log` with provenance
6. `Action register` with one owner and due date per action
7. `Follow-up drafts`
8. `Recurring continuity and memory candidates`
9. `Approval queue` for requested external actions

Run [`scripts/merge_meeting_actions.py`](scripts/merge_meeting_actions.py) when consolidating structured artifacts from several meetings.

## Chain Rules

- `memory`
- `reporting`
- `research`

## Resources

- Read [`references/meeting-operating-system.md`](references/meeting-operating-system.md) for phase and portfolio details.
- Compare against [`examples/multi-meeting-day-example.md`](examples/multi-meeting-day-example.md) for conflict-aware coordination.
