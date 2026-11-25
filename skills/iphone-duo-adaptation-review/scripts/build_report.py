#!/usr/bin/env python3
"""Build concise channel-neutral reports from already validated screenshot judgments."""
import argparse
import hashlib
import html
import json
import shutil
import sys
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from workflow import check_intake

def dump(path,data):path.write_text(json.dumps(data,ensure_ascii=False,indent=2))
def esc(s):return html.escape(str(s),quote=True)
def hashfile(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def reference_delivery(ref):
    from urllib.parse import urlparse, parse_qs
    import re
    source_type=ref.get('source_type')
    resource=ref.get('resource_url','')
    link=urlparse(resource)
    if source_type is None and link.hostname in {'figma.com','www.figma.com'}:
        source_type='apple_ui_kit'
    result={'source_type':source_type} if source_type else {}
    if source_type!='apple_ui_kit':return result
    match=re.match(r'^/(?:design|file)/([^/]+)(?:/branch/([^/]+))?',link.path)
    node_id=parse_qs(link.query).get('node-id',[''])[0].replace('-',':')
    if link.scheme!='https' or link.hostname not in {'figma.com','www.figma.com'} or not match or not re.fullmatch(r'\d+:\d+',node_id):
        raise ValueError('UI Kit requires a Figma resource URL pointing to its source Frame')
    result['figma_delivery']={'preferred':'native_frame','native_source':{'file_key':match.group(2) or match.group(1),'node_id':node_id,'url':resource},'image_role':'preview_or_document_export'}
    return result

def reference_numbers(ref,selected_numbers):
    numbers=ref.get('problem_numbers')
    if not isinstance(numbers,list) or not numbers or not set(numbers)<=selected_numbers:
        raise ValueError('Official figure must explicitly map to current problem_numbers')
    if len(numbers)!=len(set(numbers)):raise ValueError('Duplicate official figure problem number')
    return numbers

def annotation_geometry(size,targets,style):
    factor=min(1,style['image_max_width']/size[0],style['image_max_height']/size[1]);w=round(size[0]*factor);h=round(size[1]*factor)
    rail=style['rail_px'];radius=style['label_radius_px'];used={s:[] for s in ('left','right','top','bottom')};items=[]
    for number,a in sorted(targets,key=lambda r:r[1]['region'][1]):
        x,y,rw,rh=a['region'];rect=[rail+x*w,rail+y*h,rw*w,rh*h]
        distances={'left':x*w,'right':(1-x-rw)*w,'top':y*h,'bottom':(1-y-rh)*h}
        side=a.get('side',min(distances,key=distances.get))
        if side not in used:raise ValueError('Invalid annotation side')
        vertical=side in ('left','right');limit=h if vertical else w
        desired=(y+rh/2)*h if vertical else (x+rw/2)*w
        coordinate=max(radius+3,min(limit-radius-3,desired))
        for prev in used[side]:
            if abs(coordinate-prev)<style['label_gap_px']:coordinate=prev+style['label_gap_px']
        if coordinate>limit-radius-3:raise ValueError('Labels overlap; split annotation views')
        used[side].append(coordinate)
        if vertical:
            cx=rail/2 if side=='left' else rail+w+rail/2;cy=rail+coordinate
            point=[rect[0] if side=='left' else rect[0]+rect[2],rail+desired]
            edge=[cx+radius if side=='left' else cx-radius,cy]
        else:
            cx=rail+coordinate;cy=rail/2 if side=='top' else rail+h+rail/2
            point=[rail+desired,rect[1] if side=='top' else rect[1]+rect[3]]
            edge=[cx,cy+radius if side=='top' else cy-radius]
        items.append({'number':number,'region':a['region'],'side':side,'rect_px':rect,'label_center_px':[cx,cy],'line_px':[point,edge]})
    return {'image_size_px':[w,h],'canvas_size_px':[w+2*rail,h+2*rail],'image_offset_px':[rail,rail],'rail_px':rail,'annotations':items}

def annotate(path,out,geo,style):
    im=Image.open(path).convert('RGB').resize(tuple(geo['image_size_px']),Image.Resampling.LANCZOS)
    canvas=Image.new('RGB',tuple(geo['canvas_size_px']),style['background']);canvas.paste(im,tuple(geo.get('image_offset_px',[geo['rail_px'],0])));d=ImageDraw.Draw(canvas)
    font=None
    for fp in ['/System/Library/Fonts/Supplemental/Arial Bold.ttf','/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf']:
        if Path(fp).exists():font=ImageFont.truetype(fp,20);break
    font=font or ImageFont.load_default();r=style['label_radius_px']
    for a in geo['annotations']:
        x,y,w,h=a['rect_px'];cx,cy=a['label_center_px'];d.rectangle([x,y,x+w,y+h],outline=style['target'],width=2)
        d.line([tuple(p) for p in a['line_px']],fill=style['annotation'],width=2)
        d.ellipse([cx-r,cy-r,cx+r,cy+r],fill=style['annotation']);d.text((cx,cy),str(a['number']),fill=style['annotation_text'],font=font,anchor='mm')
    canvas.save(out)

def choose_examples(groups, findings, by_e, by_p):
    """Cover all problem numbers with shared pages; each number has one owner."""
    preferred={r['evidence_key'] for g in groups for r in g['representatives']}
    candidates={}
    for f in findings:
        for eid in f['evidence_ids']:
            candidates.setdefault(eid,set()).add(f['number'])
    uncovered={g['number'] for g in groups}; result=[]
    order={eid:i for i,eid in enumerate(by_e)}
    while uncovered:
        eid=max(candidates,key=lambda e:(len(candidates[e]&uncovered),e in preferred,-order[e]))
        owned=candidates[eid]&uncovered
        if not owned:raise ValueError('Missing representative for problem number')
        result.append({'evidence_key':eid,'title':by_p[by_e[eid]['page_id']]['title'],'problem_numbers':sorted(owned)})
        uncovered-=owned
    for g in groups:
        g['representatives']=[{'evidence_key':r['evidence_key'],'title':r['title']} for r in result if g['number'] in r['problem_numbers']]
    return result

def build(run,rule_root,style_path):
    intake=check_intake(json.loads((run/'intake.json').read_text()),require_video=False)
    sys.path.insert(0,str(rule_root/'scripts'))
    from validate_review import validate
    validate(run/'review.json',rule_root)
    data=json.loads((run/'review.json').read_text());capture=json.loads((run/'capture.json').read_text())
    if {p['id'] for p in data['pages']}!={p['id'] for p in capture['pages']}:raise ValueError('Not all captured pages reviewed')
    for key in ('id','page_id','video_id','image','image_sha256','size_px','time_seconds'):
        if {e['id']:e[key] for e in data['evidence']}!={e['id']:e[key] for e in capture['evidence']}:raise ValueError('Review evidence differs from capture')
    selected=[f for f in data['findings'] if f['decision']=='issue' or (f['decision']=='guidance_deviation' and intake['content']=='defects-and-guidance')]
    groups={}
    for f in selected:groups.setdefault(f['group_id'],[]).append(f)
    specs={g['group_id']:g for g in data.get('report_groups',[])}
    if len(specs)!=len(data.get('report_groups',[])):raise ValueError('Duplicate report group')
    if not set(groups)<=set(specs):raise ValueError('Write one concise explanation per group')
    style=json.loads(style_path.read_text());out=run/'report'
    if out.exists():raise ValueError('Report exists; preserve it and use a new revision directory')
    assets={};by_e={e['id']:e for e in data['evidence']};by_p={p['id']:p for p in data['pages']}
    result_groups=[]
    for gid,rows in sorted(groups.items(),key=lambda r:r[1][0]['number']):
        s=specs[gid]
        if not all(isinstance(s.get(k),str) and s[k].strip() for k in ('problem_type','problem_point','basis_zh')):raise ValueError('Missing concise group copy')
        if len({f['decision'] for f in rows})!=1:raise ValueError('Do not merge guidance and visible defects')
        owned={eid for f in rows for eid in f['evidence_ids']};reps=s['representative_evidence_ids']
        if not reps or not set(reps)<=owned:raise ValueError('Invalid representative screenshot')
        # Representatives must actually illustrate every referenced rule in this group.
        if {f['rule_id'] for f in rows}!={f['rule_id'] for f in rows if set(f['evidence_ids'])&set(reps)}:raise ValueError('Representatives do not cover group rules')
        bases=[]
        for f in rows:
            b=f['basis'];entry={'label':'官方依据','url':b['url'],'summary':b.get('quote_zh',s['basis_zh'])}
            if not any(x['url']==entry['url'] for x in bases):bases.append(entry)
        category='平台布局差异' if rows[0]['decision']=='guidance_deviation' else ('通用显示问题' if any(f['rule_id'].startswith('IOS-') and f.get('cause_attribution')!='confirmed_duo_related' for f in rows) else '适配显示缺陷')
        result_groups.append({'number':rows[0]['number'],'category':category,'problem_type':s['problem_type'],'problem_point':s['problem_point'],'basis':bases,'representatives':[{'evidence_key':eid,'title':by_p[by_e[eid]['page_id']]['title']} for eid in reps]})
    owners={f['page_id'] for f in selected};result_pages=[]
    for p in data['pages']:
        if p['id'] not in owners:continue
        relevant={eid for f in selected if f['page_id']==p['id'] for eid in f['evidence_ids']}
        result_pages.append({'title':p['title'],'images':[{'evidence_key':eid} for eid in p['evidence_ids'] if eid in relevant]})
    reference_specs=[]
    reference_file=run/'official-references.json'
    if reference_file.exists() and selected:
        reference_specs=json.loads(reference_file.read_text())['figures']
        selected_numbers={f['number'] for f in selected}
        for ref in reference_specs:
            reference_numbers(ref,selected_numbers)
            if not ref['url'].startswith('https://developer.apple.com/'):raise ValueError('Reference must have an Apple source URL')
            if ref.get('resource_url'):
                from urllib.parse import urlparse
                link=urlparse(ref['resource_url'])
                if link.scheme!='https' or link.hostname not in {'figma.com','www.figma.com','developer.apple.com'}:raise ValueError('Invalid official resource detail URL')
            ref.update(reference_delivery(ref))
            if ref.get('image'):
                source=Path(ref['image'])
                if not source.is_absolute():source=run/source
                with Image.open(source) as img:img.verify()
                ref['_source']=source
            elif ref.get('source_type')=='apple_ui_kit' and intake['output']=='figma':
                ref['_source']=None
            else:raise ValueError('Official image or Lark UI Kit reference requires an export image')
    # All validation precedes generating assets.
    out.mkdir();(out/'images').mkdir()
    for eid in {r['evidence_key'] for p in result_pages for r in p['images']}:
        e=by_e[eid];targets=[(f['number'],a) for f in selected for a in f['annotations'] if a['evidence_id']==eid]
        geo=annotation_geometry(e['size_px'],targets,style);name=f'images/{eid}.png';annotate(run/e['image'],out/name,geo,style)
        assets[eid]={'orig_image':str((run/e['image']).resolve()),'annotated_image':str((out/name).resolve()),'preview_image':name,**geo}
    form_label={'outer':'折叠态','inner-landscape':'展开－横屏','inner-portrait':'展开－竖屏','mixed':'多种屏幕姿态'}[intake['form']]
    issue_pages={f['page_id'] for f in data['findings'] if f['decision']=='issue'}
    guidance_pages={f['page_id'] for f in data['findings'] if f['decision']=='guidance_deviation'}-issue_pages
    counts={'reviewed_pages':len(data['pages']),'needs_changes':len(issue_pages),'suggestions_only':len(guidance_pages),'passed':len(data['pages'])-len(issue_pages)-len(guidance_pages),'displayed_pages':len(result_pages)}
    defect_groups=sum(g['category']!='平台布局差异' for g in result_groups)
    guidance_groups=len(result_groups)-defect_groups
    summary=form_label+'：'+('本次审查发现'+str(defect_groups)+'类显示问题' if defect_groups else '本次截图未发现显示问题')
    if guidance_groups:summary+='，另有'+str(guidance_groups)+'类布局指导差异'
    summary+='。'
    representatives=choose_examples(result_groups,selected,by_e,by_p)
    for rep in representatives:
        eid=rep['evidence_key'];e=by_e[eid]
        targets=[(f['number'],a) for f in selected if f['number'] in rep['problem_numbers'] for a in f['annotations'] if a['evidence_id']==eid]
        geo=annotation_geometry(e['size_px'],targets,style);name=f'images/example-{eid}.png';annotate(run/e['image'],out/name,geo,style)
        assets[eid]['example']={'orig_image':assets[eid]['orig_image'],'annotated_image':str((out/name).resolve()),'preview_image':name,**geo}
    references=[]
    for index,ref in enumerate(reference_specs,1):
        item={'url':ref['url'],'caption':ref.get('caption',''),'problem_numbers':ref['problem_numbers'],**reference_delivery(ref)}
        if ref.get('resource_url'):item['resource_url']=ref['resource_url']
        if ref['_source'] is not None:
            name=f"images/official-{index}{ref['_source'].suffix}"
            shutil.copy2(ref['_source'],out/name)
            item['image']=name
        references.append(item)
    presentation={'layout_version':style['layout_version'],'structure':['summary','official_standard_examples','consolidated_examples_and_explanations','issue_page_gallery'],'representatives':representatives,'reference_style':'matched_abstract_reference_first_compact_unmodified_source','gallery_caption':'page_title_only','style':style,'example_annotations':'owned_problem_numbers_only'}
    report={'schema_version':'1.2','title':intake['flow']+'｜iPhone Duo 适配审查','form':form_label,'summary':summary,'counts':counts,'presentation':presentation,'official_references':references,'groups':result_groups,'pages':result_pages,'empty_message':'本次截图检查通过。' if not selected else ''}
    dump(out/'report.json',report);dump(out/'report-assets.json',assets)
    blocks=[{'type':'heading','level':1,'text':report['title']},{'type':'paragraph','text':summary}]
    parts=[];figures=[];explanations=[]
    if references:
        blocks.append({'type':'heading','level':2,'text':'苹果官方规范示例'})
        official_figures=[]
        for ref in references:
            correspondence='对应'+ '、'.join(str(n) for n in ref['problem_numbers'])
            blocks.append({'type':'heading','level':3,'text':correspondence})
            if ref.get('image'):blocks.append({'type':'image','path':str((out/ref['image']).resolve()),'alt':ref['caption'] or '苹果官方规范示例'})
            if ref['caption']:blocks.append({'type':'paragraph','text':ref['caption']})
            blocks.append({'type':'paragraph','runs':[{'text':'官方来源 ↗','url':ref['url']}]})
            detail=''
            if ref.get('resource_url'):
                blocks.append({'type':'paragraph','runs':[{'text':'资源 Frame ↗','url':ref['resource_url']}]})
                detail=' · <a href="'+esc(ref['resource_url'])+'">资源 Frame ↗</a>'
            preview='<img src="'+esc(ref['image'])+'" alt="苹果官方规范示例">' if ref.get('image') else ''
            official_figures.append('<figure><h3>'+esc(correspondence)+'</h3>'+preview+'<figcaption>'+esc(ref['caption'])+'</figcaption><a href="'+esc(ref['url'])+'">官方来源 ↗</a>'+detail+'</figure>')
        parts.append('<section class="official"><h2>苹果官方规范示例</h2><div class="official-figures">'+''.join(official_figures)+'</div></section>')
    if result_groups:
        blocks.append({'type':'heading','level':2,'text':'App 问题示例'})
    for rep in representatives:
        asset=assets[rep['evidence_key']]['example']
        blocks.extend([{'type':'image','evidence_key':rep['evidence_key'],'path':asset['annotated_image'],'alt':rep['title']},{'type':'paragraph','text':rep['title']}])
        figures.append(f'<figure><img src="{esc(asset["preview_image"])}" alt="{esc(rep["title"])}"><figcaption>{esc(rep["title"])}</figcaption></figure>')
    for g in result_groups:
        qualifier='建议调整' if g['category']=='平台布局差异' else g['category']
        heading=f"{g['number']}｜{g['problem_type']} · {qualifier}"
        blocks.append({'type':'heading','level':3,'text':heading})
        problem_copy='问题点：'+g['problem_point'].removeprefix('问题点：')
        blocks.append({'type':'paragraph','text':problem_copy});basis_html=[]
        for b in g['basis']:
            blocks.append({'type':'paragraph','runs':[{'text':'官方依据','url':b['url']},{'text':'：'+b['summary']}]})
            basis_html.append(f'<p class="basis"><a href="{esc(b["url"])}">官方依据</a>：{esc(b["summary"])}</p>')
        explanations.append('<article class="copy"><h3>'+esc(heading)+'</h3><p>'+esc(problem_copy)+'</p>'+''.join(basis_html)+'</article>')
    if result_groups:
        parts.append('<h2>App 问题示例</h2><section class="consolidated"><div class="representatives">'+''.join(figures)+'</div><div class="explanations">'+''.join(explanations)+'</div></section>')
    gallery=[]
    if result_pages:blocks.append({'type':'heading','level':2,'text':'问题页面汇总'})
    for p in result_pages:
        blocks.append({'type':'heading','level':3,'text':p['title']});images=[]
        for i in p['images']:
            a=assets[i['evidence_key']];blocks.append({'type':'image','evidence_key':i['evidence_key'],'path':a['annotated_image'],'alt':p['title']});images.append(f'<img src="{esc(a["preview_image"])}" alt="{esc(p["title"])}">')
        gallery.append('<article>'+''.join(images)+'<h3>'+esc(p['title'])+'</h3></article>')
    if result_pages:parts.append('<h2>问题页面汇总</h2><div class="gallery">'+''.join(gallery)+'</div>')
    else:blocks.append({'type':'paragraph','text':report['empty_message']});parts.append('<p>'+report['empty_message']+'</p>')
    css=f'body{{background:{style["background"]};color:{style["text"]};font:16px/1.6 -apple-system,sans-serif;margin:32px}}img{{max-width:100%;height:auto}}.official-figures{{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,{style["official_image_max_width"]}px));gap:24px;align-items:start;text-align:left}}.official img{{max-width:100%;max-height:{style["official_image_max_height"]}px;width:auto;height:auto;object-fit:contain}}.consolidated{{display:grid;grid-template-columns:1fr 1fr;gap:28px;margin:30px 0;align-items:start}}.representatives{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px}}figure{{margin:0;min-width:0}}.copy{{background:{style["card_background"]};color:{style["card_text"]};padding:24px;margin-bottom:24px}}a{{color:{style["link"]};text-decoration:underline}}.basis{{margin-top:{style["basis_gap_px"]}px}}.gallery{{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:24px}}h3{{font-size:16px}}@media(max-width:900px){{.consolidated{{grid-template-columns:1fr}}.gallery{{grid-template-columns:repeat(2,minmax(0,1fr))}}.representatives{{grid-template-columns:repeat(2,minmax(0,1fr))}}}}'
    (out/'preview.html').write_text('<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+esc(report['title'])+'</title><style>'+css+'</style><h1>'+esc(report['title'])+'</h1><p>'+esc(summary)+'</p>'+''.join(parts)+'</html>')
    dump(out/'lark-blocks.json',blocks)
    dump(out/'publication.json',{'status':'draft','channel':intake['output'],'target':intake['target'],'report_sha256':hashfile(out/'report.json'),'node_mapping':{},'block_mapping':{},'official_reference_mapping':{}})
    return {'report':str(out),'displayed_pages':len(result_pages),'retained_pages':len(data['pages']),'groups':len(result_groups),'publication_status':'draft'}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('run',type=Path);p.add_argument('--rule-root',type=Path,default=Path(__file__).resolve().parents[2]/'iphone-duo-design-guidelines');p.add_argument('--style',type=Path,default=Path(__file__).resolve().parents[1]/'assets/report-style.json')
    a=p.parse_args();print(build(a.run.resolve(),a.rule_root.resolve(),a.style.resolve()))
