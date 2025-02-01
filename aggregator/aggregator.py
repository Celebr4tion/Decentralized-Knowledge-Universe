import argparse
import json
import zstandard
import ipfshttpclient
from fractal_hash import fractal_hash

def create_aku(content: str, tags: list, source: str) -> dict:
    """Constructs an AKU dict, compresses content, calculates fractal hash."""
    # 1) Compress content
    compressor = zstandard.ZstdCompressor()
    compressed = compressor.compress(content.encode('utf-8'))

    # 2) Build metadata
    metadata = {
        "tags": tags,
        "embeddings": [0.0 for _ in range(384)],  # placeholder
        "sources": [
            {
                "type": "general",
                "url": source
            }
        ]
    }

    # 3) Calculate fractal hash
    uuid = fractal_hash(compressed, metadata)

    # 4) Initialize metrics
    metrics = {
        "richness": 0.0,
        "truthfulness": 0.0,
        "stability": 0.0
    }

    aku = {
        "uuid": uuid,
        "content_compressed": compressed,
        "metadata": metadata,
        "metrics": metrics
    }
    return aku

def store_aku(aku: dict, ipfs_client) -> str:
    """Convert the AKU to JSON, add to IPFS, return the resulting CID."""
    # Convert bytes to hex so JSON can handle it
    aku_copy = aku.copy()
    aku_copy["content_compressed"] = aku_copy["content_compressed"].hex()

    aku_json = json.dumps(aku_copy)
    cid = ipfs_client.add_json(aku_json)
    return cid

def retrieve_aku(cid: str, ipfs_client) -> dict:
    """Fetch and reconstruct AKU from IPFS by CID."""
    aku_json = ipfs_client.get_json(cid)
    aku_dict = json.loads(aku_json)
    # Convert hex back to bytes
    aku_dict["content_compressed"] = bytes.fromhex(aku_dict["content_compressed"])
    return aku_dict

def decompress_content(aku: dict) -> str:
    """Return the original textual content from an AKU dict."""
    decompressor = zstandard.ZstdDecompressor()
    raw = decompressor.decompress(aku["content_compressed"])
    return raw.decode('utf-8')

def main():
    parser = argparse.ArgumentParser(
        description="DKU Phase 1 Aggregator: Create or Retrieve AKUs."
    )
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Create command
    create_parser = subparsers.add_parser("create", help="Create a new AKU.")
    create_parser.add_argument("--content", required=True, help="Textual content for the AKU.")
    create_parser.add_argument("--tags", required=False, default="", help="Comma-separated tags.")
    create_parser.add_argument("--source", required=False, default="", help="Source link or reference.")

    # Retrieve command
    retrieve_parser = subparsers.add_parser("retrieve", help="Retrieve an AKU by CID.")
    retrieve_parser.add_argument("--cid", required=True, help="IPFS CID of the AKU.")

    args = parser.parse_args()

    # Connect to local IPFS
    ipfs_client = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001')

    if args.command == "create":
        content = args.content
        tags = [t.strip() for t in args.tags.split(",")] if args.tags else []
        source = args.source

        aku = create_aku(content, tags, source)
        cid = store_aku(aku, ipfs_client)

        print("AKU created!")
        print(f"UUID: {aku['uuid']}")
        print(f"CID: {cid}")

    elif args.command == "retrieve":
        cid = args.cid
        aku = retrieve_aku(cid, ipfs_client)
        original_text = decompress_content(aku)
        print(f"UUID: {aku['uuid']}")
        print(f"Content: {original_text}")
        print("Metadata:", json.dumps(aku["metadata"], indent=2))
        print("Metrics:", json.dumps(aku["metrics"], indent=2))

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
