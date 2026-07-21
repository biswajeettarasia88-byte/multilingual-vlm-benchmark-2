
import json
import hashlib
import os
from datetime import datetime

def freeze_benchmark(manifest_path, out_json_path, out_sha_path):
    with open(manifest_path, "r") as f:
        data = f.read()
    
    sha256 = hashlib.sha256(data.encode('utf-8')).hexdigest()
    assets = json.loads(data)
    
    release_info = {
        "release_version": "v0.1.0",
        "release_date": datetime.now().isoformat(),
        "schema_version": "1.0",
        "benchmark_manifest_checksum": sha256,
        "approved_asset_count": len(assets),
        "supported_tasks": ["Scene Text OCR", "Document OCR"],
        "supported_languages": ["en"],
        "supported_scripts": ["Latin"],
        "license_summary": "Various, see manifest",
        "known_limitations": "Pilot release only",
        "citation": "Benchmark v0.1.0"
    }
    
    with open(out_json_path, "w") as f:
        json.dump(release_info, f, indent=2)
        
    with open(out_sha_path, "w") as f:
        f.write(sha256)
        
    return release_info, sha256
