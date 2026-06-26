# UI Constraints

External owner boundary:

- Use `hallmark` for design-system tokens, visual taste, responsive gates, animation taste, component state coverage, and anti-slop decisions.

Keep these local stack constraints:

- Use the project's existing component primitives first.
- Use accessible primitives for keyboard or focus-heavy UI.
- Do not mix primitive systems inside one interaction surface.
- Use the repo's `cn`/class merge helper when one exists.
- Add accessible labels to icon-only controls.
- Do not rebuild keyboard/focus behavior by hand unless explicitly requested.
- Do not block paste in inputs or textareas.
- Animate only compositor properties when animation is required.
- Respect `prefers-reduced-motion`.
- Prefer CSS Grid for multi-column layouts.
- Keep fixed overlays from covering content or safe areas.
- Prefer render logic over `useEffect` when no external synchronization is needed.

For colors, typography, macrostructure, themes, glass, shadows, and polish, chain to `hallmark`.
