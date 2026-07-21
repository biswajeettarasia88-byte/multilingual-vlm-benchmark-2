
import unittest
import sys
import os
import uuid

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tools.review.mock_reviewer import MockReviewer
from tools.review.review_engine import process_review

class TestReviewFramework(unittest.TestCase):
    def setUp(self):
        self.asset = {
            "asset_uuid": str(uuid.uuid4()),
            "dataset_name": "TEST",
            "license": "CC",
            "validation_summary": "PASSED",
            "provenance": {"ok": True}
        }
        # Clear audit log before tests
        if os.path.exists("review_history.json"):
            os.remove("review_history.json")
        
    def test_approval(self):
        rev = MockReviewer("tester1", ["APPROVE"])
        decision = rev.review(self.asset)
        res = process_review(self.asset, decision, "FRAMEWORK_VALIDATION")
        self.assertEqual(res["status"], "PROMOTED")
        self.assertTrue(res["asset"]["benchmark_id"].startswith("BENCHMARK-"))
        
    def test_rejection(self):
        rev = MockReviewer("tester1", ["REJECT"])
        decision = rev.review(self.asset)
        res = process_review(self.asset, decision, "FRAMEWORK_VALIDATION")
        self.assertEqual(res["status"], "REJECTED_OR_PENDING")
        
    def test_invalid_decision(self):
        rev = MockReviewer("tester1", ["INVALID_JUNK"])
        decision = rev.review(self.asset)
        with self.assertRaises(ValueError):
            process_review(self.asset, decision, "FRAMEWORK_VALIDATION")
            
    def test_missing_provenance(self):
        bad_asset = self.asset.copy()
        del bad_asset["provenance"]
        rev = MockReviewer("tester1", ["APPROVE"])
        decision = rev.review(bad_asset)
        with self.assertRaises(ValueError):
            process_review(bad_asset, decision, "FRAMEWORK_VALIDATION")

if __name__ == '__main__':
    unittest.main()
