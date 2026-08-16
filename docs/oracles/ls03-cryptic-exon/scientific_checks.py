from __future__ import annotations
import csv,json,math
from pathlib import Path
ACCEPTED=True
def _rows(p):
    try:
        with p.open(encoding='utf-8-sig',newline='') as h:return list(csv.DictReader(h,delimiter='\t'))
    except Exception:return []
def check(workspace:Path):
    g=json.loads((Path(__file__).parent/'gold.json').read_text());rows=_rows(workspace/'output'/'cryptic_exon.tsv');one=len(rows)==1;r=rows[0] if one else {};gene=str(r.get('gene','')).upper()=='GNG10';chrom=str(r.get('chrom','')).lower().replace('chr','')=='9'
    def eq(k):
        try:return int(float(r.get(k)))==g[k]
        except Exception:return False
    start=eq('start');end=eq('end')
    try:left=int(float(r.get('left_junction_reads')))==32;right=int(float(r.get('right_junction_reads')))==25
    except Exception:left=right=False
    expression=bool(r.get('expression_evidence','').strip());jr=_rows(workspace/'output'/'junctions.tsv');jcov=len(jr)==2;coords=[];supports=[];novel=[]
    expected={(111661716,111664536,32),(111664590,111666814,25)}
    for x in jr:
        try:coords.append((int(float(x.get('intron_start',x.get('start')))),int(float(x.get('intron_end',x.get('end')))),int(float(x.get('read_support',x.get('reads'))))))
        except Exception:coords.append((-1,-1,-1))
        novel.append(str(x.get('novel','')).lower() in {'true','1','yes'})
    jcoords=set(coords)==expected;core=(10 if gene else 0)+(6 if chrom else 0)+(8 if start and end else 0)+(8 if left and right else 0)+(8 if jcov and jcoords and all(novel) else 0)
    decision=gene and start and end and jcoords and all(novel) and expression
    report=(workspace/'output'/'report.md').read_text(errors='replace').lower() if (workspace/'output'/'report.md').is_file() else '';summary='gng10' in report and ('111664537' in report or '111,664,537' in report) and ('32' in report and '25' in report) and ('ensembl' in report and '112' in report)
    failures=[]
    for ok,code in [(one,'ONE_EXON'),(gene,'GENE'),(chrom,'CHROM'),(start and end,'EXON_COORDS'),(left and right,'READ_SUPPORT'),(jcov and jcoords,'JUNCTION_COORDS'),(all(novel),'NOVELTY'),(expression,'EXPRESSION_EVIDENCE'),(summary,'REPORT')]:
        if not ok:failures.append(code+'_MISMATCH')
    return {'core_science':core,'direction':15 if decision else 0,'summary':5 if summary else 0,'hardgate_pass':one and core==40 and decision,'failure_codes':failures,'criteria':{'one_exon':one,'GNG10':gene,'chr9':chrom,'exon_111664537_111664589':start and end,'supports_32_and_25':left and right,'two_novel_junctions_exact':jcov and jcoords and all(novel),'expression_evidence':expression,'report_annotation_and_support':summary}}
