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
        max_sim = max([x[1] for x in m])
        self.assertAlmostEqual(max_sim, 0.3703, places=2)
        for (text1, text2), sim in m:
            if sim > 0.35:
                print("=" * 64)
                print(f"Similarity: {sim:.4f}")
                print("-" * 64)
                print(text1)
                print("-" * 64)
                print(text2)
                print("-" * 64)
                print("")
