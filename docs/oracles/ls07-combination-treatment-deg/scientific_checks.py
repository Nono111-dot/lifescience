from __future__ import annotations
import csv,gzip,json,math
from pathlib import Path
ACCEPTED=True
NULL={'','na','nan','null','none'}
def _table(path,compressed=False):
    try:
        h=gzip.open(path,'rt',encoding='utf-8-sig',newline='') if compressed else path.open(encoding='utf-8-sig',newline='')
        with h:return list(csv.DictReader(h))
    except Exception:return []
def _id(r):return r.get('gene_id') or r.get('') or r.get('Unnamed: 0') or ''
def _num(a,b):
    if str(b).strip().lower() in NULL:return str(a).strip().lower() in NULL
    try:return math.isclose(float(a),float(b),rel_tol=2e-5,abs_tol=1e-8)
    except Exception:return False
def _bool(x):return str(x).strip().lower() in {'true','1','yes'}
def check(workspace:Path):
    gold=_table(Path(__file__).parent/'reference_results.csv.gz',True);rows=_table(workspace/'output'/'differential_expression.csv');gb={_id(r):r for r in gold};by={_id(r):r for r in rows};coverage=len(rows)==len(by)==len(gold)==18029 and set(by)==set(gb);stats=[];passes=[]
    for gid,g in gb.items():
        r=by.get(gid,{})
        stats.append(all(_num(r.get(k,''),g.get(k,'')) for k in ('baseMean','log2FoldChange','lfcSE','stat','pvalue','padj')))
        passes.append(_bool(r.get('pass'))==_bool(g.get('pass_strict')))
    try:s=json.loads((workspace/'output'/'summary.json').read_text())
    except Exception:s={}
    count_ok=int(s.get('passing_genes',s.get('pass_count',-1)))==555;contrast=str(s.get('contrast','')).lower();contrast_ok='cisplatin_ic50_cbd_ic50' in contrast and 'dmso' in contrast and str(s.get('design','group')).lower().replace('~','').strip()=='group'
    core=(12 if coverage else 0)+(20 if all(stats) else 0)+(8 if all(passes) else 0);direction=count_ok and contrast_ok
    report=(workspace/'output'/'report.md').read_text(errors='replace').lower() if (workspace/'output'/'report.md').is_file() else '';summary='555' in report and '0.05' in report and '0.5' in report and ('strict' in report or 'greater than' in report)
    failures=[]
    for ok,code in [(coverage,'GENE_COVERAGE'),(all(stats),'DE_STATISTICS'),(all(passes),'PASS_PREDICATE'),(count_ok,'PASS_COUNT'),(contrast_ok,'CONTRAST_DESIGN'),(summary,'REPORT')]:
        if not ok:failures.append(code+'_MISMATCH')
    return {'core_science':core,'direction':15 if direction else 0,'summary':5 if summary else 0,'hardgate_pass':coverage and all(stats) and all(passes) and direction,'failure_codes':failures,'criteria':{'18029_unique_genes':coverage,'statistics_correct_rows':sum(stats),'statistics_total':len(stats),'pass_correct_rows':sum(passes),'local_pass_count_555':count_ok,'six_sample_group_contrast':contrast_ok,'report_thresholds_and_count':summary}}
