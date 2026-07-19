import unittest
import os
import json
from pathlib import Path
from project.loader import DatasetLoader, DatasetSchema

class TestDatasetLoader(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path("tests/temp_test_data")
        self.test_dir.mkdir(parents=True, exist_ok=True)
        self.jsonl_path = self.test_dir / "test.jsonl"
        
        with open(self.jsonl_path, "w", encoding="utf-8") as f:
            f.write(json.dumps({"id": "1", "image": "img1.jpg", "text": "A test"}) + "\n")
            f.write(json.dumps({"id": "2", "image_url": "http://img2.jpg", "caption": "A test 2"}) + "\n")
            
    def tearDown(self):
        if self.jsonl_path.exists():
            os.remove(self.jsonl_path)
        try:
            os.rmdir(self.test_dir)
        except:
            pass

    def test_schema_detection(self):
        loader = DatasetLoader(str(self.jsonl_path), str(self.test_dir), download_missing=False)
        self.assertEqual(loader.schema.id_field, "id")
        self.assertEqual(loader.schema.url_field, "image_url")
        self.assertIn(loader.schema.caption_field, ["text", "caption"])
        self.assertEqual(len(loader.records), 2)
