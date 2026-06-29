# Hooks

Skill-owned hook entrypoints for skills-management.

- `external-skills-check.sh` checks `references/external-skills.yaml` against the selected runtime and reports missing external skills. It forwards checker selectors such as `--skill` and `--chain`, and stays report-only unless `AGENT_COMPANY_AUTO_INSTALL_EXTERNAL_SKILLS=1` is set.
