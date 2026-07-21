
import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tools.archive.extractor import safe_extract
from tools.archive.checksum import verify_checksum

class TestArchiveFramework(unittest.TestCase):
    def test_path_traversal_prevention(self):
        with self.assertRaises(ValueError):
            safe_extract("../malicious.zip", "/tmp/dest")
            
    def test_missing_checksum(self):
        # We assume file exists for test, but we mock it here.
        # verify_checksum handles NOT_AVAILABLE
        res = verify_checksum("dummy.txt", None)
        self.assertEqual(res, "NOT_AVAILABLE")

if __name__ == '__main__':
    unittest.main()
