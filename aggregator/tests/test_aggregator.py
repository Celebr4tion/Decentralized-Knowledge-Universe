import unittest
import zstandard
from aggregator.aggregator import create_aku, store_aku, retrieve_aku, decompress_content

class TestAggregator(unittest.TestCase):
    def test_create_and_store_aku(self):
        content = "Test AKU content"
        tags = ["test", "phase1"]
        source = "https://example.com"
        agent = "test-agent"
        aku = create_aku(content, tags, source, agent)
        
        # Basic checks on the AKU structure
        self.assertIn("uuid", aku)
        self.assertIn("content_compressed", aku)
        self.assertIn("metadata", aku)
        self.assertIn("metrics", aku)
        
        # Store the AKU in IPFS using the external IPFS command.
        cid = store_aku(aku)
        self.assertIsNotNone(cid)
        print("Stored CID:", cid)
        
        # Retrieve the AKU from IPFS using its CID.
        aku_retrieved = retrieve_aku(cid)
        original_text = decompress_content(aku_retrieved)
        
        self.assertEqual(content, original_text)
        self.assertEqual(aku_retrieved["uuid"], aku["uuid"])

if __name__ == '__main__':
    unittest.main()
