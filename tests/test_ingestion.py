
import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tools.ingestion.asset_validator import validate_asset
from tools.ingestion.metadata_builder import build_metadata
from tools.ingestion.ingestion_pipeline import run_pipeline

class TestIngestionFramework(unittest.TestCase):
    def setUp(self):
        self.fixtures = os.path.join(os.path.dirname(__file__), "fixtures", "ingestion")
        
    def test_invalid_format(self):
        valid, reason = validate_asset(os.path.join(self.fixtures, "unsupported_file.txt"))
        self.assertFalse(valid)
        self.assertEqual(reason, "UNSUPPORTED_FORMAT")
        
    def test_corrupted_image(self):
        valid, reason = validate_asset(os.path.join(self.fixtures, "corrupted_image.png"))
        self.assertFalse(valid)
        self.assertEqual(reason, "CORRUPTED_FILE")
        
    def test_duplicate_rejection(self):
        file_path = os.path.join(self.fixtures, "valid_image.png")
        meta = build_metadata(file_path)
        # Seed known_checksums with it
        res = run_pipeline(file_path, {meta["checksum"]})
        self.assertEqual(res["status"], "REJECTED")
        self.assertEqual(res["reason"], "DUPLICATE_ASSET")
        
if __name__ == '__main__':
    unittest.main()
