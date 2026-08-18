# Frozen input provenance report

This repository freezes inputs for 25 life-science desktop-agent evaluation tasks. The authoritative selection is `selected-tasks-v1.tsv`; file hashes are recorded in `inputs/SHA256SUMS.tsv`.

## Source policy

- CompBioBench inputs were downloaded from `Genentech/compbiobench-data-v1` at the Hugging Face `main` revision available on 2026-08-14. The selected upstream question ID is recorded in the task manifest.
- BixBench capsule archives were downloaded from `futurehouse/BixBench`. Only files under `CapsuleData-*` were retained. Executed notebooks and other answer-bearing capsule content were explicitly excluded from agent-visible inputs.
- Custom fixtures were created for this repository where the reviewed upstream benchmarks did not cover the required workflow. They are synthetic, contain no patient data, and are intended for CC0-1.0 release after scientific review.
- Inputs are not yet gold answers. Oracle files and hidden expected mappings must remain outside `docs/inputs/`.

## Size review

The upstream datasets vary substantially in size. Tasks above the internal L2 recommendation of 20 MB must either be classified as L3 or receive a scientifically valid, independently reviewed subset before formal UI acceptance. In particular, raw FASTQ, tagAlign, pseudobulk and sparse-matrix tasks require a size review before release.

The original `histone-chip-q1` candidate was rejected because its two input files were approximately 167 MB and 173 MB, exceeding GitHub's normal per-file limit. It was replaced by the smaller CompBioBench `genome-coords-q1` task.

## Current closure

All 25 selected input directories now have a matching standalone task card, accepted static oracle, deterministic rubric and frozen manifest entry. Reference and negative-control evidence is retained under the evaluator-only oracle directories. The authoritative current decision and disclosed review/runtime deviations are in `formal-eval-release-status-2026-08-17.md`; this document records input provenance rather than release status.
