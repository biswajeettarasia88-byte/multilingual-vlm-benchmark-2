
import uuid
from datetime import datetime

class MockReviewer:
    def __init__(self, reviewer_id, deterministic_decisions):
        self.reviewer_id = reviewer_id
        self.decisions = deterministic_decisions
        self.idx = 0
        
    def review(self, asset):
        decision = self.decisions[self.idx]
        self.idx += 1
        return {
            "review_id": str(uuid.uuid4()),
            "asset_uuid": asset["asset_uuid"],
            "reviewer_id": self.reviewer_id,
            "decision": decision,
            "decision_source": "MOCK_REVIEWER",
            "review_timestamp": datetime.now().isoformat(),
            "confidence": "HIGH",
            "quality_rating": "GOOD",
            "review_version": 1
        }
