# Formal C0/T1 release status — 2026-08-17

Requested campaign: 25 tasks × (`C0`, `T1`) × 1 trial = 50 serial Codex runs.

Status: **operator release / execution authorized**.

## Closed gates

- All 25 task input directories are materialized; the canonical manifest contains 92 files and verifies byte-for-byte.
- All 25 task-local scientific checkers are present and `ACCEPTED=True`; an empty workspace fails every hard gate without checker exceptions.
- Task-specific frozen gold now covers all 25 tasks. Newly adjudicated reference-intensive tasks include GRCh38/Gencode/Ensembl/Axolotl references, full DE and enrichment tables, and explicit normalization/decision rules.
- Opentrons 7.1.0 is pre-provisioned. The reference protocol completes simulation with exit code 0 in three clean repetitions; format-correct wrong, empty and legacy-tip controls fail.
- The strict T1 plan remains frozen: `scgpt` for one task, `scvi-tools` for three tasks, and `NONE` for 21 tasks. Both selected skills install from commit `fb309c32ee9a54dad169fa845638057d1cfac77f`, match their workbook SHA-256, and are visible in a fresh Codex task.
- The serial runner creates a one-use Codex profile and workspace per queue row, copies only public task inputs, preserves immutable logs, performs evaluator-owned clean reruns, freezes outputs, and invokes static task oracles.

## Recorded protocol deviations

- The campaign host is macOS arm64. Opentrons 7.1.0 passed on-host while the repository's production simulator lock targets Linux x86_64/CPython 3.10. The package/protocol API is identical, but platform identity is reported as a deviation.
- No independent human reviewers were available during the unattended run. Deterministic grading remains valid and blinded narrative judging is performed in separate fresh Codex tasks with condition/model/score hidden. This does not satisfy a literal two-human sign-off requirement and is disclosed in the final denominator notes.
- The first frozen `ls01-vector-orf-audit` submission exposed a contradiction between the public rule and its gold for the 32-nt `c02` insert. The public rule prevailed: the gold was corrected, a 3× reference/empty/old-wrong regression test was added, the submission was not modified or rerun, and both pre/post grader results are preserved locally.
- `ls05-protein-shape` and the two LS09 tasks are local-extension/calibration items and are reported separately as well as in the requested all-25 table.

No agent output or score is committed to GitHub; those records remain under the local campaign folder and in the final Feishu document.
