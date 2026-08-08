# Notion Signals Workflow

Use this reference for concrete Notion operations. Work from fetched IDs and
schemas; tool labels differ by runtime, but the required capabilities are
search, fetch, data-source query, database/schema update, page create/update,
linked-view create/update, and view query.

## Contents

- [Inspect the workspace](#inspect-the-workspace)
- [Query before writing](#query-before-writing)
- [Create or extend the schema](#create-or-extend-the-schema)
- [Create or update signal pages](#create-or-update-signal-pages)
- [Add filtered linked views](#add-filtered-linked-views)
- [Verify completion](#verify-completion)

## Inspect the workspace

1. Search for `Signals`, `People`, and `Companies` and retain URLs or IDs for all
   plausible matches.
2. Fetch each database. Extract its database ID, every `<data-source>`
   `collection://` URL, schema, property types, templates, and views.
3. Select the canonical data source from its schema and parent context. Do not
   assume a database has only one data source.
4. Search or query target records within the selected People and Companies data
   sources, then fetch each exact page before using its ID in a relation or view.
5. If duplicate titles exist, resolve by stable identifiers. Do not depend on a
   title-only match.

## Query before writing

Query the Signals data source for likely duplicates using parameterized values
where supported. Include enough of source URL, event date, type, People relation,
and Companies relation to find the same logical event. Query filters on a view
are not inherited by direct data-source queries.

Do not use workspace-wide semantic search as proof that no structured Signals row
exists. Query the canonical data source.

## Create or extend the schema

Perform this section only in explicit setup scope.

When no compatible Signals database exists, create it under the user's stated CRM
or workspace parent. A minimum schema can map to this shape, substituting the
fetched People and Companies data source IDs:

```sql
CREATE TABLE (
  "Signal" TITLE,
  "Type" SELECT('Funding':green, 'Hiring':blue, 'Leadership':purple, 'Expansion':orange, 'Launch':blue, 'Technology':gray, 'Intent':green, 'Engagement':yellow, 'Risk':red),
  "Signal date" DATE,
  "Evidence" RICH_TEXT,
  "Source URL" URL,
  "Confidence" SELECT('High':green, 'Medium':yellow, 'Low':red),
  "Why now" RICH_TEXT,
  "People" RELATION('<people-data-source-id>'),
  "Companies" RELATION('<companies-data-source-id>'),
  "Status" STATUS,
  "Captured at" CREATED_TIME
)
```

Treat this as a logical starting point, not a mandate to replace a compatible
schema. If Signals exists, add only required missing properties with additive
schema statements. Prefer one-way relations from Signals because filtered linked
views do not require mutating the target databases. Reuse compatible two-way
relations when they already exist.

Never drop, rename, or change the type of an existing property without a separate
explicit request and impact review.

## Create or update signal pages

1. Use the Signals **data source ID** as the page parent, not a database page ID
   guessed from a URL.
2. Use the fetched title property name; every new row must include it.
3. Format dates and property values according to the fetched schema.
4. Set relation properties to arrays of exact related page IDs or URLs.
5. Update a duplicate row only with the smallest property/content change needed.
   Omitted properties must remain unchanged.
6. Fetch every changed page and compare the returned values with the staged
   record before continuing to views.

## Add filtered linked views

Read `notion://docs/view-dsl-spec` through the Notion fetch capability before
composing filters. Do not insert a text summary or a second database in place of
a linked view.

For each target record page:

1. Fetch the page and inspect existing linked databases and views.
2. Reuse a linked view that already references the canonical Signals data source
   and filters to the same record. Update it only when its purpose is unambiguous.
3. Otherwise create an inline linked view with:
   - `parent_page_id`: exact People or Companies record page ID;
   - `data_source_id`: canonical Signals data source ID;
   - `type`: `table` unless the user requests another presentation;
   - `name`: `Signals` or the workspace's existing equivalent; and
   - `configure`: relation filter, newest-first date sort, and useful visible
     properties.

Pass filters, sorts, and shown properties through the single documented
`configure` DSL string. Do not invent JSON fields such as `filter`, `sort`,
`visible_properties`, or relation operators that the connector does not expose.

Conceptual company configuration:

```text
FILTER "Companies" = "Acme";
SORT BY "Signal date" DESC;
SHOW "Signal", "Type", "Signal date", "Confidence", "Source URL"
```

Conceptual person configuration:

```text
FILTER "People" = "Priya Shah";
SORT BY "Signal date" DESC;
SHOW "Signal", "Type", "Signal date", "Confidence", "Source URL"
```

Replace every label and value with fetched schema and record values. The view DSL
documents displayed values but not stable relation page-ID operands. Use a
displayed title only when it is unique. When duplicate record titles exist, use a
page ID or URL only if the current connector documentation explicitly supports
it; otherwise do not create an ambiguous view. Query every created view and
inspect each row's exact relation page ID rather than trusting creation success.

Do not bind a database template's linked view permanently to the example record.
Use a supported current-record filter only when the connector documents and
verifies it; otherwise add views to actual pages.

## Verify completion

Verify two independent surfaces:

1. **Canonical row**: Fetch or query the Signals record and confirm title, type,
   event date, evidence, source URL, and exact relation IDs.
2. **Embedded view**: Query the created or updated view with its returned view URL
   or ID. Confirm every row has the intended relation and no unrelated row is
   exposed.

Record created/updated page IDs and view IDs. Report partial completion when page
writes succeed but view creation, filtering, or verification is unavailable.
