# Routing Decision Examples for `personalize`

These examples show how to correctly dispatch requests to child skills.

---

## Example 1 → `communication-style`

**Request**: "I want the agent to be more direct and less verbose in its responses."

**Decision**: This is about tone and register — how the agent communicates. Route to `communication-style`.

**Why not `calibration`?** Calibration adjusts _what_ the agent does (scope, accuracy, signal/noise). Communication style adjusts _how_ it expresses results.

---

## Example 2 → `voice`

**Request**: "We need to update our writing style — we've moved from a formal enterprise tone to more casual, founder-to-founder."

**Decision**: This is a brand-level voice shift affecting all written content. Route to `voice`.

**Why not `communication-style`?** Voice is brand-wide and applies to all outward-facing content. Communication style is specific to agent/assistant interaction patterns.

---

## Example 3 → `calibration`

**Request**: "The code review agent keeps flagging style issues on well-written code. It's too noisy."

**Decision**: This is a skill behavior problem — the agent's output scope is miscalibrated. Route to `calibration`.

**Why not `communication-style`?** The issue isn't how the agent writes — it's what it includes in the output.

---

## Example 4 → `positioning`

**Request**: "How should we frame our product for a security-first enterprise buyer vs. a startup CTO?"

**Decision**: This is about market positioning and messaging by segment. Route to `positioning`.

**Why not `icp`?** ICP defines _who_ to target. Positioning defines _what to say_ to each segment.

---

## Example 5 → `icp`

**Request**: "We're getting too many trial signups from companies that can't afford us. Help us tighten our ICP."

**Decision**: This is an ideal customer profile definition/refinement task. Route to `icp`.

**Why not `positioning`?** Positioning is about messaging. ICP is about qualifying who should receive that messaging.

---

## Ambiguous Requests

Some requests touch multiple children:

**Request**: "We're pivoting upmarket. Update our ICP and our messaging."
- Route `icp` first (define the new ICP).
- Then route `positioning` (update messaging for the new ICP).
- Optionally chain to `voice` if the tone also needs to shift.

**Request**: "Make the agent sound more like us."
- If unclear: ask whether they mean the agent's interaction style (`communication-style`) or the brand's written content voice (`voice`).
