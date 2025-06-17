import unittest

from mm import CompareManifesto


class TestCase(unittest.TestCase):
    def test_build_emb_idx_for_cabinet_decisions(self):
        comp = CompareManifesto()
        comp.build_emb_idx_for_cabinet_decisions()

    def test_build_emb_idx_for_manifesto(self):
        comp = CompareManifesto()
        comp.build_emb_idx_for_manifesto()

    def test_get_similarity_matrix(self):
        comp = CompareManifesto()
        m = comp.get_similarity_matrix()
        self.assertIsNotNone(m)

    def test_get_high_similarity_pairs(self):
        comp = CompareManifesto()
        data_list = comp.get_high_similarity_pairs(min_sim=0.5)
        self.assertGreater(len(data_list), 0)
