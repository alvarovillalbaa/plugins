# REST API Design Example: Task Management Service

A worked example of a well-designed REST API. Shows resource modeling, consistent
conventions, auth, pagination, and error handling — the bar a new API should meet.

## Resources

```
/v1/tasks
/v1/tasks/{taskId}
/v1/tasks/{taskId}/comments
/v1/projects
/v1/projects/{projectId}/tasks
```

Plural nouns, no verbs in paths, hierarchy reflects ownership. Versioned with
`/v1` so breaking changes can ship under `/v2` without disrupting clients.

## Endpoints

| Method | Path | Purpose | Success |
| --- | --- | --- | --- |
| GET | `/v1/tasks` | List tasks (filter, paginate) | 200 |
| POST | `/v1/tasks` | Create a task | 201 + `Location` |
| GET | `/v1/tasks/{id}` | Fetch one task | 200 / 404 |
| PATCH | `/v1/tasks/{id}` | Partial update | 200 |
| DELETE | `/v1/tasks/{id}` | Delete a task | 204 |

`PATCH` for partial updates; `PUT` is reserved for full replacement. `DELETE`
returns 204 with no body. `POST` returns 201 with the created resource and a
`Location` header.

## Request / response shape

```jsonc
// POST /v1/tasks
{
  "title": "Write API design doc",
  "projectId": "proj_9f3",
  "dueDate": "2026-07-15",
  "priority": "high"        // enum: low | medium | high
}
```

```jsonc
// 201 Created
{
  "id": "task_1a2b",
  "title": "Write API design doc",
  "projectId": "proj_9f3",
  "status": "open",         // enum: open | in_progress | done
  "priority": "high",
  "dueDate": "2026-07-15",
  "createdAt": "2026-06-29T10:00:00Z",
  "updatedAt": "2026-06-29T10:00:00Z"
}
```

- `camelCase` field names, consistent everywhere.
- Timestamps are ISO 8601 UTC, named `createdAt` / `updatedAt`.
- Enumerated fields documented inline; servers reject unknown values.
- IDs are opaque, prefixed strings (`task_…`) — not sequential integers.

## Filtering, sorting, pagination

```
GET /v1/tasks?status=open&priority=high&sort=-dueDate&limit=25&cursor=eyJpZCI6...
```

```jsonc
{
  "data": [ /* ...tasks... */ ],
  "pagination": {
    "nextCursor": "eyJpZCI6...",   // null when no more pages
    "limit": 25
  }
}
```

Cursor-based pagination (stable under inserts), `limit` capped server-side
(e.g. max 100), `sort` with `-` prefix for descending.

## Authentication & authorization

- `Authorization: Bearer <token>` on every request; 401 if missing/invalid.
- Object-level authorization enforced server-side: a task is only visible to
  members of its project. Non-owned ids return 404, not 403, to avoid leaking
  existence.

## Errors

Consistent problem-detail body (RFC 9457 style):

```jsonc
// 422 Unprocessable Entity
{
  "type": "https://errors.acme.dev/validation",
  "title": "Validation failed",
  "status": 422,
  "detail": "priority must be one of: low, medium, high",
  "errors": [
    { "field": "priority", "message": "invalid enum value" }
  ]
}
```

| Status | When |
| --- | --- |
| 400 | Malformed request (bad JSON) |
| 401 | Missing/invalid auth |
| 403 | Authenticated but not permitted |
| 404 | Resource not found (or not owned) |
| 409 | Conflict (duplicate, version mismatch) |
| 422 | Validation failed |
| 429 | Rate limited (`Retry-After` header) |

## Why this is "good"

- Contract-first: every shape above lives in `openapi.yaml` and is linted with
  `scripts/api_linter.py`.
- Predictable: same naming, pagination, and error shape across all resources.
- Safe defaults: bounded page sizes, opaque ids, ownership checks, no verbose errors.
- Evolvable: versioned path + additive changes; breaking changes go to `/v2`.
