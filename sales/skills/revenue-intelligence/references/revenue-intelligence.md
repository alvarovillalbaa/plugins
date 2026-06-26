# Revenue Intelligence

Load this file when the task involves sales-call transcript analysis, Gong-style call intelligence, objection mining, buying-signal extraction, competitor mentions, content ROI, attribution models, unified client reporting, or anomaly detection across marketing and revenue data.

## Role in GTM

Revenue intelligence closes the loop between market activity and commercial proof.

Use it to answer questions such as:

- what prospects keep saying on calls
- which objections or competitors are slowing deals
- what content or channels influenced pipeline or closed revenue
- what changed this month across traffic, pipeline, SEO, or call quality
- what action marketing, sales, or CS should take next

Do not treat it as reporting theater. The point is to improve decisions.

## Operating model

Work in three linked layers:

1. Call insight extraction
2. Revenue attribution
3. Client or executive reporting

Use one layer when the request is narrow. Use all three when the user needs a full revenue story.

## 1. Call insight extraction

Use this when the user has transcripts, call notes, or Gong-style data and wants structured insight.

### Extract these signal groups

- objections: pricing, timing, competition, authority, need
- buying signals: budget confirmed, timeline mentioned, decision maker engaged, champion identified
- competitive mentions: who was named and whether sentiment was positive, negative, or neutral
- pricing discussions: anchors, pushback, ROI concerns, willingness indicators
- content topics: repeated objections or questions that should become content, battle cards, or enablement
- follow-up actions: next steps for the rep, marketer, or account team

### Workflow

1. Identify the call type: discovery, evaluation, pricing, renewal, expansion, or implementation.
2. Pull out repeated objections and separate one-off comments from patterns.
3. Mark buying signals only when the transcript shows real evidence.
4. Capture competitor context and whether the mention is threat, benchmark, or displacement target.
5. Translate the findings into GTM actions:

- messaging changes
- sales enablement or battle cards
- content ideas
- follow-up sequence updates

### Output expectation

A strong output includes:

- top objections with counts or frequency notes
- strongest buying signals
- competitor mentions with context
- pricing friction summary
- 3-5 concrete GTM actions

If the user only provides a few transcripts, do not pretend the patterns are statistically stable.

## 2. Revenue attribution

Use this when the user wants to prove content ROI, tie campaigns to pipeline, compare attribution models, or find content gaps in the buyer journey.

### Core questions

- which content pieces influenced pipeline or revenue
- which content types perform best
- what funnel stages have weak or missing content support
- whether the current channel mix produces efficient revenue

### Attribution models

Use these defaults unless the user provides a company-specific model:

- first-touch: best when the question is what introduced or sourced the deal
- linear: best when multiple touches matter and the team wants shared credit
- time-decay: best when later touches deserve more weight in a longer sales cycle

Always name the model being used. Do not present one model as objective truth.

### Data requirements

At minimum, confirm:

- touchpoint or content interaction data from analytics or marketing systems
- deal, opportunity, or close data from CRM
- join logic across contacts, companies, sessions, or URLs
- date ranges and any attribution window assumptions

Weak joins mean weak conclusions. State the caveat clearly.

### Workflow

1. Define the business question: sourcing, influence, ROI, CPA, or gap analysis.
2. Choose the attribution model that matches the buying motion.
3. Validate data coverage and join quality before calculating anything.
4. Rank the top content, campaigns, or channels by attributed pipeline or revenue.
5. Compare performance by content type when useful.
6. Identify content gaps by funnel stage, objection theme, or segment.
7. Recommend what to invest in, cut, or test next.

### Output expectation

Include:

- chosen attribution model and why
- top revenue-influencing content, campaigns, or channels
- content-type or channel comparison
- content gaps or missing instrumentation
- action plan tied to budget, production, or enablement

## 3. Client or executive reporting

Use this when the user needs a unified monthly or quarterly readout across analytics, CRM, SEO, and call data.

Common sources include:

- analytics systems for sessions, users, top pages, and channels
- CRM for opportunities, pipeline movement, closed revenue, and deal stages
- SEO tools for rankings, backlinks, and domain authority trends
- call systems for objection frequency, pricing friction, talk ratios, or win-pattern notes

### Reporting structure

Bias toward a compact readout with:

- executive summary
- traffic and channel movement
- pipeline and revenue movement
- content or SEO contribution
- call-quality or call-insight summary
- anomalies, risks, and next actions

### Interpretation rules

- separate leading indicators from lagging outcomes
- compare period over period when the baseline is credible
- call out anomalies only when the change is meaningful enough to warrant action
- tie every section to a decision, not just a metric

Good reports explain:

- what changed
- why it likely changed
- whether it matters commercially
- what the team should do next

## Data-quality rules

- Do not claim precision beyond the quality of the source systems.
- Missing CRM hygiene, inconsistent UTMs, or weak identity resolution should change the confidence level.
- Separate observed facts from inferred causes.
- If the user lacks real system access, provide the schema, model, and analysis plan instead of fake numbers.

## Cadence

Use this default rhythm unless the user specifies another one:

- weekly: call insight extraction and objection review
- monthly: attribution and client or executive reporting
- quarterly: content-gap analysis and channel or message reallocation

## Decision rules

- Repeated objections should feed messaging, content, product feedback, or enablement.
- Repeated buying signals should sharpen ICP and qualification.
- Competitor mentions should inform battle cards and differentiation, not vanity comparisons.
- Attribution should influence spend and content planning, not just satisfy reporting demands.
- A report is incomplete if it names metrics but not actions.
