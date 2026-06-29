# Knowledge Base Design Reference

Reference for knowledge-base improvement: structure, tagging, retrieval patterns, dedupe, canonical-page health, missing-source promotion, and drift repair. A KB is only as good as its retrievability and freshness — design for findability and maintain against decay. Edits to other departments' knowledge are human-gated.

## What makes a KB useful

A knowledge base succeeds when the right entry is **findable** at the moment of need and **trustworthy** when found. The two failure modes are: it's in there but nobody can retrieve it (structure/retrieval problem), or it's retrievable but wrong/stale (freshness problem). KB work targets both.

## Structure

### Canonical pages
- **One canonical page per concept.** Each topic has a single authoritative entry; everything else links to it. This is the antidote to drift and duplication.
- **Atomic and self-contained** — an entry covers one thing well and stands alone (a reader landing cold understands it).
- **Consistent template** per entry type (concept, how-to, reference, decision) — predictable structure aids both humans and retrieval.
- **Clear titles** that match how people search (their words, not internal jargon).

### Hierarchy & linking
- Shallow hierarchy + rich cross-linking beats deep nesting. People find via search and links, not by drilling folders.
- Link related entries bidirectionally so navigation surfaces neighbors.
- Maintain an index/map of canonical pages.

## Tagging & metadata

Good metadata is what makes retrieval work:
- **Topic tags** — the subject(s); enables faceted browse and filtered retrieval.
- **Type** — concept / how-to / reference / decision / FAQ.
- **Source** — where the knowledge came from (provenance for trust and staleness checks).
- **Owner** — who maintains it.
- **Last-verified date** — not just last-edited; when was the content confirmed true.
- **Status** — canonical / candidate / deprecated.

Use a controlled vocabulary for tags (a fixed set), not free-form — inconsistent tags fragment retrieval.

## Retrieval patterns

- **Keyword/full-text** — fast, exact; depends on titles/body using the searcher's language.
- **Semantic / embedding** — matches meaning, not just words; good for natural-language queries (route deep RAG design to engineering's `context-memory-rag`).
- **Tag/faceted** — filter by topic, type, recency.
- **Hybrid** — combine semantic recall with keyword/tag precision; usually best.
- **Chunking** — for long docs, chunk at semantic boundaries so retrieval returns the relevant section, not a whole document.

Design entries *for* retrieval: descriptive titles, a one-line summary up top, keyword-rich phrasing, and metadata. The best content nobody can find is worthless.

## Dedupe

Duplicates erode trust (which is right?) and split retrieval signal.
- **Detect**: near-identical titles, overlapping content, multiple entries answering the same question.
- **Propose a merge**: pick the best/most-current as canonical, fold in unique content from the others, redirect/link the rest.
- **Never silently delete** — preserve unique information; merge rather than drop. Surface the merge proposal for approval before acting on shared KBs.

## Canonical-page health

Audit the authoritative pages:
- **Completeness** — does it fully cover its concept, or are there gaps?
- **Accuracy** — verify against current reality; flag stale claims (this overlaps documentation-drift detection).
- **Freshness** — last-verified date within an acceptable window for its volatility.
- **Linkage** — is it linked from where people would look? Orphan pages don't get found.
- **Single-source** — no competing entries for the same concept.

## Missing-source promotion

Knowledge often lives outside the KB (chats, docs, tickets, sessions). Promote it:
1. **Detect gaps** — recurring questions with no canonical answer; valuable knowledge trapped in transient sources.
2. **Evaluate** — is it durable, broadly useful, and accurate enough to canonicalize?
3. **Promote** — write/refine a canonical entry, tag it, set provenance and verified date.
4. **Gate promotion** — candidate → canonical is an approval step; keep candidates separate until reviewed (overlaps `lessons` promotion).

## Drift repair

KBs decay as the world changes:
- **Detect drift** — last-verified dates aging out, claims contradicting current reality, broken links, references to removed features/tools.
- **Repair** — update to current truth (verify first), fix links, deprecate obsolete entries (mark, don't just delete), reconcile contradictions to the canonical.
- **Run on a cadence** and on major changes — drift is silent and compounds.

## Quality gates

- **Verify before trusting** — a KB entry is a claim from when it was written; re-check current state before acting on it, and update if stale.
- **Provenance on everything** — every entry records its source and verified date.
- **Merge, don't drop** — preserve unique info during dedupe.
- **Human-gated for shared/other-department KBs** — promotion, merges, and deletions need approval.
- **Respect licensing/privacy** — don't ingest secrets or PII into shared knowledge.

## Handoffs

- Deep retrieval/RAG architecture → engineering `context-memory-rag`.
- Stale-doc detection in code/instruction files → productivity `documentation-drift`.
- Durable cross-session memory → `memory`.
- Lessons promotion → `lessons`.
- Skill content maintenance → `skills-management`.
