"""Exact consecutive candidate folding and a local image-input ledger (stdlib only)."""
import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


def write_json(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def candidate_plan(rows, sheet_size, keep_all=False):
    """Never fold nonconsecutive matches or unverified/missing full-image hashes."""
    groups = []
    for row in rows:
        signature = row.get('visual_sha256')
        if (not keep_all and signature and groups
                and groups[-1]['visual_sha256'] == signature):
            groups[-1]['candidates'].append(row)
        else:
            groups.append({'visual_sha256': signature, 'candidates': [row]})
    representatives, mapping = [], []
    for group in groups:
        items = group['candidates']
        chosen = items[:1] + (items[-1:] if len(items) > 1 else [])
        representatives.extend(chosen)
        mapping.append({
            'candidate_ids': [r['id'] for r in items],
            'representative_ids': [r['id'] for r in chosen],
            'visual_sha256': group['visual_sha256'],
            'start_seconds': items[0].get('time_seconds', items[0].get('time_s')),
            'end_seconds': items[-1].get('time_seconds', items[-1].get('time_s')),
        })
    return {
        'schema_version': 1, 'method': 'consecutive-exact-full-frame',
        'candidate_count': len(rows), 'representative_count': len(representatives),
        'folded_count': len(rows) - len(representatives), 'groups': mapping,
        'sheet_candidate_ids': [[r['id'] for r in representatives[i:i + sheet_size]]
                                for i in range(0, len(representatives), sheet_size)],
        'coverage_review_complete': False,
    }, representatives


def record(path, session, stage, images, call_limit, session_limit):
    """Record actual image blocks returned, including repeated reads; no history reset."""
    path = Path(path)
    data = json.loads(path.read_text()) if path.exists() else {
        'schema_version': 1, 'scope': 'observed image inputs; actual request may contain more',
        'events': []}
    details = []
    for image in images:
        p = Path(image).resolve()
        details.append({'path': str(p), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()})
    prior = [event for event in data['events'] if event['session'] == session]
    known = {img['sha256'] for event in prior for img in event['images']}
    repeats = 0
    for item in details:
        repeats += item['sha256'] in known
        known.add(item['sha256'])
    data['events'].append({'time_utc': datetime.now(timezone.utc).isoformat(),
                           'session': session, 'stage': stage, 'images': details,
                           'repeated_inputs': repeats})
    total = sum(len(event['images']) for event in prior) + len(details)
    write_json(path, data)
    return {'recorded_inputs': len(details), 'session_inputs': total,
            'repeated_inputs': repeats, 'call_budget_exceeded': len(details) > call_limit,
            'checkpoint_due': total >= session_limit,
            'note': 'Local observed count only; starting a batch does not clear request history.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    plan = sub.add_parser('plan', help='Create text-only batches from an image path list')
    plan.add_argument('manifest', help='JSON array of image paths')
    plan.add_argument('output')
    plan.add_argument('--batch-size', type=int, default=6)
    log = sub.add_parser('record')
    log.add_argument('ledger')
    log.add_argument('--session', required=True, help='Actual chat/context identity')
    log.add_argument('--stage', required=True)
    log.add_argument('--image', action='append', required=True)
    log.add_argument('--call-limit', type=int, default=6)
    log.add_argument('--session-limit', type=int, default=30)
    args = parser.parse_args()
    if args.command == 'plan':
        if args.batch_size < 1:
            parser.error('batch-size must be positive')
        items = json.loads(Path(args.manifest).read_text())
        if not isinstance(items, list) or not all(isinstance(p, str) for p in items):
            parser.error('manifest must be a JSON array of image paths')
        root = Path(args.manifest).resolve().parent
        paths = [str((root / p).resolve()) for p in items]
        if not all(Path(p).is_file() for p in paths):
            parser.error('manifest contains a missing image')
        batches = [paths[i:i + args.batch_size] for i in range(0, len(paths), args.batch_size)]
        write_json(args.output, {'image_count': len(paths), 'batches': batches})
        print(json.dumps({'image_count': len(paths), 'batch_count': len(batches)}))
    else:
        if min(args.call_limit, args.session_limit) < 1:
            parser.error('budgets must be positive')
        print(json.dumps(record(args.ledger, args.session, args.stage, args.image,
                                args.call_limit, args.session_limit), ensure_ascii=False))


if __name__ == '__main__':
    main()
