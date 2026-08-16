from __future__ import annotations
import json,math
from pathlib import Path
ACCEPTED=True
def check(workspace:Path):
    g=json.loads((Path(__file__).parent/'gold.json').read_text())
    try:d=json.loads((workspace/'output'/'build_call.json').read_text())
    except Exception:d={}
    label=str(d.get('build','')).lower().replace('grch37','hg19');build=label in {'hg19','hg19/hg19','hg19 (grch37)','hg19/hg19 (grch37)'} or 'hg19' in label
    def eq(k):
        try:return int(d.get(k))==g[k]
        except Exception:return False
    n=eq('n_variants_checked');m=eq('n_ref_matches');mm=eq('n_ref_mismatches');evidence=bool(str(d.get('evidence','')).strip());conf=str(d.get('confidence','')).lower() in {'high','very high','1','1.0'}
    core=(12 if n else 0)+(12 if m else 0)+(8 if mm else 0)+(8 if build else 0)
    report=(workspace/'output'/'report.md').read_text(errors='replace').lower() if (workspace/'output'/'report.md').is_file() else '';summary='hg19' in report and ('84664' in report or '84,664' in report) and ('ref' in report or 'allele' in report)
    failures=[]
    for ok,code in [(build,'BUILD'),(n,'VARIANT_COUNT'),(m,'REF_MATCH'),(mm,'REF_MISMATCH'),(evidence,'EVIDENCE'),(conf,'CONFIDENCE'),(summary,'REPORT')]:
        if not ok:failures.append(code+'_MISMATCH')
    return {'core_science':core,'direction':15 if build and conf and evidence else 0,'summary':5 if summary else 0,'hardgate_pass':core==40 and evidence and conf,'failure_codes':failures,'criteria':{'hg19_call':build,'variants_84664':n,'matches_84664':m,'mismatches_zero':mm,'high_confidence':conf,'allele_evidence_present':evidence,'report_consistent':summary}}
