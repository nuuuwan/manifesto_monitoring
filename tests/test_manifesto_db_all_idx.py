import os
import unittest

from utils import File

from tests.test_manifesto import TEST_MANIFESTO

TEST_DATA_PATH = os.path.join("tests", "test_manifesto_db_all_idx.txt")


# flake8: noqa: F401
class TestCase(unittest.TestCase):
    def test_all_idx(self):
        all_idx = TEST_MANIFESTO.all_idx
        print("\t".join(["key", "item"]))

        lines = File(TEST_DATA_PATH).read_lines()

        for line in lines:
            key, _, item = line.partition(" ")
            row = all_idx.get(key)
            self.assertIsNotNone(row, f"Key not found: {key}")
            self.assertEqual(row["key"], key)
            self.assertEqual(
                row["item"],
                item,
                f"Item mismatch for key {key}: {item} != {row['item']}",
            )
