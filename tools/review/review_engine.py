
import uuid
from datetime import datetime
from .audit import append_audit
from .promotion_manager import promote
from .decision_validator import validate_decision

def process_review(asset, review_data, execution_mode):
    if not validate_decision(review_data["decision"]):
        raise ValueError("Invalid decision")
        
    append_audit({
        "event_id": str(uuid.uuid4()),
        "asset_uuid": asset["asset_uuid"],
        "timestamp": datetime.now().isoformat(),
        "actor": review_data["reviewer_id"],
        "actor_type": review_data["decision_source"],
        "action": "REVIEW",
        "previous_state": "STAGING",
        "new_state": review_data["decision"],
        "notes": review_data.get("comments", "")
    })
    
    if review_data["decision"] == "APPROVE":
        return promote(asset, review_data, execution_mode)
    else:
        return {"status": "REJECTED_OR_PENDING", "reason": review_data["decision"]}
