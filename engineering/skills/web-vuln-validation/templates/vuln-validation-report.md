# Vulnerability Validation Report — <Finding Title>

Single-finding validation record: confirms a suspected vulnerability is real,
reproducible, and scored. Roll multiple of these into a full pentest report.

- **Finding ID:** <WEB-XX>
- **Target:** <url / endpoint>
- **Validated by:** <tester>
- **Date:** <YYYY-MM-DD>
- **Authorization:** <scope reference>
- **Status:** Confirmed / Not exploitable / Needs more info

## Classification

| Field | Value |
| --- | --- |
| Vulnerability class | <IDOR / XSS / SQLi / SSRF / …> |
| CWE | <CWE-id> |
| OWASP | <category> |

## CVSS 3.1 Scoring

- **Vector:** `AV:_/AC:_/PR:_/UI:_/S:_/C:_/I:_/A:_`
- **Base score:** <0.0–10.0> (<severity>)
- **Justification:** Why each metric was chosen; environmental adjustments.

## Summary

One paragraph: what the vulnerability is and the realistic impact.

## Preconditions

- Authentication state required: <none / user / admin>
- Other requirements: <feature flag, specific role, timing>

## Reproduction

Exact, copy-pasteable steps. Include the raw request and response.

```http
GET /api/v2/orders/10231 HTTP/1.1
Host: api.example.com
Authorization: Bearer <token>
```

```http
HTTP/1.1 200 OK
Content-Type: application/json

{ ... evidence of impact ... }
```

## Proof of Impact

What the response proves (e.g., access to another user's data). Keep extraction
to the minimum needed to demonstrate the issue.

## Evidence

- `evidence/<id>-request.txt`
- `evidence/<id>-response.txt`
- `evidence/<id>-screenshot.png`

## False-Positive Analysis

Why this is a real issue and not scanner noise (e.g., confirmed cross-account,
not the tester's own data).

## Remediation

Specific fix and a verification test that should pass once fixed.
