
from datetime import datetime
def generate_provenance(filepath):
    return {
        "fixture_name": filepath,
        "source_type": "TEST_FIXTURE",
        "ingestion_mode": "FRAMEWORK_VALIDATION",
        "pipeline_version": "1.0",
        "timestamps": datetime.now().isoformat(),
        "validation_history": "PASSED",
        "benchmark_eligible": False
    }
