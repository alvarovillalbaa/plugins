---
type: retrospective
date: YYYY-MM-DD
team: [team name]
subject: [what happened — incident, launch, decision]
facilitator: [name]
---

# Retrospective: [Subject]

**Date**: YYYY-MM-DD  
**Attendees**: [List names or roles]  
**Duration**: [X minutes]

---

## What Happened

[Factual timeline of the event. Who did what, when. No blame — just sequence.
For incidents: include exact timestamps. For launches: include key milestones.]

- [Timestamp] [Event]
- [Timestamp] [Event]
- [Timestamp] [Event]

---

## What Went Well

[Things that worked — processes, tools, decisions, communication. Be specific.
These are as important as what went wrong — repeat them intentionally next time.]

- [Positive 1]
- [Positive 2]
- [Positive 3]

---

## What Went Poorly

[Things that didn't work. Still no blame — focus on process and system failures, not individuals.]

- [Problem 1]
- [Problem 2]
- [Problem 3]

---

## Root Cause Analysis

[For each major problem above, go one level deeper. Ask "why" until you reach an actionable root cause.]

**Problem**: [Problem 1]  
**Root cause**: [Why did this happen?]  
**Contributing factors**: [What made this more likely or harder to catch?]

---

## Action Items

| Action | Owner | Due Date | Status |
|--------|-------|----------|--------|
| [Action 1] | [Name] | YYYY-MM-DD | open |
| [Action 2] | [Name] | YYYY-MM-DD | open |

---

## Lessons Extracted

[For each generalizable lesson, add a lesson card block below.]

```yaml
id: [kebab-case-unique-id]
category: [product|engineering|process|team|sales|marketing]
severity: [low|medium|high]
lesson: "[One sentence: the generalized principle.]"
context: "[When does this apply?]"
action: "[What should we do differently?]"
evidence: "[What data or outcome supports this lesson?]"
```

```yaml
id: [second-lesson-id]
category: [category]
severity: [severity]
lesson: "[Lesson]"
context: "[Context]"
action: "[Action]"
evidence: "[Evidence]"
```

---

## Follow-Up Review

- [ ] Action items reviewed at: [date or meeting]
- [ ] Lessons added to `system/skills/lessons/` knowledge base
- [ ] Affected skill/process documentation updated
