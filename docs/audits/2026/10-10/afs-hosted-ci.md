# Hosted CI limit

Checked migration head `3bec99c24bbf29bc429e5e6668f5207a418eeed3`:
[validate job](https://github.com/alvarovillalbaa/plugins/actions/runs/38079640789/job/114293711967).
Structure (seven plugins), metadata (147 skills) and conflicts passed. The
hook/script audit reports one defect: `paas-ops/SKILL.md` claims executable
helpers but owns no non-test script assets.

The local `python3 scripts/audit_hooks_scripts.py .` reproduces the same
failure. The complete `engineering/skills/paas-ops/` subtree and both relevant
validator scripts have zero diff against pulled baseline `4ae3173`; the
baseline also tracks no `paas-ops/scripts` assets. This is inherited source
drift outside the AFS migration. No check was disabled and no CI change or
rerun was requested. The focused contract tests remain separate local proof.
