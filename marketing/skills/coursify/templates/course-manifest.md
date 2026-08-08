---
purpose: Canonical blueprint for a source-grounded course and its production lanes.
audience: Course designers, subject-matter experts, and production agents.
---

# Course Manifest: <title>

## Contract

- Title (`title`):
- Audience (`audience`):
- Entry level (`entry_level`):
- Desired transformation (`desired_transformation`):
- Delivery format (`format`):
- Prerequisites (`prerequisites[]`):
- Total duration and cadence:
- Constraints and non-goals:

## Accessibility

- Known needs (`accessibility.needs[]`; use an empty array when none are known):
- Provisions (`accessibility.provisions[]`):
- Unresolved gaps (`accessibility.gaps[]`; use an empty array when verified):

## Outcomes

| ID | Learner will be able to | Evidence of mastery |
| --- | --- | --- |
| outcome-1 | <observable performance> | <assessment evidence> |

## Source Map (`source_map[]`)

| Source ID | Location | Authority or observed date | Used-by IDs | Notes or license |
| --- | --- | --- | --- | --- |

## Curriculum

### Module `<module-id>`: <title>

- Aligned outcomes:
- Prerequisite module IDs (`prerequisites[]`; empty for the first module):

| Lesson ID | Objective | Minutes | Formats | Source refs | Exercise type and instructions | Assessment type, evidence, and outcome IDs |
| --- | --- | ---: | --- | --- | --- | --- |

## Capstone (`capstone`)

- Required (`required`):
- Authentic task:
- Aligned outcome IDs:
- Rubric or acceptance criteria:
- Answer key or scoring anchors location:
- Remediation path:
- If not required, rationale:

## Production Plan (`production_plan[]`)

| Artifact ID | Artifact | Canonical unit ID | Owning skill | Status | Verification |
| --- | --- | --- | --- | --- | --- |

Use `planned`, `in-production`, `complete`, `blocked`, or `deferred` as the
status. Every lesson ID needs at least one production artifact. Use `course` or
`capstone` only for artifacts owned at those levels.

## Coverage and Risks

- Outcomes not yet taught (derived by validator):
- Outcomes not yet assessed (derived by validator):
- Source or factual gaps:
- Accessibility gaps:
- Unverified code or media:

Mirror these field names in the JSON manifest and run
`python3 scripts/validate_course_manifest.py <manifest.json>` before expanding
the course. The validator checks source references, prerequisite cycles,
teaching and assessment coverage, exercise completeness, production coverage,
and modality-specific accessibility provisions.
