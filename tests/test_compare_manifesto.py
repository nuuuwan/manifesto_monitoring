import unittest

from mm import CompareManifesto

TEST_COMPARE_MANIFESTO = CompareManifesto()


class TestCase(unittest.TestCase):

    def test_manifesto_items(self):
        self.assertEqual(TEST_COMPARE_MANIFESTO.n_manifesto_items, 1345)

    @unittest.skip("n_cabinet_decisions changes as more decisiosn are made.")
    def test_cabinet_decisions(self):
        self.assertEqual(TEST_COMPARE_MANIFESTO.n_cabinet_decisions, 421)

    def test_similarity_matrix(self):
        self.assertIsNotNone(TEST_COMPARE_MANIFESTO.similarity_matrix)

    def test_similarity_data_list(self):
        self.assertIsNotNone(TEST_COMPARE_MANIFESTO.get_similarity_data_list())

    def test_get_overall_progress_by_date(self):
        progress = TEST_COMPARE_MANIFESTO.get_overall_progress_by_date()
        self.assertIsInstance(progress, list)
        first_d = progress[0]

        self.assertEqual(
            first_d["progress"], TEST_COMPARE_MANIFESTO.get_overall_progress()
        )
