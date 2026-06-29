# Worked Example: Validating an IDOR in a REST API

Shows how to take a *suspected* issue from a scanner/observation and validate it
into a confirmed, scored finding. Fictional target.

- **Finding ID:** WEB-01
- **Target:** `https://api.example.com/api/v2/orders/{id}`
- **Validated by:** A. Rivera
- **Date:** 2026-06-10
- **Authorization:** `SCOPE.md` (api.example.com in scope)
- **Status:** Confirmed

## Classification

| Field | Value |
| --- | --- |
| Vulnerability class | IDOR (Broken Object Level Authorization) |
| CWE | CWE-639 |
| OWASP | API1:2023 BOLA |

## CVSS 3.1 Scoring

- **Vector:** `AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:N`
- **Base score:** 6.5 (Medium)
- **Justification:** Network-exploitable, low complexity, requires a low-priv
  authenticated account, no user interaction. High confidentiality impact
  (customer PII), no integrity/availability impact. Reported as High to the
  client given regulated data (environmental).

## Summary

The order-detail endpoint authenticates the caller but does not verify that the
requested order belongs to them. Any logged-in user can read any order by ID.

## Preconditions

- Authentication state required: any standard user account.
- Other requirements: none — IDs are sequential integers.

## Reproduction

1. Authenticate as `tester-a`; capture the bearer token.
2. Note `tester-a`'s own order is `10180`.
3. Request a nearby ID belonging to another account:

```http
GET /api/v2/orders/10231 HTTP/1.1
Host: api.example.com
Authorization: Bearer eyJhbGciOi...<tester-a>
```

```http
HTTP/1.1 200 OK
Content-Type: application/json

{"order_id":10231,"customer_id":884,"email":"victim@example.com",
 "ship_to":"42 Pine St","total":"$420.00","items":[...]}
```

`customer_id` 884 is `tester-b`, not `tester-a` (id 791).

## Proof of Impact

Returned record belongs to a different customer and includes name, email, and
shipping address. Confirmed reproducible for IDs 10231 and 10232. Stopped at two
records per rules of engagement (no bulk extraction).

## Evidence

- `evidence/web-01-request.txt`
- `evidence/web-01-response.txt`

## False-Positive Analysis

Not a self-access false positive: the authenticated principal (id 791) differs
from the returned `customer_id` (884). The endpoint applied no ownership check —
a 403 would be expected for a correctly authorized API.

## Remediation

Enforce object-level authorization: `WHERE order.customer_id = :authenticated_id`.
Add a regression test asserting a 403/404 when a user requests an order they do
not own. Audit sibling endpoints (`/api/v2/invoices/{id}`, `/shipments/{id}`)
for the same pattern.
