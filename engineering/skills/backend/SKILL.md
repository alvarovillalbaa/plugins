---
name: backend
description: >-
  Router for backend API/service design and database/persistence work.
---

# Backend Router

This parent is a router. Select the narrowest child and load that child before using lane-specific assets.

## Children

- [`api-service-design`](../api-service-design/SKILL.md) - API contracts, service boundaries, serializers, request/response shape, jobs, queues, and backend application design
- [`database-persistence`](../database-persistence/SKILL.md) - database schemas, migrations, persistence models, indexing, transactions, normalization, and data-integrity constraints

## Route

| User asks for | Use |
| --- | --- |
| API contracts, service boundaries, serializers, request/response shape, jobs, queues, and backend application design | [`api-service-design`](../api-service-design/SKILL.md) |
| database schemas, migrations, persistence models, indexing, transactions, normalization, and data-integrity constraints | [`database-persistence`](../database-persistence/SKILL.md) |

## Chain Rules

- `quality-assurance/backend-test-engineering`
- `quality-assurance/passive-security-review`
- `cloud-management`
- `ai-engineering`

## Operating Rules

- Keep this `SKILL.md` small and routing-focused.
- Do not recreate the old broad parent behavior here; put execution depth in child assets.
- If no child matches, handle only shared methodology/default workflow or document the missing lane.
- Every child and parent skill must keep `examples/`, `hooks/`, `references/`, `scripts/`, and `templates/`.

## Shared Map

See [`../../../skills-chaining-map.md`](../../../skills-chaining-map.md) for the complete skills-chaining graph.
