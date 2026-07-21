
def stage_asset(metadata, provenance):
    return {
        "asset_uuid": metadata["uuid"],
        "metadata": metadata,
        "provenance": provenance,
        "review_status": "TEST_ONLY",
        "benchmark_status": "NOT_IMPORTED",
        "source_type": "TEST_FIXTURE"
    }
