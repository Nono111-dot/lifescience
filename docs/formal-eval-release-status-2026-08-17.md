# Formal C0/T1 release status — 2026-08-17

Campaign scope: 25 tasks × (`C0`, `T1`) × 1 trial = 50 serial Codex runs.

Status: **dataset delivery ready; capability-use limitations disclosed**.

## Closed dataset gates

- The selected-task, input-inventory, deterministic-rubric, native-rubric, skill-plan and run-queue task-ID sets agree on 25 unique tasks.
- Every task has one participant-facing card, one input directory and one evaluator-only static oracle.
- The canonical manifest covers exactly the files inside the 25 task input directories and verifies byte-for-byte.
- All 25 task-local scientific checkers are present and marked accepted; empty output fails every hard gate without checker exceptions.
- The 50-row queue contains exactly one `C0` and one `T1` run per task.
- The serial runner copies only the selected task's inputs into a one-use workspace, preserves logs, freezes outputs and invokes the static oracle outside the participant workspace.

## T1 capability record

- Fifteen tasks received one or more predeclared Agent Skills; ten tasks received `NONE`.
- Eighteen unique selected skills are pinned to an exact repository, commit, path and `SKILL.md` SHA-256 in `docs/capability-runtime-mapping-v1.tsv`.
- All 18 selected skills have successful install/hash evidence and a clean post-run removal/reset attestation.
- Twelve selected skills were visibly opened or invoked in at least one scored run. Six were installed and exposed but not opened by the evaluated agent: `ITEM-035`, `ITEM-036`, `KDENSE-bulk-rnaseq`, `KDENSE-deepspot-m`, `KDENSE-pysam` and `KDENSE-scvi-tools`.

Installation/exposure is therefore the T1 treatment. Do not claim that every installed skill was used, or attribute a task result to a specific non-invoked skill.

## Recorded deviations

- The campaign host was macOS arm64. Opentrons 7.1.0 passed on-host while the production simulator lock targets Linux x86_64/CPython 3.10.
- No independent human reviewers were available during the unattended run. Deterministic grading remains reproducible; the literal two-human sign-off requirement was not met.
- The first frozen `ls01-vector-orf-audit` submission exposed a contradiction between the public rule and the original gold for the 32-nt `c02` insert. The public rule prevailed, the gold and regression test were corrected, and the submission was not altered.
- `ls05-protein-shape`, both LS05 structure extensions and the two LS09 tasks are local-extension/calibration items and must be labeled separately from upstream benchmark-derived tasks.

## Distribution boundary

The participant receives only one task card Prompt and the matching `inputs/` directory. `docs/oracles/`, gold files, reference outputs, grader testdata, run logs and scores are evaluator-only. If this repository is public or accessible to the evaluated agent, package participant materials separately and keep evaluator material private.

No agent output, score or frozen run workspace is committed to GitHub.
