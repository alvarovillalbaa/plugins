---
name: lead-signals
description: Discover evidence-backed buying, hiring, funding, and intent signals for prospects, write them to a Notion Signals database, and link them to People/Companies records.
---

# Lead Signals

Turn timely prospect evidence into canonical, traceable Notion records. Keep one
Signals database as the source of truth and surface it through filtered linked
views on the relevant People and Companies pages.

## Select the operation

Infer the authorized operation from the user's verbs:

- **Discover**: Find and return candidate signals without changing the workspace.
- **Capture**: Deduplicate and write signals to an existing Signals database.
- **Surface**: Add or repair filtered linked Signals views on existing records.
- **Set up**: Create the Signals database or add missing relation properties.

Do not convert a discovery-only request into workspace writes. Treat explicit
requests to add, log, save, sync, connect, introduce, or set up as authorization
for the corresponding scoped writes. Require direction before creating a
database in an unknown parent, changing a shared schema outside setup scope, or
creating missing People or Companies records.

## Load the guidance

- Read [`references/signal-model.md`](references/signal-model.md) before
  classifying, relating, or deduplicating signals.
- Read [`references/notion-workflow.md`](references/notion-workflow.md) before
  inspecting or mutating Notion databases, records, relations, or views.

## Execute the workflow

### 1. Inspect before mutating

1. Identify the requested people, companies, saved view, list, and date window.
2. Locate the canonical Signals, People, and Companies databases.
3. Fetch each database and its data source before querying or writing. Record the
   exact database IDs, `collection://` data source IDs, property names, property
   types, templates, and existing views.
4. Reuse compatible databases and properties. Never create a near-duplicate
   because a title, relation, or field name differs from an assumption.
5. Stop only the ambiguous item when multiple databases or entity records remain
   plausible; continue safely resolvable items.

### 2. Resolve the subjects

Resolve Companies by stable identifiers such as canonical domain or company
profile URL. Resolve People by work email or public professional profile URL,
then verify name, role, and current employer. Use a normalized name only when it
is unique in scope.

Relate a signal according to its evidence:

- Company event: relate the Company.
- Individual action or role change: relate the Person.
- Individual evidence materially concerning a verified current employer: relate
  both the Person and Company.

Never infer a company relation solely because the person once worked there.
Require at least one resolved People or Companies relation for every saved
signal.

### 3. Discover meaningful events

Prefer primary, attributable, dated evidence: company announcements, filings,
careers pages, product or documentation changes, and the person's own
professional activity. Use reputable secondary sources for discovery or
corroboration, not as a substitute for a reachable primary source when one
exists.

Capture an event only when it can change fit, timing, risk, or the next sales
action. Treat static firmographics, generic content, undated claims, and weak
rumors as enrichment or unresolved candidates rather than signals. Keep the
observed fact separate from the sales implication, and label inference.

Use only professionally relevant public information or data the user is
authorized to access. Exclude protected or sensitive personal attributes and do
not infer them.

### 4. Stage and deduplicate

For each candidate, stage the exact subject records, type, event date, evidence,
primary source URL, capture time, confidence, sales implication, and fingerprint.
Query existing Signals before creating anything.

Treat coverage of the same event as one signal. Update the existing record when
new evidence is more authoritative or materially richer; preserve useful prior
evidence and relations. Create separate records only for distinct events.

### 5. Prepare the database

Map the logical contract in `references/signal-model.md` onto the fetched schema.
Use exact existing property names and types.

In setup mode, create one Signals database only when no compatible canonical
database exists and the parent location is known. Add only missing properties or
relations. Never rename, drop, or repurpose existing properties as a side effect
of capture.

Outside setup mode, request one narrow decision if a missing required relation or
field prevents a valid write. Do not save orphaned or misleading records just to
finish the batch.

### 6. Write the signals

Create one Signals page per atomic event under the fetched Signals data source.
Use exact property names, absolute dates, canonical source URLs, and arrays of
the resolved record page IDs or URLs for relation properties.

Batch only records that share the verified schema and resolution state. Skip
weak, duplicate, ambiguous, or relationless candidates and retain their reasons
for the completion report.

### 7. Surface related signals

For every in-scope People or Companies page, fetch the page and check whether it
already contains a linked view of the canonical Signals data source.

Reuse or narrowly repair a matching view. Otherwise, append one inline linked
database view that:

- references the canonical Signals data source rather than copying records;
- filters the People or Companies relation to the current record;
- sorts the signal date newest first; and
- shows only useful signal fields.

Use only the connector's documented view configuration DSL. Do not invent
structured filter fields or undocumented relation operators. If duplicate record
titles make the documented relation filter ambiguous and no stable page-ID or
URL value is supported, leave that one view uncreated and report the limitation.

Do not emulate a linked database by pasting signal text into the page. Do not add
duplicate views. Treat template-level current-record filters as valid only when
the connector explicitly supports them; otherwise create and verify views on the
actual record pages.

### 8. Verify and report

Read back every created or updated signal and verify its evidence, date, source,
and exact relation targets. Query every created or changed view and confirm that
all returned rows relate to the intended page and that unrelated rows are absent.

Report:

- scope and date window;
- counts discovered, created, updated, skipped, and unresolved;
- changed record and view links or IDs;
- skipped or ambiguous items with reasons; and
- any incomplete schema, relation, or view operation.

Count each candidate in exactly one disposition: created, updated, skipped, or
unresolved. Report view outcomes separately so totals do not double-count the
same evidence.

Never claim the signals are connected or visible until both the records and
filtered views pass read-back verification.

## Chain rules

- Chain to `prospect` for a complete account/persona brief, ICP/ICA scoring, or
  next-best-motion analysis beyond atomic signal capture.
- Chain to `research` for broader source collection or multi-pass investigation.
- Chain to `revenue-intelligence` for call, opportunity, attribution, forecast,
  or cross-pipeline pattern analysis.
- Chain to `sales-pipeline` for deal-stage changes and opportunity actions.
- Chain to `outreach` only when the user separately requests messaging. Preserve
  the human approval gate for sending or enrolling outreach.

## Failure rules

- Do not guess database IDs, property names, relation targets, dates, or sources.
- Do not create People or Companies merely to avoid an unresolved relation.
- Do not overwrite stronger evidence with weaker secondary coverage.
- Do not expose confidential CRM data through public or caching tools.
- Do not hide connector limitations. Complete safe independent work, then state
  the exact remaining manual or blocked step.
