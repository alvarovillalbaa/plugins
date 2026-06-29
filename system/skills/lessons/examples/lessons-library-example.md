# Lessons Library Example

A sample lessons library showing lessons across multiple categories. This is the format for `system/skills/lessons/` knowledge base entries.

---

## Engineering Lessons

### E001 — Don't rename tables without auditing materialized views

**Category**: Engineering  
**Severity**: High  
**Lesson**: Schema migrations must audit all dependent objects (views, materialized views, functions, triggers), not just foreign keys and indexes.  
**Context**: Any time you rename, drop, or alter a table in a production database.  
**Action**: Run a dependency audit script before every migration. Add materialized view refresh as an explicit migration step.  
**Evidence**: 2026-Q1 incident — migrated table rename caused materialized views to serve stale data for 3 hours. $40K in compute and engineering cost.

---

### E002 — Feature flags need explicit deletion plans

**Category**: Engineering  
**Severity**: Medium  
**Lesson**: Every feature flag created must have a defined deletion date or conditions for removal.  
**Context**: Any time you create a feature flag.  
**Action**: Add a `remove_by` field to your feature flag config. Review flags quarterly.  
**Evidence**: Accumulated 80+ flags in 18 months; 60% were stale but required investigation before deletion.

---

## Product Lessons

### P001 — Don't gate activation on third-party actions

**Category**: Product  
**Severity**: High  
**Lesson**: Any activation gate that requires the user to take an action outside the product (invite someone, connect a tool) will disproportionately hurt solo evaluators.  
**Context**: Designing onboarding and activation flows.  
**Action**: Make social/collaborative steps optional. Defer team invite to post-first-value.  
**Evidence**: 2026-Q2: required team invite gate caused 35% drop-off at step 3. Removed gate → 12% drop-off.

---

### P002 — Measure activation, not signups

**Category**: Product  
**Severity**: Medium  
**Lesson**: Signup count is a vanity metric. The metric that predicts retention is time-to-first-value (TTFV).  
**Context**: Setting up product analytics; defining success metrics for onboarding.  
**Action**: Define a specific activation event ("aha moment") and measure how long it takes new users to reach it. Optimize TTFV, not signup count.  
**Evidence**: Cohorts that reached activation within 24 hours had 3× higher 30-day retention than those that activated at day 3+.

---

## Process Lessons

### PR001 — Post-mortems within 48 hours

**Category**: Process  
**Severity**: Medium  
**Lesson**: The longer you wait after an incident, the more detail is lost and the more defensive people become.  
**Context**: After any incident or significant failure.  
**Action**: Hold the retrospective within 48 hours. Use the retrospective template. Focus on system failures, not blame.  
**Evidence**: Retrospectives held 5+ days after incidents consistently produced shallower analysis and more defensive framing.

---

## Lessons Library Format

Each lesson card should include:
- **ID**: Unique identifier (category prefix + number + short slug)
- **Category**: Engineering / Product / Process / Team / Sales / Marketing
- **Severity**: Low / Medium / High (impact if the lesson is forgotten)
- **Lesson**: One sentence, generalized
- **Context**: When does this apply?
- **Action**: What to do differently
- **Evidence**: Data or outcome that supports the lesson
