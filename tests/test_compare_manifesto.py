import unittest

from mm import CompareManifesto


class TestCase(unittest.TestCase):

    def test_similarity_matrix(self):
        self.assertIsNotNone(CompareManifesto().similarity_matrix)

    def test_high_similarity_pairs(self):
        self.assertIsNotNone(CompareManifesto().high_similarity_pairs)
