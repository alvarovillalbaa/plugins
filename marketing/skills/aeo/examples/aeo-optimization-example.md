# Example: Optimizing a FAQ page for featured snippets and AI answers

**Scenario:** A SaaS billing tool has an `/faq` page that ranks on page 1 for
"how to issue a prorated refund" but never wins the featured snippet or gets
cited by AI answer engines.

## Step 1 — Audit the current state

Run the schema check:

```
$ python scripts/check_schema_markup.py https://example.com/faq
JSON-LD blocks found : 1
Types                : WebPage, BreadcrumbList
AEO-relevant types   : BreadcrumbList
No AEO-relevant structured data. Add FAQPage/HowTo/Article JSON-LD...
```

Finding: no `FAQPage` markup, and the on-page answer buries the response.

## Step 2 — Diagnose the answer block

**Before (current copy):**

> ## Refunds
> We understand billing can be confusing. There are many factors that go into
> how refunds work at our company, and our team is always happy to help. In
> general, depending on your plan and timing, you may be eligible for a
> prorated amount...

Problems: no question-shaped heading, the answer is not in the first sentence,
and it hedges ("may be eligible", "depending on") so no engine will quote it.

**After (AEO-optimized):**

> ## How do I issue a prorated refund?
> To issue a prorated refund, open **Billing → Invoices**, select the invoice,
> and click **Refund → Prorated**. The system credits the unused days of the
> current cycle automatically. Prorated refunds are available on monthly and
> annual plans within 30 days of the charge.

This leads with the action, is self-contained (~50 words), and states the
concrete limit (30 days).

## Step 3 — Add FAQPage structured data

Using `templates/faq-schema-template.json`:

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [{
    "@type": "Question",
    "name": "How do I issue a prorated refund?",
    "acceptedAnswer": {
      "@type": "Answer",
      "text": "Open Billing → Invoices, select the invoice, and click Refund → Prorated. The system credits the unused days of the current cycle. Prorated refunds are available on monthly and annual plans within 30 days of the charge."
    }
  }]
}
```

## Step 4 — Expand coverage from real questions

Pull People-Also-Ask and support tickets for adjacent questions and add an
answer block + schema entry for each:
- "Can I get a refund after downgrading?"
- "How long does a prorated refund take to appear?"
- "Do annual plans get prorated refunds?"

## Step 5 — Verify

```
$ python scripts/check_schema_markup.py https://example.com/faq
AEO-relevant types   : FAQPage, BreadcrumbList
```

## Result (8 weeks later)

- Featured snippet captured for "how to issue a prorated refund"
- Page cited by two AI answer engines for refund-timing questions
- 3 new long-tail queries now surface the page in PAA boxes

## Takeaways

1. Structured data is necessary but not sufficient — the visible answer must be
   quotable too.
2. Lead with the answer; state concrete limits and numbers.
3. One question = one heading = one self-contained answer = one schema entry.
