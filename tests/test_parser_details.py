import unittest

from tests.test_parser import TEST_M


class TestCase(unittest.TestCase):
    def test_l2_splits(self):
        self.assertEqual(len(TEST_M.l2_splits), 39)
