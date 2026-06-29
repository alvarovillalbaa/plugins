# Threat Model — <System / Feature>

- **System:** <name>
- **Author(s):** <name>
- **Date:** <YYYY-MM-DD>
- **Status:** Draft / Reviewed
- **Reviewers:** <names>

## 1. Scope and Assets

What is being modeled and what is worth protecting.

| Asset | Why it matters | Sensitivity |
| --- | --- | --- |
| Customer PII | Regulatory + reputational | High |
| Session tokens | Account takeover | High |
| Billing data | Financial | High |

## 2. Architecture Overview

Brief description plus a data-flow sketch. Identify trust boundaries (where data
crosses from less-trusted to more-trusted zones).

```
[Browser] --TLS--> [API Gateway] --> [Service] --> [DB]
                         |  trust boundary  |
```

- **Entry points:** <public endpoints, webhooks, admin UI>
- **Trust boundaries:** <internet↔gateway, service↔db, tenant↔tenant>
- **External dependencies:** <payment processor, auth provider>

## 3. Threats (STRIDE)

For each component / data flow, enumerate threats.

| ID | Component | STRIDE | Threat | Existing control | Risk |
| --- | --- | --- | --- | --- | --- |
| T1 | Order API | Information disclosure | IDOR exposes other tenants' orders | None | High |
| T2 | Login | Spoofing | Credential stuffing | Rate limit | Medium |
| T3 | Session | Tampering | Token forgery | Signed JWT | Low |

STRIDE = Spoofing, Tampering, Repudiation, Information disclosure,
Denial of service, Elevation of privilege.

## 4. Mitigations and Actions

| Threat | Mitigation | Owner | Status |
| --- | --- | --- | --- |
| T1 | Object-level authorization + tests | API team | Planned |
| T2 | Account lockout + bot detection | Platform | Done |

## 5. Residual Risk

Risks knowingly accepted, by whom, and why. Re-evaluation date.

## 6. Assumptions

Security assumptions this model relies on (e.g., "TLS terminates at the gateway",
"the database network is private").
