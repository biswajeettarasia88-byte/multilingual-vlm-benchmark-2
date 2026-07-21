"""
Tool: download_images.py
Description: Downloads images from a manifest, verifies checksums, supports retries and resume.
"""
import os
import json
import hashlib
import requests
import logging
from typing import List, Dict, Optional
from tqdm import tqdm

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def sha256_checksum(filepath: str) -> str:
    """Calculate SHA-256 checksum of a file."""
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def download_file(url: str, dest: str, expected_hash: Optional[str] = None, retries: int = 3) -> bool:
    """Download a file with resume support and optional checksum verification."""
    headers = {}
    if os.path.exists(dest):
        if expected_hash and sha256_checksum(dest) == expected_hash:
            logger.info(f"File {dest} already exists and is verified.")
            return True
        file_size = os.path.getsize(dest)
        headers["Range"] = f"bytes={file_size}-"
    else:
        file_size = 0

    for attempt in range(retries):
        try:
            with requests.get(url, headers=headers, stream=True, timeout=15) as r:
                r.raise_for_status()
                mode = 'ab' if file_size > 0 else 'wb'
                with open(dest, mode) as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
            
            if expected_hash:
                actual_hash = sha256_checksum(dest)
                if actual_hash != expected_hash:
                    logger.error(f"Checksum mismatch for {dest}. Expected {expected_hash}, got {actual_hash}.")
                    os.remove(dest)
                    return False
            return True
        except Exception as e:
            logger.warning(f"Attempt {attempt+1} failed for {url}: {e}")
            headers = {} # Reset headers for full retry if range failed
    return False

def process_manifest(manifest_path: str, output_dir: str):
    """Process a JSON manifest of image URLs."""
    if not os.path.exists(manifest_path):
        raise FileNotFoundError(f"Manifest {manifest_path} not found.")
    
    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)
        
    os.makedirs(output_dir, exist_ok=True)
    report = {"success": 0, "failed": 0, "failures": []}
    
    for item in tqdm(manifest, desc="Downloading Images"):
        url = item.get("url")
        expected_hash = item.get("sha256")
        filename = item.get("filename", os.path.basename(url))
        dest = os.path.join(output_dir, filename)
        
        if download_file(url, dest, expected_hash):
            report["success"] += 1
        else:
            report["failed"] += 1
            report["failures"].append({"url": url, "filename": filename})
            
    with open(os.path.join(output_dir, "outputs/archive/download_report.json"), "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

if __name__ == "__main__":
    pass # TODO: Add argparse for CLI usage
