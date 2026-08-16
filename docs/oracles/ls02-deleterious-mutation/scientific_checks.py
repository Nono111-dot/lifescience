from __future__ import annotations

import csv
import json
from pathlib import Path

ACCEPTED = True


def _norm_chrom(value: object) -> str:
    return str(value).lower().removeprefix("chr")


def check(workspace: Path) -> dict:
    output = workspace / "output"
    gold = json.loads((Path(__file__).parent / "gold.json").read_text(encoding="utf-8"))
    try:
        with (output / "variant.tsv").open(encoding="utf-8-sig", newline="") as handle:
            rows = list(csv.DictReader(handle, delimiter="\t"))
    except Exception:
        rows = []
    one = len(rows) == 1
    row = rows[0] if one else {}

    def integer(keys: tuple[str, ...], expected: int) -> bool:
        for key in keys:
            if key in row:
                try:
                    return int(float(row[key])) == expected
                except (TypeError, ValueError):
                    return False
        return False

    locus = _norm_chrom(row.get("chrom", row.get("chromosome", ""))) == "9" and integer(("position_1based", "position", "pos"), gold["position_1based"])
    alleles = str(row.get("ref", "")).upper() == "G" and str(row.get("alt", "")).upper() == "T"
    gene = str(row.get("gene", row.get("gene_symbol", ""))).upper() == "STXBP1"
    consequence_text = " ".join(str(row.get(k, "")) for k in ("consequence", "effect", "variant_effect")).lower()
    consequence = "stop_gained" in consequence_text or "nonsense" in consequence_text or "stop gained" in consequence_text
    protein = str(row.get("protein_change", row.get("hgvsp", ""))).lower().replace("*", "ter") in {"p.glu117ter", "glu117ter"}

    try:
        evidence = json.loads((output / "evidence.json").read_text(encoding="utf-8"))
    except Exception:
        evidence = {}

    def ev_number(names: tuple[str, ...]):
        for name in names:
            if name in evidence:
                try:
                    return float(evidence[name])
                except (TypeError, ValueError):
                    return None
        return None

    alt_reads = ev_number(("alt_reads", "alternate_reads"))
    total_reads = ev_number(("total_reads", "depth", "coverage"))
    vaf = ev_number(("vaf", "variant_allele_fraction", "allele_fraction"))
    read_support = alt_reads == 18 and total_reads == 94 and vaf is not None and abs(vaf - gold["vaf"]) <= 0.01
    pli = ev_number(("pli", "pLI"))
    loeuf = ev_number(("loeuf", "LOEUF"))
    constraint = pli is not None and pli >= 0.99 and loeuf is not None and loeuf <= 0.11
    transcript = str(evidence.get("mane_transcript", evidence.get("transcript", ""))) == gold["mane_transcript"]

    core = sum((10 if locus and alleles else 0, 8 if gene else 0, 8 if consequence else 0, 4 if protein else 0, 6 if read_support else 0, 4 if constraint and transcript else 0))
    interpretation = " ".join(str(evidence.get(k, "")) for k in ("interpretation", "classification", "conclusion")).lower()
    decision = locus and alleles and gene and consequence and read_support and ("deleterious" in interpretation or "loss-of-function" in interpretation or "loss of function" in interpretation)
    report = (output / "report.md").read_text(encoding="utf-8", errors="replace").lower() if (output / "report.md").is_file() else ""
    summary = all(term in report for term in ("stxbp1", "127661125")) and ("18/94" in report or "19.1%" in report or "0.191" in report) and ("stop" in report or "nonsense" in report) and not any(term in report for term in ("clinically pathogenic", "diagnostic proof", "confirmed disease-causing"))
    checks = {
        "exactly_one_variant": one,
        "grch38_chr9_127661125_g_to_t": locus and alleles,
        "gene_stxbp1": gene,
        "stop_gained": consequence,
        "protein_p_glu117ter": protein,
        "read_support_18_of_94_vaf_tolerance_0_01": read_support,
        "mane_and_constraint": constraint and transcript,
        "deleterious_not_clinical_decision": decision,
        "report_consistent_and_restrained": summary,
    }
    failures = ["LS02_DELETERIOUS_" + key.upper() for key, ok in checks.items() if not ok]
    return {
        "core_science": core,
        "direction": 15 if decision else 0,
        "summary": 5 if summary else 0,
        "hardgate_pass": one and locus and alleles and gene and consequence and read_support,
        "failure_codes": failures,
        "criteria": checks,
    }
