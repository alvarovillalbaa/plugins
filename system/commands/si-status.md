---
name: si:status
description: Show memory health dashboard — line counts, capacity warnings, topic files, and top recommendations.
allowed-tools: [Read, Bash, Glob]
---

Generate a memory health dashboard.

## Steps

1. **Count MEMORY.md lines**:
   ```bash
   wc -l ~/.claude/projects/*/memory/MEMORY.md 2>/dev/null
   ```

2. **List topic files**:
   ```bash
   ls -lh ~/.claude/projects/*/memory/*.md 2>/dev/null | grep -v MEMORY.md
   ```

3. **Count CLAUDE.md lines**:
   ```bash
   wc -l CLAUDE.md ~/.claude/CLAUDE.md 2>/dev/null
   ```

4. **List rules files**:
   ```bash
   find .claude/rules -name "*.md" -exec wc -l {} \; 2>/dev/null
   ```

5. **Output dashboard**:

```
Memory Health Dashboard — YYYY-MM-DD

┌─────────────────────────────────────────────────────────┐
│  Auto-Memory                                            │
│  MEMORY.md:  [N] lines / 200 limit  [OK / WARNING]     │
│  Topic files: [N] files                                 │
├─────────────────────────────────────────────────────────┤
│  Enforced Rules                                         │
│  CLAUDE.md (project): [N] lines / 150 soft limit        │
│  CLAUDE.md (user):    [N] lines                         │
│  .claude/rules/:      [N] files                         │
└─────────────────────────────────────────────────────────┘

Status:
  [OK]      MEMORY.md has space for new learnings
  [WARNING] CLAUDE.md approaching soft limit — consider moving to rules/
  [CRITICAL] MEMORY.md over 200 lines — lines past 200 are NOT loaded

Recommendations:
  1. [action if any]
  2. [action if any]
  3. Run /si:review to find promotion candidates
```

**Thresholds:**
- MEMORY.md > 150 lines → WARNING
- MEMORY.md > 200 lines → CRITICAL
- CLAUDE.md > 150 lines → WARNING
