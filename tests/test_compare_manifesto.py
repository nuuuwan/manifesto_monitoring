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

        e_max_sim = 0.6
        self.assertAlmostEqual(max_sim, e_max_sim, places=1)
        for (text1, text2), sim in reversed(m):
            if sim > e_max_sim - 0.1:
                print("=" * 64)
                print(f"Similarity: {sim:.4f}")
                print("-" * 64)
                print(text1)
                print("")
                print("-" * 64)
                print(text2)
                print("")
                print("-" * 64)
                print("")
