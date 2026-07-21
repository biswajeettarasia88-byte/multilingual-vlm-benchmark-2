
import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from evaluation.environment_detector import detect_environment
from evaluation.adapter_registry import EasyOCRAdapter

class TestM26(unittest.TestCase):
    def test_env(self):
        env = detect_environment()
        self.assertIn("os", env)
        
    def test_adapter_skip(self):
        adapter = EasyOCRAdapter()
        status = adapter.check_availability()
        self.assertIn(status, ["AVAILABLE", "NOT_INSTALLED", "IMPORT_FAILED"])

if __name__ == '__main__':
    unittest.main()
