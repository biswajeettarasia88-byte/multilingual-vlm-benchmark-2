
import uuid
import json
from datetime import datetime

def register_benchmark(asset, review_data):
    benchmark_id = "BENCHMARK-" + str(uuid.uuid4())[:8]
    promoted = {
        "benchmark_id": benchmark_id,
        "asset_uuid": asset["asset_uuid"],
        "dataset": asset["dataset_name"],
        "license": asset["license"],
        "validation_summary": asset["validation_summary"],
        "provenance": asset["provenance"],
        "review_history": [review_data],
        "benchmark_version": "1.0",
        "benchmark_status": "APPROVED",
        "reviewer_id": review_data["reviewer_id"],
        "promotion_timestamp": datetime.now().isoformat()
    }
    return {"status": "PROMOTED", "asset": promoted}
