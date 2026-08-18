# Task cards

This directory is the participant-facing entry point for the 25 frozen life-science task cards. Each task has one standalone file containing an exact packaged-input inventory, paste-once Prompt, deliverables, scientific hard gates, deterministic scoring details and capability expectation.
Evaluator-only answers, oracle fixtures, run outputs and scores are not stored in these cards and must never be copied into a participant workspace.

## Card index
- [`ls01-grna-offtarget-rank`](ls01-grna-offtarget-rank.md)
- [`ls01-primer-transcript-audit`](ls01-primer-transcript-audit.md)
- [`ls01-vector-orf-audit`](ls01-vector-orf-audit.md)
- [`ls02-deleterious-mutation`](ls02-deleterious-mutation.md)
- [`ls02-find-deletion`](ls02-find-deletion.md)
- [`ls02-infer-genome-build`](ls02-infer-genome-build.md)
- [`ls03-atac-sample-swap`](ls03-atac-sample-swap.md)
- [`ls03-cryptic-exon`](ls03-cryptic-exon.md)
- [`ls03-genome-coordinates`](ls03-genome-coordinates.md)
- [`ls04-differential-composition`](ls04-differential-composition.md)
- [`ls04-perturbseq-reference-map`](ls04-perturbseq-reference-map.md)
- [`ls04-spatial-deconvolution`](ls04-spatial-deconvolution.md)
- [`ls05-low-confidence-pocket`](ls05-low-confidence-pocket.md)
- [`ls05-protein-shape`](ls05-protein-shape.md)
- [`ls05-structure-model-ranking`](ls05-structure-model-ranking.md)
- [`ls06-eno1-effect-size`](ls06-eno1-effect-size.md)
- [`ls06-eno1-significance-audit`](ls06-eno1-significance-audit.md)
- [`ls07-combination-treatment-deg`](ls07-combination-treatment-deg.md)
- [`ls07-combination-treatment-mechanism`](ls07-combination-treatment-mechanism.md)
- [`ls08-enhancer-promoter-integration`](ls08-enhancer-promoter-integration.md)
- [`ls08-multiome-column-match`](ls08-multiome-column-match.md)
- [`ls09-opentrons-sop`](ls09-opentrons-sop.md)
- [`ls09-plate-dilution-recovery`](ls09-plate-dilution-recovery.md)
- [`ls10-neun-power-analysis`](ls10-neun-power-analysis.md)
- [`ls10-treatment-response-model`](ls10-treatment-response-model.md)

## Controlling contracts

- Input hashes and provenance: [`docs/inputs/SHA256SUMS.tsv`](../docs/inputs/SHA256SUMS.tsv)
- Deterministic score allocation: [`docs/contracts/deterministic-rubrics-v2.tsv`](../docs/contracts/deterministic-rubrics-v2.tsv)
- C0/T1 protocol: [`docs/contracts/evaluation-protocol-c0-t1-v2.md`](../docs/contracts/evaluation-protocol-c0-t1-v2.md)
- Formal release status: [`docs/contracts/formal-eval-release-status-2026-08-17.md`](../docs/contracts/formal-eval-release-status-2026-08-17.md)
