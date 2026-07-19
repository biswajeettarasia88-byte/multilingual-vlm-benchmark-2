"""
Tool: duplicate_checker.py
Description: Detects exact (SHA-256) and near duplicates (Perceptual Hash) in a directory.
"""
import os
import json
import hashlib
from typing import Dict, List, Tuple
from collections import defaultdict
try:
    from PIL import Image
    import imagehash
except ImportError:
    pass

def get_hashes(image_path: str) -> Tuple[str, str]:
    """Return SHA-256 and Perceptual Hash of an image."""
    sha = hashlib.sha256()
    with open(image_path, "rb") as f:
        for block in iter(lambda: f.read(4096), b""):
            sha.update(block)
    
    try:
        img = Image.open(image_path)
        phash = str(imagehash.phash(img))
    except Exception:
        phash = ""
        
    return sha.hexdigest(), phash

def check_duplicates(directory: str, threshold: int = 5) -> Dict:
    """Find duplicate clusters based on SHA-256 and pHash distance."""
    sha_map = defaultdict(list)
    phash_list = [] # List of tuples (filepath, phash_obj)
    
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                filepath = os.path.join(root, file)
                sha, ph = get_hashes(filepath)
                sha_map[sha].append(filepath)
                if ph:
                    phash_list.append((filepath, imagehash.hex_to_hash(ph)))
                    
    exact_duplicates = {sha: paths for sha, paths in sha_map.items() if len(paths) > 1}
    
    near_duplicates = []
    visited = set()
    for i in range(len(phash_list)):
        if i in visited: continue
        path_a, hash_a = phash_list[i]
        cluster = [path_a]
        visited.add(i)
        for j in range(i+1, len(phash_list)):
            if j in visited: continue
            path_b, hash_b = phash_list[j]
            if hash_a - hash_b <= threshold:
                cluster.append(path_b)
                visited.add(j)
        if len(cluster) > 1:
            near_duplicates.append(cluster)
            
    report = {
        "exact_duplicates": exact_duplicates,
        "near_duplicate_clusters": near_duplicates
    }
    return report

if __name__ == "__main__":
    pass
