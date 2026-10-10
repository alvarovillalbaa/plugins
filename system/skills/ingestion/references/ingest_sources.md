# Ingest Sources Playbook

Last updated: 2026-10-10

Use this reference for source-specific extraction. Read the parent
[`brain contract`](../../brain/references/brain_contract.md) and applicable
`AGENTS.md` before writes. Durable raw material lives in private Drive;
`SOURCES.md` records stable artifact URLs, original/member paths, bytes,
SHA256, fetched date, source type, and unprocessed/processed/blocked status.

## General contract

1. Select the requested workspace and ownership-appropriate connected Drive account.
2. Create an invocation-owned temporary extraction directory outside the repo:
   ```sh
   capture_dir=$(mktemp -d "${TMPDIR:-/tmp}/afs-ingest.XXXXXX")
   ```
3. Preserve originals unchanged. Tool examples below write derived captures into
   `$capture_dir`; this staging directory is not a canonical source store.
4. Upload originals and relevant captures through the authorized Drive connector.
   Verify remote download size and SHA256 before removing an explicitly migrated
   local original. Missing access is a blocker, not a local raw-folder fallback.
5. Record provenance and reading status in `SOURCES.md`. Capture metadata may use
   `source`, `url`, `fetched`, `status`, and `blocked_reason`. Never commit
   temporary paths, signed download URLs, credentials, or private source content.
6. Compile readable evidence into existing maintained owners. Knowledge requires
   unique generalized synthesis; copied summaries remain source or library material.
7. Mark catalog entries processed only after successful owner writes; retain
   originals in Drive. Remove only owned temporary captures after preservation.

Metadata-only sources, previews, login walls, paywalls, missing media, and
unsupported binaries remain blocked. Extraction tooling does not grant access
or authority to bypass a site's protections.

---

## Twitter / X

Preferred CLI: `xurl`

`xurl` is a command-line interface for fetching X (Twitter) content via the X API v2. Install or verify with `which xurl`.

If `xurl` is unavailable and no equivalent authenticated export is available, mark the item blocked. Do not scrape X pages blindly.

### Fetch commands

```sh
# Fetch a single tweet by ID
xurl tweet <tweet-id>

# Fetch a full conversation thread
xurl thread <tweet-id>

# Fetch recent tweets from a user
xurl profile <username> --limit 20

# Search recent tweets
xurl search "<query>" --limit 50

# Search with quality filter (high engagement only)
xurl search "<query>" --min-likes 10 --sort likes
```

### Research loop (adapted from x-research-skill)

When doing a multi-angle research pass rather than a single fetch:

1. **Decompose** — break the topic into 3–5 distinct sub-queries.
2. **Search** — run each sub-query with `xurl search "<q>" --limit 50 --min-likes 5`.
3. **Follow threads** — for high-engagement tweets, fetch the full thread with `xurl thread <id>`.
4. **Deep-dive linked content** — for tweets with URLs, fetch those URLs using the web or PDF ingestion pattern below.
5. **Synthesize** — compile results into one themed markdown research document.
6. **Save** — preserve fetched source captures in Drive and place the synthesis in the relevant research unit (slug: `x-research_<slug>`).

### Noise reduction

- Append `-is:retweet` to all search queries unless retweets are explicitly wanted.
- Append `-is:reply` in quick-scan mode.
- Filter out crypto/spam topics by adding negation operators: `-bitcoin -nft -giveaway`.
- Use `--min-likes 10` as the default quality threshold; lower to 3 for niche topics.

### Watchlist pattern

For recurring monitoring, record monitored accounts in `SOURCES.md`; derive a temporary `$capture_dir/watchlist.json` for a bounded capture:

```json
{
  "accounts": [
    { "username": "example", "note": "Why we follow", "addedAt": "YYYY-MM-DD" }
  ]
}
```

Poll watchlist on a schedule:

```sh
jq -r '.accounts[].username' "$capture_dir/watchlist.json" |
while IFS= read -r account; do
  xurl profile "$account" --limit 10
done
```

### Output format

Save each Twitter ingest to `$capture_dir/` as markdown:

```md
---
source: twitter
url: https://x.com/username/status/ID
fetched: YYYY-MM-DD
status: unprocessed
---

**@username** · YYYY-MM-DD · ❤️ N · 👁 N

Tweet text here.

[Tweet URL](https://x.com/username/status/ID)

---
[Thread or linked tweets below if applicable]
```

---

## LinkedIn

LinkedIn does not offer a public API for post or profile scraping. Use one of these approaches depending on access:

### Personal data export (recommended)

Download your own LinkedIn data from `Settings → Data Privacy → Get a copy of your data`. Unzip and find `posts.csv`, `messages.csv`, `connections.csv`, and `profile.json`. Place the relevant files in `$capture_dir/` for compilation.

### URL page capture

For any public LinkedIn post or profile URL, use `defuddle` or `curl` to capture the readable text:

```sh
defuddle parse "https://www.linkedin.com/posts/username_slug" --md \
  -o "$capture_dir"/linkedin_slug.md
```

If `defuddle` cannot render the page (login wall), use `agent-browser` with an authenticated session:

```sh
agent-browser open "https://www.linkedin.com/posts/username_slug"
agent-browser get text "article"
```

Save the extracted text to `$capture_dir/` with the standard frontmatter and `source: linkedin`.

### Notes

- Respect LinkedIn's terms of service. Use these tools for your own content or for public research purposes only.
- LinkedIn profile pages often require login; prefer the data export for personal content.
- If only a preview card, profile shell, or login wall is readable, keep the item blocked.

---

## Web URLs

Preferred tool: `defuddle`

`defuddle` extracts the main article body from a web page and outputs clean markdown.

```sh
# Basic URL capture
defuddle parse "https://example.com/article" --md \
  -o "$capture_dir"/web_slug.md

# Multiple URLs from a list file
while IFS= read -r url; do
  slug=$(echo "$url" | sed 's|https\?://||;s|/|-|g' | cut -c1-60)
  defuddle parse "$url" --md -o "$capture_dir/$(date +%F)_web_${slug}.md"
done < "$capture_dir/pending-urls.txt"
```

Fallback when `defuddle` is unavailable:

```sh
curl -s "https://example.com/article" | pandoc -f html -t markdown \
  -o "$capture_dir"/web_slug.md
```

For dynamic or authenticated pages use `agent-browser`:

```sh
agent-browser open "https://example.com/dashboard"
agent-browser get text "main"
```

### Hard-to-scrape websites (Firecrawl)

For JavaScript-heavy, bot-protected, or dynamically rendered sites where `defuddle` and `agent-browser` fail, escalate to Firecrawl:

```sh
# Single page — prefer this first
firecrawl scrape "https://example.com/article" --only-main-content \
  -o "$capture_dir"/web_slug.md

# Discover and scrape top results in one pass
firecrawl search "query terms" --scrape \
  -o "$capture_dir"/web_query.json --json

# Map a known site to find the right subpage, then scrape
firecrawl map "https://docs.example.com" --search "topic" \
  -o "$capture_dir/site-map.txt"
firecrawl scrape "https://docs.example.com/found-page" --only-main-content \
  -o "$capture_dir"/web_slug.md

# Crawl a bounded site section (use sparingly — check credits first)
firecrawl crawl "https://docs.example.com" \
  --include-paths /docs --limit 50 --wait \
  -o "$capture_dir"/crawl_slug.json
```

Escalation order: `scrape` → `search --scrape` → `map + scrape` → `crawl bounded section` → `interact`.

If the Firecrawl plugin is installed, use its skills (`firecrawl-scrape`, `firecrawl-search`, `firecrawl-crawl`) instead of the CLI directly. See the `web-research-collection` overlay in `productivity/skills/research/references/` for the full escalation pattern, output hygiene, and lane plays.

If a page only yields metadata, cookie banners, paywall text, or navigation chrome, keep it blocked until readable source text exists.

### Bookmarks batch ingestion

If you export browser bookmarks (e.g., Netscape HTML format), convert them:

```sh
# Extract all URLs from a bookmarks HTML file
grep -oP 'HREF="\K[^"]+' bookmarks.html > "$capture_dir/pending-urls.txt"
```

Then run the URL capture loop above.

---

## YouTube Videos

Preferred tool: `yt-dlp`

Install: `pip install yt-dlp` or `brew install yt-dlp`

### Transcript extraction (preferred — no download needed)

```sh
# Fetch auto-generated subtitles as SRT
yt-dlp --skip-download --write-auto-sub --sub-lang en \
  --sub-format srt -o "$capture_dir/%(upload_date)s_youtube_%(title)s" \
  "https://www.youtube.com/watch?v=VIDEO_ID"

# Convert SRT to plain text (strip timestamps)
sed '/^[0-9]/d;/^$/d;s/<[^>]*>//g' "$capture_dir"/*.srt > "$capture_dir"/youtube_slug.txt
```

### Metadata only

```sh
yt-dlp --dump-json --no-download "https://www.youtube.com/watch?v=VIDEO_ID" \
  | jq '{title, uploader, upload_date, description, duration, view_count, like_count}' \
  > "$capture_dir"/youtube_meta_slug.json
```

### Playlist ingestion

```sh
yt-dlp --skip-download --write-auto-sub --sub-lang en \
  --sub-format srt --yes-playlist \
  -o "$capture_dir/%(upload_date)s_%(title)s" \
  "https://www.youtube.com/playlist?list=PLAYLIST_ID"
```

### Output format

After extraction, prepend the standard frontmatter to the transcript file:

```md
---
source: youtube
url: https://www.youtube.com/watch?v=VIDEO_ID
title: Video Title
channel: Channel Name
published: YYYY-MM-DD
fetched: YYYY-MM-DD
duration_min: N
status: unprocessed
---

[Transcript follows]
```

During compilation, treat each logical section of the transcript (typically every 3–5 minutes of spoken content) as a separate extractable segment.

Metadata-only video entries are not enough for canonical claims. Keep them blocked unless the description itself is the source being compiled.

---

## Research Papers and PDFs

Preferred tools: `pdftotext` (poppler), `mutool` (mupdf), or Python `pdfplumber`

### Text extraction

```sh
# Single PDF — plain text
pdftotext input.pdf "$capture_dir"/paper_slug.txt

# Single PDF — preserve layout (useful for tables)
pdftotext -layout input.pdf "$capture_dir"/paper_slug.txt

# Using mutool (mupdf)
mutool draw -F txt input.pdf > "$capture_dir"/paper_slug.txt
```

Python fallback using `pdfplumber`:

```python
import pdfplumber, sys, pathlib
pdf = pathlib.Path(sys.argv[1])
out = pathlib.Path(sys.argv[2]) / f"{pdf.stem}.txt"  # temporary extraction directory
with pdfplumber.open(pdf) as p:
    out.write_text("\n\n".join(page.extract_text() or "" for page in p.pages))
```

### Metadata extraction

```sh
pdfinfo input.pdf  # title, author, subject, keywords, pages, date
```

### Output format

```md
---
source: pdf
original_file: filename.pdf
title: Paper Title
authors: Author 1, Author 2
published: YYYY-MM-DD
doi: 10.xxxx/yyyy
fetched: YYYY-MM-DD
pages: N
status: unprocessed
---

[Extracted text follows]
```

### Compilation notes for papers

When absorbing a research paper into the knowledge base:

- Extract: abstract, problem statement, key claims, methods, results, limitations, and citations.
- Preserve the paper and extracted text in Drive; catalog it in `SOURCES.md`. Put its evidence and interpretation in the relevant research unit. Update knowledge only when a unique generalized synthesis follows from the evidence.
- Link cited papers that already exist as canonical pages.
- Note whether the paper's claims confirm, extend, or contradict existing canonical knowledge.
- If the PDF is scanned, encrypted, or image-only and OCR is unavailable, mark it blocked with the exact extraction blocker.

---

## Images and Figures

When raw material includes images, screenshots, charts, or figures that carry semantic content:

1. Stage images alongside the corresponding capture in `$capture_dir/assets/`, then preserve the bundle in Drive.
2. Reference them in the markdown file using a relative path: `![Alt text](assets/filename.png)`.
3. During compilation, the assistant should inspect the image and extract key information (labels, data, layout) into the canonical page text so the knowledge is not image-locked.

For screenshots of text (e.g., Twitter screenshots, PDF screenshots):

```sh
# macOS OCR via Shortcuts or tesseract
tesseract screenshot.png "$capture_dir"/ocr_slug -l eng
```

---

## Plain Markdown and Text Files

For `.md`, `.txt`, and `.rst` files already in `$capture_dir/`:

- These are the simplest case — no extraction step needed.
- Ensure the standard frontmatter block is present; add it if missing.
- Proceed directly to the compile pass against `AGENTS.md`.

For bulk file imports:

```sh
# Add frontmatter to all .md files in $capture_dir/ that are missing it
for f in "$capture_dir"/*.md; do
  head -1 "$f" | grep -q "^---" && continue
  tmp=$(mktemp)
  printf -- "---\nsource: import\nfetched: $(date +%F)\nstatus: unprocessed\n---\n\n" | cat - "$f" > "$tmp"
  mv "$tmp" "$f"
done
```

---

## Other Local Data

For local source files not covered above:

- `.html` / `.htm`: parse through `defuddle`, `pandoc`, or readable text extraction.
- `.json`: parse relevant fields into markdown; preserve the original raw file.
- `.csv` / `.tsv`: convert rows into a compact markdown table or grouped bullet list before absorb.
- `.srt` / `.vtt`: strip timestamps and speaker artifacts before absorb.
- archives such as `.zip`: inventory contents first; extract only readable files needed for the current compile pass.
- office files such as `.docx` or `.pptx`: use a document-aware extractor when available; otherwise mark blocked.
- audio/video without transcript: use a transcript pipeline when available; otherwise mark blocked.
- unknown binary files: mark blocked rather than guessing.

---

## Raw and Memory Compilation Agent Loop

For a scoped Drive source queue:

1. Select the explicit workspace and read root/scoped AGENTS.md and SOURCES.md.
2. Inspect the authorized Drive artifacts; local inventory is not remote proof.
3. Fetch only scoped originals into temporary staging and verify catalog hashes.
4. Extract with the matching tool; preserve derived captures in Drive when useful.
5. Keep inaccessible or metadata-only entries blocked with exact reasons.
6. Read indexes and existing maintained owners before compiling readable evidence.
7. Route unique synthesis, facts, decisions, procedures, and research to their owners.
8. Refresh navigation and brief logs; link longer evidence from results or audits.
9. Update catalog status after successful writes and retain the original artifact.
10. Report processed/blocked entries, owners changed, contradictions, and open threads.

### Type detection heuristics

| Extension / source field | Action |
|---|---|
| `.md`, `.txt`, `.rst` | Direct absorb |
| `.pdf` | `pdftotext` → absorb |
| `.srt`, `.vtt` | Strip timestamps → absorb |
| `.json` | Parse fields → absorb |
| `.csv` | Convert rows → absorb |
| `.html`, `.htm` | Extract readable body → absorb |
| `.png`, `.jpg`, `.gif` | OCR or vision inspect → absorb |
| `.zip` | Inventory, extract readable members only |
| `.docx`, `.pptx` | Document-aware extraction or blocked |
| unknown binary | Block with reason |
| `source: twitter` | Treat as tweet corpus |
| `source: youtube` | Treat as transcript |
| `source: linkedin` | Treat as professional content |
| `source: pdf` | Already extracted text |
| `source: web` | Article body text |
| Memory dirs | Treat as experience evidence, then compile durable learnings |

---

## Ingestion Priority Rules

When the cataloged Drive queue is large, prioritize in this order:

1. Items flagged with `priority: high` in frontmatter.
2. Items with the most recent `fetched` date.
3. Items from primary sources (papers, official docs) before secondary (social media commentary).
4. Items directly linked from existing canonical pages (they extend something already known).
5. Items on watchlist accounts or monitored topics.

---

## Brain-Specific Structures

These structures appear in second-brain repos and require special handling outside the cataloged Drive source queue.

### `facts/` folder

The fact surfaces hold durable ambient context, split by fact type. Ask `use-afs` for the types and their paths.

- No extraction step is needed — these are already markdown.
- Ensure the standard frontmatter block is present before compiling; add it if missing with `source: facts`.
- They are living (non-timestamped) files; prefer updating existing fact pages rather than creating duplicates.
- Compile them into `knowledge/` on request or when their content is stale relative to the canonical page.

### `lib/` folder

`lib/` is the library for AI-generated content: drafts, synthesized summaries, and reusable artifacts produced during brain runs.

- Do not treat `lib/` as a source of truth or ingest it as raw evidence.
- During compilation, generated summaries and drafts go to `lib/` before promotion to `knowledge/`.
- Treat `lib/` items as candidates awaiting review. Promote them to canonical pages only after human or agent approval.
- `lib/` content may be referenced as an intermediate artifact but never as a primary source claim.
