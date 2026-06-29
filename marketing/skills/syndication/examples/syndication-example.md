# Syndication Example: Blog Post → Dev.to + Hashnode + Newsletter

**Original**: "Building a Multi-Tenant Database in Postgres" (company blog, published 2026-06-15)  
**Original URL**: `https://example.com/blog/multi-tenant-postgres`  
**Target platforms**: Dev.to, Hashnode, weekly newsletter

---

## Step 1: Confirm Canonical Setup

Before syndicating:
- [ ] Original article has `<link rel="canonical" href="https://example.com/blog/multi-tenant-postgres" />`
- [ ] Original article has been indexed by Google (check Search Console or wait 24h after publish)

---

## Step 2: Dev.to Syndication

**What to change:**
- Add "Originally published at [example.com](https://example.com/blog/multi-tenant-postgres)" as the first line.
- Remove company-specific CTAs ("Try our product" → generic "I'd love your thoughts in the comments").
- Set canonical URL in the Dev.to publish settings (under "Advanced settings" → "Canonical URL").
- Add tags: `postgres`, `database`, `architecture`, `backend` (max 4 on Dev.to).

**What to keep:**
- Full article text (Dev.to supports long-form well).
- All code blocks.
- Images (re-upload to Dev.to — don't hotlink from your blog).

**Schedule**: Tuesday or Thursday, 9–11am UTC.

---

## Step 3: Hashnode Syndication

**What to change:**
- Set canonical URL in Hashnode's "SEO" panel.
- Add publication to your Hashnode blog (not generic feed).
- Tags: same as Dev.to but can add more (`sql`, `startup`).

**What to keep:**
- Full article text — Hashnode renders MDX well.
- Code blocks.

**Schedule**: 48 hours after Dev.to publish (avoid competing with yourself).

---

## Step 4: Newsletter Adaptation

For email, the full 2000-word article becomes a 400-word summary:

**Subject line**: "How we handle multi-tenant data isolation at scale (and why RLS changed everything)"

**Email structure:**
1. **Hook** (2 sentences): "Last week I wrote about our Postgres multi-tenancy approach. Here's the TL;DR for those who prefer their engineering in email form."
2. **The problem** (2 sentences): What is multi-tenancy and why does it matter?
3. **Our approach** (3–4 bullets): Key takeaways from the full article.
4. **CTA**: "Read the full post with code examples → [link]"

---

## Syndication Timing

| Platform | Publish | Notes |
|----------|---------|-------|
| Company blog | Day 0 | Original, indexed |
| Dev.to | Day 2 | First syndication |
| Hashnode | Day 4 | Second syndication |
| Newsletter | Day 7 | Summary edition |
| LinkedIn article | Day 14 | Adapted version, not a copy |
