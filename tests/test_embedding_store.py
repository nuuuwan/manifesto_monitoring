import unittest

from mm import EmbeddingStore


class TestCase(unittest.TestCase):

    def test_embedding(self):
        key_to_text = {
            "A1": "I am Nuwan.",
            "A2": "Nuwan is me.",
            "B": "The price of cheese is high.",
        }
        embedding_store = EmbeddingStore(
            emb_id="test_embedding_store", key_to_text=key_to_text
        )
        m = embedding_store.embedding_matrix

        self.assertEqual(len(m), 3)
        self.assertEqual(len(m[0]), 1536)
        self.assertAlmostEqual(m[0][0], -0.026, places=3)
