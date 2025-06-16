import unittest

from mm import CompareManifesto


class TestCase(unittest.TestCase):
    def test_build_emb_idx_for_cabinet_decisions(self):
        comp = CompareManifesto()
        comp.build_emb_idx_for_cabinet_decisions()
