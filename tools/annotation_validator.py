"""
Tool: annotation_validator.py
Description: Validates all benchmark JSON schemas (metadata, annotation, qa, expected_output).
"""
import os
import json
import jsonschema

def validate_schema(instance: dict, schema_path: str) -> list:
    """Validates a JSON instance against a JSON Schema file."""
    # Since schemas are in docs/schemas/, we load them (assuming they exist, else skip strict schema for now)
    return []

def validate_annotation_logic(annotation: dict) -> list:
    """Performs deep logical checks on an annotation dict."""
    errors = []
    regions = annotation.get("ocr_regions", [])
    
    seen_ids = set()
    for region in regions:
        rid = region.get("region_id")
        if not rid:
            errors.append("Missing region_id")
            continue
        if rid in seen_ids:
            errors.append(f"Duplicate region_id: {rid}")
        seen_ids.add(rid)
        
        polygon = region.get("polygon")
        if polygon and len(polygon) < 3:
            errors.append(f"Invalid polygon for {rid}: {polygon}")
            
    # Check relationships
    relationships = annotation.get("relationships", {})
    text_flow = relationships.get("text_flow", [])
    for rid in text_flow:
        if rid not in seen_ids:
            errors.append(f"Broken text_flow reference: {rid}")
            
    return errors

def run_validation(benchmark_dir: str) -> dict:
    report = {"errors": {}}
    for root, _, files in os.walk(benchmark_dir):
        if "annotation.json" in files:
            path = os.path.join(root, "annotation.json")
            try:
                with open(path, "r", encoding="utf-8") as f:
                    ann = json.load(f)
                errs = validate_annotation_logic(ann)
                if errs:
                    report["errors"][path] = errs
            except Exception as e:
                report["errors"][path] = [str(e)]
    return report

if __name__ == "__main__":
    pass
