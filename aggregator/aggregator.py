import argparse
import json
import zstandard
import tempfile
import os
import sys
from .fractal_hash import fractal_hash
from .ipfs_utils import ipfs_check, add_file_to_ipfs
import datetime

def create_aku(content: str, tags: list, source: str, agent: str = "manual") -> dict:
    """Constructs an improved AKU with versioning and enhanced metadata."""
    # 1) Compress the content
    compressor = zstandard.ZstdCompressor()
    compressed = compressor.compress(content.encode('utf-8'))

    # 2) Build enhanced metadata
    metadata = {
        "tags": tags,
        "embeddings": [0.0 for _ in range(384)],  # placeholder for embeddings
        "sources": [{"type": "general", "url": source}],
        "created_at": datetime.datetime.utcnow().isoformat() + "Z",
        "agent": agent
    }

    # 3) Calculate fractal hash (unique identifier) based on immutable fields
    uuid = fractal_hash(compressed, metadata)

    # 4) Initialize metrics
    metrics = {"richness": 0.0, "truthfulness": 0.0, "stability": 0.0}

    aku = {
        "uuid": uuid,
        "version": 1,
        "content_compressed": compressed,
        "metadata": metadata,
        "metrics": metrics,
        "history": []  # For future updates
    }
    return aku

def store_aku(aku: dict) -> str:
    """
    Stores the AKU (as a JSON file) on IPFS and returns the CID.
    This function writes the JSON to a temporary file and then calls the external ipfs command.
    """
    # Convert the AKU dictionary to JSON.
    # We need to encode the binary content as hex for JSON serialization.
    aku_copy = aku.copy()
    aku_copy["content_compressed"] = aku_copy["content_compressed"].hex()
    aku_json = json.dumps(aku_copy, indent=2)

    # Write the JSON to a temporary file
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as tmp_file:
        tmp_file.write(aku_json)
        tmp_file_path = tmp_file.name

    # Use our helper function to add the file to IPFS
    cids = add_file_to_ipfs(tmp_file_path)
    # Optionally remove the temporary file after adding
    os.remove(tmp_file_path)

    # For simplicity, return the first CID in the list (if multiple lines are returned)
    if cids:
        return cids[0]
    else:
        print("Error: No CID returned from IPFS.")
        sys.exit(1)

def retrieve_aku(cid: str) -> dict:
    """
    Retrieve an AKU from IPFS using the CID.
    This function downloads the file using the ipfs command and reconstructs the AKU.
    """
    import subprocess  # Import here if not already imported above
    # Create a temporary file to store the downloaded JSON.
    tmp_file_path = tempfile.mktemp(suffix=".json")
    cmd = 'ipfs get -o "{}" "{}"'.format(tmp_file_path, cid)
    try:
        subprocess.check_output(cmd, shell=True)
    except subprocess.CalledProcessError as e:
        print("IPFS get failed for CID {}: {}".format(cid, e))
        sys.exit(1)

    # Read the JSON back in
    with open(tmp_file_path, "r") as f:
        aku_dict = json.load(f)
    os.remove(tmp_file_path)

    # Convert the hex string back to bytes for content_compressed
    aku_dict["content_compressed"] = bytes.fromhex(aku_dict["content_compressed"])
    return aku_dict

def decompress_content(aku: dict) -> str:
    """Decompress the content from the AKU dictionary and return the original text."""
    decompressor = zstandard.ZstdDecompressor()
    raw = decompressor.decompress(aku["content_compressed"])
    return raw.decode('utf-8')

def main():
    # Ensure IPFS daemon is running
    from .ipfs_utils import ipfs_check
    ipfs_check()

    parser = argparse.ArgumentParser(
        description="DKU Phase 1 Aggregator: Create or Retrieve AKUs."
    )
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Create command
    create_parser = subparsers.add_parser("create", help="Create a new AKU.")
    create_parser.add_argument("--content", required=True, help="Text content for the AKU.")
    create_parser.add_argument("--tags", required=False, default="", help="Comma-separated tags.")
    create_parser.add_argument("--source", required=False, default="", help="Source URL or reference.")

    # Retrieve command
    retrieve_parser = subparsers.add_parser("retrieve", help="Retrieve an AKU by CID.")
    retrieve_parser.add_argument("--cid", required=True, help="IPFS CID of the AKU.")

    args = parser.parse_args()

    if args.command == "create":
        content = args.content
        tags = [t.strip() for t in args.tags.split(",")] if args.tags else []
        source = args.source

        aku = create_aku(content, tags, source)
        cid = store_aku(aku)

        print("AKU created!")
        print("UUID: {}".format(aku["uuid"]))
        print("CID: {}".format(cid))

    elif args.command == "retrieve":
        cid = args.cid
        aku = retrieve_aku(cid)
        original_text = decompress_content(aku)
        print("UUID: {}".format(aku["uuid"]))
        print("Content: {}".format(original_text))
        print("Metadata: {}".format(json.dumps(aku["metadata"], indent=2)))
        print("Metrics: {}".format(json.dumps(aku["metrics"], indent=2)))
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
