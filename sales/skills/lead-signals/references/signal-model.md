# Lead Signal Model

Use this reference to decide what qualifies as a lead signal, how to relate it,
and whether an existing record should be updated or a new record created.

## Contents

- [Signal test](#signal-test)
- [Taxonomy](#taxonomy)
- [Evidence and confidence](#evidence-and-confidence)
- [Entity resolution](#entity-resolution)
- [Logical Signals contract](#logical-signals-contract)
- [Deduplication](#deduplication)
- [Freshness](#freshness)

## Signal test

Treat evidence as a signal only when all of these are true:

1. It describes an event, action, or meaningful change rather than a static fact.
2. It has an attributable source and a defensible event date.
3. It resolves to at least one canonical People or Companies record.
4. It can change account fit, timing, risk, prioritization, or next action.

Examples of non-signals include a generic company description, an old role listed
without a recent change, an undated directory entry, a broad thought-leadership
post with no relevance to the offer, and an unsupported rumor.

## Taxonomy

Use the workspace's existing controlled vocabulary when present. Otherwise map
candidates to the narrowest useful type:

| Scope | Common types | Examples |
| --- | --- | --- |
| Company | Funding, hiring, leadership, expansion, launch, partnership, technology, procurement, risk | Funding announcement, relevant open roles, executive hire, new market, migration, regulatory event |
| Person | Role change, promotion, authored intent, event, engagement, evaluation | New remit, promotion, problem-specific post, conference talk, demo or pricing activity |
| Both | Champion movement, employer-specific intent, buying-committee activity | New leader starts a relevant initiative, employee evaluates a tool for the current company |

Include negative and risk signals when they materially change the next action.
Sentiment is not a substitute for a precise type.

## Evidence and confidence

Store the observed fact separately from its implication.

- **Evidence**: State what happened, to whom, when, and where it was published.
- **Why now**: Explain how the evidence may affect fit, timing, risk, or next
  action. Mark this as inference unless the source states it directly.
- **High confidence**: Use for direct first-party evidence with exact identity and
  date, or independently corroborated authoritative evidence.
- **Medium confidence**: Use for a credible secondary source with clear identity
  and date, or first-party evidence whose commercial implication is inferred.
- **Low confidence**: Use for indirect, ambiguous, undated, or single-source rumor
  evidence. Do not save it by default; keep it unresolved unless the user asks to
  retain low-confidence candidates.

Preserve both the event date and capture time. Never replace an unknown event
date with the article publication date without labeling that substitution.

## Entity resolution

Resolve stable identifiers before names:

| Entity | Preferred identifiers | Required checks |
| --- | --- | --- |
| Company | Canonical domain, verified company profile URL, external CRM ID | Rebrands, redirects, subsidiaries, archived records |
| Person | Work email, verified professional profile URL, external CRM ID | Full name, current title, current employer, duplicate names |

Apply these relation rules:

- Relate a Company when the event is about the organization.
- Relate a Person when the event is about that individual's action or role.
- Relate both only when the evidence ties the individual event to the verified
  current company.
- Hold the item when identity remains ambiguous. Do not pick the first search
  result or create an entity record unless entity creation is explicitly in
  scope.

## Logical Signals contract

Map these semantics onto the actual fetched schema. Equivalent existing property
names are valid; do not force the labels below.

| Logical field | Requirement | Guidance |
| --- | --- | --- |
| Signal | Required title | Use a concise event title such as `Acme - VP Sales hired` |
| Type | Required | Use the existing controlled option or the narrowest supported type |
| Signal date | Required | Store the event date; record uncertainty explicitly |
| Evidence | Required | Store the factual event summary, not promotional copy |
| Source URL | Required | Store the canonical primary URL when available |
| People | Conditional relation | Populate for each resolved person the evidence concerns |
| Companies | Conditional relation | Populate for each resolved company the evidence concerns |
| Confidence | Recommended | High, Medium, or Low under the rules above |
| Why now | Recommended | Store the sourced implication or a labeled inference |
| Captured at | Recommended | Use created time or an explicit timestamp |
| Status | Recommended | Reuse the workspace lifecycle, such as New, Verified, Dismissed, or Expired |
| Corroborating sources | Optional | Preserve secondary URLs without duplicating the event |
| Fingerprint | Optional | Store a deterministic dedupe key when the schema supports it |

Require at least one of People or Companies. If neither relation can be resolved,
do not write the signal.

## Deduplication

Build a logical fingerprint from:

1. a normalized atomic event key;
2. event date;
3. narrow signal type; and
4. sorted resolved People and Companies page IDs.

Before creation, query likely matches by source URL, relations, type, and nearby
date as well as by any stored fingerprint. Normalize tracking parameters and
redirects, but preserve the canonical source. Do not treat a different article
URL as a different event.

Treat multiple articles about one funding round, leadership change, launch, or
role change as corroboration of one event. Update an existing record when the new
source is more primary, the date becomes exact, evidence becomes materially
richer, or a missing valid relation is resolved. Preserve useful previous
evidence and do not broaden relations beyond what the sources support.

Split one source into multiple records only when it contains independently
actionable events with distinct types, dates, or subjects.

## Freshness

Honor the user's window or existing monitoring policy. When none exists, favor
recent events and report the dates used instead of inventing a universal cutoff.
Mark older but still relevant evidence as historical context, not a new signal.
