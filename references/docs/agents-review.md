# Plugin Agents Review — 2026-08-03

## Result

- Reviewed all 7 department plugins and every active file under their `agents/` directories.
- 26 generalized agents now cover all 146 skills declared by plugin profiles.
- Every active agent is registered in its plugin profile and has explicit scope, primary-skill, and routing-boundary declarations.
- No agent embeds this repository's organization or maintainer identity, a personal email address, or an absolute user-home path.
- Exact duplicate skill portfolios are rejected. Agent pairs with substantial overlap must name each other in mutual routing boundaries.

## Portfolio decisions

### Consolidated redundant roles

- Removed `productivity/executive`. Organization-level decisions remain with `ceo`; operating cadence and follow-through remain with `vp-of-operations`.
- Removed `sales/sales-prospecting`. Pre-opportunity research, signal capture, qualification, and outbound execution now have one owner: `sdr`.

### Filled real orchestration gaps

- Added `productivity/reviewer` for independent code, design, content, documentation, and reasoning review. This fills review coverage without duplicating executive or operating ownership.
- Added `system/system-steward` for plugin-wide maintenance, knowledge flows, personalization policy, evaluation, and improvement. Narrow command-bound work still routes to `experiment-runner`, `memory-analyst`, or `skill-extractor`.

### Clarified adjacent lanes

- Engineering separates technical strategy (`cto`), cross-system delivery (`principal-engineer`), scoped implementation (`software-engineer`), AI systems (`ai-engineer`), cloud topology (`cloud-architect`), bounded PR review (`pr-reviewer`), and queue triage (`pr-triage`).
- Finance separates policy and capital decisions (`cfo`), accounting evidence and close mechanics (`accountant`), and models or market analysis (`financial-analyst`).
- Product separates product scope and validation (`product-manager`) from experience and visual design (`designer`).
- Sales separates strategy (`cso`), GTM systems (`gtm-engineer`), pre-opportunity execution (`sdr`), and qualified deal progression (`account-executive`).

## Coverage

| Plugin | Agents | Skills covered |
| --- | ---: | ---: |
| `engineering` | 7 | 45/45 |
| `finances` | 3 | 10/10 |
| `marketing` | 1 | 23/23 |
| `product` | 2 | 17/17 |
| `productivity` | 5 | 16/16 |
| `sales` | 4 | 18/18 |
| `system` | 4 | 17/17 |
| **Total** | **26** | **146/146** |

Marketing intentionally uses one broad `growth-lead` orchestrator because its local skills form one coherent narrative-to-distribution workflow. Role count is not increased merely to mirror individual skills.

## Verification contract

Run:

```bash
python3 scripts/audit_agents.py .
python3 scripts/skillctl.py conflicts check --root .
python3 -m unittest scripts.tests.test_audit_agents scripts.tests.test_skillctl
```

The first command proves current profile parity, same-plugin skill coverage, skill resolution, required scope and boundary declarations, duplicate and high-overlap handling, bounded size, and portability. The existing conflict checker independently validates names, references, tools, commands, manifests, and profile inventory.
