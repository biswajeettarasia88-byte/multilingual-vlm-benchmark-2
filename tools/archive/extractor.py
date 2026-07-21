
import os
def safe_extract(archive_path, dest_dir):
    # Mocking safe extraction with traversal prevention
    if "../" in archive_path or "/etc/" in archive_path:
        raise ValueError("Path traversal detected")
    return True
