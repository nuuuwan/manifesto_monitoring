import os
import unittest

from utils import TSVFile

from tests.test_manifesto import TEST_MANIFESTO

DIR_TABLES = os.path.join("data", "manifestos", "tables")


class TestCase(unittest.TestCase):
    def test_tables(self):
        table = TEST_MANIFESTO.l1_topics_table
        path = os.path.join(DIR_TABLES, "l1_topics.tsv")
        TSVFile(path).write(table)

        for table, label in [
            [TEST_MANIFESTO.l1_topics_table, "l1_topics"],
            [TEST_MANIFESTO.l2_topics_table, "l2_topics"],
            [TEST_MANIFESTO.activities_table, "activities"],
        ]:
            path = os.path.join(DIR_TABLES, f"{label}.tsv")
            TSVFile(path).write(table)
