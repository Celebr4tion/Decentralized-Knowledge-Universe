"""
Miner Agent for the Decentralized Knowledge Universe (DKU)
This agent retrieves content from an external source (Wikipedia API for this example)
and creates a new AKU from it.
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import requests
import argparse
from aggregator.aggregator import create_aku, store_aku
import json
import time

# Configuration parameters
CONFIG = {
    "wikipedia_api": "https://en.wikipedia.org/api/rest_v1/page/summary/",
    "default_article": "Quantum_entanglement",
    "poll_interval": 3600  # seconds between polls (1 hour)
}

def fetch_wikipedia_summary(article_title: str) -> dict:
    """Fetch a summary from Wikipedia using the REST API."""
    url = CONFIG["wikipedia_api"] + article_title
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch article {article_title}: {response.status_code}")
    return response.json()

def miner_task(article_title: str):
    """Perform a single mining task: fetch, create AKU, and store it."""
    try:
        data = fetch_wikipedia_summary(article_title)
        # Extract the summary and title
        content = data.get("extract", "")
        if not content:
            print("No extract available for", article_title)
            return

        # Use the article title as a tag, add "wikipedia" as a source type.
        tags = [article_title.lower(), "wikipedia"]
        source_url = data.get("content_urls", {}).get("desktop", {}).get("page", CONFIG["wikipedia_api"] + article_title)
        
        # Create the AKU using the aggregator
        aku = create_aku(content, tags, source_url, agent="miner")
        cid = store_aku(aku)
        
        print("AKU created by Miner Agent!")
        print("Article:", article_title)
        print("AKU UUID:", aku["uuid"])
        print("Stored CID:", cid)
    except Exception as e:
        print("Error in miner_task:", e)

def main():
    parser = argparse.ArgumentParser(description="Miner Agent for DKU")
    parser.add_argument("--article", type=str, default=CONFIG["default_article"],
                        help="Wikipedia article title to fetch")
    parser.add_argument("--loop", action="store_true", help="Run continuously at set intervals")
    args = parser.parse_args()

    if args.loop:
        while True:
            miner_task(args.article)
            print("Waiting for next poll...")
            time.sleep(CONFIG["poll_interval"])
    else:
        miner_task(args.article)

if __name__ == "__main__":
    main()
