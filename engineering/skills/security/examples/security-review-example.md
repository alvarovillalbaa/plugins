# Worked Example: Security Review of an Authenticated REST API

Passive security review of a new `/api/v2/orders` feature PR. Demonstrates the
depth expected from this lane. No exploitation performed — findings are filed for
engineering. Fictional code.

## Context

- **PR:** #4821 "Add order detail + update endpoints"
- **Surface:** `GET /api/v2/orders/{id}`, `PATCH /api/v2/users/me`
- **Auth model:** Bearer JWT, role claim `user|admin`
- **Standard:** internal checklist (`templates/security-review-checklist.md`) + ASVS L2

## Findings

### SEC-01 — Missing object-level authorization (High)

**Where:** `orders/handler.go:42`

```go
func GetOrder(c *gin.Context) {
    id := c.Param("id")
    order := db.FindOrder(id)          // no ownership check
    c.JSON(200, order)
}
```

**Issue.** The handler authenticates (middleware) but never checks that the order
belongs to the caller. Any user can read any order (IDOR / BOLA).

**Impact.** Cross-customer PII disclosure.

**Fix.**
```go
order := db.FindOrder(id)
if order.CustomerID != auth.PrincipalID(c) {
    c.AbortWithStatus(http.StatusNotFound); return
}
```
Add a test asserting 404 when a user requests another user's order.

**Checklist item:** Authorization → object-level checks → **Fail**.

### SEC-02 — Mass assignment on profile update (High)

**Where:** `users/handler.go:88`

```go
var body map[string]any
c.BindJSON(&body)
db.UpdateUser(uid, body)   // binds arbitrary fields, including "role"
```

**Issue.** A client can send `{"role":"admin"}` and self-escalate.

**Fix.** Bind to an explicit struct with only updatable fields (`name`, `email`);
never accept `role` from the request body.

**Checklist item:** Authorization → mass assignment → **Fail**.

### SEC-03 — Verbose DB errors returned to client (Medium)

**Where:** `middleware/errors.go:20` returns `err.Error()` to the response,
leaking SQL fragments and table names. Return a generic message; log details
server-side.

### SEC-04 — Dependency with known CVE (Medium)

`pip-audit` flagged `requests==2.19.0` (CVE-2018-18074). Bump to a patched
version; lockfile updated.

## Items That Passed

- Parameterized queries throughout (no SQL injection vectors observed).
- Passwords hashed with argon2id.
- TLS enforced; HSTS present.

## Outcome

- **Reviewer:** A. Rivera  **Date:** 2026-06-11
- **Outcome:** Changes requested — SEC-01 and SEC-02 are blocking.
- **Filed:** SEC-01..04 in the tracker; SEC-01/02 linked to PR #4821.
