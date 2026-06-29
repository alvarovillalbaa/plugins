# Calibration Methods Reference

Reference for calibrating communication and output preferences from examples, feedback, and prior accepted work. Calibration tunes *how* the agent produces output (tone, format, depth, style) to match a specific user — distinct from learning domain facts. Store preferences with their reason so edge cases can be judged later.

## What calibration is

Calibration = detecting and encoding a user's preferences so future output matches without being re-told each time. Sources of signal:
- **Explicit feedback** — "be more concise," "stop summarizing," "I like this format."
- **Accepted work** — what the user kept, shipped, or praised (validated preferences).
- **Corrections** — edits the user made to your output reveal the gap between produced and desired.
- **Examples** — samples the user points to as "like this."

The aim: never make the user give the same guidance twice.

## Preference dimensions

| Dimension | Spectrum / options |
| --- | --- |
| **Length** | Terse ↔ thorough |
| **Tone** | Formal ↔ casual; direct ↔ diplomatic |
| **Format** | Prose ↔ bullets ↔ tables; headers or none |
| **Depth of explanation** | Just the answer ↔ show reasoning |
| **Proactivity** | Do exactly asked ↔ anticipate next steps |
| **Code comments** | None ↔ heavy |
| **Confidence display** | Hedge ↔ commit to a recommendation |
| **Summaries** | Wants trailing summaries ↔ "I can read the diff" |
| **Vocabulary** | Domain jargon ok ↔ plain language |

Capture per-context where it varies (e.g., terse in chat, thorough in docs).

## Detecting preferences

### From explicit feedback
- Direct statements are highest-signal — encode immediately.
- Note the **scope**: is "be concise" global, or just for this task? Default to the stated scope; don't over-generalize.

### From corrections (implicit)
- Diff what you produced vs. what the user kept/edited. The delta is the preference.
- Repeated corrections in the same direction = a strong, durable preference.
- A single edit might be task-specific; a pattern across tasks is a real preference.

### From accepted work (positive signal)
- What got shipped without changes is validated — replicate its characteristics.
- **Watch the quiet confirmations**: accepting an unusual choice without pushback is a signal to keep doing it, not just to avoid mistakes. Calibrating only from corrections drifts you toward over-caution.

## Encoding preferences

- **Lead with the rule**, then the **reason** (why the user wants it), then **when it applies**. The reason lets you judge edge cases instead of blindly following.
- **Scope it** — global vs. project vs. task-type vs. channel.
- **Link related preferences** so they form a coherent style, not contradictory rules.
- **Store, don't just remember** — persist to the appropriate preference/memory location (route to `memory`, `communication-style`, `voice`).
- **Dedupe** — update an existing preference rather than adding a near-duplicate.

## Confidence & strength

Not all signals are equal. Weight by:
- **Explicitness** — stated > inferred.
- **Repetition** — recurring > one-off.
- **Recency** — recent preferences override older contradicting ones (people change).
- **Consistency** — does it hold across contexts, or is it situational?

Hold weak inferences loosely; confirm before treating a single data point as a rule.

## Applying calibration

- Apply preferences proactively — that's the point — but let the user override per-task without "fighting" them.
- **When a preference conflicts with the current request, the request wins** for that task; note whether it signals a preference change.
- Re-calibrate continuously — preferences drift; stale preferences cause friction. Update the record when signals change.

## Avoiding over-calibration

- Don't over-generalize from one correction into a sweeping rule.
- Don't become so cautious you stop making useful judgment calls — calibrate from successes too.
- Don't encode contradictory preferences; reconcile or scope them.
- Distinguish a true preference from a one-time situational need.

## Output / handoffs

A calibration result records: the preference, its reason, its scope, the supporting signal, and a confidence level. Persist via `memory`; feed style specifics to `communication-style` and `voice`; surface patterns worth a durable lesson to `lessons`.
