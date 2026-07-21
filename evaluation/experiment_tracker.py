
import json
import uuid
import os
from datetime import datetime

def record_experiment(registry_path, release_info, adapter, metrics_summary):
    exp = {
        "experiment_id": str(uuid.uuid4()),
        "execution_mode": "FRAMEWORK_VALIDATION",
        "benchmark_release": release_info["release_version"],
        "benchmark_checksum": release_info["benchmark_manifest_checksum"],
        "adapter_name": adapter.name,
        "adapter_version": adapter.version,
        "runtime_environment": "pytest/sandbox",
        "evaluation_timestamp": datetime.now().isoformat(),
        "metrics_version": "1.0",
        "configuration_checksum": "dummy",
        "python_version": "3.12",
        "hardware_information": "CPU mock",
        "metrics": metrics_summary
    }
    
    history = []
    if os.path.exists(registry_path):
        with open(registry_path, "r") as f:
            history = json.load(f)
    history.append(exp)
    
    with open(registry_path, "w") as f:
        json.dump(history, f, indent=2)
        
    return exp
