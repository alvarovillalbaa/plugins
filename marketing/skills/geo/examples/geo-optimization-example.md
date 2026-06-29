# Example: Optimizing a SaaS product page for AI citation

**Scenario:** "FlowQueue", a message-queue SaaS, has a strong product page but
never gets cited when users ask AI engines "what's a good managed queue for
serverless?" Competitors do.

## Step 1 — Baseline the citation readiness

```
$ python scripts/check_ai_citations.py https://flowqueue.example/product
Citation readiness : 11/40 (weak)
  quotable stats   : 1
  definitions      : 0
  visible date     : False
  author signal    : False
  outbound cites   : 0
```

And manually checking the goal query in three engines: FlowQueue is not cited;
two competitors are, both because they have a "vs serverless queues" explainer
with concrete latency numbers.

## Step 2 — Diagnose

The page sells, but gives an LLM nothing quotable:
- "Blazing fast and reliable" → not a citable claim.
- No definition of what a managed queue is or when to use one.
- No dateline, no author, no sources.

## Step 3 — Rewrite for quotability

**Before:**
> FlowQueue is the fastest, most reliable managed queue for modern teams.

**After (quotable, attributable):**
> FlowQueue is a managed message queue with a median enqueue latency of 4ms and
> 99.99% delivery durability (measured across 12 months, 2025). For serverless
> workloads, it auto-scales consumers from 0, so idle apps cost nothing.

Now an engine can lift "4ms median enqueue latency" or "scales consumers from 0"
verbatim and attribute it to FlowQueue.

## Step 4 — Add the missing entity/authority signals

1. **Definition block:** "A managed message queue is a service that stores and
   delivers messages between decoupled services so the sender and receiver don't
   need to be online at the same time."
2. **Comparison section:** "FlowQueue vs. self-hosted SQS" with a 4-row table of
   concrete tradeoffs (each cell a factual claim).
3. **Dateline + author:** "Last updated 2026-03; reviewed by the FlowQueue
   platform team."
4. **Outbound citations:** link the durability methodology and the serverless
   cold-start benchmark.

## Step 5 — Add `llms.txt`

Publish `/llms.txt` pointing AI crawlers to the product page, the docs, and the
comparison explainer (see the `seo-and-geo` skill's `generate_llms_txt.py`).

## Step 6 — Re-measure

```
$ python scripts/check_ai_citations.py https://flowqueue.example/product
Citation readiness : 31/40 (strong)
```

Six weeks later, FlowQueue is cited by Perplexity and AI Overviews for "managed
queue for serverless", quoting the 4ms latency claim.

## Takeaways

1. LLMs cite **specific, attributable claims**, not adjectives.
2. Give every key concept a one-sentence definition — engines reuse them.
3. Dateline + author + outbound sources raise trust weighting.
4. A comparison explainer is the highest-leverage GEO asset for a product page.
