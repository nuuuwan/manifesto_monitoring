import unittest

from mm import Embedding


class TestCase(unittest.TestCase):
    @unittest.skip("Skipping test for OpenAI API key requirement")
    def test_embedding(self):
        text1 = "I am Nuwan."
        text2 = "Nuwan is me."
        text3 = "The price of cheese is high."

        idx = Embedding([text1, text2, text3]).get_idx()
        e1 = idx[text1]
        self.assertEqual(len(e1), 1536)
        self.assertAlmostEqual(e1[0], -0.0263)

        m = Embedding.get_similarity_matrix(idx)
        print(m)
        self.assertEqual(
            m,
            [
                (("I am Nuwan.", "I am Nuwan."), 1.0),
                (("Nuwan is me.", "Nuwan is me."), 1.0),
                (
                    (
                        "The price of cheese is high.",
                        "The price of cheese is high.",
                    ),
                    1.0,
                ),
                (("I am Nuwan.", "Nuwan is me."), 0.7942),
                (("Nuwan is me.", "I am Nuwan."), 0.7942),
                (("I am Nuwan.", "The price of cheese is high."), 0.0116),
                (("The price of cheese is high.", "I am Nuwan."), 0.0116),
                (("Nuwan is me.", "The price of cheese is high."), -0.0128),
                (("The price of cheese is high.", "Nuwan is me."), -0.0128),
            ],
        )
