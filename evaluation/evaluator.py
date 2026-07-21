
import json
import os
from .metric_registry import cer
from datetime import datetime

def run_evaluation(benchmark_release_info, manifest_path, adapter, predictions_dir):
    with open(manifest_path, "r") as f:
        assets = json.load(f)
        
    results = []
    
    adapter_dir = os.path.join(predictions_dir, adapter.name)
    os.makedirs(adapter_dir, exist_ok=True)
    
    for asset in assets:
        # Predict
        pred = adapter.infer("dummy_path")
        # In reality, ground truth comes from annotations
        gt = asset.get("ground_truth", "mock prediction text") # for validation
        metric_val = cer(pred, gt)
        
        results.append({
            "asset_uuid": asset["asset_uuid"],
            "prediction": pred,
            "cer": metric_val
        })
        
    with open(os.path.join(adapter_dir, "predictions.json"), "w") as f:
        json.dump(results, f, indent=2)
        
    # overall metrics
    avg_cer = sum(r["cer"] for r in results) / len(results) if results else 0.0
    metrics_summary = {"avg_cer": avg_cer}
    
    with open(os.path.join(adapter_dir, "metrics.json"), "w") as f:
        json.dump(metrics_summary, f, indent=2)
        
    with open(os.path.join(adapter_dir, "evaluation.log"), "w") as f:
        f.write(f"Evaluated {len(assets)} assets at {datetime.now().isoformat()}\n")
        
    return metrics_summary
