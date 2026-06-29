# Second Brain

Build and maintain an AFS-aligned, storage-agnostic knowledge base that compounds over time instead of resetting each session.

## Use this for

- turning scattered notes, meetings, chats, research, and files into a maintained wiki
- routing that wiki through `BRAIN.md` boundaries so one workspace can host multiple second brains safely
- consolidating duplicates and preserving provenance
- restoring continuity at the start of a session
- generating outputs, reports, or artifacts grounded in a living knowledge base

## Install

```bash
npx -y skills add ./system/skills/brain
mkdir -p ~/.codex/skills
cp -R system/skills/brain ~/.codex/skills/
```

Codex `$skill-installer` path:

```text
https://github.com/alvarovillalbaa/plugins/tree/main/system/skills/brain
```

## What is bundled

- `references/` — brain contract, operational modes, page model, compound loop, and Obsidian adapter
- `../ingestion/references/` — wiki compiler and **ingest sources** (Twitter/xurl, YouTube, LinkedIn, web URLs, PDFs, images, structured files)
- `agents/openai.yaml` — Second Brain agent definition
- `../../commands/ingest.md` — `/ingest` command for any source type
- `../../commands/compile-raw.md` — `/compile-raw` command for batch processing `raw/` and repo-local Memory inputs

This skill is one of the strongest starting points in the system plugin. Read [`SKILL.md`](./SKILL.md) before adapting it to any tool-specific setup.
