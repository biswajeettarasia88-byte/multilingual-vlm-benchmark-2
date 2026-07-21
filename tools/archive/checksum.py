
import hashlib
def verify_checksum(filepath, expected, algo="sha256"):
    if not expected: return "NOT_AVAILABLE"
    hasher = hashlib.new(algo)
    with open(filepath, "rb") as f:
        hasher.update(f.read())
    return "VERIFIED" if hasher.hexdigest() == expected else "INVALID"
