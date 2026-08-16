# Input index

Task inputs are read-only fixtures. Copy the contents of exactly one task directory into a fresh workspace's `inputs/` directory. Never edit the repository copy during a run.

| Task ID | Files | License/provenance | Notes |
| --- | --- | --- | --- |
| `life-l2-paired-expression` | `paired_expression.csv` | CC0-1.0 synthetic fixture created for this repository | Expression values are arbitrary normalized units; they are not patient data. |
| `ls06-eno1-effect-size` | two XLSX workbooks | BixBench v1.5 `bix-37` capsule | Proteomics target plus unrelated MeRIP decoy. |
| `ls06-eno1-significance-audit` | two XLSX workbooks | BixBench v1.5 `bix-37` capsule | Same frozen bytes; adjusted-p-value task. |
| `ls07-combination-treatment-deg` | counts, layout, Ensembl display-name mapping | BixBench v1.5 `bix-43` capsule | Participant-visible inputs complete; accepted DESeq2 reference still pending. |
| `ls07-combination-treatment-mechanism` | LS07 expression inputs, `Reactome_2022.gmt`, explicit background, resource manifest | BixBench plus official Enrichr `Reactome_2022` retrieval | Resource and universe frozen 2026-08-16; accepted enrichment reference still pending. |
| `ls08-multiome-column-match` | ATAC and RNA gzip matrices | Genentech CompBioBench frozen revision | Inputs complete; hidden mapping/normalization acceptance pending. |
| `ls08-enhancer-promoter-integration` | Hi-C and CRISPR-expression CSVs | Genentech CompBioBench frozen revision | Files contain EP1–EP7 despite the source question's EP1–EP8 wording. |
| `ls09-opentrons-sop` | SOP, instrument, labware, reagent map, sample map, simulator contract | Locally authored synthetic fixture; Opentrons official API basis | Simulator contract pinned; identical cross-harness provisioning and real-simulator acceptance pending. |
| `ls09-plate-dilution-recovery` | request, pipettes, plate map, run log, source inventory | Locally authored synthetic fixture | Five inputs and accepted checker are complete. |
| `ls10-neun-power-analysis` | NeuN CSV | BixBench v1.5 `bix-19` capsule | Two labeled groups; no decoy. |
| `ls10-treatment-response-model` | response-model XLSX | BixBench v1.5 `bix-51` capsule | Named model columns plus distractor covariates. |

The current formal scope is the ten LS06–LS10 rows above. Every one of those task directories now has its own README with file roles, provenance/license boundary, schema/units, missing-value rules, and integrity/readiness notes.

`SHA256SUMS.tsv` must cover every agent-visible file copied from a task directory, including its README and any resource/simulator manifest. A missing or stale manifest entry blocks formal preparation.

## Adding an input set

Each `docs/inputs/<task-id>/` directory must include a README stating provenance, redistribution terms, schema, units, missing-value representation, and integrity information. Do not include secrets, personal data, controlled clinical data, or files whose license prohibits redistribution.
