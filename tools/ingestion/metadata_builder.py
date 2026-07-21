
import os
import hashlib
import uuid

def build_metadata(filepath):
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        hasher.update(f.read())
        
    return {
        "uuid": str(uuid.uuid4()),
        "file_size": os.path.getsize(filepath),
        "checksum": hasher.hexdigest(),
        "checksum_algorithm": "SHA-256",
        "validation_status": "VALID",
        "duplicate_status": "NONE"
    }
