# UI Anti-Slop

External owner boundary:

- Use `hallmark` for anti-AI-slop design rules, generic UI pattern detection, theme selection, macrostructure, typography, palette, motion, and responsive gates.

Local use:

- When reviewing a UI, invoke `hallmark audit`.
- When fixing UI slop, invoke `hallmark redesign` after confirming scope.
- Keep only repo-specific constraints locally, such as installed component primitives, existing tokens, or product copy that must not change.

Do not copy Hallmark's forbidden-pattern lists into this file.
