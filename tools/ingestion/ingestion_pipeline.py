
from .asset_validator import validate_asset
from .provenance import generate_provenance
from .metadata_builder import build_metadata
from .staging_manager import stage_asset

def run_pipeline(filepath, known_checksums):
    valid, reason = validate_asset(filepath)
    if not valid: return {"status": "REJECTED", "reason": reason}
    
    metadata = build_metadata(filepath)
    if metadata["checksum"] in known_checksums:
        return {"status": "REJECTED", "reason": "DUPLICATE_ASSET"}
        
    provenance = generate_provenance(filepath)
    staged = stage_asset(metadata, provenance)
    return {"status": "STAGED", "asset": staged}
