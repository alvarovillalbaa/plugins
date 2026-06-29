# Personalize — Routing Guide

Router for skill and agent personalization. Routes to the appropriate personalization skill.

## Child Skills

| Child | Owns |
|-------|------|
| `calibration` | Calibrating agent behavior from preferences and feedback |
| `voice` | Communication style and tone personalization |
| `icp` | Ideal customer profile definition |
| `communication-style` | Output format and communication preferences |

## Routing Decision Tree

```
Is this about adjusting how the agent responds (format, tone, style)?
  → voice or communication-style

Is this about adjusting which actions the agent takes autonomously?
  → calibration

Is this about defining who the ideal customer/user is?
  → icp

Is this about customizing a skill's behavior for a specific company or user?
  → calibration (for behavior), personalize overlay files (for content)
```

## Personalization Boundaries

**Allowed in overlays** (company/user-specific, stays local):
- Company name, product name, brand voice.
- Internal terminology and abbreviations.
- Specific customer names or deal details.
- API keys, endpoints, infrastructure details.

**Not allowed in overlays** (belongs upstream in skill):
- Corrections to factual errors in references.
- Bug fixes in scripts or hooks.
- Improvements to skill instructions that benefit all users.

## Personalization Files

Personalization is applied through local overlay files that are excluded from upstream contributions:

```
skill-name/
├── personalize.local.yml    # Primary local personalization
├── .company/                # Company-specific overlays
└── .user/                   # User-specific overlays
```

These files override skill defaults without modifying the upstream skill content.
