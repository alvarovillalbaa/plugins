# LinkedIn Post Examples

Five post formats with worked examples. Each demonstrates a different hook style.

---

## Format 1: The Contrarian Take

**Hook style**: Challenge a widely-held belief.

---

Everyone says "move fast and break things."

We moved fast. We broke our database in production at 2am.

Here's what we learned:

Speed without observability is just luck.

Three things we added after that incident:
→ Structured logging on every API endpoint
→ Rollback runbook for every deploy
→ On-call rotation starting at 4 engineers, not 10

We still move fast. We just move smart now.

What's one infrastructure mistake that changed how you build?

---

## Format 2: The Specific Lesson

**Hook style**: Lead with the hard number or outcome.

---

I spent 47 hours debugging a race condition.

Here's the 3-line fix:

```python
with db.transaction(isolation="serializable"):
    balance = account.get_balance()
    account.debit(amount)
```

The lesson: Most "complex" bugs are just missing transaction boundaries.

If you're seeing inconsistent state in your data — check your isolation level first.

Save this if you work with any database.

---

## Format 3: The Founder Story

**Hook style**: Personal narrative with a business insight.

---

We almost ran out of runway in month 8.

We had a great product. We had happy users. We had no revenue.

The hard truth our first investor told us:

"Users who don't pay don't validate your business. They validate your marketing."

That conversation changed our pricing strategy in 48 hours.

We went from free-forever to a 14-day trial with a credit card required.

Conversions dropped 40%. Revenue went up 3x.

The right customers were there all along. We just hadn't asked them to commit.

---

## Format 4: The List Post

**Hook style**: Promise a specific number of actionable items.

---

5 code review rules my team follows that cut our bug rate in half:

1. No PR over 400 lines. Large PRs hide problems.

2. The author writes the first comment. Explain your decisions before reviewers guess.

3. Review the tests before the code. Tests reveal intent better than code does.

4. One approve required, one async "looks good" preferred. Don't block on 3-person consensus.

5. Every PR needs a screenshot if it touches UI. "Looks fine" isn't a review.

What would you add?

---

## Format 5: The Insight Post

**Hook style**: Share a non-obvious observation from your work.

---

The best engineers I've hired had one thing in common:

They could explain what they didn't know.

Not "I'm not familiar with that yet."

Specifically:
"I know how it works conceptually, but I've never debugged it in production — so I'd estimate 2x longer on that piece."

That level of self-knowledge is rare. It's also what separates engineers who deliver from engineers who disappear into rabbit holes.

In your next interview, ask: "What's something technical you're currently weak in?"

The answer tells you everything.

---

*Note: Adapt tone, topic, and CTA to your brand voice. Run every post through the humanizing skill before publishing.*
