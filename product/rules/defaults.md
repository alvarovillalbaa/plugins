# Product — Operating Defaults & Routing Rules

Runtime-neutral policy for the Product plugin. These rules apply to every product skill and agent. Platform safety requirements and the user's explicitly authorized scope take precedence; narrower skills may add compatible method detail but may not relax the authorization gates or contradict the ownership boundaries below.

## Department boundary

Product owns direction, discovery, requirements, product experiments, product marketing, positioning, packaging/pricing strategy, and design (taste, systems, polish, critique). Finances owns pricing economics and financial guardrails; Marketing owns demand-generation assets and distribution; Sales owns deal execution; Engineering owns implementation. Product decides what outcome to pursue and why, then chains to the relevant domain owner for execution.

## Routing constraints

Route to the **narrowest** owning skill. The `product-development` router selects discovery/strategy children.

| Request shape | Route to |
| --- | --- |
| Vision, strategy, roadmap framing | `strategy`, `direction` |
| Customer discovery, JTBD, prioritization (RICE/ICE/WSJF), assumption tests | `discovery` |
| Write a PRD / spec | `prds` |
| Design or analyze an experiment | `experiments` |
| User stories, acceptance criteria | `user-stories` |
| Positioning, messaging, packaging, pricing strategy, launch narrative | `product-marketing`; chain `finances/fundamentals` for economic validation |
| Conversion optimization | `cro`, `buyer-psychology` |
| Content-led growth, lead magnets | `content-led`, `lead-magnets` |
| Visual/interaction design, design systems, polish | `design`, `design-systems`, `taste`, `polish`, `critique` |

Default discovery → delivery chain: `discovery` → `prds`/`user-stories` → hand off to `engineering`; validate with `experiments`.

## Operating defaults

- **Start from the user problem**, not the solution. Frame work as jobs/outcomes before features.
- **Make assumptions explicit and testable.** Separate what is known from what is believed; attach a cheap test to risky assumptions.
- **Prioritize transparently.** Show the scoring (reach/impact/confidence/effort) behind any ranking; do not assert priority without rationale.
- **Write for the builder.** PRDs and stories must be unambiguous, include acceptance criteria, and call out non-goals.
- **Context is supplied, not embedded.** Pull product, audience, roadmap, metric, and organization-specific facts from user-provided or workspace-local sources; never hardcode them into reusable rules.
- **Evidence over opinion.** Tie recommendations to research, data, or a named heuristic; flag when something is a hunch.

## Authorization gates

The request may authorize local product artifacts and analysis. Confirm at the point of action before committing shared roadmap scope, changing live experiences, contacting participants, or publishing externally.

- **Roadmap and scope commitments**: propose dates, cuts, and resource allocations unless the request explicitly authorizes the decision and its affected scope.
- **Customer-facing experiments**: live UX, packaging, or pricing changes require explicit authorization plus coordination with Engineering and, for financial impact, Finances.
- **External communication**: launch posts, customer emails, and public roadmaps are drafts until final content and recipients are authorized.
- **Discovery with people**: interview scripts and outreach are drafts by default; contact participants only with explicit authorization. Treat research data as confidential.

## Quality bar

- A PRD without acceptance criteria and non-goals is incomplete.
- A prioritization without an explicit rubric is an opinion, not a decision.
- Design recommendations cite a principle or pattern, not just preference.
- Kill or de-scope ideas when evidence is weak — half-validated features are not "ready."
