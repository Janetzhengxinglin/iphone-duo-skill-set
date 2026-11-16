#!/usr/bin/env python3
"""Validate this rule bundle's provenance and local references; no AI behavior claim."""
import hashlib
import json
import re
from pathlib import Path


def validate(root):
    refs = root / 'references'
    source_map = {s['id']: s for s in json.loads((refs / 'sources.json').read_text())['sources']}
    texts = {}
    for sid, source in source_map.items():
        path = root / source['snapshot']
        assert path.exists(), (sid, 'missing snapshot')
        assert hashlib.sha256(path.read_bytes()).hexdigest() == source['sha256'], (sid, 'hash mismatch')
        texts[sid] = path.read_text()
        if source.get('supplemental_snapshot'):
            extra = root / source['supplemental_snapshot']
            assert hashlib.sha256(extra.read_bytes()).hexdigest() == source['supplemental_sha256']
        for extra_record in source.get('additional_snapshots', []):
            extra = root / extra_record['path']
            assert hashlib.sha256(extra.read_bytes()).hexdigest() == extra_record['sha256']
            if extra.suffix == '.md': texts[sid] += '\n' + extra.read_text()
    timed_quotes = {sid: {(row['start'], row['text']) for row in json.loads(text)} for sid, text in texts.items() if source_map[sid]['kind'] == 'official-video-transcript'}
    kit = json.loads(texts['kit-ios27'])
    tab = json.loads((root / source_map['kit-ios27']['supplemental_snapshot']).read_text())

    def node_ids(value):
        found = set()
        if isinstance(value, dict):
            if isinstance(value.get('id'), str):
                found.add(value['id'])
            for child in value.values():
                found.update(node_ids(child))
        elif isinstance(value, list):
            for child in value:
                found.update(node_ids(child))
        return found

    known_nodes = node_ids(kit) | node_ids(tab)
    bundle = json.loads((refs / 'rules.json').read_text())
    rules = bundle['rules']
    ids = [r['id'] for r in rules]
    assert len(ids) == len(set(ids)), 'duplicate rule IDs'
    index = json.loads((refs / 'context-index.json').read_text())
    assert index['version'] == bundle['version']
    for context in index['contexts'].values():
        assert set(context['priority']) <= set(ids)
    for topic in index['topics'].values():
        assert set(topic) <= set(ids)
    profiles = json.loads((refs / 'audit-profiles.json').read_text())
    assert profiles['version'] == bundle['version']
    assert profiles['default'] in profiles['profiles']
    for profile in profiles['profiles'].values():
        visible, guidance = set(profile['visible_rules']), set(profile['guidance_rules'])
        excluded = set(profile['excluded_rules'])
        assert not visible & guidance and not (visible | guidance) & excluded
        assert visible | guidance | excluded == set(ids)
        assert set(profile['contexts']) <= set(index['contexts'])
    visual = json.loads((refs / 'source-snapshots/video-111466-visual-review.json').read_text())
    for frame in visual['frames']:
        assert 0 <= frame['time_seconds'] <= source_map['video-111466']['duration_seconds']
        assert hashlib.sha256((root / frame['image']).read_bytes()).hexdigest() == frame['sha256']
    conflicts = json.loads((refs / 'conflicts.json').read_text())['conflicts']
    conflict_ids = {c['id'] for c in conflicts}
    required = {'id', 'source_id', 'source_quote', 'source_section', 'applies_when', 'exceptions',
                'required_evidence', 'fail_condition', 'insufficient_evidence_condition',
                'source_strength', 'review_mode', 'evidence_refs', 'reasoning_required'}
    for rule in rules:
        assert required <= set(rule), (rule['id'], 'missing fields')
        assert rule['source_quote'] in texts[rule['source_id']], (rule['id'], 'primary quote')
        assert rule['review_mode'] in {'guideline', 'advisory'}
        for cid in rule.get('conflict_ids', []):
            assert cid in conflict_ids
        for evidence in rule['evidence_refs']:
            sid = evidence['source_id']
            assert sid in source_map
            if evidence['kind'] == 'document':
                assert evidence['quote'] in texts[sid], (rule['id'], 'document quote')
            elif evidence['kind'] == 'video-transcript':
                assert (evidence['start_seconds'], evidence['quote']) in timed_quotes[sid], (rule['id'], 'video quote/time')
                assert 0 <= evidence['start_seconds'] <= source_map[sid].get('duration_seconds', source_map[sid].get('last_transcript_start_seconds'))
            elif evidence['kind'] == 'kit-example':
                assert evidence['node_id'] in known_nodes, (rule['id'], 'kit node')
                assert evidence['version'] == '27.1.4'
                if evidence.get('image'):
                    assert (root / evidence['image']).exists()
            else:
                raise AssertionError((rule['id'], 'unknown evidence kind'))
    for conflict in conflicts:
        assert set(conflict['affected_rules']) <= set(ids)
        for evidence in conflict['evidence']:
            if evidence.get('quote'):
                if evidence['source_id'] in timed_quotes:
                    assert (evidence['start_seconds'], evidence['quote']) in timed_quotes[evidence['source_id']]
                else:
                    assert evidence['quote'] in texts[evidence['source_id']]
    for case in json.loads((refs / 'benchmark-cases.json').read_text())['cases']:
        assert set(case['rule_ids']) <= set(ids)
    checklist = json.loads((refs / 'component-checklist.json').read_text())
    assert checklist['version'] == bundle['version']
    cids = {c['id'] for c in checklist['cards']}
    assert len(cids) == len(checklist['cards'])
    from checklist import COMPONENTS, card_components
    for c in checklist['cards']:
        assert c['component'] in COMPONENTS and set(c['rule_ids']) <= set(ids)
        assert set(card_components(c)) <= COMPONENTS and card_components(c)
        assert c['contexts'] and c['inspect'] and c['fail_when'] and c['exceptions']
        for e in c['official_refs']:
            assert e['quote'] in texts[e['source_id']], (c['id'], 'check quote')
            assert e['url'].startswith(source_map[e['source_id']]['url'])
    coverage = json.loads((refs / 'source-coverage.json').read_text())
    assert coverage['version'] == bundle['version']
    assert len({e['id'] for e in coverage['entries']}) == len(coverage['entries'])
    for e in coverage['entries']:
        assert e['source_id'] in source_map and e['reason']
        assert set(e['check_ids']) <= cids
        if e['disposition'] == 'mapped': assert e['check_ids']
        if 'quote' in e:
            if e['source_id'] in timed_quotes:
                assert (e['start_seconds'], e['quote']) in timed_quotes[e['source_id']]
            else:
                assert e['quote'] in texts[e['source_id']]
    for sid, count in coverage['paragraph_inventory'].items():
        assert sum(e['source_id']==sid and '-P' in e['id'] for e in coverage['entries']) == count
    for path in [root / 'SKILL.md', *refs.glob('*.md')]:
        for link in re.findall(r'\]\(([^)]+)\)', path.read_text()):
            if '://' not in link:
                assert (path.parent / link.split('#')[0]).exists(), (path, link)
    fm = re.match(r'^---\n(.*?)\n---', (root / 'SKILL.md').read_text(), re.S)
    assert fm, 'missing frontmatter'
    fields = dict(line.split(': ', 1) for line in fm.group(1).splitlines())
    assert fields['name'] == root.name
    assert re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', fields['name'])
    assert len(fields['name']) <= 64 and len(fields['description']) <= 1024
    print(f'PASS: {len(source_map)} source hashes, {len(rules)} rules, exact quotes/times, Kit nodes, conflicts and local links.')
    print('Boundary-case expectations checked structurally only; AI behavior has not been evaluated.')


if __name__ == '__main__':
    validate(Path(__file__).resolve().parents[1])
