# Life Science UI Evaluation Tasks

This repository contains reproducible desktop UI evaluation tasks for life-science workflows.

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

