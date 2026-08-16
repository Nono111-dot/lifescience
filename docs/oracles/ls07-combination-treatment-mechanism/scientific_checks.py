from __future__ import annotations
import csv,gzip,json,math,re
from pathlib import Path
ACCEPTED=True
def _rows(path,gz=False):
    try:
        h=gzip.open(path,'rt',encoding='utf-8-sig',newline='') if gz else path.open(encoding='utf-8-sig',newline='')
        with h:return list(csv.DictReader(h))
    except Exception:return []
def _close(a,b):
    try:return math.isclose(float(a),float(b),rel_tol=2e-5,abs_tol=1e-8)
    except Exception:return False
def check(workspace:Path):
    gold=_rows(Path(__file__).parent/'reference_enrichment.csv.gz',True);rows=_rows(workspace/'output'/'pathway_enrichment.csv');gb={r['term']:r for r in gold};by={r.get('term',''):r for r in rows};coverage=len(rows)==len(by)==len(gold)==1818 and set(by)==set(gb);values=[]
    for term,g in gb.items():
        r=by.get(term,{});values.append(all(_close(r.get(k,''),g[k]) for k in ('overlap_n','term_size','p_value','adjusted_p_value','odds_ratio','query_size','background_size')) and set(filter(None,re.split(r'[;,|]',r.get('overlap_genes',''))))==set(filter(None,g['overlap_genes'].split(';'))))
    try:c=json.loads((workspace/'output'/'mechanism_call.json').read_text())
    except Exception:c={}
    mech=str(c.get('primary_mechanism',c.get('mechanism',''))).lower();term=str(c.get('top_term',''));call_ok='tp53' in mech and 'cell cycle' in mech and term=='TP53 Regulates Transcription Of Cell Cycle Genes R-HSA-6791312'
    top=by.get('TP53 Regulates Transcription Of Cell Cycle Genes R-HSA-6791312',{});top_ok=_close(top.get('overlap_n'),8) and _close(top.get('term_size'),49) and _close(top.get('odds_ratio'),7.239451664589638)
    core=(28 if coverage and all(values) else 0)+(12 if top_ok else 0)
    report=(workspace/'output'/'report.md').read_text(errors='replace').lower() if (workspace/'output'/'report.md').is_file() else '';summary='tp53' in report and 'cell cycle' in report and ('8/49' in report or ('8' in report and '49' in report)) and ('not significant' in report or 'adjusted' in report or 'fdr' in report)
    failures=[]
    for ok,code in [(coverage,'PATHWAY_COVERAGE'),(all(values),'ENRICHMENT_VALUES'),(top_ok,'TOP_TERM_METRICS'),(call_ok,'MECHANISM_CALL'),(summary,'REPORT')]:
        if not ok:failures.append(code+'_MISMATCH')
    return {'core_science':core,'direction':15 if call_ok else 0,'summary':5 if summary else 0,'hardgate_pass':coverage and all(values) and top_ok and call_ok,'failure_codes':failures,'criteria':{'1818_pathways_exact':coverage,'pathway_rows_correct':sum(values),'top_overlap_8_of_49_and_OR_7.239':top_ok,'TP53_cell_cycle_call':call_ok,'report_FDR_restraint':summary}}
