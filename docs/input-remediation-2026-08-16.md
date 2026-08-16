# LS06–LS10 input remediation — 2026-08-16

This pass reconciles participant-visible inputs, provenance, integrity metadata, task cards, oracle status, and the formal execution queue. It deliberately does not convert an unresolved scientific reference into a gold answer.

## Added inputs and environment contracts

- Every LS06–LS10 task input directory now includes a task-local `README.md` covering file roles, provenance/license boundaries, schema or workbook semantics, units, missing-value rules, integrity, and readiness.
- LS07-2 now includes the official Enrichr `Reactome_2022` GMT export retrieved on 2026-08-16, a deterministic sorted-union background, and a machine-readable provenance/hash manifest. The export contains 1,818 terms and the background contains 10,489 unique gene symbols.
- LS09-1 now includes `simulator_contract.json`. The matching evaluator environment under `docs/environments/opentrons-api-2.16/` pins CPython 3.10, Linux x86_64, `opentrons==7.1.0`, every transitive dependency, every wheel hash, the simulator command, capture rules, and fail-closed behavior.

## Reconciled integrity and run control

- `docs/inputs/SHA256SUMS.tsv` now describes all agent-visible formal-scope files, including the current LS09 files, task READMEs, Reactome files, and simulator contract.
- The LS09 oracle-local input manifests now include every copied task file.
- `scripts/prepare-workspace.ps1` verifies manifest coverage, file presence, byte size, and SHA-256 before creating a one-use workspace.
- `scripts/audit-evaluation-readiness.ps1` reports missing, duplicate, or stale input-manifest entries as formal blockers.
- `docs/formal-run-queue-2026-08-16.tsv` is the current fail-closed 10-task × 4-condition queue. The 2026-08-14 queue remains immutable historical evidence.

## Current release boundary

Scientifically ready, pending harness preflight: LS06-1, LS06-2, LS09-2, LS10-1, and LS10-2.

Still blocked from formal scoring:

- LS07-1: PyDESeq2 0.5.0 reference table, 677/679 threshold adjudication, and 3/3 acceptance are incomplete.
- LS07-2: the missing Reactome resource/universe defect is fixed, but the upstream DE adjudication, full enrichment reference, and 3/3 checker acceptance remain incomplete.
- LS08-1: hidden permutation and normalization policy are not independently accepted.
- LS08-2: EP1–EP8 source inconsistency and aggregation/normalization/tie rules are not independently accepted.
- LS09-1: the environment contract is pinned, but identical Codex/Duanyan provisioning and real-simulator 3/3 acceptance have not been recorded.

No blocked item may enter a scored run merely because its participant-visible inputs are now complete.

## External provenance

- Enrichr library endpoint: <https://maayanlab.cloud/Enrichr/geneSetLibrary?mode=text&libraryName=Reactome_2022>
- Enrichr citations: <https://maayanlab.cloud/Enrichr/#stats>
- Reactome licensing: <https://reactome.org/license>
- Opentrons simulator documentation: <https://github.com/Opentrons/opentrons/blob/edge/api/README.rst>

Exact retrieval metadata and hashes live beside the supplied resources rather than in this narrative report.
