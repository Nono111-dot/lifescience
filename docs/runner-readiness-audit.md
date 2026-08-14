# Runner readiness audit

## Outcome

The repository can safely prepare isolated one-use workspaces and capture calibration evidence. It cannot yet produce a formal headline result: the LS06–LS10 readiness audit currently reports 0/10 tasks with a 3/3-accepted scientific checker.

This distinction is enforced by the runner. `-Mode formal` refuses an unaccepted oracle; `-Mode calibration` preserves artifacts and the blocked oracle result without presenting it as a score.

## Implemented controls

- `scripts/prepare-workspace.ps1` creates a non-overwriting workspace with task-only inputs, an empty `output/`, and an input SHA-256 manifest.
- Harness/condition pairing is enforced: Codex/C0 and 端砚/T0–T2.
- `scripts/audit-evaluation-readiness.ps1` reports missing inputs, oracle entry points, scientific checkers, and oracle acceptance.
- `scripts/freeze-and-score.ps1` verifies unchanged input bytes, rejects reparse points, creates an append-only result directory, hashes the workspace, invokes the static oracle, records interpretation metadata, and marks captured files read-only.
- `scripts/summarize-results.ps1` separates formal scored runs from calibration/non-scoreable runs in a readable Markdown table.
- Runtime results are ignored by Git under `results/`; they remain on disk as experiment evidence and must be backed up according to the experiment retention policy.

The read-only file attribute is an accidental-write guard, not a security boundary. The operator must still revoke client write access before invoking the freeze command.

## Commands

PowerShell execution policy is disabled on the current machine, so invoke scripts explicitly with a process-scoped bypass:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\audit-evaluation-readiness.ps1 -Scope ls06-ls10 -JsonOut .tmp_tests\readiness-audit.json

powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\prepare-workspace.ps1 -TaskId ls06-eno1-effect-size -Harness codex -Condition C0 -Trial 1

# Only after the UI run has stopped and write access has been revoked:
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\freeze-and-score.ps1 -TaskId ls06-eno1-effect-size -Harness codex -Condition C0 -Trial 1 -Mode calibration

powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\summarize-results.ps1 -OutFile .\results\summary.md
```

Change `-Mode calibration` to `-Mode formal` only after the task's checker has independently passed the reference, empty-output, and scientifically-wrong-output acceptance tests and is reviewed and marked `ACCEPTED = True`.

## Manual controls still required

The scripts cannot operate or attest the 端砚 UI. For every run, the operator must record the exact client/model/build, timer, permission interventions, completion status, capability inventory and trace, screen/log evidence, and the after-run capability reset. The next run remains blocked until the normalized post-reset inventory equals the frozen baseline and a fresh-conversation smoke check shows no previous task state.

The present `run-record-template.tsv` has fields for this evidence, but no automatic 端砚 export integration is available in the repository. Therefore a UI run without the corresponding run record and reset evidence is incomplete even if artifacts exist.
