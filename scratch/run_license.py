
import sys
import json
sys.path.append(r"D:\Internsip Work")
from tools.license_checker import check_licenses
rep = check_licenses(r"D:\Internsip Work\scratch\pilot_manifest.json")
with open(r"D:\Internsip Work/license_report.json", "w", encoding="utf-8") as f:
    json.dump(rep, f, indent=2)
