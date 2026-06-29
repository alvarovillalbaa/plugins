# Lesson Capture Example

**Source**: Post-incident review after a failed product launch  
**Date**: 2026-05-12  
**Captured by**: Engineering team retrospective

---

## Raw Incident Notes

> We launched the v2 onboarding flow on May 8. Within 24 hours, 35% of new signups dropped off at step 3 (team invite). We had tested the flow internally but hadn't tested with users who didn't have team members readily available. We rolled back the "team invite required" gate on May 9.

---

## Extracted Lesson

**Lesson**: Don't gate activation on actions that require a third party.

**Category**: Product / Activation

**Severity**: High (caused measurable activation drop)

**Generalized form**: Any activation gate that requires the user to take an action outside the product (invite someone, connect a tool, share with a team) will disproportionately hurt solo evaluators and small teams in the early stages of a trial. These gates should be optional or deferred to after the user has seen value.

**When it applies**: Any time an activation or onboarding flow includes a step that can't be completed alone.

**What to do instead**:
1. Make social/collaborative steps optional in the activation flow.
2. Defer team invite to post-first-value (after the user has seen the product work for them).
3. If a team is required for the product to work, qualify this upfront before onboarding starts, not during.

**Evidence**:
- Pre-change: 35% drop-off at step 3 (team invite)
- Post-change: 12% drop-off at step 3 (team invite made optional)

---

## Storage Target

This lesson should be saved to:
- `system/skills/lessons/` — as a permanent lesson card
- `product/skills/product-development/references/activation-lessons.md` — domain-specific reference

---

## Lesson Card (Condensed)

```yaml
id: activation-solo-evaluator-gate
category: product
severity: high
lesson: "Don't gate activation on actions requiring a third party."
context: "Any step that requires inviting someone or connecting to a tool the user doesn't control will hurt solo evaluators."
action: "Make social steps optional. Defer team invite to post-first-value."
evidence: "May 2026 onboarding rollback: 35% → 12% drop-off after removing required team invite gate."
```
