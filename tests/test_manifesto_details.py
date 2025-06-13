import unittest

from tests.test_manifesto_base import TEST_M


class TestCase(unittest.TestCase):
    def test_get_splits_by_l1(self):
        TEST_M.get_splits_by_l1()
