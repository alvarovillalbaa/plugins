# Sales — Operating Defaults & Routing Rules

Runtime-neutral policy for the Sales plugin. These rules apply to every sales skill and agent. Platform safety requirements and the user's explicitly authorized scope take precedence; narrower skills may add compatible channel or stage detail but may not relax the authorization gates or contradict the ownership boundaries below.

## Department boundary

Sales owns go-to-market execution, pipeline, one-to-one outreach, commercial documents, launch motions, viral/referral mechanics, quota/territory operations, and customer expansion. Product owns product scope, positioning, packaging, and pricing strategy; Finances owns pricing economics and financial guardrails; Marketing owns demand-generation assets, distribution, and marketing-channel experiments. Sales applies approved pricing and messaging to deals without redefining them.

## Routing constraints

Route to the **narrowest** owning skill. The `go-to-market` and `outreach` routers select children.

| Request shape | Route to |
| --- | --- |
| GTM strategy, motion design | `go-to-market` |
| First customers, design partners, founder-led | `first-customers` |
| Technical/solution selling | `technical-sales` |
| Prospect/lead signal discovery, Signals capture, related record views | `lead-signals` |
| Pipeline health, forecasting, call/deal signals | `sales-pipeline`, `revenue-intelligence`, `revenue-ops` |
| Quotes, proposals, MSAs, buyer docs | `commercial-docs`, `collateral` |
| First-touch cold outreach | `initial` |
| Multi-touch cadence design | `sequence` |
| Follow-up after a touch | `follow-up` |
| LinkedIn 1:1 engagement/DMs | `linkedin-dms` |
| X 1:1 DMs | `x-dms` |
| Launch orchestration and viral/referral mechanics | `launches`, `virality` |
| Expansion, retention, churn risk | `growth` |

Default signal chain: `lead-signals` (timely evidence and CRM capture) → `productivity/prospect` (full brief when needed) → `initial` (first touch). Default outbound chain: `productivity/prospect`/`initial` (first touch) → `sequence` (cadence) → `follow-up`. Default expansion chain: `growth` reads account health → tailored play.

## Operating defaults

- **Personalize from real signal.** Every message references something specific and true about the account/person. No generic spray.
- **No fabricated proof.** Do not invent customers, metrics, case studies, or capabilities. Use only approved, sourced claims; mark placeholders.
- **Respect the channel and the person.** Match LinkedIn/X/email norms; keep first touches short, value-first, and easy to say no to.
- **Lead with relevance, not the ask.** Earn the reply before the pitch.
- **Context is supplied, not embedded.** Pull ICP, product, account, and voice facts from user-provided or workspace-local sources; never hardcode them into reusable rules.
- **One clear next step** per message.

## Authorization gates

The request may authorize research, CRM preparation, and drafting. Confirm the final content, recipients, channel, timing, and commercial terms at the point of action before sending, enrolling, connecting, or committing.

- **Sending and connecting**: outreach, DMs, sequences, and connection requests are drafts by default. Sending or enrollment requires explicit authorization for the exact audience and final content.
- **Commercial commitments**: pricing, discounts, terms, and contract language must stay within approved policy and financial guardrails; otherwise draft and escalate rather than commit.
- **Compliance**: follow applicable anti-spam, privacy, consent, and opt-out requirements for the recipient and jurisdiction. No scraped-list blasting, deceptive subject lines, or ignored unsubscribes.
- **Mass targeting**: do not generate high-volume undifferentiated outreach; keep volume and personalization in human-reviewable bounds.
- **Customer data**: treat CRM and prospect data as confidential; do not paste into third-party tools that publish or cache content.

## Quality bar

- A message a human wouldn't send is not done — would the recipient feel it was written for them?
- Sequences specify channel, timing, and what changes between touches (not the same ask reworded).
- Every claim in collateral is sourced and approved.
- Expansion plays cite the account-health signal that triggered them.
