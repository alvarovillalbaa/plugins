# Pre-Shipping Polish

External owner boundary:

- Use `hallmark` for visual polish, anti-slop checks, responsive design gates, typography, token discipline, motion, and component-state completeness.
- This file keeps only local release-polish sequencing.

## Local sequence

1. Confirm the feature is functionally complete.
2. Confirm the target routes, components, and viewport scope.
3. Invoke `hallmark audit` for visual findings or `hallmark redesign` for approved source edits.
4. Verify the changed surface with the repo's normal browser, accessibility, lint, typecheck, and test commands.
5. Report remaining visual or runtime risks explicitly.

Do not polish unrelated surfaces while touching the target.

## Non-visual checks

- no console errors in the target flow
- no debug logging added
- no dead imports or unused files from the polish pass
- route still loads with representative data
- keyboard navigation reaches the edited controls
- errors and empty states still have recovery paths
