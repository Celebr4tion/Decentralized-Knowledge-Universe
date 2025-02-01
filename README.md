# Decentralized Knowledge Universe (DKU)

**Version: Phase 1 (MVP)**  
**License: [AGPLv3](./LICENSE)**  

## Overview

The **Decentralized Knowledge Universe (DKU)** is an open-source project designed to combat misinformation and preserve truthful data in a censorship-resistant, community-driven environment. The DKU stores knowledge as tiny, verifiable "Atomic Knowledge Units" (AKUs) and uses **IPFS** for decentralized storage. Each AKU is identified by a **fractal hash** (unique combination of content & metadata hashes), ensuring integrity and transparency.

This repository contains the **Phase 1** MVP:
- **Fractal Hashing** for AKUs.
- **Zstandard Compression** for textual knowledge (up to ~1KB).
- **Basic Aggregator** to create, store, and retrieve AKUs on IPFS.

> **Note**: Future phases will introduce AI Agents, self-healing consensus, domain agencies, and a Knowledge Token economy.

---

## Features in Phase 1

1. **Atomic Knowledge Units (AKUs)**  
   - Minimal textual knowledge (~1KB or less when compressed).  
   - Metadata (tags, references, placeholders for embeddings).  
   - Basic metrics fields (richness, truthfulness, stability) initialized to 0.

2. **Fractal Hashing**  
   - Hash of compressed content + hash of metadata → combined to form a unique 64-character hex string.

3. **Decentralized Storage**  
   - **IPFS** integration to store and retrieve AKUs as JSON objects.  
   - Local IPFS node usage (can be extended to remote IPFS gateways if desired).

4. **Easy CLI / Script Usage**  
   - A Python-based aggregator script to add new AKUs or retrieve existing ones by CID.

---

## Requirements

- **Python 3.9+** (tested on Python 3.9 and 3.10)
- **IPFS Daemon**  
  - Install and initialize [IPFS](https://docs.ipfs.io/install/command-line/).  
  - Run `ipfs daemon` in a separate terminal before using the aggregator.
- **Dependencies**  
  - Listed in [`aggregator/requirements.txt`](./aggregator/requirements.txt)

---

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/<your-username>/Decentralized-Knowledge-Universe.git
   cd Decentralized-Knowledge-Universe
   ```

2. **Install Dependencies**

   ```bash
   cd aggregator
   python3 -m venv venv
   source venv/bin/activate  # (Linux/macOS)
   # or venv\Scripts\activate.bat (Windows)

   pip install --upgrade pip
   pip install -r requirements.txt
   ```

3. **Start IPFS Daemon**

   ```bash
   ipfs init   # Only if you haven't initialized IPFS before
   ipfs daemon
   ```

4. **Test Basic Setup**

   Open a separate terminal, still inside the `aggregator/` directory, then run:

   ```bash
   python -m unittest tests/test_aggregator.py
   ```

   - If all tests pass, the Phase 1 aggregator is operational!

---

## Usage

### 1. Create a New AKU

```bash
cd aggregator
source venv/bin/activate  # (or the Windows equivalent)

python aggregator.py create --content "The sun is a star." \
    --tags "astronomy, sun" \
    --source "https://en.wikipedia.org/wiki/Sun"
```

**Explanation:**

- `--content`: The text to store (<= 1KB ideally).
- `--tags`: Comma-separated tags.
- `--source`: Reference or link for the content’s provenance.

- This command returns:
   - A unique UUID (fractal hash).
   - An IPFS CID for the JSON file storing the AKU.

**Example Output:**

```makefile
AKU created!
UUID: 8f5c6f21...
CID: QmXYZabcd...
```

### 2. Retrieve an AKU by CID

```bash
python aggregator.py retrieve --cid QmXYZabcd...
```

**Explanation:**

- Downloads the AKU JSON from IPFS and reconstructs the original text.
- Prints the fractal hash, tags, metrics, etc.

**Example Output:**

```yaml
UUID: 8f5c6f21...
Content: The sun is a star.
Metadata:
  tags: ['astronomy', 'sun']
  embeddings: [0.0, 0.0, ...]  # placeholder
  sources: [{'type': 'general', 'url': 'https://en.wikipedia.org/wiki/Sun'}]
Metrics:
  richness: 0.0
  truthfulness: 0.0
  stability: 0.0
```

---

## Project Roadmap

**Phase 1 (current):**
- Minimal aggregator & fractal hashing.
- IPFS storage & retrieval.

**Phase 2:**
- Simple web front-end for user submissions & retrieval.
- Community building & documentation improvements.

**Phase 3:**
- Basic AI Agents (Miner, Debater) + minimal conflict detection.

**Phase 4+:**
- Self-healing consensus, advanced tokenomics, domain agencies, etc.

---

## Contributing

- Fork the repo & clone locally.
- Create a branch for your feature:  
  `git checkout -b feature-my-improvement`
- Commit your changes & push:  
  `git push origin feature-my-improvement`
- Open a Pull Request describing your changes.

We welcome all forms of contributions — bug reports, features, docs, tests, or just general feedback.

---

## License

This project is licensed under the AGPLv3. See [LICENSE](./LICENSE) for details.

---

## Contact / Community

- **Project Owner:** [@Celebr4tion](https://github.com/Celebr4tion)
- **Chat / Discussion:** (to be created)
- **Issues:** [GitHub Issues](https://github.com/Celebr4tion/Decentralized-Knowledge-Universe/issues)

Thank you for helping build a decentralized knowledge ecosystem!
