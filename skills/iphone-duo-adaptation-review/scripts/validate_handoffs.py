"""Validate scoped worker handoffs; does not judge images or merge review data."""
import argparse
import hashlib
import json
from pathlib import Path


def require(ok, message):
    if not ok:
        raise ValueError(message)


def unique_strings(items, label, allow_empty=False):
    require(isinstance(items, list) and (items or allow_empty), label + ' must be a list')
    require(all(isinstance(x, str) and x.strip() for x in items), label + ' has invalid IDs')
    require(len(items) == len(set(items)), label + ' has duplicate IDs')
    return set(items)


def digest(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def contained(root, relative):
    require(isinstance(relative, str) and relative, 'Missing task-local path')
    require(not Path(relative).is_absolute(), 'Output paths must be task-local')
    p = (root / relative).resolve()
    require(root in p.parents, 'Output path escapes its task directory')
    return p


def validate(path, plan_only=False):
    path = Path(path).resolve()
    root = path.parent
    spec = json.loads(path.read_text(encoding='utf-8'))
    require(isinstance(spec, dict), 'Manifest must be an object')
    require(spec.get('schema_version') == 1, 'Unsupported handoff schema')
    phase = spec.get('phase')
    require(phase in {'capture', 'review', 'recheck'}, 'Invalid phase')
    require(isinstance(spec.get('rule_version'), str) and spec['rule_version'], 'Missing rule version')
    expected = unique_strings(spec.get('expected_units'), 'expected_units')
    evidence = spec.get('evidence')
    require(isinstance(evidence, dict) and evidence, 'Missing pinned evidence')
    for eid, record in evidence.items():
        require(isinstance(eid, str) and eid and isinstance(record, dict), 'Invalid evidence')
        source = Path(record['path'])
        if not source.is_absolute():
            source = root / source
        require(source.is_file(), 'Missing evidence: ' + eid)
        require(digest(source) == record.get('sha256'), 'Changed evidence: ' + eid)
    tasks = spec.get('tasks')
    require(isinstance(tasks, list) and tasks, 'Missing tasks')
    task_ids, assigned, output_dirs = set(), set(), []
    for task in tasks:
        require(isinstance(task, dict), 'Invalid task record')
        tid = task.get('id')
        require(isinstance(tid, str) and tid and tid not in task_ids, 'Duplicate or invalid task ID')
        task_ids.add(tid)
        units = unique_strings(task.get('units'), 'task units')
        require(not (assigned & units), 'Overlapping unit assignments')
        require(units <= expected, 'Assigned units outside expected scope')
        assigned |= units
        inputs = unique_strings(task.get('evidence_ids'), 'task evidence_ids')
        require(inputs <= set(evidence), 'Unknown task evidence')
        out = contained(root, task.get('output_dir'))
        require(all(out != old and out not in old.parents and old not in out.parents
                    for old in output_dirs), 'Overlapping output directories')
        output_dirs.append(out)
    require(assigned == expected, 'Unassigned expected units')
    if plan_only:
        return {'valid_plan': True, 'phase': phase, 'task_count': len(tasks),
                'unit_count': len(expected), 'ready_for_merge': False}
    results = set()
    for task, out in zip(tasks, output_dirs):
        receipt_path = out / 'handoff.json'
        require(receipt_path.is_file(), 'Missing handoff: ' + task['id'])
        require(receipt_path.resolve().parent == out, 'Handoff escapes its task directory')
        receipt = json.loads(receipt_path.read_text(encoding='utf-8'))
        require(isinstance(receipt, dict), 'Invalid receipt')
        require(receipt.get('task_id') == task['id'] and receipt.get('phase') == phase, 'Wrong task or phase')
        require(receipt.get('rule_version') == spec['rule_version'], 'Rule version mismatch')
        require(receipt.get('status') == 'complete', 'Task is incomplete: ' + task['id'])
        completed = unique_strings(receipt.get('completed_units'), 'completed_units')
        require(completed == set(task['units']), 'Missing or unexpected completed units')
        pending = unique_strings(receipt.get('pending_units'), 'pending_units', allow_empty=True)
        require(not pending, 'Task still has pending units')
        expected_hashes = {eid: evidence[eid]['sha256'] for eid in task['evidence_ids']}
        require(receipt.get('evidence_hashes') == expected_hashes, 'Receipt evidence mismatch')
        files = receipt.get('result_files')
        require(isinstance(files, list) and files, 'No result files')
        seen = set()
        for item in files:
            require(isinstance(item, dict), 'Invalid result file record')
            result = contained(out, item.get('path'))
            require(result != receipt_path and result not in seen and result not in results, 'Invalid or shared result file')
            require(result.is_file() and digest(result) == item.get('sha256'), 'Missing or changed result file')
            seen.add(result)
            results.add(result)
    return {'valid_plan': True, 'phase': phase, 'task_count': len(tasks),
            'unit_count': len(expected), 'ready_for_merge': True,
            'scope': 'Handoff identity, assignment coverage and hashes only; run platform validators and visual review.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('manifest')
    parser.add_argument('--plan-only', action='store_true')
    args = parser.parse_args()
    try:
        print(json.dumps(validate(args.manifest, args.plan_only), ensure_ascii=False))
    except (ValueError, KeyError, TypeError, OSError) as exc:
        print(json.dumps({'ready_for_merge': False, 'error': str(exc)}, ensure_ascii=False))
        raise SystemExit(1)


if __name__ == '__main__':
    main()
