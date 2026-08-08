---
name: browser-trace
description: Capture browser observability for one URL and return searchable network, DOM, screenshot, and console evidence.
argument-hint: "<URL> [output dir]"
allowed-tools: [Bash, Read, Write, AskUserQuestion, Skill]
---

Use skill: **frontend-e2e** — `skills/frontend-e2e/SKILL.md`.

Capture browser observability with `skills/frontend-e2e/scripts/browser_trace.py`, then interpret the artifacts. This command owns trace collection; use `repo-review` for a repository-wide review and `review-pr` for a change review.

## Steps

1. **Confirm the target** — If no URL was provided, ask for it. If no output directory was specified, default to `/tmp/browser-trace-<timestamp>`.

2. **Run the trace:**
   ```bash
   python "${CLAUDE_PLUGIN_ROOT}/skills/frontend-e2e/scripts/browser_trace.py" \
     --url <URL> \
     --output <output-dir> \
     [--wait "<selector>"] \
     [--playwright-trace]
   ```
   Add `--wait "<selector>"` if the page is a SPA that loads content asynchronously. Add `--playwright-trace` if a visual trace viewer is needed.

3. **Read the summary:**
   ```bash
   cat <output-dir>/summary.json
   ```

4. **Search the artifacts** — always run at minimum:
   ```bash
   # API surface
   grep '"/api/' <output-dir>/network/requests.jsonl | head -30

   # Error responses
   grep -E '"status": [45][0-9][0-9]' <output-dir>/network/responses.jsonl

   # Console errors and JS exceptions
   cat <output-dir>/console/errors.log

   # Failed network requests
   cat <output-dir>/network/failed.jsonl 2>/dev/null || echo "(none)"
   ```

5. **Report findings** — summarize:
   - Total requests, responses, errors, and snapshots
   - API endpoints discovered (unique `/api/...` paths)
   - Any HTTP 4xx/5xx responses with URLs
   - Console errors and page errors
   - Notable DOM patterns (forms, error states, data-testid attributes)
   - Screenshot paths for visual review

6. **Next step suggestion** — based on findings, suggest whether to:
   - Run the full live web app QA workflow (`quality-assurance` → Live web app QA)
   - Use `BrowserTrace.attach()` inline in an E2E test for flaky test diagnosis
   - Diff this trace against another run to find regression
   - Use the API endpoints discovered to scaffold contract tests
