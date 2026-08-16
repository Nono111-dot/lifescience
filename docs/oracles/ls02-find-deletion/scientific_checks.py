from __future__ import annotations
import csv,json,math
from pathlib import Path
ACCEPTED=True
def check(workspace:Path):
    g=json.loads((Path(__file__).parent/'gold.json').read_text())
    try:
        with (workspace/'output'/'deletion.tsv').open(encoding='utf-8-sig',newline='') as h:rows=list(csv.DictReader(h,delimiter='\t'))
    except Exception:rows=[]
    one=len(rows)==1;r=rows[0] if one else {}
    chrom=str(r.get('chrom','')).lower().replace('chr','')=='22'
    def near(k,tol=50000):
        try:return abs(float(r.get(k))-g[k])<=tol
        except Exception:return False
    start=near('start_100kb');end=near('end_100kb');size=near('size_bp',100000);support=('coverage' in r.get('supporting_signals','').lower() and ('pair' in r.get('supporting_signals','').lower() or 'discord' in r.get('supporting_signals','').lower()))
    try:q=json.loads((workspace/'output'/'qc.json').read_text())
    except Exception:q={}
    try:pair_ok=int(q.get('total_pairs',-1))==g['total_pairs'];map_ok=int(q.get('mapped_reads',-1))==g['mapped_reads'];span_ok=int(q.get('breakpoint_spanning_pairs',q.get('discordant_pairs',-1)))>=5
    except Exception:pair_ok=map_ok=span_ok=False
    core=(8 if chrom else 0)+(10 if start else 0)+(10 if end else 0)+(6 if size else 0)+(6 if pair_ok and map_ok and span_ok else 0)
    decision=chrom and start and end and size and support and span_ok
    report=(workspace/'output'/'report.md').read_text(errors='replace').lower() if (workspace/'output'/'report.md').is_file() else '';summary=('chr22' in report or 'chromosome 22' in report) and ('20,000,000' in report or '20.0 mb' in report or '20 mb' in report) and ('21,000,000' in report or '21.0 mb' in report or '21 mb' in report) and ('100 kb' in report or 'precision' in report)
    failures=[]
    for ok,code in [(one,'ONE_EVENT'),(chrom,'CHROMOSOME'),(start,'START'),(end,'END'),(size,'SIZE'),(support,'SUPPORT_TEXT'),(pair_ok,'PAIR_QC'),(map_ok,'MAPPED_QC'),(span_ok,'BREAKPOINT_SUPPORT'),(summary,'REPORT')]:
        if not ok:failures.append(code+'_MISMATCH')
    return {'core_science':core,'direction':15 if decision else 0,'summary':5 if summary else 0,'hardgate_pass':one and decision and pair_ok and map_ok,'failure_codes':failures,'criteria':{'one_interval':one,'chr22':chrom,'start_20Mb_plusminus50kb':start,'end_21Mb_plusminus50kb':end,'size_1Mb_plusminus100kb':size,'coverage_and_pair_evidence':support,'total_pairs_exact':pair_ok,'mapped_reads_exact':map_ok,'at_least_5_spanning_pairs':span_ok,'report_precision_limit':summary}}
