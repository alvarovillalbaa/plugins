---
name: message-outreach
description: >-
  Messaging skill for default outbound/sequence drafting plus routing to
  sender voice calibration and follow-up messaging children.
---

# Message Outreach Router

This parent keeps shared methodology/default workflow ownership and routes specialized lanes to children.

## Children

- [`sender-voice-calibration`](../sender-voice-calibration/SKILL.md) - sender voice learning, approved-message analysis, style guides, forbidden phrases, and personalized writing constraints
- [`follow-up-messaging`](../follow-up-messaging/SKILL.md) - follow-up messages, waiting-state nudges, reply drafting, conversation continuation, and next-step recovery

## Route

| User asks for | Use |
| --- | --- |
| sender voice learning, approved-message analysis, style guides, forbidden phrases, and personalized writing constraints | [`sender-voice-calibration`](../sender-voice-calibration/SKILL.md) |
| follow-up messages, waiting-state nudges, reply drafting, conversation continuation, and next-step recovery | [`follow-up-messaging`](../follow-up-messaging/SKILL.md) |

## Chain Rules

- `prospect-research`
- `go-to-market/first-customer-gtm`
- `sales-pipeline`
- `auto-improve/writing-style-learning`

## Operating Rules

- Keep this `SKILL.md` small and routing-focused.
- Do not recreate the old broad parent behavior here; put execution depth in child assets.
- If no child matches, handle only shared methodology/default workflow or document the missing lane.
- Every child and parent skill must keep `examples/`, `hooks/`, `references/`, `scripts/`, and `templates/`.

## External Skill Chains

Use live external skills when they are installed. If one is missing, report the fallback command instead of copying its guidance inline. Local skill rules, repo-specific facts, safety gates, product/channel constraints, and explicit local exceptions win over external guidance when they conflict.

- `unslop`: Remove AI tells from prose while preserving meaning and voice. Install: `python scripts/install-external-skills.py --skill unslop --agent codex`.
- `stop-slop`: Apply stricter prose cleanup for predictable AI writing patterns. Install: `python scripts/install-external-skills.py --skill stop-slop --agent codex`.

Registry: [`../../../references/external-skills.yaml`](../../../references/external-skills.yaml).

## Shared Map

See [`../../../skills-chaining-map.md`](../../../skills-chaining-map.md) for the complete skills-chaining graph.
