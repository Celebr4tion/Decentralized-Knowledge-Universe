import unittest
import zstandard
import ipfshttpclient
from aggregator import create_aku, store_aku, retrieve_aku, decompress_content

class TestAggregator(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001')

    def test_create_and_store_aku(self):
        content = "Test AKU content"
        tags = ["test", "phase1"]
        source = "https://example.com"
        aku = create_aku(content, tags, source)

        # Basic checks
        self.assertIn("uuid", aku)
        self.assertIn("content_compressed", aku)
        self.assertIn("metadata", aku)
        self.assertIn("metrics", aku)

        cid = store_aku(aku, self.client)
        self.assertIsNotNone(cid)

        # Retrieve
        aku_retrieved = retrieve_aku(cid, self.client)
        original_text = decompress_content(aku_retrieved)

        self.assertEqual(content, original_text)
        self.assertEqual(aku_retrieved["uuid"], aku["uuid"])

if __name__ == '__main__':
    unittest.main()
