---
name: icp
description: Capture, refine, and apply ideal-customer-profile signals for research, positioning, sales, and marketing work.
---

# ICP

Use this skill for the named lane in the current taxonomy. Route to sibling skills when the request crosses ownership boundaries, and preserve local rules over external guidance when they conflict.

Use `scripts/score_prospect.py --model <model.json> --prospect <prospect.json>` only after defining an evidence-backed scoring model. Start from `templates/icp-score-model.json`; never substitute the included example fields or weights for a real ICP.

See [`../../../skills-chaining-map.md`](../../../skills-chaining-map.md) for the complete skills-chaining graph.
