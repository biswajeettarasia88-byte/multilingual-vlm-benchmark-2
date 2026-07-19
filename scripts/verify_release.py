import os
import json
import sys

base_dir = r"D:\Internsip Work"
examples_dir = os.path.join(base_dir, "examples")
manifest_path = os.path.join(examples_dir, "manifest.json")

required_files = [
    "README.md",
    "image.jpg",
    "thumbnail.jpg",
    "metadata.json",
    "annotation.json",
    "qa.json",
    "expected_output.json",
    "failure_cases.json",
    "visualization.png"
]

def verify():
    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)
        
    if len(manifest) != 23:
        print("Error: Manifest does not have exactly 23 entries.")
        sys.exit(1)
        
    ids = set()
    for entry in manifest:
        ids.add(entry["example_id"])
        folder_path = os.path.join(examples_dir, entry["folder_name"])
        if not os.path.isdir(folder_path):
            print(f"Error: Directory {entry['folder_name']} not found.")
            sys.exit(1)
            
        for req in required_files:
            if not os.path.isfile(os.path.join(folder_path, req)):
                print(f"Error: Missing file {req} in {entry['folder_name']}")
                sys.exit(1)
                
    if len(ids) != 23:
        print("Error: Duplicate IDs found in manifest.")
        sys.exit(1)
        
    print("Verification Passed.")

if __name__ == "__main__":
    verify()
