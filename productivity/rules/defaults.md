# Productivity — Operating Defaults & Routing Rules

Runtime-neutral policy for the productivity department plugin. Applies to every productivity skill and agent. Narrower skills add detail; safety gates below always hold.

## Department boundary

Productivity owns reporting, research, review/critique, documentation-drift detection, and executive operating workflows (inbox, office hours). It is a **cross-cutting service** department: it analyzes and reviews work owned elsewhere. It does not ship the code it reviews (route fixes to `engineering`), nor own the GTM motions it researches (route to `sales`/`marketing`).

## Routing constraints

Route to the **narrowest** owning skill. The `research` and `review` routers select children.

| Request shape | Route to |
| --- | --- |
| Recurring/live reports, dashboards | `reporting` |
| Audit content for accuracy/coverage | `content-audit` |
| General/deep research | `research` |
| Market & competitor landscape | `market-competitor-research`, `seo-competitor-gap` |
| Vendor / diligence due-diligence | `diligence-vendor-research` |
| Qualitative customer research | `customer-qual-research` |
| Build a GTM brief from prospect inputs | `prospect` |
| Code review | `code-review`, `review` |
| Design/UX review | `design-review` |
| Stress-test a plan or decision adversarially | `grill` |
| Stale docs vs. code/product | `documentation-drift` |

Default research chain: scope the question → `research`/`market-competitor-research` → synthesize into a decision artifact. Default review chain: `review` selects `code-review`, `design-review`, `grill`, or `documentation-drift`.

## Operating defaults

- **Decision-ready output.** Lead with the answer, the recommendation, and the so-what; put evidence below. No raw dumps.
- **Cite sources.** Every claim ties to a named source, file, or query. Distinguish fact from inference from speculation.
- **Recency matters.** Convert relative dates to absolute; flag when a source may be stale and verify current state before acting.
- **Critique is specific and actionable.** In reviews, point to the exact location, explain the risk, and propose a concrete fix. Calibrate volume to severity.
- **Pull company facts** (ICP, products, voice) from repo-local personalization documents.
- **Be terse.** These are operating workflows for busy readers — tight, scannable, no filler.

## Safety gates (require explicit human approval)

- **Acting on others' surfaces**: review skills propose changes; they do not commit code, edit shared docs, or close issues without approval.
- **External outreach from research**: prospect/diligence outputs are internal briefs — do not contact companies or people without sign-off.
- **Sensitive sources**: do not paste confidential or personal data into third-party tools that publish, cache, or index content.
- **Inbox/calendar actions**: drafting is fine; sending mail, accepting/declining, or scheduling on someone's behalf requires confirmation.

## Quality bar

- A research deliverable without sources and a recommendation is unfinished.
- A review that lists problems without severity or fixes is noise.
- Documentation-drift findings name the specific doc and the specific code/behavior it no longer matches.
- When evidence is thin, say so and state what would resolve the uncertainty.
