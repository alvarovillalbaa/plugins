---
type: calibration-brief
skill: [skill-id]
date: YYYY-MM-DD
status: [draft|approved|applied]
---

# Calibration Brief: [Skill Name]

## Observed Issue

**Symptom**: [Describe what the agent/skill does wrong. Be specific — "too verbose" isn't enough. Say "produces 800-word responses for 3-line code changes" or "misses off-by-one errors while commenting on style".]

**Frequency**: [Every time / Intermittent / Under specific conditions]

**Impact**: [Low / Medium / High — what does the team lose because of this behavior?]

---

## Example of Current Behavior

> [Paste a representative output that shows the problem. Include the input that triggered it.]

**Input**:
```
[Paste input here]
```

**Output (problematic)**:
```
[Paste the bad output here]
```

---

## Root Cause Hypothesis

[What in the current skill definition, agent prompt, or configuration is causing this behavior?]

Check:
- [ ] SKILL.md — is the scope too broad or underspecified?
- [ ] References — is there a reference that's introducing conflicting guidance?
- [ ] Quality gates in `.skillmeta.yml` — are they miscalibrated?
- [ ] Agent definition — is the agent persona drifting the behavior?

---

## Proposed Change

**File to change**: [path/to/file]

**Before**:
```
[Current content]
```

**After**:
```
[Proposed content]
```

---

## Test Plan

After applying the change, test against:

1. **Normal case**: [Input that should produce a clean output — confirm no false positives]
2. **Problem case**: [Input that previously triggered the bad behavior — confirm it's resolved]
3. **Edge case**: [Input near the boundary of what the skill handles]

---

## Expected Outcome

[One sentence: what does "better" look like after this change?]

---

## Log Entry

After applying and validating:

```yaml
- date: YYYY-MM-DD
  skill: [skill-id]
  change: "[Summary of change]"
  reason: "[Why this was needed]"
  outcome: "[What improved]"
```
