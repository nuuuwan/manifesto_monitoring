import os
import unittest

from utils import TSVFile

from tests.test_manifesto import TEST_MANIFESTO

DIR_TABLES = os.path.join("data", "manifestos", "tables")


class TestCase(unittest.TestCase):
    def test_l1_topics_table(self):
        l1_topics_table = TEST_MANIFESTO.l1_topics_table
        l1_topics_table_path = os.path.join(DIR_TABLES, "l1_topics.tsv")
        TSVFile(l1_topics_table_path).write(l1_topics_table)
