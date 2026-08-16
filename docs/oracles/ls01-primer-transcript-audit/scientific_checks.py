from __future__ import annotations
import csv,json,math,re
from pathlib import Path
ACCEPTED=True
def _bool(x): return str(x).strip().lower() in {'true','1','yes'}
def check(workspace:Path):
    try:
        with (workspace/'output'/'primer_audit.csv').open(encoding='utf-8-sig',newline='') as h:rows=list(csv.DictReader(h))
    except Exception:rows=[]
    gold=json.loads((Path(__file__).parent/'gold.json').read_text())['rows'];by={r.get('pair_id',''):r for r in rows};ids=len(rows)==len(by)==3 and set(by)=={g['pair_id'] for g in gold}
    hits=[];lens=[];cds=[];status=[];reason=[]
    for g in gold:
        r=by.get(g['pair_id'],{}); hits.append(r.get('transcripts_matched','').strip()==g['transcripts_matched'])
        if g['amplicon_length'] is None:lens.append(r.get('amplicon_length','').strip().lower() in {'','null','na','none'})
        else:
            try:lens.append(int(float(r.get('amplicon_length','nan')))==g['amplicon_length'])
            except Exception:lens.append(False)
        cds.append(_bool(r.get('cds_compatible')) is False);status.append(r.get('status','').lower()==g['status']);reason.append('cds' in r.get('reason','').lower() and ('range' in r.get('reason','').lower() or 'metadata' in r.get('reason','').lower()))
    core=(12 if all(hits) else 0)+(12 if all(lens) else 0)+(8 if all(cds) else 0)+(8 if all(reason) else 0)
    report=(workspace/'output'/'report.md').read_text(errors='replace').lower() if (workspace/'output'/'report.md').is_file() else ''
    summary=('101-700' in report or 'cds' in report) and ('out of range' in report or 'invalid' in report or 'malformed' in report) and ('no valid' in report or 'none' in report)
    failures=[]
    for ok,code in [(ids,'PAIR_COVERAGE'),(all(hits),'BINDING'),(all(lens),'AMPLICON_LENGTH'),(all(cds),'CDS_COMPATIBILITY'),(all(reason),'METADATA_ERROR'),(all(status),'STATUS'),(summary,'REPORT')]:
        if not ok:failures.append(code+'_MISMATCH')
    return {'core_science':core,'direction':15 if all(status) else 0,'summary':5 if summary else 0,'hardgate_pass':ids and all(hits) and all(lens) and all(cds) and all(reason) and all(status),'failure_codes':failures,'criteria':{'all_pairs_once':ids,'binding_3_of_3':sum(hits),'amplicon_3_of_3':sum(lens),'cds_incompatibility_3_of_3':sum(cds),'metadata_error_3_of_3':sum(reason),'status_3_of_3':sum(status),'report_no_valid_pair':summary}}
