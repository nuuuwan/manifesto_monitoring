import unittest

from mm import Embedding


class TestCase(unittest.TestCase):
    def test_embedding(self):
        text = "My name is Nuwan."
        e = Embedding([text]).get_idx()[text]

        self.assertEqual(len(e), 1536)
        self.assertAlmostEqual(e[0], -0.010304543189704418, places=7)
