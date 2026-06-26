# Marketing

Marketing workflows for content, SEO/GEO, social engagement, slide decks, visuals, and video.

## What lives here

- Skills: `content-writing`, `seo-and-geo`, `social-media-management`, `video-generation`, `code-as-images`, `code-slides`, `html-visual`
- Commands: `blog-draft`, `content-brief`, `social-pack`, `linkedin-engage`, `x-engage`, `slides`, `video`
- Agents: `growth-lead`

Use this plugin when the output is meant to be published, distributed, or presented externally.

## Install

Install the whole plugin with `skills`:

```bash
npx -y skills add ./marketing
```

Install one skill into Codex manually:

```bash
mkdir -p ~/.codex/skills
cp -R marketing/skills/code-slides ~/.codex/skills/
```

Use Codex `$skill-installer` against the plugin path:

```text
https://github.com/alvarovillalbaa/plugins/tree/main/marketing
```

## Skills

- [`content-writing`](./skills/content-writing/README.md): end-to-end content creation, audit, refresh, and repurposing
- [`seo-and-geo`](./skills/seo-and-geo/README.md): SEO, GEO, AEO, audits, and search visibility work
- [`social-media-management`](./skills/social-media-management/README.md): LinkedIn and X engagement writing
- [`video-generation`](./skills/video-generation/README.md): Remotion-based video production workflows
- [`code-as-images`](./skills/code-as-images/README.md): human-written stub for a still-incomplete skill
- [`code-slides`](./skills/code-slides/README.md): code-based slide decks and presentation systems
- [`html-visual`](./skills/html-visual/README.md): self-contained visual explainers and dashboards
