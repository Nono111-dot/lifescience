from __future__ import annotations
import csv, json, math, re
from pathlib import Path

# Checker exists, but formal acceptance remains blocked until Reactome_2022 is archived
# and the enrichment table is independently reproduced from the frozen counts.
ACCEPTED = False

def check(workspace: Path):
    out=workspace/'output'; failures=[]; criteria={}
    try:
        with (out/'pathway_enrichment.csv').open(encoding='utf-8-sig',newline='') as f: rows=list(csv.DictReader(f))
    except Exception: rows=[]
    try: call=json.loads((out/'mechanism_call.json').read_text(encoding='utf-8'))
    except Exception: call={}
    text=json.dumps(call,ensure_ascii=False).lower()
    native_semantic=bool('tp53' in text and ('cell cycle' in text or 'cell_cycle' in text))
    fields_ok=bool(rows) and all(all(k in r for k in ('pathway_id','pathway_name','overlap','p_value','padj','direction')) for r in rows)
    finite=True
    for r in rows:
        try:
            p=float(r['p_value']); q=float(r['padj']); finite &= math.isfinite(p) and math.isfinite(q) and 0<=p<=1 and 0<=q<=1
        except Exception: finite=False
    core=(15 if fields_ok else 0)+(10 if finite and rows else 0)+(15 if native_semantic else 0)
    direction=15 if native_semantic else 0
    report=(out/'report.md').read_text(encoding='utf-8',errors='replace').lower() if (out/'report.md').is_file() else ''
    summary=5 if native_semantic and 'tp53' in report and ('cell cycle' in report or 'cell-cycle' in report) else 0
    if not fields_ok: failures.append('REACTOME_TABLE_SCHEMA')
    if not finite: failures.append('REACTOME_VALUES_INVALID')
    if not native_semantic: failures.append('BIX_NATIVE_MECHANISM_MISMATCH')
    failures.append('REACTOME_2022_NOT_PINNED')
    criteria.update(table_schema=fields_ok,finite_probabilities=finite,native_tp53_cell_cycle=native_semantic,
                    formal_blocker='Reactome_2022 resource and reference run not pinned')
    return {'core_science':core,'direction':direction,'summary':summary,'hardgate_pass':False,
            'failure_codes':failures,'criteria':criteria}
