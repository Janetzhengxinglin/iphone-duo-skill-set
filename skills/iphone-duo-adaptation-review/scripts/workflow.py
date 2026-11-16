#!/usr/bin/env python3
"""Initialize an interactive review run and seed evidence, without judging pages."""
import argparse
import json
from pathlib import Path
from urllib.parse import urlparse

def write(path,data): path.write_text(json.dumps(data,ensure_ascii=False,indent=2))

def check_intake(d, require_video=True):
    if d.get('schema_version')!='1.0' or not isinstance(d.get('flow'),str) or not d['flow'].strip(): raise ValueError('Flow is required')
    if d.get('form') not in {'outer','inner-landscape','inner-portrait','mixed'}: raise ValueError('Choose display form')
    if d.get('output') not in {'figma','lark'}: raise ValueError('Choose Figma or Lark')
    if d.get('content') not in {'defects-only','defects-and-guidance'}: raise ValueError('Choose report content')
    u=urlparse(d.get('target',''));host=(u.hostname or '').lower()
    if u.scheme!='https': raise ValueError('HTTPS output target required')
    if d['output']=='figma': valid=host in {'figma.com','www.figma.com'} and u.path.startswith('/design/')
    else: valid=(host=='larksuite.com' or host.endswith('.larksuite.com') or host=='feishu.cn' or host.endswith('.feishu.cn')) and u.path.startswith(('/wiki/','/docx/','/drive/'))
    if not valid: raise ValueError('Target does not match chosen output')
    if require_video and not Path(d.get('video','')).is_file(): raise ValueError('Source video missing')
    return d

def seed(run,rule_root):
    intake=check_intake(json.loads((run/'intake.json').read_text()),require_video=False);capture=json.loads((run/'capture.json').read_text())
    if (run/'review.json').exists(): raise ValueError('Review exists; do not overwrite judgment')
    bundle=json.loads((rule_root/'references/rules.json').read_text())
    for page in capture['pages']:
        context=page['context'];form='outer' if context['display']=='outer' else 'inner-'+context['orientation']
        if intake['form']!='mixed' and intake['form']!=form: raise ValueError('Screenshot form conflicts with intake; clarify')
        page['component_inventory']=[]
    d={'schema_version':'1.0','rule_version':bundle['version'],'checklist_version':bundle['version'],'audit_profile':'three-form-screenshot','title':intake['flow']+'｜iPhone Duo 适配审查','scope':intake['flow'],**{k:capture[k] for k in ('videos','pages','evidence')},'checks':[],'check_items':[],'findings':[],'report_groups':[]}
    write(run/'review.json',d);return {'pages':len(d['pages']),'status':'evidence_seeded_not_reviewed'}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);s=p.add_subparsers(dest='command',required=True)
    a=s.add_parser('init');a.add_argument('intake',type=Path);a.add_argument('run',type=Path)
    a=s.add_parser('seed');a.add_argument('run',type=Path);a.add_argument('--rule-root',type=Path,default=Path(__file__).resolve().parents[2]/'iphone-duo-design-guidelines')
    args=p.parse_args()
    if args.command=='init':
        data=check_intake(json.loads(args.intake.read_text()));args.run.mkdir(parents=True,exist_ok=True)
        if (args.run/'intake.json').exists(): raise ValueError('Run intake already exists')
        write(args.run/'intake.json',data);print(args.run)
    else: print(seed(args.run.resolve(),args.rule_root.resolve()))
