import unittest

from mm import CompareManifesto


class TestCase(unittest.TestCase):
    def test_build_emb_idx_for_cabinet_decisions(self):
        comp = CompareManifesto()
        comp.build_emb_idx_for_cabinet_decisions()

    def test_get_most_similar_cabinet_decisions(self):
        comp = CompareManifesto()
        (text_i, text_j), sim = comp.get_most_similar_cabinet_decisions()

        self.assertEqual(
            text_i[:60],
            "An Act to amend the Penal Code (Corporal Punishment) (Chapte",
        )
        self.assertEqual(
            text_j[:60],
            "Amendment to the Code of Criminal Procedure Act, No.15 of 19",
        )
        self.assertAlmostEqual(sim, 0.8734528714286569, places=7)
