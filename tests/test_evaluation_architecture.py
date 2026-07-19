import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from evaluation.registry import METRIC_REGISTRY
import evaluation.metrics

class TestArchitecture(unittest.TestCase):
    def test_registry(self):
        self.assertTrue("ocr_accuracy" in METRIC_REGISTRY.list_all())

if __name__ == '__main__':
    unittest.main()
