import json
import re
import unicodedata
from typing import List, Dict

WHITELIST = {"CC-BY-4.0", "CC-BY-SA-4.0", "CC0-1.0", "PUBLIC-DOMAIN", "CC-BY-SA-3.0", "CC-BY-3.0", "CC-BY-2.0"}

ALIASES = {
    "CC BY-SA 4.0": "CC-BY-SA-4.0",
    "CC BY 4.0": "CC-BY-4.0",
    "PUBLIC DOMAIN": "PUBLIC-DOMAIN",
    "CC0": "CC0-1.0",
    "CC BY-SA 3.0": "CC-BY-SA-3.0",
    "CC BY 3.0": "CC-BY-3.0"
}

def normalize_license(raw: str) -> str:
    s = unicodedata.normalize("NFKC", raw)
    s = s.strip()
    s = re.sub(r'\s+', ' ', s)
    s = s.upper()
    # Direct alias replacement
    if s in ALIASES:
        return ALIASES[s]

    # Manual fallback replacements if not in direct aliases
    s = s.replace(" ", "-").replace("_", "-")
    return s

def check_licenses(manifest_path: str) -> Dict[str, List[Dict]]:
    with open(manifest_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    report = {"approved": [], "rejected": []}

    for item in data:
        raw = item.get("license", "")
        norm = normalize_license(raw)
        result = {
            "id": item.get("unique_id", item.get("image_id", "unknown")),
            "raw_license": raw,
            "normalized_license": norm
        }

        if norm in WHITELIST:
            result["validation_result"] = "PASS"
            result["rejection_reason"] = None
            report["approved"].append(result)
        else:
            result["validation_result"] = "FAIL"
            result["rejection_reason"] = f"License '{norm}' not in whitelist."
            report["rejected"].append(result)

    return report
