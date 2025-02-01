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
   - Hash of compressed content + hash of metadata => combined to form a unique 64-character hex string.

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
