
import unittest
import sys
import os
import tempfile
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from evaluation.release_manager import freeze_benchmark
from evaluation.adapter_registry import MockOCRAdapter
from evaluation.evaluator import run_evaluation

class TestEvaluationFramework(unittest.TestCase):
    def setUp(self):
        self.tmp_manifest = tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.json')
        json.dump([{"asset_uuid": "123", "ground_truth": "abc"}], self.tmp_manifest)
        self.tmp_manifest.close()
        
        self.tmp_out_json = tempfile.mktemp(suffix='.json')
        self.tmp_out_sha = tempfile.mktemp(suffix='.sha256')
        
    def tearDown(self):
        os.remove(self.tmp_manifest.name)
        if os.path.exists(self.tmp_out_json): os.remove(self.tmp_out_json)
        if os.path.exists(self.tmp_out_sha): os.remove(self.tmp_out_sha)

    def test_freeze_benchmark(self):
        rel, sha = freeze_benchmark(self.tmp_manifest.name, self.tmp_out_json, self.tmp_out_sha)
        self.assertEqual(rel["release_version"], "v0.1.0")
        self.assertTrue(os.path.exists(self.tmp_out_json))
        self.assertTrue(os.path.exists(self.tmp_out_sha))
        
    def test_mock_adapter(self):
        adapter = MockOCRAdapter()
        pred = adapter.infer("test.jpg")
        self.assertIsInstance(pred, str)
        
if __name__ == '__main__':
    unittest.main()
