import os
import unittest

from utils import File

from tests.test_manifesto import TEST_MANIFESTO

TEST_DATA_PATH = os.path.join("tests", "test_manifesto_db_all_idx.txt")


# flake8: noqa: F401
class TestCase(unittest.TestCase):
    def __get_test_data_list__(self):
        lines = File(TEST_DATA_PATH).read_lines()
        test_data_list = []

        for line in lines:
            key, _, item = line.partition(" ")
            key = key.strip()
            item = item.strip()
            if not key or not item:
                continue

            test_data_list.append((key, item))

        return test_data_list

    @unittest.skip("Skip test for now")
    def test_test_data_list(self):
        test_data_list = self.__get_test_data_list__()
        self.assertEqual(
            len(test_data_list),
            9,
        )

    def test_all_idx(self):
        all_idx = TEST_MANIFESTO.all_idx
        test_data_list = self.__get_test_data_list__()
        for key, item in test_data_list:
            row = all_idx.get(key)
            self.assertIsNotNone(row, f"Key not found: {key}")
            self.assertEqual(row["key"], key)
            self.assertEqual(
                row["item"],
                item,
                f"Item mismatch for key {key}: {item} != {row['item']}",
            )
