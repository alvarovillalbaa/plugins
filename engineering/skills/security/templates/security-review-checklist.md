# Security Code Review Checklist

Use during PR review or a focused passive security pass. Mark each item
Pass / Fail / N/A and link evidence (file:line). This lane is review-only —
findings go to engineering; active exploitation belongs in `pentest`.

## Authentication & Session

- [ ] Auth required on every non-public route (deny by default)
- [ ] Session tokens rotated on privilege change; logout invalidates server-side
- [ ] Passwords hashed with a slow KDF (argon2/bcrypt/scrypt), never plaintext/MD5
- [ ] MFA paths cannot be bypassed; no auth secrets logged

## Authorization

- [ ] Object-level checks: caller owns / is permitted the requested resource (no IDOR)
- [ ] Function-level checks: privileged actions verify role server-side
- [ ] No `role`/`is_admin`-style fields settable from client input (mass assignment)

## Input Handling & Injection

- [ ] SQL/NoSQL uses parameterized queries / prepared statements
- [ ] OS command execution avoids shell concatenation; args passed as a list
- [ ] Output encoded for context (HTML/JS/URL) — no raw user data into the DOM
- [ ] Path/file inputs canonicalized and confined (no traversal)
- [ ] SSRF: outbound URLs validated against an allow-list; metadata endpoints blocked

## Secrets & Configuration

- [ ] No hardcoded secrets/keys/tokens in source or history (gitleaks clean)
- [ ] Secrets sourced from a manager/env, not committed config
- [ ] Debug/verbose errors and stack traces disabled in production responses

## Data Protection

- [ ] PII/sensitive data encrypted at rest and in transit (TLS enforced)
- [ ] Logs do not contain secrets, tokens, full PANs, or full PII
- [ ] Least-privilege DB/service accounts

## Dependencies & Supply Chain

- [ ] No known-vulnerable dependencies (npm audit / pip-audit / osv-scanner clean)
- [ ] Lockfile committed; integrity/hashes verified
- [ ] No suspicious or unmaintained packages added

## Transport & Headers

- [ ] HTTPS enforced; HSTS set
- [ ] Security headers present (CSP, X-Content-Type-Options, frame-ancestors)
- [ ] CORS not wildcard with credentials

## Error & Failure Handling

- [ ] Failures are explicit; no security checks swallowed by broad catch blocks
- [ ] Fails closed (deny) on auth/permission errors, not open

## Sign-off

- **Reviewer:** <name>  **Date:** <YYYY-MM-DD>
- **Outcome:** Approved / Changes requested / Blocked
- **Open findings filed:** <links>
