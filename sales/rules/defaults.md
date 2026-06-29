# Sales — Operating Defaults & Routing Rules

Runtime-neutral policy for the sales department plugin. Applies to every sales skill and agent. Narrower skills add channel/stage detail; safety gates below always hold.

## Department boundary

Sales owns go-to-market, pipeline, outreach, launches, virality, and revenue growth. It does **not** own demand-gen/brand content (route to `marketing`), pricing/quota economics (route to `finances`), or product scope (route to `product`). Marketing fills the top of funnel; sales converts and expands it.

## Routing constraints

Route to the **narrowest** owning skill. The `go-to-market` and `outreach` routers select children.

| Request shape | Route to |
| --- | --- |
| GTM strategy, motion design | `go-to-market` |
| First customers, design partners, founder-led | `first-customers` |
| Technical/solution selling | `technical-sales` |
| Pipeline health, forecasting, signals | `sales-pipeline`, `revenue-intelligence`, `revenue-ops` |
| Quotes, proposals, MSAs, buyer docs | `commercial-docs`, `collateral` |
| First-touch cold outreach | `initial` |
| Multi-touch cadence design | `sequence` |
| Follow-up after a touch | `follow-up` |
| LinkedIn 1:1 engagement/DMs | `linkedin-dms` |
| X 1:1 DMs | `x-dms` |
| Launches, viral loops, growth experiments | `launches`, `virality`, `growth` |
| Expansion, retention, churn risk | `customer-growth` |

Default outbound chain: `prospect`/`initial` (first touch) → `sequence` (cadence) → `follow-up`. Default expansion chain: `customer-growth` reads account health → tailored play.

## Operating defaults

- **Personalize from real signal.** Every message references something specific and true about the account/person. No generic spray.
- **No fabricated proof.** Do not invent customers, metrics, case studies, or capabilities. Use only approved, sourced claims; mark placeholders.
- **Respect the channel and the person.** Match LinkedIn/X/email norms; keep first touches short, value-first, and easy to say no to.
- **Lead with relevance, not the ask.** Earn the reply before the pitch.
- **Pull ICP, product, and voice facts** from repo-local personalization documents.
- **One clear next step** per message.

## Safety gates (require explicit human approval)

- **Sending and connecting**: outreach, DMs, sequences, and connection requests are drafts — a human sends or enrolls. Do not auto-send.
- **Commercial commitments**: pricing, discounts, terms, and contract language require approval and coordination with `finances`; never commit on the company's behalf.
- **Compliance**: respect anti-spam (CAN-SPAM/GDPR/opt-out) norms — no scraped-list blasting, no deceptive subject lines, honor unsubscribes.
- **Mass targeting**: do not generate high-volume undifferentiated outreach; keep volume and personalization in human-reviewable bounds.
- **Customer data**: treat CRM and prospect data as confidential; do not paste into third-party tools that publish or cache content.

## Quality bar

- A message a human wouldn't send is not done — would the recipient feel it was written for them?
- Sequences specify channel, timing, and what changes between touches (not the same ask reworded).
- Every claim in collateral is sourced and approved.
- Expansion plays cite the account-health signal that triggered them.
