"""
Tool: dataset_manifest.py
Description: Generates benchmark_manifest.json from raw data.
"""
import os
import json
from typing import List, Dict

def build_manifest(metadata_dir: str, output_path: str):
    """Aggregate all metadata.json files into a single manifest."""
    manifest = []
    
    for root, _, files in os.walk(metadata_dir):
        if "metadata.json" in files:
            path = os.path.join(root, "metadata.json")
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                
                # Transform to manifest schema
                entry = {
                    "unique_id": data.get("image_id", ""),
                    "split": data.get("split", "unknown"),
                    "filename": data.get("filename", ""),
                    "category": data.get("scene_type", ""),
                    "country": data.get("country", ""),
                    "city": data.get("city", ""),
                    "languages": list(data.get("language_distribution", {}).keys()),
                    "scripts": list(data.get("script_distribution", {}).keys()),
                    "license": data.get("license", ""),
                    "photographer": data.get("photographer", ""),
                    "collection_date": data.get("annotation_timestamp", ""),
                    "checksum": data.get("image_sha256", ""),
                    "validation_status": data.get("validation_status", "pending"),
                    "annotation_status": data.get("review_status", "pending"),
                    "qa_status": "pending"
                }
                manifest.append(entry)
            except Exception:
                pass
                
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

if __name__ == "__main__":
    pass
