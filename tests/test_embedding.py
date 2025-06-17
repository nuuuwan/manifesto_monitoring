import unittest

from mm import Embedding


class TestCase(unittest.TestCase):
    @unittest.skip("Uses openai api")
    def test_embedding(self):
        text1 = "I am Nuwan."
        text2 = "Nuwan is me."
        text3 = "The price of cheese is high."

        idx = Embedding([text1, text2, text3]).get_idx()
        e1 = idx[text1]
        self.assertEqual(len(e1), 1536)
        self.assertAlmostEqual(e1[0], -0.026, places=3)

        m = Embedding.get_similarity_matrix(idx, idx)
        self.assertAlmostEqual(m[0][0], 1.0, places=1)
        self.assertAlmostEqual(m[0][1], 0.8, places=1)
        self.assertAlmostEqual(m[0][2], 0.0, places=1)
