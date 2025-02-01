import hashlib
import json

def fractal_hash(content_compressed: bytes, metadata: dict) -> str:
    """
    Generate a fractal hash from compressed content and metadata.
    Returns a 64-character hex string (SHA-256).
    """
    # Step 1: Hash the compressed content
    content_hash = hashlib.sha256(content_compressed).hexdigest()

    # Step 2: Hash the metadata (serialize first)
    metadata_str = json.dumps(metadata, sort_keys=True)
    metadata_hash = hashlib.sha256(metadata_str.encode('utf-8')).hexdigest()

    # Step 3: Combine + hash again
    combined = content_hash + ":" + metadata_hash
    final = hashlib.sha256(combined.encode('utf-8')).hexdigest()
    return final