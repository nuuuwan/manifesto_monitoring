import unittest

from mm import EmbIdx


class TestCase(unittest.TestCase):
    def test_multiget(self):
        text_list = ["My name is Nuwan.", "Nuwan is me."]
        emb_idx = EmbIdx("test")
        idx = emb_idx.multiget(text_list)
        self.assertEqual(len(idx), 2)
        self.assertIn("My name is Nuwan.", idx)
        self.assertIn("Nuwan is me.", idx)
