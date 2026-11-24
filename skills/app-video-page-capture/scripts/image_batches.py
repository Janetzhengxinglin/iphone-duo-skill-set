"""Exact consecutive candidate folding and pre-read budgets and a local input ledger (stdlib only)."""
import argparse
import hashlib
import json
import struct
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


def dimensions(path):
    # Read image headers locally; never decode or return image blocks to the model.
    with Path(path).open('rb') as f:
        head = f.read(32)
        if head[:8] == b'\x89PNG\r\n\x1a\n':
            return struct.unpack('>II', head[16:24])
        if head[:6] in (b'GIF87a', b'GIF89a'):
            return struct.unpack('<HH', head[6:10])
        if head[:4] == b'RIFF' and head[8:12] == b'WEBP':
            kind = head[12:16]
            if kind == b'VP8X':
                return (1 + int.from_bytes(head[24:27], 'little'),
                        1 + int.from_bytes(head[27:30], 'little'))
            if kind == b'VP8L' and head[20] == 0x2f:
                bits = int.from_bytes(head[21:25], 'little')
                return (1 + (bits & 0x3fff), 1 + ((bits >> 14) & 0x3fff))
            if kind == b'VP8 ' and head[23:26] == b'\x9d\x01\x2a':
                return tuple(n & 0x3fff for n in struct.unpack('<HH', head[26:30]))
        if head[:2] == b'\xff\xd8':
            f.seek(2)
            while True:
                byte = f.read(1)
                if not byte:
                    break
                if byte != b'\xff':
                    continue
                marker = f.read(1)
                while marker == b'\xff':
                    marker = f.read(1)
                if not marker or marker[0] in (0xd9, 0xda):
                    break
                if marker[0] in (0x01, 0xd8) or 0xd0 <= marker[0] <= 0xd7:
                    continue
                length = struct.unpack('>H', f.read(2))[0]
                if marker[0] in (0xc0, 0xc1, 0xc2, 0xc3, 0xc5, 0xc6,
                                  0xc7, 0xc9, 0xca, 0xcb, 0xcd, 0xce, 0xcf):
                    _, height, width = struct.unpack('>BHH', f.read(5))
                    return width, height
                if length < 2:
                    break
                f.seek(length - 2, 1)
    raise ValueError('Unsupported or invalid image header: ' + str(path))


def detail(image):
    path = Path(image).resolve()
    width, height = dimensions(path)
    if min(width, height) < 1:
        raise ValueError('Invalid image dimensions: ' + str(path))
    return {'path': str(path), 'width': width, 'height': height,
            'pixels': width * height, 'bytes': path.stat().st_size,
            'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}


def read_ledger(path):
    return json.loads(Path(path).read_text()) if Path(path).exists() else {
        'schema_version': 2, 'scope': 'local observed/attempted inputs; history may contain more',
        'events': []}


def budgets(args):
    return dict(call_limit=args.call_limit, session_limit=args.session_limit,
                max_pixels=args.max_pixels, max_edge=args.max_edge, max_bytes=args.max_bytes)


def violations(items, call_limit, max_pixels, max_edge, max_bytes):
    reasons = []
    if not items:
        reasons.append('empty_batch')
    if len(items) > call_limit:
        reasons.append('image_count')
    if sum(i['pixels'] for i in items) > max_pixels:
        reasons.append('total_pixels')
    if any(max(i['width'], i['height']) > max_edge for i in items):
        reasons.append('longest_edge')
    if sum(i['bytes'] for i in items) > max_bytes:
        reasons.append('total_bytes')
    return reasons


def check(path, session, images, call_limit=2, session_limit=30,
          max_pixels=4000000, max_edge=2560, max_bytes=8388608):
    items = [detail(p) for p in images]
    prior = [e for e in read_ledger(path)['events'] if e['session'] == session]
    failed = [e for e in prior if e.get('status') == 'failed']
    effective_call = min(call_limit, 1) if failed else call_limit
    effective_pixels = max_pixels // 2 if failed else max_pixels
    reasons = violations(items, effective_call, effective_pixels, max_edge, max_bytes)
    attempted = sum(len(e['images']) for e in prior)
    if attempted + len(items) > session_limit or attempted >= session_limit:
        reasons.append('context_budget')
    if len(failed) >= 2:
        reasons.append('repeated_failures_use_new_context')
    signature = sorted(i['sha256'] for i in items)
    if any(signature == sorted(i['sha256'] for i in e['images']) for e in failed):
        reasons.append('unchanged_failed_batch')
    return {'ready': not reasons, 'reasons': reasons, 'images': items,
            'attempted_context_inputs': attempted, 'failure_count': len(failed),
            'effective_call_limit': effective_call, 'effective_max_pixels': effective_pixels,
            'checkpoint_due': attempted + len(items) >= session_limit,
            'note': 'Local guard only; tool history and actual platform limits are not controlled.'}


def record(path, session, stage, images, call_limit=2, session_limit=30,
           status='returned', max_pixels=4000000, max_edge=2560, max_bytes=8388608):
    # Log actual returns/failures even if a caller bypassed the guard.
    result = check(path, session, images, call_limit, session_limit, max_pixels, max_edge, max_bytes)
    data = read_ledger(path)
    prior = [e for e in data['events'] if e['session'] == session]
    known = {i['sha256'] for e in prior for i in e['images']}
    repeats = 0
    for item in result['images']:
        repeats += item['sha256'] in known
        known.add(item['sha256'])
    data['schema_version'] = 2
    data['events'].append({'time_utc': datetime.now(timezone.utc).isoformat(),
                           'session': session, 'stage': stage, 'status': status,
                           'images': result['images'], 'repeated_inputs': repeats,
                           'guard_reasons': result['reasons']})
    write_json(path, data)
    total = result['attempted_context_inputs'] + len(images)
    return {'recorded_inputs': len(images), 'session_inputs': total, 'status': status,
            'repeated_inputs': repeats, 'call_budget_exceeded': bool(result['reasons']),
            'guard_reasons': result['reasons'],
            'checkpoint_due': total >= session_limit or
                result['failure_count'] + (status == 'failed') >= 2,
            'note': 'Failed requests conservatively count as attempts; recording is not review completion.'}


def manifest_paths(manifest):
    path = Path(manifest).resolve()
    items = json.loads(path.read_text())
    if not isinstance(items, list) or not all(isinstance(p, str) for p in items):
        raise ValueError('manifest must be a JSON array of image paths')
    return [str((path.parent / p).resolve()) for p in items]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    plan = sub.add_parser('plan', help='Text-only batches; preserve oversized images as blocked')
    plan.add_argument('manifest')
    plan.add_argument('output')
    plan.add_argument('--batch-size', type=int, default=2)
    gate = sub.add_parser('check', help='Run before returning any image blocks')
    gate.add_argument('ledger')
    gate.add_argument('manifest', help='JSON path list for this batch only')
    for command in ['record', 'fail']:
        log = sub.add_parser(command)
        log.add_argument('ledger')
        log.add_argument('--image', action='append', required=True)
    for p in [plan, gate, sub.choices['record'], sub.choices['fail']]:
        p.add_argument('--call-limit', type=int, default=2)
        p.add_argument('--session-limit', type=int, default=30)
        p.add_argument('--max-pixels', type=int, default=4000000)
        p.add_argument('--max-edge', type=int, default=2560)
        p.add_argument('--max-bytes', type=int, default=8388608)
        if p is not plan:
            p.add_argument('--session', required=True, help='Actual context ID; renaming does not reset history')
            p.add_argument('--stage', required=True)
    args = parser.parse_args()
    limits = budgets(args)
    if min(limits.values()) < 1 or (args.command == 'plan' and args.batch_size < 1):
        parser.error('budgets must be positive')
    try:
        if args.command == 'plan':
            items = [detail(p) for p in manifest_paths(args.manifest)]
            batches, current = [], []
            limits.pop('session_limit')
            limits['call_limit'] = min(args.batch_size, args.call_limit)
            for item in items:
                if current and violations(current + [item], **limits):
                    batches.append(current)
                    current = []
                current.append(item)
                if violations(current, **limits):
                    batches.append(current)
                    current = []
            if current:
                batches.append(current)
            blocked = [{'batch_index': n, 'reasons': violations(b, **limits)}
                       for n, b in enumerate(batches) if violations(b, **limits)]
            write_json(args.output, {'image_count': len(items),
                       'batches': [[i['path'] for i in b] for b in batches],
                       'batch_metrics': [{'pixels': sum(i['pixels'] for i in b),
                                          'bytes': sum(i['bytes'] for i in b)} for b in batches],
                       'blocked_batches': blocked, 'local_budgets': limits})
            result = {'image_count': len(items), 'batch_count': len(batches),
                      'blocked_batch_count': len(blocked)}
        elif args.command == 'check':
            result = check(args.ledger, args.session, manifest_paths(args.manifest), **limits)
            result['stage'] = args.stage
        else:
            result = record(args.ledger, args.session, args.stage, args.image,
                            status='failed' if args.command == 'fail' else 'returned', **limits)
        print(json.dumps(result, ensure_ascii=False))
        if args.command == 'check' and not result['ready']:
            raise SystemExit(2)
    except (OSError, ValueError, KeyError, struct.error) as exc:
        parser.error(str(exc))


if __name__ == '__main__':
    main()
