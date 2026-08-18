# Evaluator documentation

The participant-facing task cards are stored only in [`../task-card/`](../task-card/). This directory contains evaluator-side contracts, operations material, provenance and hidden grading resources.

- [`contracts/`](contracts/): active task selection, deterministic rubrics, protocol, release status, run queue and T1 capability mappings.
- [`operations/`](operations/): preflight, blind-review and run-record templates.
- [`provenance/`](provenance/): input-source and local-extension provenance.
- [`inputs/`](inputs/): participant-visible task inputs and the canonical SHA-256 manifest.
- [`oracles/`](oracles/): evaluator-only gold data and static scientific graders.
- [`benchmark-rubrics/`](benchmark-rubrics/): upstream/native rubric evidence.
- [`research/`](research/): scientific provenance and adjudication evidence.
- [`environments/`](environments/): pinned runtime contracts.

Do not expose `oracles/`, research evidence, run records or scoring contracts to evaluated participants.
