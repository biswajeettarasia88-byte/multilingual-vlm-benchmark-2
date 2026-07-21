
import json
import os

AUDIT_FILE = "review_history.json"

def append_audit(event):
    history = []
    if os.path.exists(AUDIT_FILE):
        with open(AUDIT_FILE, "r") as f:
            history = json.load(f)
    history.append(event)
    with open(AUDIT_FILE, "w") as f:
        json.dump(history, f, indent=2)
