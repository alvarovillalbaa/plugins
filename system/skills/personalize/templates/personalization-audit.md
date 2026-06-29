---
type: personalization-audit
date: YYYY-MM-DD
plugin: [plugin name]
---

# Personalization Audit: [Plugin / Company Name]

Use this template to review the current state of personalization across all relevant skills. Run quarterly or after a major repositioning.

---

## Voice

**Current voice definition**:
- [ ] Reviewed `skills/voice/references/` — voice profile exists and is up to date
- [ ] Voice matches how the team actually communicates externally today
- [ ] Voice guidelines are reflected in content skill outputs

**Issues or drift**:
- [ ] None
- [ ] [Describe any gap]

**Action**:
- [ ] No change needed
- [ ] Update `skills/voice/` — route to `voice` skill

---

## ICP

**Current ICP definition**:
- [ ] Reviewed `skills/icp/references/` — ICP is defined
- [ ] ICP is based on won/lost deal data (not just intuition)
- [ ] ICP has been reviewed in the last 90 days

**Issues or drift**:
- [ ] None
- [ ] We're attracting deals outside our ICP
- [ ] ICP is based on intuition, not data
- [ ] ICP hasn't been updated in 90+ days

**Action**:
- [ ] No change needed
- [ ] Update ICP — route to `icp` skill

---

## Positioning

**Current positioning**:
- [ ] Reviewed `skills/positioning/references/` — positioning is defined by segment
- [ ] Positioning reflects current product capabilities (not roadmap features)
- [ ] Messaging is consistent across sales and marketing materials

**Issues or drift**:
- [ ] None
- [ ] [Describe any gap]

**Action**:
- [ ] No change needed
- [ ] Update positioning — route to `positioning` skill

---

## Communication Style

**Current agent communication style**:
- [ ] Agents are calibrated to the team's preferred response style
- [ ] No complaints about verbosity, tone, or formality from frequent users

**Issues or drift**:
- [ ] None
- [ ] Agents are too verbose
- [ ] Agents are too formal / informal
- [ ] [Describe any gap]

**Action**:
- [ ] No change needed
- [ ] Update style — route to `communication-style` skill

---

## Calibration

**Agent calibration status**:
- [ ] No open calibration issues
- [ ] Calibration log reviewed: `.calibration-log.json`

**Known calibration issues**:
- [ ] None
- [ ] [Skill]: [Issue]

**Action**:
- [ ] No change needed
- [ ] Address calibration — route to `calibration` skill

---

## Summary

| Area | Status | Action Needed |
|------|--------|---------------|
| Voice | [current/stale] | [yes/no] |
| ICP | [current/stale] | [yes/no] |
| Positioning | [current/stale] | [yes/no] |
| Comm style | [good/issues] | [yes/no] |
| Calibration | [clean/issues] | [yes/no] |

**Next review**: YYYY-MM-DD
