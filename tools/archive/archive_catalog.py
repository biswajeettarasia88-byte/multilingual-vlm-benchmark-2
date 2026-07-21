
import json
import os
def write_catalog(entries, path):
    with open(path, "w") as f:
        json.dump(entries, f, indent=2)
