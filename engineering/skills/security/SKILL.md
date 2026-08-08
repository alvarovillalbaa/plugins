---
name: security
description: Use for passive security review, threat modeling, secure-code checks, dependency review, and compliance-oriented findings. Child of `quality-assurance`.
---

# Passive Security Review

This child skill owns passive security review, threat modeling, secure-code checks, dependency review, and compliance-oriented findings. It carries the detailed assets for this lane after the corrected fragmentation split.

## Use When

- The request is primarily about passive security review, threat modeling, secure-code checks, dependency review, and compliance-oriented findings.
- The parent router [`../quality-assurance/SKILL.md`](../quality-assurance/SKILL.md) selects this child.
- The work needs this lane's references, scripts, examples, or templates.

## Assets

- `references/` contains lane-specific guidance moved from the original parent skill.
- `scripts/security_scanner.py` performs passive source-pattern triage for
  injection, XSS, command injection, and path traversal.
- `scripts/secret_scanner.py` is the canonical, higher-fidelity secrets scanner;
  secret detection is intentionally not duplicated in `security_scanner.py`.
- `scripts/compliance_checker.py` and `scripts/threat_modeler.py` produce
  deterministic compliance and threat-model artifacts.
- `templates/` contains reusable output or implementation templates for this lane.
- `examples/` contains sample inputs, outputs, or usage artifacts.

For dependency vulnerabilities, use current ecosystem or advisory-backed tools
against the real lockfile. This repository deliberately does not ship a frozen
miniature CVE database, because it would become incomplete and misleading.

## Chain Rules

- Chain to `pentest`, `ai-engineering/ai-evals-observability`, `frontend`, `backend`, `prs`, `cloud` when the task crosses this child's boundary.
- This skill owns passive source, secret, dependency, threat-model, and
  compliance review. Chain authorized browser/network exploit validation to
  `pentest/web-vuln-validation`.
- Use repo-local personalization documents for company, product, voice, cloud, QA, or finance facts instead of hardcoding them here.
- Preserve parent safety and approval rules for destructive, security-sensitive, finance-sensitive, or cloud-costly work.

## Shared Map

See [`../../../skills-chaining-map.md`](../../../skills-chaining-map.md) for the complete skills-chaining graph.
