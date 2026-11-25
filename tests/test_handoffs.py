"""Exercise worker coverage and evidence invariants with synthetic task receipts."""
import importlib.util
import json
from pathlib import Path
import sys
import subprocess
import tempfile
import unittest

SCRIPT = (Path(sys.argv.pop(1)).resolve() if len(sys.argv) > 1 and sys.argv[1].endswith('.py')
          else Path(__file__).resolve().parents[1] / 'skills/iphone-duo-adaptation-review/scripts/validate_handoffs.py')
spec = importlib.util.spec_from_file_location('handoffs', SCRIPT)
handoffs = importlib.util.module_from_spec(spec)
spec.loader.exec_module(handoffs)


class HandoffTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.manifest = self.root / 'manifest.json'
        self.source = self.root / 'source.png'
        self.source.write_bytes(b'synthetic evidence; not an App screenshot')
        self.sha = handoffs.digest(self.source)
        self.spec = {'schema_version': 1, 'phase': 'review', 'rule_version': 'test-1',
                     'expected_units': ['U1', 'U2'],
                     'evidence': {'E1': {'path': 'source.png', 'sha256': self.sha}},
                     'tasks': [{'id': 'T1', 'units': ['U1'], 'evidence_ids': ['E1'], 'output_dir': 'tasks/T1'},
                               {'id': 'T2', 'units': ['U2'], 'evidence_ids': ['E1'], 'output_dir': 'tasks/T2'}]}
        self.receipts = {}
        for task in self.spec['tasks']:
            out = self.root / task['output_dir']
            out.mkdir(parents=True)
            result = out / 'review-fragment.json'
            result.write_text('{}', encoding='utf-8')
            self.receipts[task['id']] = {'task_id': task['id'], 'phase': 'review',
                'rule_version': 'test-1', 'status': 'complete',
                'completed_units': task['units'][:], 'pending_units': [],
                'evidence_hashes': {'E1': self.sha},
                'result_files': [{'path': result.name, 'sha256': handoffs.digest(result)}]}
        self.save()

    def save(self):
        self.manifest.write_text(json.dumps(self.spec), encoding='utf-8')
        for tid, receipt in self.receipts.items():
            (self.root / 'tasks' / tid / 'handoff.json').write_text(json.dumps(receipt), encoding='utf-8')

    def rejects(self, message):
        self.save()
        with self.assertRaisesRegex(ValueError, message):
            handoffs.validate(self.manifest)

    def test_cli_complete(self):
        result = subprocess.run([sys.executable, str(SCRIPT), str(self.manifest)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(json.loads(result.stdout)['ready_for_merge'])

    def test_cli_rejects_incomplete(self):
        (self.root / 'tasks/T1/handoff.json').unlink()
        result = subprocess.run([sys.executable, str(SCRIPT), str(self.manifest)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertFalse(json.loads(result.stdout)['ready_for_merge'])

    def test_complete_handoff(self):
        result = handoffs.validate(self.manifest)
        self.assertTrue(result['ready_for_merge'])
        self.assertEqual(result['unit_count'], 2)

    def test_plan_does_not_claim_completion(self):
        (self.root / 'tasks/T1/handoff.json').unlink()
        self.assertFalse(handoffs.validate(self.manifest, plan_only=True)['ready_for_merge'])

    def test_unassigned_unit(self):
        self.spec['tasks'].pop()
        self.rejects('Unassigned')

    def test_overlap(self):
        self.spec['tasks'][1]['units'] = ['U1']
        self.rejects('Overlapping unit')

    def test_out_of_scope(self):
        self.spec['tasks'][1]['units'] = ['U3']
        self.rejects('outside expected')

    def test_nested_output_directories(self):
        self.spec['tasks'][1]['output_dir'] = 'tasks/T1/child'
        self.rejects('Overlapping output')

    def test_output_escapes(self):
        self.spec['tasks'][1]['output_dir'] = '../outside'
        self.rejects('escapes')

    def test_missing_handoff(self):
        (self.root / 'tasks/T1/handoff.json').unlink()
        with self.assertRaisesRegex(ValueError, 'Missing handoff'):
            handoffs.validate(self.manifest)

    def test_pending_unit(self):
        self.receipts['T1']['pending_units'] = ['U1']
        self.rejects('pending units')

    def test_incomplete_status(self):
        self.receipts['T1']['status'] = 'incomplete'
        self.rejects('incomplete')

    def test_wrong_completed_scope(self):
        self.receipts['T1']['completed_units'] = ['U2']
        self.rejects('completed units')

    def test_wrong_phase(self):
        self.receipts['T1']['phase'] = 'recheck'
        self.rejects('Wrong task or phase')

    def test_wrong_rules(self):
        self.receipts['T1']['rule_version'] = 'old'
        self.rejects('Rule version')

    def test_wrong_evidence_receipt(self):
        self.receipts['T1']['evidence_hashes'] = {'E1': 'old'}
        self.rejects('Receipt evidence')

    def test_changed_input(self):
        self.source.write_bytes(b'new evidence')
        self.rejects('Changed evidence')

    def test_changed_result(self):
        (self.root / 'tasks/T1/review-fragment.json').write_text('{"changed": true}', encoding='utf-8')
        self.rejects('changed result')

    def test_shared_result_through_symlink(self):
        result = self.root / 'tasks/T1/review-fragment.json'
        result.unlink()
        result.symlink_to(self.root / 'tasks/T2/review-fragment.json')
        self.rejects('escapes')

    def test_empty_result_files(self):
        self.receipts['T1']['result_files'] = []
        self.rejects('No result files')


if __name__ == '__main__':
    unittest.main()
