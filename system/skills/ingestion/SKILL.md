---
name: ingestion
description: >-
  Raw source ingestion, transcript/artifact parsing, canonical page promotion,
  and Memory-to-knowledge compilation. Child of `brain`; use when this is the
  narrowest owner.
---

# Raw Ingestion

This child skill owns raw source ingestion, transcript or artifact parsing, canonical page promotion, unreadable-source preservation, and BRAIN.md-bound cleanup. It carries the detailed assets for this lane after the corrected fragmentation split.

## Use When

- The request is primarily about raw source ingestion, transcript or artifact parsing, canonical page promotion, unreadable-source preservation, and BRAIN.md-bound cleanup.
- The request asks to process `raw/`, source URLs, local files, transcripts, PDFs, screenshots, structured exports, or repo-local Memory folders into `knowledge/`.
- The parent router [`../brain/SKILL.md`](../brain/SKILL.md) selects this child.
- The work needs this lane's references, scripts, examples, or templates.

## Required Reading

- [`../brain/references/brain_contract.md`](../brain/references/brain_contract.md) before write-bearing runs.
- [`references/ingest_sources.md`](references/ingest_sources.md) for source-specific fetch and parse instructions.
- [`references/wiki_compiler.md`](references/wiki_compiler.md) for absorb, cleanup, rebuild, and reorganize loops.
- [`../../../references/docs/promotion-matrix.md`](../../../references/docs/promotion-matrix.md) before promoting raw or Memory evidence into durable docs.

## Assets

- `references/` contains lane-specific guidance moved from the original parent skill.
- `scripts/` contains executable helpers owned by this lane.
- `templates/` contains reusable output or implementation templates for this lane.
- `examples/` contains sample inputs, outputs, or usage artifacts.

## Chain Rules

- Chain to `knowledge-base`, `code-documentation`, `research`, `reporting` when the task crosses this child's boundary.
- Use repo-local personalization documents for company, product, voice, cloud, QA, or finance facts instead of hardcoding them here.
- Preserve parent safety and approval rules for destructive, security-sensitive, finance-sensitive, or cloud-costly work.
- Treat missing extraction tools, login walls, deleted media, encrypted files, and metadata-only pages as blocked raw inputs, not as permission to infer claims.

## External Skill Chains

Use live external skills when they are installed. If one is missing, report the fallback command instead of copying its guidance inline. Local skill rules, repo-specific facts, safety gates, product/channel constraints, and explicit local exceptions win over external guidance when they conflict.

- `writing-great-skills`: Use external skill-authoring quality rules when creating or revising skills. Install: `python3 scripts/install-external-skills.py --skill writing-great-skills --agent codex`.
- `teach`: Create mission-grounded learning material, resources, records, and lessons. Install: `python3 scripts/install-external-skills.py --skill teach --agent codex`.
- `grilling`: Interview one decision at a time until a plan or design is sharp. Install: `python3 scripts/install-external-skills.py --skill grilling --agent codex`.
- `grill-me`: Shortcut into a grilling session for plan or design stress testing. Install: `python3 scripts/install-external-skills.py --skill grill-me --agent codex`.
- `grill-with-docs`: Stress-test a plan or design while maintaining docs, ADRs, and glossary context. Install: `python3 scripts/install-external-skills.py --skill grill-with-docs --agent codex`.
- `use-afs`: Use the AFS filesystem layout and naming conventions instead of duplicating local filesystem guidance. Install: `python3 scripts/install-external-skills.py --skill use-afs --agent codex`.
- `clous-knowledge-retrieval`: Use Clous-owned retrieval guidance for knowledge lookup and source-grounded context. Install: `python3 scripts/install-external-skills.py --skill clous-knowledge-retrieval --agent codex`.

Registry: [`../../../references/external-skills.yaml`](../../../references/external-skills.yaml).
Reference-only sources: [`../../../references/external-sources.yaml`](../../../references/external-sources.yaml).

## Shared Map

See [`../../../skills-chaining-map.md`](../../../skills-chaining-map.md) for the complete skills-chaining graph.
