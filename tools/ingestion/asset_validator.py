
import os
def validate_asset(filepath):
    if not os.path.exists(filepath): return False, "FILE_NOT_FOUND"
    if filepath.endswith(".txt"): return False, "UNSUPPORTED_FORMAT"
    if os.path.getsize(filepath) == 0: return False, "CORRUPTED_FILE"
    return True, None
