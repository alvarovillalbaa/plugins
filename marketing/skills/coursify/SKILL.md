---
name: coursify
description: >-
  Turn source material or an idea into a teachable course with learning
  outcomes, curriculum, lessons, exercises, and a production plan. Chains to
  slides, video, or image skills as needed.
---

# Coursify

Build the course as a learning system, not a pile of content. Establish the
instructional contract, design backward from demonstrated outcomes, then route
only the production lanes the chosen format needs.

## Workflow

1. Inspect the source and preserve a source map. Separate supplied facts from
   examples, interpretation, and material that still needs research.
2. Establish the audience, entry level, desired transformation, measurable
   outcomes, constraints, delivery format, duration, and accessibility needs.
   Infer only low-risk gaps and state the assumption; ask when a missing choice
   would materially change the course.
3. Draft a course manifest from
   [`templates/course-manifest.md`](templates/course-manifest.md). Align every
   module and assessment to at least one outcome.
4. Validate a JSON form of the manifest with
   `python3 scripts/validate_course_manifest.py <manifest.json>` before
   producing a large course.
5. Produce the smallest complete vertical slice first: one representative
   lesson, its exercise, its assessment, and its media. Use it to settle tone,
   depth, and production cost before expanding the remaining modules.
6. Build the remaining lessons, then verify source fidelity, outcome coverage,
   prerequisite order, assessment validity, accessibility, and runnable code.
7. Deliver the finished artifacts plus a production ledger that distinguishes
   complete, blocked, and intentionally deferred items.

Read [`references/course-design-and-routing.md`](references/course-design-and-routing.md)
for backward design, modality selection, assessment patterns, and quality
checks.

## Chain Rules

Chain to these internal skills when the approved manifest requires their
artifacts:

- `content`
- `slides`
- `images`
- `video`
- `visualization`
- `frontend`
- `code-documentation`
- `quality-assurance`

## Production Routing

Select the minimum chain that owns the requested artifacts:

| Need | Chain to |
| --- | --- |
| Learning design and teaching strategy | external `teach` |
| Lesson prose, scripts, and workbooks | `content`, `copywrite`, `humanizing` |
| Deck-led lessons | `slides` and, when installed, `frontend-slides` |
| Diagrams and still media | `images`, `visualization`, `visual-explainer` |
| Video lessons | `video`, then an installed external `hyperframes`, `remotion`, or `manim-video` skill |
| Interactive HTML lessons | `visualization`, `frontend` |
| Code labs and runnable examples | `code-documentation`, `frontend` or `backend`, then `quality-assurance` |

Do not invoke every media skill by default. Route from the approved course
manifest and keep one canonical source of lesson content so modalities do not
drift.

## Guardrails

- Do not invent expertise, citations, learner results, or source claims.
- Do not copy source material beyond its license or the user's authorization.
- Keep answer keys and hidden assessment material separate from learner-facing
  artifacts.
- Require confirmation before publishing, uploading, purchasing media, or
  sending learner communications.
- Include captions or transcripts for audio/video, text alternatives for
  meaningful visuals, keyboard access for interactive work, and non-color-only
  status cues.
- Mark code as unverified until it has actually run in the target environment.

## Output Contract

Return:

- the course manifest and source map
- the produced learner and instructor artifacts
- outcome-to-lesson-to-assessment coverage
- the media and production ledger
- validation evidence, assumptions, and unresolved blockers
