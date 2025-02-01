# Design Overview

Welcome to the **Decentralized Knowledge Universe (DKU) – Phase 1** documentation. This `design_overview.md` provides an **architectural** and **rationale** perspective for how the current prototype (aggregator, fractal hashing, IPFS integration) is set up and what comes next.

---

## 1. Purpose of Phase 1

In **Phase 1**, our goal is to create a **Minimum Viable Product (MVP)** that:

1. **Defines an Atomic Knowledge Unit (AKU)** data structure.  
2. **Implements fractal hashing** to produce a unique ID per AKU.  
3. **Compresses content** (Zstandard) to keep knowledge atomic (~1KB compressed text).  
4. **Stores and retrieves** each AKU from a local IPFS node, ensuring decentralized data availability.  
5. **Provides basic tests** to validate the system works end-to-end.

With this initial setup, we can **confidently** store small pieces of information in IPFS and retrieve them by their CID. Everything else (like advanced AI Agents, consensus, self-healing protocols) will build upon this core.

---

## 2. Overall Architecture

Below is a high-level representation of the Phase 1 architecture:
```pgsql
               +----------------------+
               |       AKU            |
               |----------------------|
               | - content (compressed)|
               | - metadata           |
               | - metrics            |
               +----------+-----------+
                          |
                          |   (Passes to)
                          v
               +----------------------+
               |   fractal_hash()     |
               |  (Generates unique   |
               |      UUID)           |
               +----------+-----------+
                          |
                          v
               +----------------------+
               |    aggregator.py     |
               | (Create, Store, and  |
               |  Retrieve AKUs)      |
               +----------+-----------+
                          |
                          |  (Uses helper functions)
                          v
               +----------------------+
               |    ipfs_utils.py     |
               | (Executes IPFS CLI   |
               |  commands for add/get)|
               +----------+-----------+
                          |
                          v
               +----------------------+
               |         IPFS         |
               |    (Local Node)      |
               +----------------------+
```

### 2.1 Aggregator

- **create_aku**: Builds the AKU dictionary with compressed content, metadata, metrics.  
- **store_aku**: Serializes the AKU to JSON, writes it to a temp file, and executes `ipfs add` to place it on IPFS.  
- **retrieve_aku**: Retrieves the AKU JSON file from IPFS (`ipfs get`), rehydrates the AKU structure, and converts the hex-encoded content back into bytes.  
- **decompress_content**: Decompresses the AKU’s binary content to get the original text.

### 2.2 Fractal Hashing

The **fractal_hash** function:
1. **Hash of compressed content** (SHA-256).  
2. **Hash of metadata** (JSON-serialized, sorted keys).  
3. **Combined** into a final SHA-256, providing a unique 64-character hex string as the AKU’s `uuid`.

This helps ensure **integrity** and **traceability** for each AKU. Any slight change in content or metadata produces a distinct hash.

### 2.3 IPFS Utilities

The **ipfs_utils.py** module:
- **ipfs_check**: Confirms the IPFS daemon is running.  
- **add_file_to_ipfs**: Actually calls `ipfs add` to publish data to the local IPFS node.  
- **get_ipfs_cid** (not currently used in the aggregator, but useful for “dry-run” or checks) only computes hashes without uploading.

These utilities rely on **subprocess** calls to the local `ipfs` command-line interface. This design choice is simple and straightforward but can be replaced by a Python IPFS client in future phases.

---

## 3. Current Code Flow

1. **Test / Developer calls** `create_aku(...)` with text content, tags, and source.  
2. The aggregator:  
   - Compresses the text.  
   - Generates a fractal hash.  
   - Prepares the AKU dictionary.  
3. **store_aku** writes JSON to a temporary file, executes `ipfs add`, and returns the resulting **CID**.  
4. **retrieve_aku** uses `ipfs get` to download the JSON, reconstitutes the AKU, and returns it for local usage.  
5. **decompress_content** decompresses the `content_compressed` field to get original text.

---

## 4. Testing and Validation

In `tests/test_aggregator.py`:

1. **create_aku** → ensures structure has `uuid`, `content_compressed`, `metadata`, `metrics`.  
2. **store_aku** → checks that the function returns a valid CID string.  
3. **retrieve_aku** → fetches from IPFS and reconstructs the AKU.  
4. **decompress_content** → verifies the original text matches what was stored.

On success, the test logs the CID and confirms an **OK** result. Example:

```bash
.
Ran 1 test in 0.888s

OK
```

---

## 5. Next Steps (Detailed Explanations)

1. **Refine Documentation**  
   - **README Clarity**: If you haven’t already, ensure your `README.md` instructs newcomers how to run the aggregator, including IPFS setup.  
   - **Wiki / GitHub Pages**: Start a small wiki or pages site that details the project’s vision and a simple tutorial.

2. **Add a Minimal Web UI (Phase 2)**  
   - Create a simple front-end (e.g., a plain HTML/JS page or a React/Vue app) that can call your aggregator’s Python CLI or service.  
   - This allows non-technical users to submit text and retrieve results by CID via an intuitive interface.  
   - Initially, it might just wrap the command-line calls. Later, you could add an HTTP layer to aggregator so it can accept REST/GraphQL requests.

3. **Establish a Community Space**  
   - You’ll want to gather early adopters/testers. Creating a **Discord** or **Matrix** channel helps.  
   - Encourage bug reports and feature suggestions.  
   - This also sets the stage for domain experts to eventually help with knowledge curation.

4. **Tighten the AKU Schema**  
   - Expand **metadata** to include optional fields (e.g., `timestamp`, `version`, `domain`).  
   - Consider a versioning approach: If an AKU is updated, do you store a brand-new AKU or keep a reference to the original?  
   - This question will matter more in future phases (self-healing, consensus).

5. **Plan for AI Agents**  
   - Start investigating how you might integrate a basic “Miner” agent in Phase 3. For instance, a script that pulls new paragraphs from public APIs or Wikipedia dumps.  
   - Each chunk becomes an AKU, with a default “untested” truthfulness metric.  
   - Put these steps in a backlog so you have a roadmap beyond storing AKUs manually.

6. **Prepare for Extended Testing**  
   - Test on large text volumes (e.g., ~1KB). Confirm compression & retrieval times remain acceptable.  
   - Evaluate performance if you store thousands of AKUs. IPFS usage might require pinned storage or an IPFS cluster.

7. **Optional: Switch to a Python IPFS Client**  
   - Currently, you’re using external `ipfs` commands via `subprocess`. This works, but you can explore the `ipfshttpclient` library for a more direct integration.  
   - This can reduce overhead from file I/O to temporary JSON files, but also has trade-offs in debugging and environment setup.

---

## 6. Future Considerations

- **Data Redundancy**: As your knowledge base grows, ensure you or collaborators pin CIDs so they don’t vanish if local IPFS nodes go offline.  
- **Security & Integrity**: While fractal hashing ensures the content is unique and tamper-evident, in future phases you’ll want cryptographic signatures or proof-of-authorship.  
- **Scalability**: If you anticipate millions of AKUs, you’ll need better content addressing strategies (like chunked or merklized approaches). For now, Phase 1 is a stepping stone.  
- **Tokenomics & Self-Healing**: This will require more robust architecture (smart contracts, domain agencies, conflict resolution workflows) that build upon the MVP.

