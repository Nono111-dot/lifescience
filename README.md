# Life Science UI Evaluation Tasks

This repository contains reproducible desktop UI evaluation tasks for life-science workflows.

Current evaluation package:

- `docs/ls06-ls10-runbook-v2.md`: current 10-task scope and per-run capability reset gate
- `docs/task-cards-v1.md`: 25 workflow-compliant task cards
- `docs/deterministic-rubrics-v2.tsv`: per-task 10/40/15/5/10 deterministic rubric
- `docs/oracles/<task-id>/oracle.py`: 25 fail-closed static oracle entry points
- `docs/input-problem-inventory-v1.tsv`: source question, level, size, readiness and blockers
- `docs/capability-whitelist-v1.tsv`: exact 222-catalog names allowed in T1/T2
- `docs/evaluation-protocol-v1.md`: Codex/端砚 conditions, SOP, scoring and go/no-go
- `docs/preflight-checklist.md`: formal-run acceptance checklist
- `docs/run-record-template.tsv`: immutable per-run record schema
- `docs/blind-judge-form.md`: blinded 20-point review form
- `scripts/prepare-workspace.ps1`: non-overwriting one-use workspace preparation

## Repository layout

```text
docs/
├── ai4s-ui-taskbook-v0.1.md
├── inputs/
│   ├── README.md
│   └── life-l2-paired-expression/
│       ├── README.md
│       └── paired_expression.csv
└── oracles/
    └── life-l2-paired-expression/
        ├── oracle.py
        └── test_oracle.py
```

Start with [the taskbook](docs/ai4s-ui-taskbook-v0.1.md). Input licensing and copying rules are documented in [the input index](docs/inputs/README.md).

## Quick start

```bash
mkdir -p workspace/inputs workspace/output
cp -R docs/inputs/life-l2-paired-expression/. workspace/inputs/

# Complete the task in workspace/, then grade it:
python3 docs/oracles/life-l2-paired-expression/oracle.py \
  --workspace workspace
```

The oracle prints JSON containing a `deterministic_score` from 0 to 80, per-criterion results, `hardgate_pass`, and `failure_codes`. Visual quality is scored separately from 0 to 20 by a blind judge.

