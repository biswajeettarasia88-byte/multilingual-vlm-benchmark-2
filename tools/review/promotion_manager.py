
from .benchmark_manager import register_benchmark

def promote(asset, review_data, execution_mode):
    if not asset.get("provenance"): raise ValueError("Provenance required")
    if asset.get("validation_summary") != "PASSED": raise ValueError("Validation must pass")
    
    return register_benchmark(asset, review_data)
