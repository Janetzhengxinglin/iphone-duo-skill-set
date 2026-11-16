#!/usr/bin/env python3
"""Validate traceability, coverage and annotation geometry, not visual correctness."""
import argparse
import hashlib
import json
import math
from pathlib import Path

DECISIONS = {'issue', 'no_issue_observed', 'needs_confirmation', 'not_verified', 'not_applicable', 'guidance_deviation'}

def require(condition, message):
    if not condition:
        raise ValueError(message)

def unique_map(rows, label):
    result = {r['id']: r for r in rows}
    require(len(result) == len(rows), f'duplicate {label} id')
    return result

def validate(path, root=None):
    root = root or Path(__file__).resolve().parents[1]
    bundle = json.loads((root / 'references/rules.json').read_text())
    rules = {r['id']: r for r in bundle['rules'] if r['lifecycle'] == 'active'}
    data = json.loads(path.read_text())
    profiles = json.loads((root / 'references/audit-profiles.json').read_text())
    profile = data.get('audit_profile', profiles['default'])
    require(profile in profiles['profiles'], 'unknown audit profile')
    policy = profiles['profiles'][profile]
    scoped = profile == 'three-form-screenshot'
    visible = set(policy['visible_rules'])
    guidance = set(policy['guidance_rules'])
    rules = {rid: r for rid, r in rules.items() if rid in visible | guidance}
    require(data['schema_version'] == '1.0', 'schema version')
    require(data['rule_version'] == bundle['version'], 'rule version mismatch')
    require(bool(data['scope']), 'missing scope')
    pages = unique_map(data['pages'], 'page')
    videos = unique_map(data['videos'], 'video')
    evidence = unique_map(data['evidence'], 'evidence')
    for video in videos.values():
        require(video['duration_seconds'] > 0, 'invalid video duration')
        if video.get('file'):
            source = path.parent / video['file']
            require(source.is_file(), 'source video missing')
            require(hashlib.sha256(source.read_bytes()).hexdigest() == video['sha256'], 'source video hash mismatch')
    for page in pages.values():
        require(bool(page['context']), 'missing page context')
        require(all(eid in evidence and evidence[eid]['page_id'] == page['id'] for eid in page['evidence_ids']), 'page evidence mismatch')
    for e in evidence.values():
        require(e['page_id'] in pages and e['video_id'] in videos, 'unknown evidence owner')
        require(0 <= e['time_seconds'] <= videos[e['video_id']]['duration_seconds'], 'timestamp out of range')
        im = path.parent / e['image']
        require(im.is_file(), f'missing image: {im}')
        require(hashlib.sha256(im.read_bytes()).hexdigest() == e['image_sha256'], 'image hash mismatch')
        require(len(e['size_px']) == 2 and min(e['size_px']) > 0, 'image dimensions')
        # PNG dimensions can be checked without a runtime imaging dependency.
        raw = im.read_bytes()
        require(raw[:8] == b'\x89PNG\r\n\x1a\n', 'evidence must be PNG')
        size = [int.from_bytes(raw[16:20], 'big'), int.from_bytes(raw[20:24], 'big')]
        require(size == e['size_px'], 'declared dimensions differ from PNG')
    checks = {}
    for c in data['checks']:
        key = (c['page_id'], c['rule_id'])
        require(key not in checks, 'duplicate page/rule check')
        require(key[0] in pages and key[1] in rules, 'unknown page/rule')
        require(c['decision'] in DECISIONS, 'unknown decision')
        require(c['decision'] in policy['allowed_decisions'], 'decision outside audit profile')
        require(bool(c['reason']), 'missing check reason')
        require(all(x in evidence and evidence[x]['page_id'] == key[0] for x in c['evidence_ids']), 'check evidence owner mismatch')
        require(all(k in c for k in ['observation','applicability_facts','exceptions_checked','missing_evidence']), 'incomplete reasoning')
        if c['decision'] in {'issue', 'no_issue_observed', 'guidance_deviation'}:
            require(bool(c['evidence_ids']) and bool(c['applicability_facts']), 'missing observation evidence/applicability')
        if c['decision'] == 'issue':
            require(not scoped or key[1] in visible, 'layout guidance cannot become visible defect')
            require(rules[key[1]]['review_mode'] != 'advisory', 'advisory cannot become issue')
            require(bool(c['exceptions_checked']), 'issue has no exceptions check')
        if c['decision'] == 'guidance_deviation':
            require(key[1] in guidance and bool(c['exceptions_checked']), 'guidance needs applicable rule and exceptions check')
        if scoped:
            require(not c['missing_evidence'], 'default screenshot review must not add unshown tests')
        if c['decision'] in {'not_verified','needs_confirmation'}:
            require(bool(c['missing_evidence']), 'missing evidence not specified')
        checks[key] = c
    require(set(checks) == {(p, r) for p in pages for r in rules}, 'incomplete rule triage')
    findings = unique_map(data['findings'], 'finding')
    numbers = set()
    group_numbers = {}
    number_groups = {}
    for f in findings.values():
        key = (f['page_id'], f['rule_id'])
        require(key in checks and checks[key]['decision'] == f['decision'], 'finding/check mismatch')
        require(f['decision'] in {'issue','needs_confirmation','guidance_deviation'} or f.get('kind') == 'advisory', 'finding must be issue, guidance, candidate or explicit advisory')
        if scoped:
            expected_kind = 'visible-defect' if f['decision'] == 'issue' else 'default-layout-guidance'
            require(f['decision'] in {'issue','guidance_deviation'} and f.get('kind') == expected_kind, 'finding category outside screenshot scope')
            group = f.get('group_id')
            require(bool(group), 'finding needs stable common issue group')
            require(group not in group_numbers or group_numbers[group] == f['number'], 'same group has different annotation numbers')
            require(f['number'] not in number_groups or number_groups[f['number']] == group, 'different groups share annotation number')
            group_numbers[group] = f['number']
            number_groups[f['number']] = group
        num = (f['page_id'], f['number'])
        require(num not in numbers and isinstance(f['number'], int) and f['number'] > 0, 'duplicate/invalid annotation number')
        numbers.add(num)
        require(bool(f['evidence_ids']), 'finding missing evidence')
        require(set(f['evidence_ids']) <= set(checks[key]['evidence_ids']), 'finding evidence differs from check')
        require(all(f.get(k) for k in ['title','observation','impact','recommendation']), 'finding explanation incomplete')
        basis = f['basis']
        rule = rules[f['rule_id']]
        refs = rule['evidence_refs']
        candidates = [{'source_id': rule['source_id'], 'quote': rule['source_quote'], 'section': rule['source_section'], 'url':rule['source_url']}] + refs
        require(any(basis['source_id'] == b['source_id'] and basis['quote'] == b.get('quote') and basis['url'] == b.get('url', rule['source_url'] if b['source_id'] == rule['source_id'] else None) and basis.get('section') == b.get('section') for b in candidates), 'basis is not an exact rule reference')
        require(bool(f['annotations']), 'finding needs target or multi-frame annotation')
        for a in f['annotations']:
            require(a['evidence_id'] in f['evidence_ids'], 'annotation evidence mismatch')
            box = a['region']
            require(len(box) == 4 and all(isinstance(v, (int,float)) and math.isfinite(v) for v in box), 'invalid box')
            x,y,w,h = box
            require(x >= 0 and y >= 0 and w > 0 and h > 0 and x+w <= 1 and y+h <= 1, 'annotation out of bounds')
    for key,c in checks.items():
        if c['decision'] in {'issue','guidance_deviation'}:
            require(any((f['page_id'],f['rule_id']) == key for f in findings.values()), 'confirmed check lacks finding')
    defect_pages = {f['page_id'] for f in findings.values() if f['decision'] == 'issue'}
    guidance_pages = {f['page_id'] for f in findings.values() if f['decision'] == 'guidance_deviation'}
    checklist_items = 0
    if scoped and policy.get('checklist_required'):
        from checklist import validate_items
        checklist_items = validate_items(data,root,pages,evidence,findings)
    return {'checklist_items':checklist_items,'pages':len(pages),'checks':len(checks),'findings':len(findings),'evidence':len(evidence),
            'audit_profile':profile,'needs_change_pages':len(defect_pages),
            'guidance_only_pages':len(guidance_pages - defect_pages)}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('review', type=Path)
    args = parser.parse_args()
    print('PASS', validate(args.review.resolve()))
