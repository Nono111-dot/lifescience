# Oracle adjudication

On 2026-08-17, the first frozen formal submission exposed an inconsistency between the public `AUDIT_RULE.md` and `gold.json`: construct `c02` has a 32-nt insert, so its length is not divisible by three and `frame_ok` must be false. The original gold incorrectly recorded `frame_ok=true` and omitted `FRAME` from `issues`.

The gold was corrected without modifying or rerunning the submission. A task-local acceptance test now requires three clean passes of the corrected reference plus rejection of an empty output and a format-correct wrong control that reproduces the old `c02` answer. The original grader result is retained locally as `oracle_pre_adjudication.json`; the frozen artifact was rescored with the corrected static checker.
