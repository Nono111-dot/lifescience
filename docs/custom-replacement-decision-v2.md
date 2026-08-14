# Seven custom-task replacement decision (v2)

Status date: 2026-08-14

This document applies a strict replacement rule: a replacement must have a verifiable benchmark task identity and public prompt provenance, must fit the LS sub-domain, and must not be represented as having a public native oracle when none is published.

## Decision summary

| Existing custom task | Decision | Benchmark replacement | Sub-domain fit | Important limitation |
|---|---|---|---|---|
| `ls01-grna-offtarget-rank` | REPLACE | CompBioBench `promoter-sequence-retrieval-q1` | LS01 molecular biology: retrieving a strand-correct regulatory DNA sequence | Tests sequence retrieval/orientation, not gRNA off-target ranking |
| `ls01-primer-transcript-audit` | REPLACE | CompBioBench `align-one-sequence-to-reference-q1` | LS01 primers/probes: short nucleic-acid sequence localization | Tests reference localization, not transcript-specific primer-pair design |
| `ls01-vector-orf-audit` | REPLACE | CompBioBench `orf-annot-q1` | LS01 vector/ORF and nucleic-acid sequence analysis | Tests main-CDS annotation, not a complete vector audit |
| `ls05-structure-model-ranking` | BLOCKED | none publicly qualified | LS05 requires protein structure/engineering | The three selected benchmarks contain no unused matching task |
| `ls05-low-confidence-pocket` | BLOCKED | none publicly qualified | LS05 requires structure confidence/pocket reasoning | BioDesignBench formal tasks and inputs are private; its public demo is explicitly not a benchmark task |
| `ls09-opentrons-sop` | BLOCKED | none publicly qualified | LS09 requires machine-executable lab automation | ABC-Bench publishes a paper prompt but not the dataset/scorer |
| `ls09-plate-dilution-recovery` | BLOCKED | none publicly qualified | LS09 includes protocol error recovery | BioProBench has a public serial-dilution protocol correction item, but it is not a machine-executable automation task |

Therefore the current result is **3 valid replacements and 4 evidence-backed gaps**, not seven fabricated mappings. The four blocked rows must not enter a formal 25-task run as benchmark-derived tasks.

## Accepted replacements: exact native prompts

### `ls01-promoter-sequence-retrieval`

- Upstream: CompBioBench `promoter-sequence-retrieval-q1`
- Public input files: none; native metadata says internet is required.
- Native answer contract: one 601 bp DNA sequence, 5′ to 3′ on the sense strand.
- Prompt:

> Using the Ensembl GRCz11 genome assembly and Ensembl gene annotation, what is the DNA sequence of the promoter region of the zebrafish gene shha? Define the promoter as the region spanning positions −500 to +100 relative to the transcription start site (TSS) of the canonical transcript, where the TSS is position 0, negative positions are upstream, and positive positions are downstream, yielding a 601 bp sequence. Return the sequence in 5′ to 3′ orientation on the sense strand (reverse complement the genomic sequence if the gene is on the − strand).

### `ls01-short-sequence-reference-alignment`

- Upstream: CompBioBench `align-one-sequence-to-reference-q1`
- Public input: `GCF_000001215.4_Release_6_plus_ISO1_MT_genomic.fna`
- Native metadata: internet is not required.
- Native answer contract: `contig:start-end`, using 0-based coordinates.
- Prompt:

> Where does CACACACAGGAGAT align to in the given GCF_000001215.4_Release_6_plus_ISO1_MT_genomic.fna? Report as 0-based coordinates in contig:start-end format (no commas).

### `ls01-main-cds-annotation`

- Upstream: CompBioBench `orf-annot-q1`
- Public input: `orf.annot.q1.fa`
- Native metadata: internet is required.
- Native answer contract: two integers in `CDS_start;protein_length` form.
- Prompt:

> You are given a fasta file containing a human mRNA sequence. Find the main CDS of the sequence, return the start position of the CDS (in a 0-based coordinate system, starting from the first base of the given sequence) and the length of the translated protein in the format 4;2.

## Why the other four were not substituted

### LS05

CompBioBench v1 contains only one `Structure` task, `protein-shape-q1`, which is already selected as `ls05-protein-shape`. BixBench v1.5 and BioAgentBench do not publish model-ranking, pLDDT/PAE, protein-pocket, or protein-engineering tasks suitable for these two slots.

BioDesignBench is domain-relevant, but its maintainers state that the 76 formal prompts, input PDBs, ground truth, and oracle outputs are private. Its public trypsin-binder demo is explicitly outside the formal benchmark and cannot be relabelled as a benchmark task.

### LS09

The three selected benchmarks contain no Opentrons, liquid-handler, plate-dilution recovery, or machine-executable protocol task.

ABC-Bench publishes the `Liquid Handling Robot v1.0.1` OpenTrons Gibson Assembly prompt and a six-part paper rubric, but the benchmark dataset and executable scorer are not public. It is evidence of a relevant benchmark, not a locally runnable replacement.

BioProBench item `TEST-ERR-000950` is publicly traceable and concerns correction of a 96-well ten-fold serial dilution protocol. It measures textual protocol error correction, not generation or execution of robot code. It may be used only if the LS09 slot is explicitly redefined from machine-executable automation to protocol audit/error recovery.

## Public provenance

- [CompBioBench frozen task table, revision c673f0855fce09d320f1677f168f7864eec52c1a](https://huggingface.co/datasets/Genentech/compbiobench-data-v1/blob/c673f0855fce09d320f1677f168f7864eec52c1a/compbiobench.v1.tsv)
- [CompBioBench ORF input](https://huggingface.co/datasets/Genentech/compbiobench-data-v1/blob/c673f0855fce09d320f1677f168f7864eec52c1a/data/orf.annot.q1.fa)
- [CompBioBench reference-genome input](https://huggingface.co/datasets/Genentech/compbiobench-data-v1/blob/c673f0855fce09d320f1677f168f7864eec52c1a/data/GCF_000001215.4_Release_6_plus_ISO1_MT_genomic.fna)
- [BioAgentBench task repository](https://github.com/bioagent-bench/bioagent-bench)
- [BixBench dataset](https://huggingface.co/datasets/futurehouse/BixBench)
- [BioDesignBench disclosure and public demo status](https://github.com/RomeroLab/BioDesignBench)
- [ABC-Bench paper](https://arxiv.org/abs/2606.11150)
- [BioProBench public ERR test data](https://huggingface.co/datasets/BioProBench/BioProBench/blob/main/ERR_test.json)

## Scoring provenance warning

CompBioBench's public task table supplies prompts, metadata, and file paths, but not per-task gold answers or public verifier code. For the three accepted replacements, the formats above are native answer contracts. Any local gold or Python oracle must be independently derived, reviewed, frozen, and labelled `derived-local-verifier`; it must not be described as a benchmark-native rubric.

