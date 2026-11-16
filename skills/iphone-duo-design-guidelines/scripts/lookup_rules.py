#!/usr/bin/env python3
"""Return versioned rule cards and source locators; never classify an App page."""
import argparse
import json
from pathlib import Path

def lookup(root, context, topics=(), profile=None, components=None):
    refs = root / 'references'
    index = json.loads((refs / 'context-index.json').read_text())
    bundle = json.loads((refs / 'rules.json').read_text())
    profiles = json.loads((refs / 'audit-profiles.json').read_text())
    profile = profile or profiles['default']
    policy = profiles['profiles'][profile]
    if context not in policy['contexts']:
        raise ValueError('This context requires an explicitly expanded review profile')
    eligible = set(policy['visible_rules'] + policy['guidance_rules'])
    selected = set(index['contexts'][context]['priority']) & eligible
    for topic in topics:
        selected.update(set(index['topics'][topic]) & eligible)
    from checklist import cards
    checklist = cards(root, context, components) if profile == 'three-form-screenshot' else []
    selected.update(rid for c in checklist for rid in c['rule_ids'] if rid in eligible)
    return {'checklist_cards': checklist, 'rule_version': bundle['version'], 'audit_profile': profile, 'policy': policy,
            'context': index['contexts'][context],
            'cards': sorted([r for r in bundle['rules'] if r['id'] in selected], key=lambda r: (policy['visible_rules'] + policy['guidance_rules']).index(r['id'])),
            'remaining_rules_to_triage': [r['id'] for r in bundle['rules'] if r['id'] in eligible - selected],
            'excluded_rules': policy['excluded_rules']}

if __name__ == '__main__':
    root = Path(__file__).resolve().parents[1]
    index = json.loads((root / 'references/context-index.json').read_text())
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('context', choices=index['contexts'])
    parser.add_argument('--topic', action='append', default=[], choices=index['topics'])
    profiles = json.loads((root / 'references/audit-profiles.json').read_text())
    parser.add_argument('--profile', choices=profiles['profiles'], default=profiles['default'])
    from checklist import COMPONENTS
    parser.add_argument('--component', action='append', choices=sorted(COMPONENTS))
    args = parser.parse_args()
    print(json.dumps(lookup(root, args.context, args.topic, args.profile, args.component), ensure_ascii=False, indent=2))
