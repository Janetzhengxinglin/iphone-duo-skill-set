#!/usr/bin/env python3
"""Independent candidate sampling and evidence extraction; no automatic UI judgment."""
import argparse
import hashlib
import json
import math
import shutil
import tempfile
from pathlib import Path
from image_batches import candidate_plan
from sequential_frames import sequential_sample, extract_frame, probe
from PIL import Image, ImageDraw, ImageFilter

FORMS = {'outer', 'inner-landscape', 'inner-portrait'}

def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for chunk in iter(lambda: f.read(1024*1024), b''): h.update(chunk)
    return h.hexdigest()

def dump(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2),encoding='utf-8')

def frame(video, seconds):
    if not math.isfinite(seconds) or seconds < 0: raise ValueError('Invalid time')
    with tempfile.TemporaryDirectory() as directory:
        path=Path(directory)/'frame.png';extract_frame(video,seconds,path)
        with Image.open(path) as image: return image.convert('RGB')

def sample(video, run, interval=1.0, keep_all=False):
    video = video.resolve(); run = run.resolve()
    if not math.isfinite(interval) or interval <= 0: raise ValueError('Invalid interval')
    target = run/'candidates'
    if target.exists(): raise ValueError('Candidate directory already exists; use a fresh run')
    run.mkdir(parents=True, exist_ok=True); (run/'source').mkdir(exist_ok=True)
    dest = run/'source'/('recording'+video.suffix.lower())
    if dest.exists():
        if sha(dest) != sha(video): raise ValueError('Source video changed')
    else: shutil.copy2(video, dest)
    duration=probe(dest)['duration_s']
    target.mkdir(); rows=[]
    for i,row in enumerate(sequential_sample(dest,target/'raw',interval)):
        raw=Path(row['path'])
        with Image.open(raw) as im:
            preview=im.convert('RGB');preview.thumbnail((200,300))
            name=f'C{i+1:05d}.jpg';preview.save(target/name,quality=85)
        rows.append({'id':f'C{i+1:05d}','time_seconds':row['time_s'],
                     'image':'candidates/'+name,'raw_image':str(raw.relative_to(run)),
                     'raw_sha256':row['sha256'],'visual_sha256':row['visual_sha256'],
                     'size_px':[row['width_px'],row['height_px']],'frame_index':row['frame_index']})
    plan, representatives=candidate_plan(rows,24,keep_all)
    dump(target/'candidate-groups.json',plan)
    for start in range(0,len(representatives),24):
        sheet=Image.new('RGB',(6*220,4*330),'#172033'); draw=ImageDraw.Draw(sheet)
        for j,row in enumerate(representatives[start:start+24]):
            im=Image.open(run/row['image']);x=(j%6)*220;y=(j//6)*330
            sheet.paste(im,(x+(220-im.width)//2,y));draw.text((x+5,y+303),f"{row['id']} {row['time_seconds']:.2f}s",fill='white')
        sheet.save(target/f'sheet-{start//24+1:03d}.jpg',quality=90)
    dump(target/'index.json',{'video':{'id':'V01','file':str(dest),'sha256':sha(dest),'duration_seconds':duration},'interval':interval,'decoder':'sequential-source-pts-v1','candidates':rows,'candidate_groups':'candidates/candidate-groups.json'})
    return {'candidates':len(rows),'representatives':len(representatives),'sheets':len(plan['sheet_candidate_ids']),'index':str(target/'index.json')}

def box(region, size):
    if len(region)!=4 or not all(isinstance(v,(int,float)) and math.isfinite(v) for v in region): raise ValueError('Invalid region')
    x,y,w,h=region
    if x<0 or y<0 or w<=0 or h<=0 or x+w>1 or y+h>1: raise ValueError('Region out of bounds')
    return (round(x*size[0]),round(y*size[1]),round((x+w)*size[0]),round((y+h)*size[1]))

def finalize(run, selection):
    run=run.resolve();spec=json.loads(selection.read_text());index=json.loads((run/'candidates/index.json').read_text())
    if (run/'capture.json').exists(): raise ValueError('Capture exists; use a new revision')
    if sha(index['video']['file'])!=index['video']['sha256']: raise ValueError('Video hash changed')
    if index.get('decoder')=='sequential-source-pts-v1':
        flags=spec.get('capture_review',{})
        if not flags.get('all_candidates_classified') or not flags.get('all_intervals_reviewed') or not flags.get('notes'): raise ValueError('Inspect all candidates and intervals before finalize')
    pages=spec['pages'];by_id={p['id']:p for p in pages}
    if len(by_id)!=len(pages) or not pages: raise ValueError('Missing/duplicate pages')
    coverage=spec['coverage'];ids=[r['candidate_id'] for r in coverage]
    if len(set(ids))!=len(ids) or set(ids)!={r['id'] for r in index['candidates']}: raise ValueError('Incomplete candidate coverage')
    for row in coverage:
        if not row.get('reason') or row['disposition'] not in {'retained','duplicate','browser','non_app','transition','loading'}: raise ValueError('Invalid coverage decision')
        if row['disposition'] in {'retained','duplicate'} and row.get('page_id') not in by_id: raise ValueError('Unknown coverage page')
    supplements=spec.get('supplementary_pages',[])
    supplementary_ids={r.get('page_id') for r in supplements}
    if len(supplementary_ids)!=len(supplements) or not supplementary_ids<=set(by_id): raise ValueError('Invalid supplementary pages')
    for row in supplements:
        if not row.get('reason') or row.get('time_seconds')!=by_id[row['page_id']]['time_seconds']: raise ValueError('Supplement needs matching time and reason')
    if not set(by_id) <= {r.get('page_id') for r in coverage if r['disposition']=='retained'} | supplementary_ids: raise ValueError('Page has no retained candidate or supplementary source')
    if index.get('decoder')=='sequential-source-pts-v1':
        for candidate in index['candidates']:
            if sha(run/candidate['raw_image'])!=candidate['raw_sha256']:raise ValueError('Candidate evidence changed')
    # Validate selection before writing any evidence.
    for p in pages:
        if not p.get('title') or not p.get('state') or p.get('form') not in FORMS: raise ValueError('Missing title/state/form')
        if not str(p['id']).replace('-','').replace('_','').isalnum(): raise ValueError('Unsafe page id')
        if not isinstance(p['time_seconds'],(int,float)) or not math.isfinite(p['time_seconds']) or not 0<=p['time_seconds']<index['video']['duration_seconds']: raise ValueError('Invalid time')
    raw_dir=run/'evidence/raw';images=run/'evidence/images';raw_dir.mkdir(parents=True,exist_ok=True);images.mkdir(parents=True,exist_ok=True)
    evidence=[];out_pages=[];audit=[]
    for p in pages:
        matches=[c for c in index['candidates'] if (c['id']==p['candidate_id'] if p.get('candidate_id') else abs(c['time_seconds']-p['time_seconds'])<1e-6)]
        if p.get('candidate_id') and (len(matches)!=1 or abs(matches[0]['time_seconds']-p['time_seconds'])>=1e-6): raise ValueError('Candidate and selected time disagree')
        raw=raw_dir/(p['id']+'.png')
        if index.get('decoder')=='sequential-source-pts-v1' and matches:
            candidate=run/matches[0]['raw_image']
            if sha(candidate)!=matches[0]['raw_sha256']: raise ValueError('Candidate evidence changed')
            shutil.copyfile(candidate,raw)
            with Image.open(raw) as original: im=original.convert('RGB')
        else:
            im=frame(index['video']['file'],p['time_seconds']);im.save(raw)
        crop=p.get('crop_px',[0,0,im.width,im.height]);x,y,w,h=crop
        if any(not isinstance(v,int) for v in crop) or min(x,y)<0 or min(w,h)<=0 or x+w>im.width or y+h>im.height: raise ValueError('Invalid raw crop')
        im=im.crop((x,y,x+w,y+h))
        for privacy in p.get('privacy',[]):
            region=privacy['region'];b=box(region,im.size)
            if not privacy.get('type') or not privacy.get('reason'): raise ValueError('Missing privacy rationale')
            large=region[2]>.82 or region[3]>.22 or region[2]*region[3]>.08
            allowed=privacy.get('allow_large') and privacy['type'] in {'face','document_photo','identity_document','full_address','video_selfie'}
            if large and not allowed: raise ValueError('Privacy region too broad')
            im.paste(im.crop(b).filter(ImageFilter.GaussianBlur(32)),b);audit.append({'page_id':p['id'],**privacy})
        path=images/(p['id']+'.png');im.save(path);eid=p['id']+'-E'
        form=p['form'];context={'display':'outer' if form=='outer' else 'inner','orientation':'landscape' if form=='inner-landscape' else 'portrait','posture':'closed' if form=='outer' else 'open','container':p.get('container','page')}
        out_pages.append({'id':p['id'],'title':p['title'],'state':p['state'],'context':context,'evidence_ids':[eid]})
        evidence.append({'id':eid,'page_id':p['id'],'video_id':index['video']['id'],'time_seconds':p['time_seconds'],'image':str(path.relative_to(run)),'raw_image':str(raw.relative_to(run)),'image_sha256':sha(path),'raw_sha256':sha(raw),'size_px':list(im.size),'crop_from_raw_px':crop})
    result={'schema_version':'1.0','videos':[index['video']],'pages':out_pages,'evidence':evidence,'coverage':coverage,'candidate_index':'candidates/index.json','privacy_audit':audit,'capture_review':spec.get('capture_review',{}),'supplementary_pages':supplements}
    dump(run/'selection.json',spec);dump(run/'capture.json',result)
    return {'pages':len(pages),'evidence':len(evidence)}

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);sub=ap.add_subparsers(dest='command',required=True)
    s=sub.add_parser('sample');s.add_argument('video',type=Path);s.add_argument('run',type=Path);s.add_argument('--interval',type=float,default=1.0);s.add_argument('--keep-all-candidates',action='store_true')
    f=sub.add_parser('frame');f.add_argument('video',type=Path);f.add_argument('seconds',type=float);f.add_argument('output',type=Path)
    z=sub.add_parser('finalize');z.add_argument('run',type=Path);z.add_argument('selection',type=Path)
    a=ap.parse_args()
    if a.command=='sample': print(sample(a.video,a.run,a.interval,a.keep_all_candidates))
    elif a.command=='finalize': print(finalize(a.run,a.selection))
    else:
        if a.output.exists(): raise ValueError('Evidence already exists; do not overwrite')
        a.output.parent.mkdir(parents=True,exist_ok=True);frame(a.video,a.seconds).save(a.output);print(a.output)
