# Course Design and Routing

Use this reference after the source has been inspected and before producing
more than one representative lesson.

## Backward design

1. Describe the learner's observable end-state.
2. Write outcomes with a verb and a checkable performance.
3. Define the evidence that would demonstrate each outcome.
4. Sequence prerequisites from foundational knowledge to independent work.
5. Choose lesson activities and media only after the evidence is clear.

Avoid outcomes such as "understand X." Prefer "diagnose X from a trace and
justify the selected fix" or "build X and pass the supplied acceptance tests."

## Course manifest model

Treat the manifest as the canonical source for every modality:

- `outcomes` define the contract.
- `modules[].aligned_outcomes` prove curriculum coverage.
- `lessons[].objective` describes the lesson-level performance.
- `lessons[].formats` selects production lanes without duplicating content.
- `assessment` records how mastery is checked.
- `source_refs` retain provenance for factual or quoted material.

Use stable, kebab-case IDs. Preserve IDs across revisions so links, progress,
and derived media stay traceable.

## Modality selection

| Learning need | Prefer | Avoid |
| --- | --- | --- |
| Explain a mental model | concise prose plus diagram | decorative video |
| Demonstrate a timed process | video or animation plus transcript | screenshots without sequence |
| Practice code or tools | runnable lab with tests | passive code walkthrough only |
| Compare alternatives | table, decision tree, worked cases | long undifferentiated lecture |
| Rehearse judgment | scenario, critique, reflection rubric | recall quiz as the only check |
| Memorize essential facts | spaced retrieval and short checks | a large capstone first |

Use multiple modalities only when each adds instructional value. Keep the
written lesson as the canonical semantic source, with derived scripts, slides,
and visuals linked back to its lesson ID.

## Assessment design

- Use checks during lessons for feedback, not punishment.
- Use an authentic task for the final assessment when the outcome is applied.
- Publish criteria before the learner attempts the work.
- Include answer keys or scoring anchors for deterministic review.
- Test prerequisite knowledge separately from the target capability.
- Do not claim a score is calibrated without human-reviewed examples.

## Production stages

1. **Blueprint:** manifest, source map, and coverage matrix.
2. **Prototype:** one complete representative lesson.
3. **Course build:** remaining learner and instructor materials.
4. **Media build:** selected slides, visuals, videos, and interactives.
5. **Verification:** links, code, accessibility, factual sources, and assessment
   alignment.

Pause between stages only when approval, source access, or a material product
choice is required. Otherwise keep progressing with explicit assumptions.

## Quality checklist

- Every outcome is assessed and taught.
- Every lesson has one primary objective.
- Module order respects prerequisites.
- Exercises require learner action.
- Examples resemble the target environment.
- Factual claims remain traceable to sources.
- Video and visuals have accessible alternatives.
- Code and interactive artifacts include reproducible verification.
- The production ledger identifies what is complete and what is not evaluated.
