
import sys
import json
sys.path.append(r"D:\Internsip Work")
from tools.duplicate_checker import check_duplicates
rep = check_duplicates(r"D:\Internsip Work\benchmark\train")
with open(r"D:\Internsip Work/duplicate_report.json", "w", encoding="utf-8") as f:
    json.dump(rep, f, indent=2)
