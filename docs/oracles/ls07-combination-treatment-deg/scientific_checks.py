from __future__ import annotations
import csv, json, math
from pathlib import Path

# Native endpoint 677 is public, but row-level DE values require a pinned DESeq2
# reference run. Keep diagnostic scoring available without admitting formal runs.
ACCEPTED = False

def num(v):
    try: return float(v)
    except (TypeError, ValueError): return math.nan

def check(workspace: Path):
    out=workspace/'output'; failures=[]; criteria={}
    try:
        with (out/'differential_expression.csv').open(encoding='utf-8-sig',newline='') as f: rows=list(csv.DictReader(f))
    except Exception: rows=[]
    ids=[str(r.get('gene_id','')) for r in rows]
    unique=bool(rows) and len(ids)==len(set(ids)) and all(ids)
    predicate_ok=True; passing=0; numeric_rows=0
    for r in rows:
        bm,lfc,padj=num(r.get('baseMean')),num(r.get('log2FoldChange')),num(r.get('padj'))
        expected=math.isfinite(bm) and math.isfinite(lfc) and math.isfinite(padj) and padj<.05 and abs(lfc)>.5 and bm>10
        reported=str(r.get('pass','')).strip().lower() in {'true','1','yes'}
        if reported!=expected: predicate_ok=False
        passing += int(reported); numeric_rows += int(math.isfinite(bm) and math.isfinite(lfc))
    try: summary=json.loads((out/'summary.json').read_text(encoding='utf-8'))
    except Exception: summary={}
    reported_count=summary.get('n_passing',summary.get('passing_genes',summary.get('count')))
    try: reported_count=int(reported_count)
    except Exception: reported_count=-1
    count_internal=reported_count==passing
    # BixBench bix-43-q3 publishes 677 as its native ideal for the frozen DESeq2 analysis.
    benchmark_count=passing==677 and reported_count==677
    core=(10 if unique else 0)+(10 if numeric_rows==len(rows) and rows else 0)+(10 if predicate_ok else 0)+(10 if benchmark_count else 0)
    direction=15 if predicate_ok and benchmark_count else 0
    summary_score=5 if count_internal and benchmark_count else 0
    if not unique: failures.append('DE_GENE_IDS_INVALID')
    if not predicate_ok: failures.append('DE_PASS_PREDICATE_MISMATCH')
    if not benchmark_count: failures.append('DE_BIX_NATIVE_COUNT_MISMATCH')
    if not count_internal: failures.append('DE_SUMMARY_MISMATCH')
    criteria.update(unique_gene_ids=unique,numeric_rows=numeric_rows,predicate_exact=predicate_ok,
                    passing_rows=passing,bix_native_count_677=benchmark_count,summary_internal=count_internal)
    failures.append('DESEQ2_REFERENCE_ENV_NOT_PINNED')
    criteria['formal_blocker']='DESeq2 version/design/reference table not pinned; 677 validates only the native endpoint'
    return {'core_science':core,'direction':direction,'summary':summary_score,
            'hardgate_pass':False,'failure_codes':failures,'criteria':criteria}
