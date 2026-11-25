#!/usr/bin/env python3
"""Initialize an interactive review run and seed evidence, without judging pages."""
import argparse
import json
from pathlib import Path
from urllib.parse import urlparse

def write(path,data): path.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')

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

def merge(captures, run):
    """Merge complete native captures; preserve all state and source references."""
    import hashlib
    import os
    run=Path(run).resolve(); destination=run/'capture.json'
    if destination.exists(): raise ValueError('Capture exists; use a new revision')
    paths=[Path(p).resolve() for p in captures]
    if not paths or len(set(paths))!=len(paths): raise ValueError('Missing or duplicate capture source')
    merged={'schema_version':'1.0','videos':[],'pages':[],'evidence':[],
            'coverage':[],'privacy_audit':[],'capture_sources':[],'supplementary_pages':[]}
    def resolve(source, value):
        path=Path(value);return path.resolve() if path.is_absolute() else (source.parent/path).resolve()
    def verified(source,value,digest):
        path=resolve(source,value)
        if hashlib.sha256(path.read_bytes()).hexdigest()!=digest: raise ValueError('Source changed: '+str(path))
        return os.path.relpath(path,run)
    seen_videos=set()
    for index, source in enumerate(paths):
        data=json.loads(source.read_text(encoding='utf-8'))
        if data.get('schema_version')!='1.0': raise ValueError('Use Apple capture schema')
        prefix='recording-%02d-'%index
        def new(value):return prefix+value
        pages={p['id'] for p in data['pages']}; evidence={e['id'] for e in data['evidence']}
        videos={v['id'] for v in data['videos']}
        if not pages or len(pages)!=len(data['pages']) or len(evidence)!=len(data['evidence']) or len(videos)!=len(data['videos']): raise ValueError('Missing or duplicate IDs')
        ci=resolve(source,data['candidate_index'])
        candidate_index=json.loads(ci.read_text(encoding='utf-8'))
        coverage=data['coverage'];candidate_ids={r['id'] for r in candidate_index['candidates']}
        if len(coverage)!=len(candidate_ids) or {r['candidate_id'] for r in coverage}!=candidate_ids: raise ValueError('Incomplete candidate coverage')
        if candidate_index.get('decoder')=='sequential-source-pts-v1':
            flags=data.get('capture_review',{})
            if not flags.get('all_candidates_classified') or not flags.get('all_intervals_reviewed') or not flags.get('notes'):raise ValueError('Capture inspection incomplete')
        for video in data['videos']:
            if video['sha256'] in seen_videos: raise ValueError('Repeated recording; reconcile source states before merge')
            seen_videos.add(video['sha256'])
            merged['videos'].append({**video,'id':new(video['id']),'file':verified(source,video['file'],video['sha256'])})
        for item in data['evidence']:
            if item['page_id'] not in pages or item['video_id'] not in videos:raise ValueError('Unknown evidence reference')
            merged['evidence'].append({**item,'id':new(item['id']),'page_id':new(item['page_id']),'video_id':new(item['video_id']),
                'image':verified(source,item['image'],item['image_sha256']),
                'raw_image':verified(source,item['raw_image'],item['raw_sha256'])})
        for page in data['pages']:
            if not page.get('evidence_ids') or not set(page['evidence_ids'])<=evidence:raise ValueError('Page evidence missing')
            merged['pages'].append({**page,'id':new(page['id']),'evidence_ids':[new(e) for e in page['evidence_ids']]})
        for row in coverage:
            if not row.get('reason') or row['disposition'] not in {'retained','duplicate','browser','non_app','transition','loading'}:raise ValueError('Invalid candidate classification')
            if row['disposition'] in {'retained','duplicate'} and row.get('page_id') not in pages:raise ValueError('Coverage page missing')
            merged['coverage'].append({**row,'candidate_id':new(row['candidate_id']),**({'page_id':new(row['page_id'])} if row.get('page_id') else {})})
        supplements=data.get('supplementary_pages',[])
        supplemental_ids={r.get('page_id') for r in supplements}
        if len(supplemental_ids)!=len(supplements) or not supplemental_ids<=pages or any(not r.get('reason') for r in supplements):raise ValueError('Invalid supplementary source')
        if not pages <= {r.get('page_id') for r in coverage if r['disposition']=='retained'} | supplemental_ids:raise ValueError('Page has no retained candidate or supplementary source')
        merged['supplementary_pages'] += [{**r,'page_id':new(r['page_id'])} for r in supplements]
        merged['privacy_audit'] += [{**a,'page_id':new(a['page_id'])} for a in data.get('privacy_audit',[])]
        merged['capture_sources'].append({'path':os.path.relpath(source,run),'sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
                                         'candidate_index':os.path.relpath(ci,run),'candidate_index_sha256':hashlib.sha256(ci.read_bytes()).hexdigest(),'id_prefix':prefix})
    merged['capture_review']={'all_candidates_classified':True,'all_intervals_reviewed':True,'notes':'Complete source captures merged; final inventory still requires actual review'}
    run.mkdir(parents=True,exist_ok=True);write(destination,merged)
    return {'pages':len(merged['pages']),'sources':len(paths),'status':'merged_not_reviewed'}

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
    a=s.add_parser('merge');a.add_argument('run',type=Path);a.add_argument('captures',type=Path,nargs='+')
    a=s.add_parser('seed');a.add_argument('run',type=Path);a.add_argument('--rule-root',type=Path,default=Path(__file__).resolve().parents[2]/'iphone-duo-design-guidelines')
    args=p.parse_args()
    if args.command=='init':
        data=check_intake(json.loads(args.intake.read_text()));args.run.mkdir(parents=True,exist_ok=True)
        if (args.run/'intake.json').exists(): raise ValueError('Run intake already exists')
        write(args.run/'intake.json',data);print(args.run)
    elif args.command=='merge': print(merge(args.captures,args.run))
    else: print(seed(args.run.resolve(),args.rule_root.resolve()))
