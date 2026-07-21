
import uuid
from datetime import datetime
class HumanReviewer:
    def __init__(self, reviewer_id):
        self.reviewer_id = reviewer_id
    def review(self, asset):
        decision = input("Decision (APPROVE/REJECT): ")
        return {
            "review_id": str(uuid.uuid4()),
            "reviewer_id": self.reviewer_id,
            "decision": decision,
            "decision_source": "HUMAN_REVIEWER",
            "review_timestamp": datetime.now().isoformat(),
            "confidence": "HIGH",
            "quality_rating": "GOOD",
            "review_version": 1
        }
