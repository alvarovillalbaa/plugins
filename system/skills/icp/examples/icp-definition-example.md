# ICP Definition Example: AI Agent Deployment Platform

**Date**: 2026-06-01  
**Source**: Won/lost deal analysis (Q1 2026, 47 deals)

---

## Firmographic ICP

| Dimension | ICP | Anti-ICP |
|-----------|-----|----------|
| Company size | 15–200 employees | <10 (budget) or >500 (procurement) |
| Stage | Series A–C | Seed (too early) or Public (compliance overhead) |
| Industry | SaaS, Fintech, DevTools | Non-software, public sector |
| Engineering team | 8–80 engineers | <5 (not enough scale) |
| Revenue | $2M–$50M ARR | <$500K (no budget) |

---

## Technographic ICP

**Required**:
- GitHub or GitLab (CI/CD integration)
- Slack (notification and approval flows)
- Linear or Jira (ticketing integration)

**Positive signal**:
- Already using 1+ AI coding tools (Copilot, Cursor, Cody)
- CI/CD pipeline with automated testing
- PR-based workflow (not trunk-based with no review)

**Disqualifying**:
- Air-gapped infrastructure (cannot connect to our service)
- No existing CI/CD pipeline
- 100% offshore development (timezone sync issues with async reviews)

---

## Behavioral / Trigger ICP

**Best-fit moments to reach out**:
1. Just hired 3+ engineers in 30 days (engineering velocity pressure)
2. Just raised a round (budget available, growth pressure)
3. Posted publicly about slow PR cycles or deployment bottlenecks
4. Job post for a "developer experience" role (already aware of the problem)
5. Using a competitor (active in-market buyer)

---

## Persona ICP

**Primary buyer**:
- Title: VP Engineering, Head of Engineering, CTO (< 100 engineers)
- Decision-making style: technical, data-driven, values benchmarks
- Biggest pain: time spent on process work vs. building product
- Preferred channel: LinkedIn, X, product-led discovery

**Economic buyer** (deals > $50K/year):
- Title: CTO, COO, CEO
- Brought in for: security review, contract sign-off
- Questions: "What's the ROI?", "Is it SOC 2?"

**Champion** (who drives internal adoption):
- Title: Senior Engineer, Tech Lead, Engineering Manager
- Motivation: personally frustrated with slow review cycles
- Channel: word of mouth, community, GitHub discovery

---

## Disqualification Criteria (Auto-DQ)

Disqualify if:
- [ ] No engineering team (product is non-technical)
- [ ] Air-gapped infrastructure (cannot integrate)
- [ ] Active procurement freeze or budget freeze
- [ ] Explicitly using a direct competitor with a multi-year contract

---

## ICP Confidence Score

| Account | ICP match | Confidence | Notes |
|---------|-----------|------------|-------|
| Acme Corp | 90% | High | Series B, 45 engineers, GitHub + Slack |
| Beta Inc | 60% | Medium | Right size, but uses SVN |
| Gamma LLC | 30% | Low | 5 engineers, no CI |

---

*Updated quarterly from won/lost analysis. Next review: 2026-09-01*
