"""Deterministic checklist routing; this module does not recognize pixels or judge UI."""
import json
COMPONENTS={'page','button','toolbar','tab','system','media','sheet','keyboard','menu','camera'}
def context_key(context):
    if isinstance(context,str):return context
    display=context['display']
    if display=='inner':return 'inner-'+context['orientation']
    return display
def card_components(card):
    return card.get('components',[card['component']])
def cards(root, context, components=None, mode='screenshot'):
    data=json.loads((root/'references/component-checklist.json').read_text())
    return [c for c in data['cards'] if c['mode']==mode and context_key(context) in c['contexts'] and (components is None or set(card_components(c)) & set(components))]
def expected_pairs(root,page):
    inventory=page['component_inventory']
    return {(page['id'],c['id'],item['id'] if item else None) for c in cards(root,page['context']) for item in ([i for i in inventory if i['type'] in card_components(c)] or [None])}
def validate_items(data,root,pages,evidence,findings):
    def need(v,m):
        if not v:raise ValueError(m)
    checklist=json.loads((root/'references/component-checklist.json').read_text())
    need(data.get('checklist_version')==checklist['version'],'missing/mismatched checklist version')
    expected=set(); inventory_by_page={}
    for p in pages.values():
        need(isinstance(p.get('component_inventory'),list),'missing component inventory')
        inv={i['id']:i for i in p['component_inventory']}
        need(len(inv)==len(p['component_inventory']),'duplicate component instance')
        need(any(i['type']=='page' for i in inv.values()),'missing whole-page scan')
        inventory_by_page[p['id']]=inv
        for i in inv.values():
            need(i['type'] in COMPONENTS,'unknown component type')
            need(i['evidence_id'] in p['evidence_ids'],'component evidence mismatch')
            box=i['region'];need(len(box)==4 and all(isinstance(v,(int,float)) for v in box),'component region')
            x,y,w,h=box;need(x>=0 and y>=0 and w>0 and h>0 and x+w<=1 and y+h<=1,'component out of bounds')
        expected |= expected_pairs(root,p)
    seen=set(); cmap={c['id']:c for c in checklist['cards']}
    for row in data.get('check_items',[]):
        key=(row['page_id'],row['check_id'],row['component_id']);need(key in expected,'check item not applicable to inventory/context')
        need(key not in seen,'duplicate check item');seen.add(key)
        need(row['decision'] in {'issue','no_issue_observed','not_applicable','guidance_deviation'},'check decision outside screenshot scope')
        need(row.get('reason') and row.get('exceptions_checked'),'missing item reason/exception triage')
        need(all(e in evidence and evidence[e]['page_id']==key[0] for e in row['evidence_ids']),'item evidence mismatch')
        if key[2] is None:need(row['decision']=='not_applicable','absent component cannot pass/fail')
        else:
            need(row.get('observation') and row['evidence_ids'],'missing instance observation')
            need(inventory_by_page[key[0]][key[2]]['evidence_id'] in row['evidence_ids'],'instance evidence not reviewed')
        need(all(fid in findings for fid in row['finding_ids']),'unknown finding')
        if row['decision'] in {'issue','guidance_deviation'}:
            need(row['finding_ids'],'flagged item missing finding')
            need(all(findings[f]['page_id']==key[0] and findings[f]['decision']==row['decision'] and findings[f]['rule_id'] in cmap[key[1]]['rule_ids'] for f in row['finding_ids']),'item/finding/rule mismatch')
        else:need(not row['finding_ids'],'unflagged item references finding')
    need(seen==expected,'incomplete per-page/component checklist')
    for f in findings.values():
        need(f.get('cause_attribution') in {'not_assessed','confirmed_duo_related'},'missing cause attribution')
        if f['cause_attribution']=='confirmed_duo_related':need(f.get('cause_evidence'),'Duo cause requires comparative/config evidence')
        need(f.get('check_ids'),'finding missing check mapping')
        need(all(any(r['page_id']==f['page_id'] and r['check_id']==cid and f['id'] in r['finding_ids'] for r in data['check_items']) for cid in f['check_ids']),'finding not linked from checklist')
    return len(seen)
