"""
Tool: license_checker.py
Description: Validates metadata licenses against a strictly approved whitelist.
"""
import os
import json
from typing import Dict, List

APPROVED_LICENSES = {
    "CC-BY-4.0", "CC-BY-SA-4.0", "CC0-1.0", "Public Domain", "MIT", "Apache-2.0"
}

def validate_license(license_str: str) -> bool:
    """Check if license is approved."""
    if not license_str:
        return False
    return license_str.strip() in APPROVED_LICENSES

def check_licenses(manifest_path: str) -> Dict:
    """Read a manifest and generate a license report."""
    report = {"approved": [], "rejected": [], "missing": []}
    
    if not os.path.exists(manifest_path):
        return report

    with open(manifest_path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            return report
            
    for item in data:
        uid = item.get("unique_id", "Unknown")
        lic = item.get("license", "")
        if not lic:
            report["missing"].append(uid)
        elif validate_license(lic):
            report["approved"].append(uid)
        else:
            report["rejected"].append({"id": uid, "license": lic})
            
    return report

if __name__ == "__main__":
    pass
